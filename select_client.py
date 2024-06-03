from socket import *

tcp = socket()
tcp.connect(("127.0.0.1", 8888))
while True:
    msg = input(">>")
    if not msg or msg == "##":
        break
    tcp.send(msg.encode())
    data = tcp.recv(1024)
    print(data.decode())
tcp.close()
