"""
基于select方法的IO网络并发
"""
from socket import *
from select import select

HOST = "0.0.0.0"
POST = 8888
ADDR = (HOST, POST)

# 创建监听套接字
sock = socket()
sock.bind(ADDR)
sock.listen(5)
sock.setblocking(False)
print("Listen the port %d" % POST)

rlist = [sock]
wlist = []
xlist = []

while True:
    rs, ws, xs = select(rlist, wlist, xlist)
    for r in rs:
        if r == sock:
            # 处理连接
            conn, addr = r.accept()
            print("Connet from", addr)
            conn.setblocking(False)
            rlist.append(conn)
        else:
            # 与客户端交互
            data = r.recv(1024)
            if not data:
                rlist.remove(r)
                r.close()
                continue
            print("收到：", data.decode())
            # r.send(b'Thanks')
            wlist.append(r)
    for w in ws:
        w.send(b"OK")
        wlist.remove(w)
