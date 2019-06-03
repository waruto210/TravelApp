import socket
import pickle


class Client:
    # 定义服务器ip
    HOST = "127.0.0.1"
    # 定义端口号
    PORT = 8000
    # 由于使用socket进行连接，需要把ip和端口先转换为元组
    addr = (HOST, PORT)
    client = None

    # client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # client.connect(('127.0.0.1', 8000))

    def __init__(self):
        """建立连接

        与服务器端借助socket进行通信
        """
        # 设定了网络连接方式，以及传输使用的协议
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接服务器
        self.client.connect(self.addr)
        print(self.client)

    def send_file(self):
        # 以只读方式打开指定的文件
        cmd = b'upload'
        self.client.send(cmd)
        with open('message.pkl', "rb") as f:
            # 以byte 的方式读取文件内容
            file = f.read()
            # 发送文件内容
            self.client.sendall(file)

    def get_file(self):
        cmd = b'download'
        self.client.send(cmd)
        data = b""
        while True:
            d = self.client.recv(1024)
            if d:
                data += d
            else:
                break
        with open("message.pkl", "wb") as f:       # 打开本地文件，将接受到的数据写入本地指定的目录
            f.write(data)

    def send_close(self):
        data = b'bye'
        self.client.send(data)

    # def main():
    #     while True:
    #         # 获取用户输入的命令
    #         cmd = input("请输入命令:")
    #         # 发送用户输入的命令
    #         c.send(bytes(cmd,encoding='gbk'))
    #         # 如果用户输入bye结束程序
    #         if cmd == "bye":
    #             break
    #         # 如果用户输入upload,调用send_file()函数，进行文件上传
    #         if cmd == "upload":
    #             send_file()
    #         # 如果用户输入down,调用get_file()函数，进行文件下载
    #         if cmd == "down":
    #             get_file()
    #         data = c.recv(20480)                     # 设置接受数据大小
    #         # 将接受的数据打印出来，没多大用
    #         # print(str(data,encoding='gbk'))
    #     # ~ c.send(b'word')  #发送字符串前面加b转换bytes比特格式
    #     c.close()


c1 = Client()
c1.get_file()
