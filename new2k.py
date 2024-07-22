import socket
import threading

# 创建一个 TCP 套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接服务器
server_address = ('112.124.2.225', 5000)
client_socket.connect(server_address)



def send_data(client_socket):
    while True:
        # 发送数据给服务器
        message = input("输入要发送给服务器的消息: ")
        client_socket.send(message.encode('utf-8'))

def receive_data(client_socket):
    while True:
    # 接收服务器响应数据
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"收到: {data.decode('utf-8')}")



# 创建两个线程来分别处理发送数据和接收数据
receive_thread = threading.Thread(target=receive_data, args=(client_socket,))
send_thread = threading.Thread(target=send_data, args=(client_socket,))

receive_thread.start()
send_thread.start()

receive_thread.join()
send_thread.join()
# 关闭套接字
client_socket.close()