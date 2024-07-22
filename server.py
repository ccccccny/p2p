#!/usr/bin/env python
# coding:utf-8

import socket
import struct
import sys
from collections import namedtuple

FullCone = "Full Cone"  # 0
RestrictNAT = "Restrict NAT"  # 1
RestrictPortNAT = "Restrict Port NAT"  # 2
SymmetricNAT = "Symmetric NAT"  # 3
UnknownNAT = "Unknown NAT" # 4
NATTYPE = (FullCone, RestrictNAT, RestrictPortNAT, SymmetricNAT, UnknownNAT)

def addr2bytes(addr, nat_type_id):  # 将主机名、端口、NAT 类型 ID 打包成字节序列并输出*****************************************
    """Convert an address pair to a hash."""
    host, port = addr
    try:
        host = socket.gethostbyname(host)  # 如果传入的host是域名，则转换为IP地址；传入的是IP地址，返回IP地址
    except (socket.gaierror, socket.error):
        raise ValueError("invalid host")  # host如果不是域名或IP则报错
    try:
        port = int(port) # 把传入的port端口转为整型
    except ValueError:
        raise ValueError("invalid port")  # 转换失败报错
    try:
        nat_type_id = int(nat_type_id)  # 把传入的NAT 类型 ID转为整型
    except ValueError:
        raise ValueError("invalid NAT type")  # 转换失败报错
    bytes = socket.inet_aton(host)  # 把主机名转换为网络字节序列的IP地址，host如果是192.168.1.1输出b'\xc0\xa8\x01\x01'
    bytes += struct.pack("H", port)  
    bytes += struct.pack("H", nat_type_id)  # H是模式，使用 struct.pack 函数将端口和 NAT 类型 ID 打包成字节序列
    return bytes


def main():
    port = sys.argv[1]
    try:
        port = int(sys.argv[1])  #先尝试从命令行参数获取端口号，并将其转换为整数
    except (IndexError, ValueError):
        pass

    sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #创建一个 UDP 套接字 sockfd
    sockfd.bind(("", port))  #将套接字 sockfd绑定到指定的端口
    print("listening on *:%d (udp)" % port)  #输出正在监听的端口

    poolqueue = {}  # poolqueue 字典用于暂存客户端1的连接请求
    # A,B with addr_A,addr_B,pool=100
    # temp state {100:(nat_type_id, addr_A, addr_B)}
    # final state {addr_A:addr_B, addr_B:addr_A}
    symmetric_chat_clients = {}  # symmetric_chat_clients 字典用于处理对称 NAT 类型客户端的聊天连接，存放2个客户端连接信息，应该是IP地址吧
    ClientInfo = namedtuple("ClientInfo", "addr, nat_type_id")  # 还定义了一个名为 ClientInfo 的具名元组用于存储客户端的地址和 NAT 类型 ID 。可能类似表格，可以使用ClientInfo['ClientInfo']吧
    while True:
        data, addr = sockfd.recvfrom(1024)  #根据len 67，addr应该包括发送方客户端地址和 NAT 类型 ID；data如果是连接请求，应该包含发送方客户端地址和 NAT 类型 ID，这不是和addr重复了吗？
        print (data)  #服务器通过套接字 sockfd 从网络中接收最多 1024 字节的(数据以及发送方的地址)，并将接收到的数据打印出来。
        if data.startswith(b"msg "):  #接收到的数据如果是msg开头，则认为data内是聊天消息；否则认为data内是连接请求，理论上这时候应该会把data添加到symmetric_chat_clients[addr]，后面代码好像不对劲
            # forward symmetric chat msg, act as TURN server
            try:  #尝试将消息转发给对称聊天客户端。
                sockfd.sendto(data[4:], symmetric_chat_clients[addr])  #尝试发送数据给接收方，data[4:]为客户端1要发送的数据，symmetric_chat_clients[addr]为客户端2的地址
                print("msg successfully forwarded to {0}".format(symmetric_chat_clients[addr]))  # 输出数据成功发送给接收客户端
                print(data[4:])  #输出发送的数据
            except KeyError:  #如果在 symmetric_chat_clients 中找不到对应的客户端地址，会捕获 KeyError 并打印错误提示。理论上应该不可能出现吧？
                print("something is wrong with symmetric_chat_clients!")
        else:  #理论上这时候应该会把data添加到symmetric_chat_clients[addr]，好像有问题？还是打洞很复杂？
            # help build connection between clients, act as STUN server
            print ("connection from %s:%d" % addr)  #输出发送方客户端地址和 NAT 类型 ID 
            pool, nat_type_id = data.strip().split()  # pool: 来源客户端地址  ; nat_type_id: NAT 类型 ID ,应该都是字节类型吧？
            print(pool,'这是pool 01')
            sockfd.sendto(("ok {0}".format(pool)).encode('utf-8'), addr)  #sockfd.sendto("ok {0}".format(pool), addr)    向客户端发送确认信息 ok {pool} 。这里可能是通过发送连接数据测试客户端和服务器的连接以及数据完整性
            print("pool={0}, nat_type={1}, ok sent to client".format(pool, NATTYPE[int(nat_type_id)]))  #输出客户端地址和NAT 类型 ID，表示已向客户端发送连接数据
            data, addr = sockfd.recvfrom(2)  #再次接收客户端的 2 字节响应，如果 data 不是 ok ，就跳过本次循环，继续等待下一次数据接收。
            if data != "ok":  # 说明客户端接收数据失败或者接收数据不完整，需要重新连接
                continue

            #如果 data 是 ok，即客户端成功接收数据，即双向连接成功
            print ("request received for pool:", pool)  #输出客户端IP

            try:  
                print(pool,'这是pool 02')
                a, b = poolqueue[pool].addr, addr  # 字典为空即报错，进入报错执行
                nat_type_id_a, nat_type_id_b = poolqueue[pool].nat_type_id, nat_type_id  # nat_type_id和addr为客户端2的连接信息
                sockfd.sendto(addr2bytes(a, nat_type_id_a), b)  # 把从字典里取出来的客户端1的连接信息字节化后 发给客户端2（b未字节化）
                sockfd.sendto(addr2bytes(b, nat_type_id_b), a)  # 把客户端2的连接信息字节化后 发给客户端1（a未字节化），地址和NAT 类型 ID都没有字节化，可能是客户端发来的也不是字节化的
                print ("linked", pool)  #输出客户端2 IP
                del poolqueue[pool]
            except KeyError:  # 向字典添加具名元组化的IP和NAT 类型 ID(客户端1的)
                print(pool)  #自己加的，pool好像有问题
                poolqueue[pool] = ClientInfo(addr, nat_type_id)

            if pool in symmetric_chat_clients:
                if nat_type_id == '3' or symmetric_chat_clients[pool][0] == '3':
                    # at least one is symmetric NAT
                    recorded_client_addr = symmetric_chat_clients[pool][1]
                    symmetric_chat_clients[addr] = recorded_client_addr
                    symmetric_chat_clients[recorded_client_addr] = addr
                    print("Hurray! symmetric chat link established.")
                    del symmetric_chat_clients[pool]
                else:
                    del symmetric_chat_clients[pool]  # neither clients are symmetric NAT
            else:
                symmetric_chat_clients[pool] = (nat_type_id, addr)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: server.py port")
        exit(0)
    else:
        assert sys.argv[1].isdigit(), "port should be a number!"
        main()