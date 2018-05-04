
answer = ''

def data(msg, PASSWD):
    import setting
    import ujson
    from mqtt import MQTTClient
    global answer
    answer = 'OK'
    IOTHUB = setting.get('iothub')
    DEVICE = setting.get('iotdevicename')
    KEY = setting.get('iotdevicesecret')
    USER = IOTHUB + '/' + DEVICE + '/api-version=2016-11-14'
    print('--------------MQTT----------')
    print('DEVICE: ', DEVICE)
    print('IOTHUB: ', IOTHUB)
    print('USER: ', USER)
    print('PASSWD: ', PASSWD)
    c = MQTTClient(DEVICE, IOTHUB, 8883, USER, PASSWD, 0, True) # client_id, server, port=0, user=None, password=None, keepalive=0, ssl=False, ssl_params={})
    c.set_callback(sub_cb)
    try:
        c.connect()
        print('--------------PUBLISH----------')
        print('DEVICE: ', 'devices/' + DEVICE + '/messages/events/')
        print('MSG: ', msg)
        c.publish('devices/' + DEVICE + '/messages/events/', msg, False, 1) # topic, msg, retain=False, qos=0
        c.subscribe('$iothub/twin/res/#', 1) # topic, qos=0
        c.publish('$iothub/twin/GET/?$rid=2', '', False, 1)
        c.wait_msg()
        dictr = {}
        dictr["RSSI"] = setting.get('RSSI')
        dictr["health"] = setting.get('health')
        dictr["hwid"] = setting.get('hwid')
        dictr["VBat"] = setting.get('VBat')
        dictr["FWversion"] = setting.get('FWversion')
        dictr["FWnumber"] = setting.get('FWnumber')
        try:
            dict = ujson.loads(answer)
            print('RX TWIN MSG: ', dict)
            dict_rep = dict["reported"]
            keyp = dict_rep["keypresses"] + 1
            dictr["keypresses"] = keyp
        except:
            dictr["keypresses"] = 1
        print('TX TWIN MSG: ', dictr)
        reported = ujson.dumps(dictr)
        c.publish('$iothub/twin/PATCH/properties/reported/?$rid=1', reported, False, 1)
        c.disconnect()
    except():
        answer = 'ERROR'
    return answer

def sub_cb(topic, recive):
    global answer
    answer = recive.decode()
