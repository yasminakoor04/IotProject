import wifiConnection


def http_get(url='http://detectportal.firefox.com/'):
    import socket
    import time
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes(
        'GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    time.sleep(1)
    rec_bytes = s.recv(10000)
    print(rec_bytes)
    s.close()


# WiFi Connection
try:
    ip = wifiConnection.connect()
except KeyboardInterrupt:
    print("Keyboard interrupt")

# HTTP request
try:
    http_get()
except (Exception, KeyboardInterrupt) as err:
    print("No Internet", err)

# WiFi Disconnect (Optional, uncomment if needed)
# wifiConnection.disconnect()
