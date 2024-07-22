import socket
import random

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 11111))

#记录口令信息
peers = {}

while True:
    message, address = s.recvfrom(2048)
    message = message.decode()
    if not message.startswith('#connectChain*'):
        continue
    chain = message.replace('#connectChain*', '')
    if chain not in peers:
        peers[chain] = address
    else:
        print('matchedPeers: ', peers[chain], address)
        verifySignature = random.randint(10000, 99999)  #签名验证,用于peers双方验证身份
        #给双方发送peer地址信息和签名
        s.sendto(str([peers[chain], verifySignature]).encode(), address)
        s.sendto(str([address,verifySignature]).encode(), peers[chain])
        peers.pop(chain)
