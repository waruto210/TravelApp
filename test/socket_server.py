import socket
import threading
import os
import pickle


class Server:
    # 定义服务器ip
    HOST = "0.0.0.0"
    # 定义端口号
    PORT = 8000
    # 由于使用socket进行连接，需要把ip和端口先转换为元组
    addr = (HOST, PORT)
    # 设定了网络连接方式，以及传输使用的协议
    conn = None
    s = None
    # server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # server.bind(('0.0.0.0', 8000))
    # server.listen(100)

    def __init__(self):
        self.control()

    @staticmethod
    def get_file(sock):
        # 向客户端发送提示信息
        # self.s.send("please sendfile:".encode("utf8"))
        # 设置接受数据大小
        print(1)
        while True:
            data = b""
            while True:
                d = sock.recv(1024)
                if d:
                    data += d
                else:
                    break
            # 向指定的目录写入客户端发送过来的信息
            with open('./data/message.pkl', 'wb') as f:
                f.write(data)
            print('get')
            break
        # 关闭连接
        sock.close()

    @staticmethod
    def send_file(sock):
        print("here")
        # 设置接受数据大小，接受客户端发送来的文件路径
        # filepath = conn.recv(1024)
        # 读取客户端指定的文件
        with open('./data/message.pkl', 'rb') as f:
            data = f.read()
        # 向客户端发送客户端指定的文件内容
        sock.sendall(data)
        print('send')
        # 关闭连接
        sock.close()
        print(1)

    def handle_sock(self, sock, addr):
        while True:
            # 接收客户端发送来的数据
            cmd = sock.recv(1024).decode('utf-8')
            # 如果客户端发送过来的是bye,结束进程
            if cmd == "bye":
                break
            # 如果客户端发送过来的是upload,调用函数get_file(),结束进程
            if cmd == "upload":
                self.get_file(sock)
                break
            # 如果客户端发送过来的是down,调用函数send_file(),结束进程
            if cmd == "download":
                print("Download")
                self.send_file(sock)
                break
            # # popen()可以执行shell命令，并读取此命令返回值
            # data = os.popen(cmd)
            # # 将得到的内容通过read()转换后给了sdata
            # sdata = data.read()
            # if sdata:
            #     # 将得到的内容全部发送给客户端
            #     conn.sendall(sdata)
            # else:
            #     # 如果客户端发送过来的是其他没有的指令，向客户端返回finish,防止程序假死
            #     conn.send("finish")
        sock.close()  # 关闭连接

    # 获取从客户端发送的数据
    # 一次获取1k的数据

    def control(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(self.addr)
        self.s.listen(100)
        while True:
            sock, addr = self.s.accept()
            # 用线程去处理新接收的连接(用户)
            print(1)
            client_thread = threading.Thread(target=self.handle_sock, args=(sock, addr))
            print(2)
            client_thread.start()
            client_thread.join()


sever = Server()