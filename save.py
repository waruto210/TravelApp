import socket_client
import user


class Save:
    """
    用于控制对象的储存与读入
    """
    def __init__(self):
        print('start')

    @staticmethod
    def register(account: str, password: str, nickname: str):
        """创建用户
            :param account: 账号
            :param password: 密码
            :param nickname: 昵称
            :return: 已存在用户时返回False,注册成功返回True
        """
        client = socket_client.Client()
        temp = client.register(account, password, nickname)
        return temp

    @staticmethod
    def log_in(account: str, password: str):
        """云端登陆

        :param account: 账号
        :param password: 密码
        :return: 已登录返回logged，未注册返回nonexistent，
                 密码错误返回error，正确返回用户
        """
        client = socket_client.Client()
        temp = client.log_in(account, password,)
        client.send_close()
        return temp

    @staticmethod
    def log_out(user_unit: user.User):
        """
        登出用户
        :param user_unit:用户对象
        """
        client = socket_client.Client()
        client.log_out(user_unit)
        client.send_close()

    @staticmethod
    def update_user(user_unit: user.User):
        """更新用户数据

        根据新用户对象，覆盖旧有用户数据
        :param user_unit:用户对象
        """
        client = socket_client.Client()
        client.update_user(user_unit)
        client.send_close()


save_unit = Save()
