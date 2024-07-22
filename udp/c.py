import socket
import threading
import time
import os
import zipfile
import hashlib

#连接服务器
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverAddress = ('112.124.2.225', 11111)

s.connect(serverAddress)
myAddress = s.getsockname() #本机ip端口
chain = input('连接口令：')
send = ('#connectChain*'+chain).encode()
s.sendall(send)
myPeer = eval(s.recv(2048).decode())  # peer ip端口
print('myAddress: ', myAddress)
print('got myPeer: ', myPeer)
s.close()

#发送一个TCP连接，用于打洞，无需对方接收
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(myAddress)
try:
    s.connect(myPeer)
except ConnectionRefusedError:
    print('已尝试打洞')
s.close()

#监听TCP连接
sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sc.bind(myAddress)
sc.listen(1)
s, address = sc.accept()
sc.close()

#聊天
def sendToMyPeer():
    while True:
        send_text = input("我方发送：（发送文件请输入wenjian）")
        if send_text=='wenjian':
            s.sendall(send_text.encode())
            name=input('输入文件地址')
            y=os.stat(name)
            print('共{y.st_size}字节')
            with open(name,'bw') as f:
                a=f.read()
        s.sendall(send_text.encode())


def recFromMyPeer():
    while True:
        message = s.recv(2048).decode()
        print('\r对方回复：'+message+'\n我方发送：', end='')

sen_thread = threading.Thread(target=sendToMyPeer)
rec_thread = threading.Thread(target=recFromMyPeer)

rec_thread.start()
sen_thread.start()


sen_thread.join()
rec_thread.join()


def calMD5(str):
    m = hashlib.md5()
    m.update(str)

     
    return m.hexdigest()

def calMD5ForFile(file):
    statinfo = os.stat(filePath + file)
     
    if int(statinfo.st_size)/(1024*1024) >= 1000 :
        print ("File size > 1000, move to big file...")
        return calMD5ForBigFile(filePath  + file)
    
    m = hashlib.md5()
    f = open(filePath + file, 'rb')
    m.update(f.read())
    f.close()
    

def wj():
    send_text = input("我方发送：（发送文件请输入wenjian）")

    if send_text=='wenjian':
        s.sendall(send_text.encode())#告诉另一客户端准备接收文件
        name=input('输入文件目录和地址，空格分开').strip().split()
        print(name)
        zip_pass=name[0]
        zip_file = name[1]
        all_pass=name[0]+'\\'+name[1]
        zip_file_new = zip_file+'.zip'
        # 如果文件存在
        if not os.path.exists(zip_file):
            print('您要压缩的文件不存在！')
        else:
            # step 2: 实例化zipfile对象
            zip = zipfile.ZipFile(zip_file_new, 'w', zipfile.ZIP_DEFLATED)
            # step 3: 写压缩文件
            zip.write(zip_file)
            print('文件压缩成功！')

        y=os.stat(name)
        t=(y+3)//1024+1
        print('共{y.st_size}字节,共发送{t}次')
        with open(name,'bw') as f:
            a=f.read()


