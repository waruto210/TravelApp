import message
import socket
import threading
import math
import os
import pickle


class Server:
    # 定义服务器ip
    HOST = "0.0.0.0"
    # HOST = "172.17.8.152"
    # HOST = "10.21.167.146"
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
        if not os.path.isfile('./data/message.pkl'):
            message_unit0 = message.Message()
            with open('./data/message.pkl', 'wb') as f:
                pickle.dump(message_unit0, f)
        else:
            with open('./data/message.pkl', 'rb') as f:
                message_unit0 = pickle.load(f)
        self.message_unit = message_unit0
        print(self.message_unit)

        self.control()

    @staticmethod
    def get_close(sock):
        # 断开连接
        sock.close()

    def register(self, sock):
        """注册用户

        :param sock:网络接口
        """
        sock.send(b'account')
        account = sock.recv(1024).decode('utf8')

        sock.send(b'password')
        password = sock.recv(1024).decode('utf8')

        sock.send(b'nickname')
        nickname = sock.recv(1024).decode('utf8')
        print(self.message_unit)
        temp = self.message_unit.register(account, password, nickname)
        if temp == True:
            # 注册成功
            sock.send(b'true')
            self.save_file()
            print('register succeed')
        else:
            # 用户已存在，注册失败
            sock.send(b'false')
            print('register fail')
        # user_unit = user.User(account, password, nickname)
        # if self.message_unit.message.get(account, False) is False:
        #     # 注册成功
        #     self.message_unit.message[user_unit.account] = user_unit
        #     sock.send(b'true')
        # else:
        #     # 用户已存在，注册失败
        #     sock.send(b'false')
        #     # 注册成功

    def log_in(self, sock):
        """
        检测并登陆用户
        """
        # 握手获取账号、密
        sock.send(b'account')
        account = sock.recv(1024).decode('utf8')

        sock.send(b'password')
        password = sock.recv(1024).decode('utf8')

        # 检测用户状态、信息
        user_unit = self.message_unit.message.get(account, False)
        if user_unit is False:
            back = "nonexistent"
        elif user_unit.password != password:
            back = "error"
        elif account in self.record:
            back = "logged"
        else:
            back = "true"

        if back != "true":
            sock.send(back.encode('utf8'))
            print('log in fail')
        else:
            # 登陆成功
            sock.send(back.encode('utf8'))

            ready = sock.recv(1024)
            if ready != b'length':
                print('wrong')
                return BufferError

            # 发送用户数据长度
            data = pickle.dumps(user_unit)
            length = str(len(data))
            sock.send(length.encode('utf8'))

            # 收到确认，发送用户数据
            ready = sock.recv(1024)
            if ready != b'ready':
                print('wrong')
                return BufferError
            sock.sendall(data)
            self.record.append(account)
            print("log in : "+account)

    def log_out(self, sock):
        """
        登出用户并改变状态
        :param sock: 网络
        """
        # 更新用户数据
        self.update_user(sock)

        # 发送确认指令
        sock.send(b'ready')

        # 接收登录账号
        account = sock.recv(1024).decode('utf8')
        print("log out : " + account)

        # 释放登录
        self.record.remove(account)

    def update_user(self, sock):
        """接收上传的用户信息，并更新

        :param sock: 网络
        """

        # 发送确认，接收数据长度
        sock.send(b'length')
        length = sock.recv(1024)
        length = int(length.decode('utf8'))

        sock.send(b'ready')

        # 接收数据
        data = b""
        time_get = math.ceil(length / 1024)
        for i in range(time_get):
            d = sock.recv(1024)
            data += d

        # 反序列化用户对象
        user_unit = pickle.loads(data)
        # 更新用户
        self.message_unit.message[user_unit.account] = user_unit
        self.save_file()

        # sock.send(b'over')

        print("update user")

    def save_file(self):
        """
        讲全体数据写入数据库
        """
        with open('./data/message.pkl', 'wb') as f:
            pickle.dump(self.message_unit, f)
        print("save")

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

            # 客户端发送log_in,调用函数log_in(),等待下一命令
            if cmd == "log_in":
                self.log_in(sock)
                continue

            # 客户端发送log_out,调用函数log_out(),等待下一命令
            if cmd == "log_out":
                self.log_out(sock)
                continue

            # 客户端发送register,调用函数register(),等待下一命令
            if cmd == "register":
                self.register(sock)
                continue

            # 客户端发送update_user,调用函数update_user(),等待下一命令
            if cmd == "update_user":
                self.update_user(sock)
                continue

    # 获取从客户端发送的数据
    # 一次获取1k的数据

    def control(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(self.addr)
        s.listen(512)
        while True:
            sock, addr = s.accept()
            # 用线程去处理新接收的连接(用户)
            client_thread = threading.Thread(target=self.handle_sock, args=(sock, addr))
            client_thread.start()


sever = Server()