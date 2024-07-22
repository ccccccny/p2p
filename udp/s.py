import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('172.24.130.144', 11111))

#记录口令信息
peers = {}

sock.listen(5)
while True:
    s, address = sock.accept()
    message = s.recv(2048).decode()
    if not message.startswith('#connectChain*'):
        continue
    chain = message.replace('#connectChain*', '')
    if chain not in peers:
        peers[chain] = (s, address)
    else:
        print('matchedPeers: ', peers[chain][1], address)
        #给双方发送peer地址信息和签名
        peers[chain][0].sendall(str(address).encode())
        s.sendall(str(peers[chain][1]).encode())
        s.close()
        peers.pop(chain)
