def now(ExTime = 600):
    from ntptime import settime
    import setting
    import utime
    import time 
    
    timeserver = setting.get('timeserver')
    try:
        print(utime.time())
        timeset = False
        nn = 0
        while timeset == False:
            try:
                if timeserver =='':
                    settime()
                    timeset = True
                else:
                    settime(timeserver)
                    timeset = True                
            except:
                timeset = False
                print('Try NTP')
                nn += 1
                if nn == 15:
                    timeset = True
                time.sleep(1)
        print(utime.time())
        IOTHUB = setting.get('iothub')
        DEVICE = setting.get('iotdevicename')
        KEY = setting.get('iotdevicesecret')
        USER = IOTHUB + '/' + DEVICE #+ '/api-version=2016-11-14'
        EXPIRES = utime.time() + 946684800 + ExTime # +30 Jahre + 10 Min
        PASSWD = GenerateAzureSasToken(IOTHUB + '/devices/' + DEVICE, KEY, EXPIRES)
    except:
        PASSWD = ''
    return PASSWD

def GenerateAzureSasToken(uri, key, expiryTimestamp, policy_name=None):
    from ubinascii   import a2b_base64, b2a_base64
    def _quote(s) :
        r = ''
        for c in str(s) :
            if (c >= 'a' and c <= 'z') or \
               (c >= '0' and c <= '9') or \
               (c >= 'A' and c <= 'Z') or \
               (c in '.-_') :
                r += c
            else :
                r += '%%%02X' % ord(c)
        return r
    uri       = _quote(uri)
    sign_key  = b'%s\n%d' % (uri, int(expiryTimestamp))
    key       = a2b_base64(key)
    hmac      = HMACSha256(key, sign_key)
    signature = _quote( b2a_base64(hmac).decode().strip() )
    token = 'sr='  + uri       + '&' + 'sig=' + signature + '&' + 'se='  + str(expiryTimestamp)
    if policy_name :
        token += '&' + 'skn=' + policy_name
    return 'SharedAccessSignature ' + token

def HMACSha256(keyBin, msgBin) :
    from uhashlib import sha256
    block_size = 64 # SHA-256 blocks size
    
    trans_5C = bytearray(256)
    for x in range(len(trans_5C)) :
        trans_5C[x] = x^0x5C

    trans_36 = bytearray(256)
    for x in range(len(trans_36)) :
        trans_36[x] = x^0x36
    
    def translate(d, t) :
        res = bytearray(len(d))
        for x in range(len(d)) :
            res[x] = t[d[x]]
        return res
    
    keyBin = keyBin + chr(0) * (block_size - len(keyBin))
  
    inner = sha256()
    inner.update(translate(keyBin, trans_36))
    inner.update(msgBin)
    inner = inner.digest()
    
    outer = sha256()
    outer.update(translate(keyBin, trans_5C))
    outer.update(inner)
    
    return outer.digest()
