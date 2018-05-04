import usocket as socket


def get_file(url, file):
    _, _, host, path = url.split('/', 3)
    if ':' in host:
        host, port = host.split(':', 1)
    else:
        port = 80
    addr = socket.getaddrinfo(host, int(port))[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))

    f = open(file, 'w')

    while True:
        datastr = s.readline()
        if datastr != b'\r\n':
            print(datastr)
        else:   
            break

    while True:
        data = s.recv(100)
        if data:
            f.write(data)
        else:
            f.close()
            break

def get(url):
    _, _, host, path = url.split('/', 3)
    if ':' in host:
        host, port = host.split(':', 1)
    else:
        port = 80
    addr = socket.getaddrinfo(host, int(port))[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))

    while True:
        datastr = s.readline()
        if datastr != b'\r\n':
            print(datastr)
        else:   
            break

    buffer = b''
    while True:
        data = s.recv(100)
        if data:
            buffer += data
        else:
            return buffer
            break
