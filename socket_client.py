import user
import socket
import math
import time
import pickle


class Client:
    """socket通信客户端

    可同时进行多线程访问
    """

    # 定义服务器ip（注意，此时应访问阿里云公网IP）
    HOST = "39.106.140.121"

    # HOST = "127.0.0.1"

    # 定义端口号
    PORT = 8000

    # 由于使用socket进行连接，需要把ip和端口先转换为元组
    addr = (HOST, PORT)

    def __init__(self):
        """建立连接

        与服务器端借助socket进行通信
        """
        # 设定了网络连接方式 IPV4，以及传输使用的协议 TCP
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 连接服务器
        self.client.connect(self.addr)

    def send_close(self):
        """断开服务器
        """
        # 发送释放端口命令
        cmd = 'bye'
        time.sleep(0.3)
        self.client.send(cmd.encode('utf8'))
        self.client.close()

    def register(self, account: str, password, nickname: str):
        """注册用户

        :param account: 账号
        :param password: 密码
        :param nickname: 昵称
        :return: 注册成功返回True，注册失败返回False
        """
        # 发送注册命令
        cmd = 'register'
        self.client.send(cmd.encode('utf8'))

        # 发送账户、密码、昵称
        back = self.client.recv(1024)
        if back != b'account':
            print('wrong')
            return BufferError
        self.client.send(account.encode('utf8'))

        back = self.client.recv(1024)
        if back != b'password':
            print('wrong')
            return BufferError
        self.client.send(password.encode('utf8'))

        back = self.client.recv(1024)
        if back != b'nickname':
            print('wrong')
            return BufferError
        self.client.send(nickname.encode('utf8'))

        flag = self.client.recv(1024).decode('utf8')
        if flag == 'false':
            return False
        else:
            return True

    def log_in(self, account: str, password: str,):
        """登陆用户

        :param account: 账号
        :param password: 密码
        :return: 已登录返回logged，未注册返回nonexistent，
                 密码错误返回error，正确返回用户
        """
        # 发送登陆请求
        cmd = 'log_in'
        self.client.send(cmd.encode('utf8'))

        # 发送账户密码
        back = self.client.recv(1024)
        if back != b'account':
            print('wrong')
            return BufferError
        self.client.send(account.encode('utf8'))

        back = self.client.recv(1024)
        if back != b'password':
            print('wrong')
            return BufferError
        self.client.send(password.encode('utf8'))

        back = self.client.recv(1024).decode('utf8')
        if back != 'true':
            # 登陆失败，返回错误原因
            return back
        else:
            # 登陆成功，接收用户数据并返回
            # 接收数据长度
            self.client.send(b'length')
            length = self.client.recv(1024)
            length = int(length.decode('utf8'))

            self.client.send(b'ready')

            # 接收数据
            data = b""
            time_get = math.ceil(length / 1024)
            for i in range(time_get):
                d = self.client.recv(1024)
                data += d

            # 反序列化用户对象并返回
            user_unit = pickle.loads(data)
            return user_unit

    def log_out(self, user_unit: user.User):
        """
        保存并退出用户
        :param user_unit: 用户对象
        """
        # 登出
        cmd = 'log_out'
        self.client.send(cmd.encode('utf8'))
        # 保存用户
        self.update_user(user_unit, False)

        # 接受ready后发送账号
        ready = self.client.recv(1024)
        if ready != b'ready':
            print('wrong')
            return BufferError

        self.client.send(user_unit.account.encode('utf8'))

    def update_user(self, user_unit: user.User, model=True):
        """更新用户信息

        :param user_unit: 用户对象
        :param model:判断保存与登出操作
        """
        # 发送更新请求
        if model:
            cmd = 'update_user'
            self.client.send(cmd.encode('utf8'))

        ready = self.client.recv(1024)
        if ready != b'length':
            print('wrong')
            return BufferError

        # 发送用户数据长度
        data = pickle.dumps(user_unit)
        length = str(len(data))
        self.client.send(length.encode('utf8'))

        # 收到确认，发送用户数据
        ready = self.client.recv(1024)
        if ready != b'ready':
            print('wrong')
            return BufferError
        self.client.sendall(data)

        # ready = self.client.recv(1024)
        # if ready != b'over':
        #     print('wrong')
        #     return BufferError
        #
        # print(ready)



