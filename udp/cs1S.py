import socket
import random

# 服务器监听的端口
SERVER_PORT = 5000

# 记录口令信息
peers = []

'''
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("172.24.130.144", SERVER_PORT))
print("Listening on *:%d (UDP)" % SERVER_PORT)
sock.listen(5)
client_socket1, client_address1 = sock.accept()
print(client_address1)
while True:
    data, addr = sock.recvfrom(2048)
    # 帮助客户端建立连接，充当 STUN 服务器
    print("Received:", data.decode())
'''

addre=[]

# 创建一个 TCP 套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定地址和端口
server_address = ('172.24.130.144', 5000)
server_socket.bind(server_address)

# 监听连接
server_socket.listen(5)
print('开始连接')
client_socket1, client_address1 = server_socket.accept()
print(f"连接来自: {client_address1},等待其他客户端连接")
addre.append(client_address1)

client_socket2, client_address2 = server_socket.accept()
print(f"连接来自: {client_address2}")
addre.append(client_address2)
print(addre)

while True: 
    # 接收客户端数据
    data1 = client_socket1.recv(1024)
    if not data1:
        continue
    else:
        print(data1)
        client_socket1.send(str(client_address2).encode())
        client_socket2.send(str(client_address1).encode())
        print('addr已发送')
        break


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto('hai!'.encode(), client_address2)
