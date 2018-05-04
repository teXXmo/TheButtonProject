def do_sta():
    import network
    import time
    import setting
    try:
        ssid = setting.get('ssid')
        password = setting.get('password')
        usedhcp = setting.get('usedhcp')
        ip = setting.get('ip')
        netmask = setting.get('netmask')
        gateway = setting.get('gateway')
        dnsserver = setting.get('dnsserver')
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        if usedhcp == 'no':
            sta_if.ifconfig((ip, netmask, gateway, dnsserver))
        sta_if.connect(ssid, password)
        setting.set('opsmode', 'client')
    except:
        print('ERROR STA WIFI')

def do_ap():
    import network
    import ubinascii
    import setting
    try:
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(True)
        mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
        mac = mac[9:100]
        mac = mac.upper()
        ap_if.config(essid='ESP_' + mac, authmode=0)
        setting.set('opsmode', 'SoftAP')
    except:
        print('ERROR AP WIFI')

def do_nothing():
    import network
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(False)
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)

def is_sta():
    import network
    import setting
    sta_if = network.WLAN(network.STA_IF)
    if sta_if.isconnected():
        try:
            print(sta_if.ifconfig())
            setting.set('ip', sta_if.ifconfig()[0])
            setting.set('netmask', sta_if.ifconfig()[1]) 
            setting.set('gateway', sta_if.ifconfig()[2])
            setting.set('dnsserver', sta_if.ifconfig()[3]) 
        except:    
            print ('ERROR in is_sta')
    return(sta_if.isconnected())

def is_ap():
    import network
    ap_if = network.WLAN(network.AP_IF)
    return(ap_if.isconnected())

def wait_sta(sec):
    import time
    nn = 0
    while nn < sec:
        if is_sta():
            return True
            break
        else:
            print('Wait for STA WLAN: ', nn)
        nn += 1
        time.sleep(1)
    return False

def scan():
    import network
    import ujson
    import ubinascii
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    decoded = sta_if.scan()
    list = []
    for element in decoded:
        dict = {}
        dict["ssid"] = element[0]
        dict["bssid"] = ubinascii.hexlify(element[1],':').decode().upper()               
        dict["channel"] = element[2]
        dict["rssi"] = element[3]
        dict["authmode"] = element[4]
        dict["hidden"] = element[5]
        list.append(dict)        
    encoded = ujson.dumps(list)        
    if encoded != '':
        return encoded
    else:
        return ''

if __name__ == '__main__':
    main()