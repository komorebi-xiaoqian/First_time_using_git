from socket import *
from select import select


class Handle:
    def __init__(self, html=None):
        self.html = html

    def _get_request(self, conn):
        request = conn.recv(1024)
        if not request:
            return
        else:
            request = request.decode().split(" ")[1]
            print(request)
            return request

    def main(self, conn):
        info = self._get_request(conn)
        self._send_response(conn, info)

    def _send_response(self, conn, info):
        if info == "/":
            info = "/index.html"
        try:
            fr = open(self.html + info, "rb")
        except:
            with open(self.html + '/404.html', "rb") as fr:
                data = fr.read()
            response = self._respose("404 Not Found", data)
        else:
            response = self._respose("200 OK", fr.read())
            fr.close()
        finally:
            conn.send(response)

    def _respose(self, status, data):
        response = "HTTP/1.1 %s\r\n" % status
        response += "Content-Type:text/html\r\n"
        response += "\r\n"
        response = response.encode() + data
        return response


class WebServer:
    def __init__(self, host="", post=0, html=None):
        self.host = host
        self.port = post
        self.address = (self.host, self.port)
        self.sock = self._create_socket()
        self.rlist = [self.sock]
        self.handle = Handle(html)

    def _create_socket(self):
        sock = socket()
        sock.bind(self.address)
        sock.setblocking(False)
        return sock

    def start(self):
        while True:
            self.sock.listen(5)
            rs, ws, xs = select(self.rlist, [], [])
            for r in rs:
                if r == self.sock:
                    conn, adrr = self.sock.accept()
                    print("Content from", conn)
                    self.rlist.append(conn)
                else:
                    self.handle.main(r)
                    self.rlist.remove(r)
                    r.close()


if __name__ == '__main__':
    web = WebServer(host="0.0.0.0", post=8888, html="./static")
    web.start()
