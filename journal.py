import time


class Journal:
    def __init__(self):
        """
        写定程序日志文件名
        """
        self.logfile_path = "./traveler.log"

    def init(self):
        """
        程序初始化事件
        :return: 无
        """
        # 获取当前时间
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        event = "\tProgram init!\n"
        with open(self.logfile_path, 'a+') as f:
            f.write(now_time + event)

    def register(self, user_name):
        """
        用户注册事件
        :param user_name: 用户名
        :return: 无
        """
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        event = "\tuser: " + user_name + " register!\n"
        with open(self.logfile_path, 'a+') as f:
            f.write(now_time + event)

    def login(self, user_name):
        """
        用户登陆事件
        :param user_name: 用户名
        :return: 无
        """
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        event = "\tuser: " + user_name + " login!\n"
        with open(self.logfile_path, 'a+') as f:
            f.write(now_time + event)

    def logout(self, user_name):
        """
        用户登出事件
        :param user_name: 用户名
        :return:
        """
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        event = "\tuser: " + user_name + " logout!\n"
        with open(self.logfile_path, 'a+') as f:
            f.write(now_time + event)

    def quit(self):
        """
        程序退出事件
        :return:
        """
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        event = "\tProgram quit!\n"
        with open(self.logfile_path, 'a+') as f:
            f.write(now_time + event)

    def query(self, user_name):
        """
        用户查询事件
        :param user_name: 用户名
        :return:
        """
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        event = "\tuser: " + user_name + " queries!\n"
        with open(self.logfile_path, 'a+') as f:
            f.write(now_time + event)

    def simulate(self, user_name):
        """
        旅行模拟事件
        :param user_name: 用户名
        :return: 无
        """
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        event = "\tuser: " + user_name + " simulates!\n"
        with open(self.logfile_path, 'a+') as f:
            f.write(now_time + event)


journal = Journal()
