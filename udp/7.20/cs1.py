#服务器
import socket

socked=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socked.bind(("172.24.130.144", 5000))
socked.listen(5)

#获取c1和c2的addr
client_socket1, client_address1 = socked.accept()
print(client_address1)
client_socket2, client_address2 = socked.accept()
print(client_address2)

#发送对方地址
client_socket1.send(client_address2.encode('utf-8'))
client_socket2.send(client_address1.encode('utf-8'))


while True:
    data = client_socket1.recv(2048)

    if not data:
        continue
    else:
        print(data.decode())
        continue