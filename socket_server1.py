import socket
import threading
import math


class Server:
    # 定义服务器ip
    HOST = "0.0.0.0"
    # HOST = "172.17.8.152"
    # 定义端口号
    PORT = 8000
    # 由于使用socket进行连接，需要把ip和端口先转换为元组
    addr = (HOST, PORT)
    # 设定了网络连接方式，以及传输使用的协议
    s = None
    # server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # server.bind(('0.0.0.0', 8000))
    # server.listen(100)

    def __init__(self):
        self.record = []
        self.control()

    @staticmethod
    def get_file(sock):
        # 向客户端发送提示信息
        # self.s.send("please sendfile:".encode("utf8"))
        # 设置接受数据大小
        sock.send(b'ready')

        length = sock.recv(1024)
        length = int(length.decode('utf8'))
        print(123)

        sock.send(b'ready')
        print(456)

        data = b""
        time_get = math.ceil(length / 1024)
        for i in range(time_get):
            d = sock.recv(1024)
            data += d

        # 向指定的目录写入客户端发送过来的信息
        with open('./data/message.pkl', 'wb') as f:
            f.write(data)

    @staticmethod
    def send_file(sock):
        # 设置接受数据大小，接受客户端发送来的文件路径
        # filepath = conn.recv(1024)
        # 读取客户端指定的文件
        with open('./data/message.pkl', 'rb') as f:
            data = f.read()
        # 向客户端发送客户端指定的文件内容
        length = str(len(data))
        sock.send(length.encode('utf8'))

        ready = sock.recv(1024)
        if ready != b'ready':
            print('wrong')
            return

        sock.sendall(data)

    @staticmethod
    def get_close(sock):

        sock.close()

    def log_in(self, sock):
        """登陆
        登录账号检测
        """
        # 发送确认指令
        sock.send(b'ready')

        # 接收登录账号
        account = sock.recv(1024)

        # 判断账号是否已登录，未登录则登录并返回true，已登录则返回logged
        if account in self.record:
            sock.send(b'logged')
        else:
            self.record.append(account.decode('utf8'))
            sock.send(b'true')

    def log_out(self, sock):
        """登出
        账号登出
        :param sock: 连接
        :return:
        """
        # 发送确认指令
        sock.send(b'ready')

        # 接收登录账号
        account = sock.recv(1024)

        # 释放登录
        self.record.remove(account.decode('utf8'))

    def handle_sock(self, sock, addr):
        while True:
            # 接收客户端发送来的数据
            cmd = sock.recv(1024)
            cmd = cmd.decode('utf-8')
            # print(cmd)

            # 如果客户端发送过来的是bye,结束进程
            if cmd == "bye":
                self.get_close(sock)
                break

            # 如果客户端发送过来的是upload,调用函数get_file(),等待下一命令
            if cmd == "upload":
                self.get_file(sock)
                continue

            # 如果客户端发送过来的是down,调用函数send_file(),等待下一命令
            if cmd == "download":
                self.send_file(sock)
                continue

            # 如果客户端发送过来的是log_in,调用函数log_in(),等待下一命令
            if cmd == "log_in":
                self.log_in(sock)
                continue

            if cmd == "log_out":
                self.log_out(sock)
                continue

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
        # sock.close()  # 关闭连接

    # 获取从客户端发送的数据
    # 一次获取1k的数据

    def control(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(self.addr)
        self.s.listen(100)
        i = 0
        while True:
            print('第'+str(i)+'次')
            i += 1
            sock, addr = self.s.accept()
            # 用线程去处理新接收的连接(用户)
            client_thread = threading.Thread(target=self.handle_sock, args=(sock, addr))
            client_thread.start()


sever = Server()

