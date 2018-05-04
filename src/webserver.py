import usocket as socket
import setting
import time
import gc
import ujson

_mimeTypes = {
    b'.txt'   : b'text/plain',
    b'.htm'   : b'text/html',
    b'.html'  : b'text/html',
    b'.css'   : b'text/css',
    b'.json'  : b'application/json',
    b'.jpg'   : b'image/jpeg',
    b'.jpeg'  : b'image/jpeg',
    b'.png'   : b'image/png',
    b'.gif'   : b'image/gif',
    b'.ico'   : b'image/x-icon'
}

_hextobyte_cache = None

def unquote(string):
    global _hextobyte_cache

    if not string:
        return b''

    if isinstance(string, str):
        string = string.encode('utf-8')

    bits = string.split(b'%')
    if len(bits) == 1:
        return string

    res = [bits[0]]
    append = res.append

    if _hextobyte_cache is None:
        _hextobyte_cache = {}

    for item in bits[1:]:
        try:
            code = item[:2]
            char = _hextobyte_cache.get(code)
            if char is None:
                char = _hextobyte_cache[code] = bytes([int(code, 16)])
            append(char)
            append(item[2:])
        except KeyError:
            append(b'%')
            append(item)

    return b''.join(res)

def start():
  print('Start Web Server ...')
  #Setup Socket WebServer
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('', 80))
  s.listen(5)  
  #s.settimeout(120)
  s.setblocking(False)  
  while True:    
    nn = 0
    gc.collect()
    print('Wait for connection.')
    while True:
        try:
            conn, addr = s.accept()
            break
        except:
            time.sleep_ms(10)
            nn += 1
            if nn == 12000:
                print('EXIT WEB Server Timeout')
                return

    print('Got a connection from ', str(addr))
    request = b''
    conn.settimeout(0.5)
    nn = 0
    try:
        while True: 
            nn += 1
            data = conn.recv(100)
            request += data
            if nn >= 20:
                break
    except (OSError):
        pass    
    if request.find(b'\r\n\r\n') != -1:
        request_spl = request.split(b' ')
        if len(request_spl) >= 2:
            met = request_spl[0]
            request_url = request_spl[1]
            request_url = request_url[1:1000]
            request_url_spl = request_url.split(b'?')
            if len(request_url_spl) >=2:
                url = request_url_spl[0]
                query = request_url_spl[1]
            else:
                url = request_url
                query = ''
            if url == b'':
                url = b'index.html'
            print("MET: ", met)
            print("URL: ", url)
            print("QUERY: ", query)
            if met == b'POST':
                _, post = request.split(b'\r\n\r\n', 1)
                print('POST: ', post)
                
                post_f = True
                if url == b'config/iothub':
                    setting.post(post.decode())
                    post_f = False
                if url == b'config/timeserver':
                    setting.post(post.decode())
                    post_f = False
                if url == b'config/wifi':
                    setting.post(post.decode())
                    post_f = False
                if url == b'config/ipconfig':
                    setting.post(post.decode())
                    post_f = False
                if url == b'config/userjson':
                    setting.post(post.decode())
                    post_f = False

                if post_f:
                    post_spl = post.split(b'&')
                    for post_val in post_spl:
                        parameter, value = post_val.split(b'=', 1)
                        value = value.replace(b'+', b' ')
                        value = unquote(value.decode())
                        val = value.decode()
                        par = parameter.decode()
                        if post == b'action=shutdown':
                            print('EXIT WEB Server')
                            return
                        if val[0:3] != '***':
                            setting.set(par, val)

            del request    
            if (met == b'GET') | (met == b'POST'):
                try:
                    try:
                        url1, ext = url.split(b'.', 1)
                        ext = b'.' + ext
                    except (ValueError):
                        ext = b'.json'
                        url = url + ext
                        pass                    
                    response = ''
                    encoded = ''
                    if url == b'iothub.html':
                        a01 = setting.get('iothub')
                        a02 = setting.get('iotdevicename')
                        a03 = setting.get('iotdevicesecret')
                        a03 = '*' * len(a03)
                        web_page = open(url)
                        response = web_page.read().format(a01, a02, a03)
                        web_page.close
                    if url == b'timeserver.html':
                        a01 = setting.get('timeserver')
                        web_page = open(url)
                        response = web_page.read().format(a01)
                        web_page.close
                    if url == b'wifi.html':
                        a01 = setting.get('ssid')
                        a02 = setting.get('password')
                        a02 = '*' * len(a02)
                        web_page = open(url)
                        response = web_page.read().format(a01, a02)
                        web_page.close
                    if url == b'ipconfig.html':
                        a01 = setting.get('usedhcp')
                        a02 = setting.get('ip')
                        a03 = setting.get('netmask')
                        a04 = setting.get('gateway')
                        a05 = setting.get('dnsserver')
                        web_page = open(url)
                        response = web_page.read().format(a01, a02, a03, a04, a05)
                        web_page.close
                    if url == b'userjson.html':
                        a01 = setting.get('userjson')
                        web_page = open(url)
                        response = web_page.read().format(a01)
                        web_page.close
                    if url == b'config/iothub.json':
                        dict = {}
                        dict["iothub"] = setting.get('iothub')
                        dict["iotdevicename"] = setting.get('iotdevicename')
                        a01 = setting.get('iotdevicesecret')
                        a01 = '*' * len(a01)
                        dict["iotdevicesecret"] = a01                        
                        response = ujson.dumps(dict)
                    if url == b'config/timeserver.json':
                        dict = {}
                        dict["timeserver"] = setting.get('timeserver')
                        response = ujson.dumps(dict)
                    if url == b'config/wifi.json':
                        dict = {}
                        dict["ssid"] = setting.get('ssid')
                        a01 = setting.get('password')
                        a01 = '*' * len(a01)
                        dict["password"] = a01
                        response = ujson.dumps(dict)
                    if url == b'config/ipconfig.json':
                        dict = {}
                        dict["usedhcp"] = setting.get('usedhcp')
                        dict["ip"] = setting.get('ip')
                        dict["netmask"] = setting.get('netmask')
                        dict["gateway"] = setting.get('gateway')
                        dict["dnsserver"] = setting.get('dnsserver')
                        response = ujson.dumps(dict)
                    if url == b'config/info.json':
                        dict = {}
                        dict["RSSI"] = setting.get('RSSI')
                        dict["health"] = setting.get('health')
                        dict["hwid"] = setting.get('hwid')
                        dict["keypresses"] = setting.get('keypresses')
                        dict["VBat"] = setting.get('VBat')
                        dict["FWversion"] = setting.get('FWversion')
                        dict["FWnumber"] = setting.get('FWnumber')
                        response = ujson.dumps(dict)
                    if url == b'config/userjson.json':
                        dict = {}
                        dict["userjson"] = setting.get('userjson')
                        response = ujson.dumps(dict)
                    if url == b'config/opsmode.json':
                        dict = {}
                        dict["opsmode"] = setting.get('opsmode')
                        response = ujson.dumps(dict)
                    if url  == b'wifi/scan.json':
                        import wifi
                        response = wifi.scan()
                    if response == '':
                        web_page = open(url)
                        web_page.close
                    
                    conn.send(b'HTTP/1.1 200 OK\n')
                    conn.send(b'Server: MP-Server\n')
                    if ext != b'':
                        try:
                            #print('MIME:', _mimeTypes[ext])
                            conn.send(b'Content-Type: ' + _mimeTypes[ext] + b'\n')
                        except (KeyError):
                            pass
                    conn.send(b'Connection: close\r\n')
                    conn.send(b'\r\n')
                    if response == '':
                        web_page = open(url)
                        conn.sendall(web_page.read())
                        web_page.close
                    else:
                        conn.sendall(response)
                        del response
                except:
                    try:
                        conn.send('HTTP/1.1 404 Not Found\n')
                        conn.send('Server: MP-Server\n')
                        conn.send('Connection: close\r\n')
                        conn.send('\r\n')
                    except (OSError, MemoryError):
                        pass
                    pass    
        else:
            print('no html data recv')
    else:
        print('no html data recv')
    conn.close()
    
