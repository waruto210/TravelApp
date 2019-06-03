import user


class Message:
    """全体用户数据

    储存多个用户对象，借助socket通信的方式与云端多线程交互数据
    同时实现注册、注销、查询、更新、输出用户日志的后端结构
    """

    def __init__(self):
        """生成全体用户数据

        同步本地与云端数据
        """
        self.message = {}
        # 检测是否已有用户数据,没有则创建防止空文件无法序列化

    def register(self, account: str, password: str, nickname: str):
        """创建用户

        :param account: 账号
        :param password: 密码
        :param nickname: 昵称
        :return: 已存在用户时返回False,注册成功返回True
        """
        message = self.message
        user_unit = user.User(account, password, nickname)
        if message.get(account, False) is False:
            message[user_unit.account] = user_unit
            return True
        else:
            return False

    def log_of(self, account: str):
        """删除用户

        :param account: 账号
        """
        self.message.pop(account)

# message_unit = Message()

