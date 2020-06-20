"""
web server 程序
完成一个类，提供给使用者
使用可通过这个类可以快速搭建web server


"""
import re
from socket import socket
from select import select
class Webserver:
    def __init__(self,host="0.0.0.0",port=8000,html=None):
        self.host=host
        self.port=port
        self.html=html
        self.address=(host,port)
        self.creat_socket()
        self.bind()
        self._rlist = []
        self._wlist = []
        self._xlist = []


    def creat_socket(self):
        self.sock=socket()
        self.sock.setblocking(False)

    def bind(self):
        self.sock.bind(self.address)
    def handle(self,connfd):
        data = connfd.recv(4096).decode()
        # if not data:
        #     connfd.close()
        #     self._rlist.remove(connfd)
        #     return
        # # print(data.decode())
        # #解析请求————》解析出请求的内容 请求行的第二部分
        # else:
        #     t = data.split(" ")[1]
        #     print(t)
        #     self.get_html(connfd,t)
        if data:
            # 提取请求内容
            t = data.split(" ")[1]
            print("请求内容：", t)
            self.get_html(connfd, t)  # 判定网页是否存在，给客户端发送
        else:
            # 配有匹配到则断开客户端
            connfd.close()
            self._rlist.remove(connfd)
            return


    def get_html(self,connfd,info):
        if info =="/":
            filename=self.html+"/index.html"
        else:
            filename=self.html+info
        try:
            f = open(filename, "rb")
        except:
            response = "HTTP/1.1 404 not found\r\n"  # 响应行
            response += "Content-Type:text/html\r\n"  # 响应头 一个
            response += "\r\n"  # 空行
            response += "fdh "  # 响应体
            response=response.encode()
        else:
            data=f.read()
            response = "HTTP/1.1 200 OK\r\n"  # 响应行
            response += "Content-Type:text/html\r\n"  # 响应头 一个
            response += "Content-Length:%d\r\n"%len(data)  # 响应头 一个
            # response += "Content-Length:%d\r\n" % len(data)
            response += "\r\n"  # 空行
            response = response.encode()+data  # 响应体
            f.close()
        finally:
            connfd.send(response)
    #启动函数 启动整个服务--客户端可以发起连接
    def start(self):
        self.sock.listen(5)
        print("Listen to the port %d"%self.port)
        self._rlist.append(self.sock)
        while True:
            rs,ws,xs=select(self._rlist,self._wlist,self._xlist)
            for r in rs:
                if r is self.sock:
                    c,addr=r.accept()
                    c.setblocking(False)
                    self._rlist.append(c)
                else:
                    self.handle(r)



if __name__ == '__main__':
    #使用者应该怎么使用我这个类

    #什么东西应该用户确定，通过参数传入
    #地址  要展示的网页
    httped = Webserver(host="0.0.0.0",port=8886,html="./static")
    httped.start()