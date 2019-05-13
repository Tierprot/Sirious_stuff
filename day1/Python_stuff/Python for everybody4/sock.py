import socket
import time

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect(("www.protres.ru", 80))
mysock.send(b'GET / HTTP/1.1\r\nhost:www.protres.ru\r\nConnection: close\r\n\r\n')
data = mysock.recv(50000).decode("WINDOWS-1251")
mysock.close()
print(data)
time.sleep(60)

