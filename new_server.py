import socket

def huo_qu_ke_hu_duan_addr():#获取客户端地址
    # 本地监听端口
    listen_port = 11111
    # 创建监听套接字
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.bind(('172.24.130.144', listen_port))
    listen_sock.listen(5)

    while True:
        # 等待客户端连接
        client_socket, client_address = listen_sock.accept()
        print(f"接收到来自客户端 {client_address} 的连接")
        data = client_socket.recv(1024)
        print(f"收到数据: {data.decode('utf-8')}")
        return client_address


# client_address：目标节点 B 的地址和端口

while True:
    client_address=huo_qu_ke_hu_duan_addr()
    print('已获取客户端地址',client_address)
# 尝试连接到节点 B
    try:
        sock_to_B = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('完成创建 数据发送服务器')
        sock_to_B.connect(client_address)
        print("数据发送服务器已连接到节点 B")
    except Exception as e:
        print(f"连接到节点 B 时出错: {e}")

# 等待节点 B 的连接
    #conn, addr = listen_sock.accept()
    #print(f"接收到来自 {addr} 的连接")

    # 从节点 B 接收数据
    data = sock_to_B.recv(1024)
    if data:
        print(f"从节点 B 收到: {data.decode('utf-8')}")

    # 向节点 B 发送数据
    message = input("输入要发送给节点 B 的消息: ")
    sock_to_B.send(message.encode('utf-8'))




# 通信逻辑
while True:
    # 从节点 B 接收数据
    data = sock_to_B.recv(1024)
    if data:
        print(f"从节点 B 收到: {data.decode('utf-8')}")

    # 向节点 B 发送数据
    message = input("输入要发送给节点 B 的消息: ")
    sock_to_B.send(message.encode('utf-8'))