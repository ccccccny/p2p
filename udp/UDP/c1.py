import socket
import threading

#连接服务器
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 5555))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverAddress = ('47.121.201.140', 5555)


s.sendto('''hhhhh'''.encode(), serverAddress)

d=s.recv(2048)
d=eval(d.decode())
print(d)

def send_test(s,d):
    while True:
        s.sendto(input('输入：').encode(), d)
        print('发送成功')

def accept_test(s):
    while True:
        c, s_address = s.recvfrom(2048)
        print(c.decode(),'\n输入：',end='')
        #s.sendto(b'hello', c)

t1=threading.Thread(target=send_test, args=(s,d))
t2=threading.Thread(target=accept_test,args=(s,))
t1.start()
t2.start()
t1.join()
t2.join()