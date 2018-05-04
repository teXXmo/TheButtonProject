LED_RED_GPIO = 12   # Pin10 RED
LED_GREEN_GPIO = 14 # Pin9 GREEN
ADC_GPIO = 0        # Button
POWER_GPIO = 5      # Power Hold

from machine import Pin,ADC,PWM,Timer
power = Pin(POWER_GPIO,Pin.OUT)
power.value(1)

import time
import webrepl
import gc
import ujson
import wifi
import setting
import RepUpdate

def led_blink(freq, ledg_duty, ledr_duty):
    led_green_pwm.freq(freq)
    led_red_pwm.freq(freq)
    led_green_pwm.duty(1023 - ledg_duty)
    led_red_pwm.duty(1023 - ledr_duty)

def shutdown(save = True):
    print('Stop Machine')
    if save == True:
        gc.collect()
        #print('RAM free: {} RAM allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
        setting.save('config.json')
        print('Save Config')
        time.sleep(2)
    print('Power Off')
    power.value(0)

led_red = Pin(LED_RED_GPIO,Pin.OUT)
led_green = Pin(LED_GREEN_GPIO,Pin.OUT)
led_green_pwm = PWM(led_green)
led_red_pwm = PWM(led_red)
led_blink(1, 0, 0)
    
adc = ADC(ADC_GPIO)
VBat = adc.read() * 3.3 / 1024

interruptCounter = 0
save_flag = True

def handleInterrupt(timer):    
    global interruptCounter
    global save_flag
    interruptCounter = interruptCounter + 1
    if interruptCounter == 1:        
        timeserver = setting.get('timeserver')
        if timeserver == '':
            setting.set('timeserver', 'pool.ntp.org') 
        webrepl.stop()
        RepUpdate.new(VBat)
                    
    if interruptCounter <= 5:
        print('<= 5 sec')
        if adc.read() < 200:
            timer.deinit()
            wifi.do_nothing()
            wifi.do_sta()
            print('Push Message')
            led_blink(10, 200, 0)
            if wifi.wait_sta(15):
                try:
                    import GenSasToken
                    import AzurePublish
                    import ubinascii
                    import network
                    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode().upper()
                    UserJson = setting.get('userjson')
                    UserJson = UserJson.strip('\n')
                    UserJson = UserJson.strip('\r')
                    UserJson = UserJson.strip('\n')
                    UserJson = UserJson.strip(' ')
                    UserJson = UserJson.lstrip('{')
                    UserJson = UserJson.rstrip('}')
                    UserJson = UserJson.strip(' ')
                    msg = '{"UniqueID": "' + mac + '"'
                    if UserJson != '':
                        msg += ',' + UserJson
                    msg += '}'
                    gc.collect()
                    token = GenSasToken.now()
                    gc.collect()
                    encoded = AzurePublish.data(msg, token)
                except:
                    encoded = 'ERROR'
            else:
                encoded = 'ERROR'
            if encoded != 'ERROR':
                try:
                    dict = ujson.loads(encoded)
                    dict = dict["desired"]
                    setting.set('FWnumberNew', dict["FWnumber"])
                    setting.set('FWurl', dict["FWurl"])
                except:
                    print('ERROR TWIN MSG')
                led_blink(1, 1023, 0)
            else:
                print('ERROR Azure TX')
                led_blink(1, 0, 1023)
            time.sleep(2)    
            led_blink(1, 0, 0)
            RepUpdate.update()
            shutdown(save_flag)
    if interruptCounter == 5:
        print('5 sec')
        led_blink(1, 200, 200)
    if interruptCounter == 10:
        print('10 sec')
        if adc.read() < 200:
            print('WEB AP ...')
            timer.deinit()
            wifi.do_nothing()
            wifi.do_ap()
            led_blink(1, 0, 200)
            time.sleep(2)
            try:
                import webserver
                webserver.start()
            except:
                print('WEB Server Crash') 
            led_blink(1, 0, 0)
            shutdown()
        else:
            led_blink(3, 200, 200)
    if interruptCounter == 15:
        print('15 sec')
        if adc.read() < 200:
            print('WEB STA ...')
            timer.deinit()
            wifi.do_nothing()
            wifi.do_sta()
            led_blink(3, 0, 200)
            if wifi.wait_sta(15):
                try:
                    import webserver
                    webserver.start()
                except:
                    print('WEB Server Crash') 
            led_blink(1, 0, 0)
            shutdown()
        else:
            led_blink(10, 0, 511)
            print('Repair Time 120 sec')
            wifi.do_nothing()
            wifi.do_ap()
            wifi.do_sta()
            wifi.wait_sta(15)
            webrepl.start()
    if interruptCounter == 120:
        timer.deinit()
        print('120 sec')
        shutdown(False)

def start(save = True):
    global save_flag
    save_flag = save
    print('')
    #print('Start Control, RAM free: {} RAM allocated: {}'.format(gc.mem_free(), gc.mem_alloc()))
    setting.load('config.json')
    timer = Timer(0)
    led_blink(1, 200, 0)
    interruptCounter = 0        
    print('Start Timer')
    timer.init(period=1000, mode=Timer.PERIODIC, callback=handleInterrupt)
    return
    
