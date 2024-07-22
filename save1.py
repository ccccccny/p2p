import socket
import threading
import time

# 创建一个 TCP 套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定地址和端口
server_address = ('172.24.130.144', 5000)
server_socket.bind(server_address)

# 监听连接
server_socket.listen(5)

addre=[]

# 等待客户端连接
client_socket1, client_address1 = server_socket.accept()
print(f"连接来自: {client_address1}")
addre.append(client_address1)


client_socket2, client_address2 = server_socket.accept()
print(f"连接来自: {client_address2}")
addre.append(client_address2)


print(addre)



def khd2(client_socket1,client_socket2):

    while True:
    # 接收客户端数据
        data2 = client_socket2.recv(1024)
        if not data2:
            break
        print(f"收到客户端2数据: {data2.decode('utf-8')}，正在发送给客户端1")

        # 发送响应数据给客户端
        response = data2
        client_socket1.send(response)
        print('已发送给客户端1')


def khd1(client_socket1,client_socket2):

    while True:
        # 接收客户端数据
        data1 = client_socket1.recv(1024)
        if not data1:
            break
        print(f"收到客户端1数据: {data1.decode('utf-8')}，正在发送")

        # 发送响应数据给客户端
        response = data1
        client_socket2.send(response)
        print('已发送给客户端2')

def xin_tiao(client_socket1,client_socket2):
    while True:
    # 发送心跳数据
        client_socket1.send('xintiao'.encode('utf-8'))
        client_socket2.send('xintiao'.encode('utf-8'))
        print("发送心跳数据",time.time())
        time.sleep(60*3)

# 创建接收数据和发送数据的线程
receive_thread = threading.Thread(target=khd1, args=(client_socket1,client_socket2))
send_thread = threading.Thread(target=khd2, args=(client_socket1,client_socket2))
xintiao_thread = threading.Thread(target=xin_tiao, args=(client_socket1,client_socket2))


receive_thread.start()
send_thread.start()
xintiao_thread.start()

receive_thread.join()
send_thread.join()
xintiao_thread.join()


# 关闭套接字
client_socket1.close()
client_socket2.close()
server_socket.close()