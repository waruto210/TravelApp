
class User:
    """用户个体信息

    保存用户账号、密码、昵称、历史查询次数、路径历史
    """
    # account = None
    # password = None
    # nickname = None

    def __init__(self, account: str, password: str, nickname: str):
        """生成函数，注册并生成用户

        :param account: 账号
        :param password: 密码
        :param nickname: 昵称
        """
        self.query_time = 0
        self.routes_list = []

        self.account = account
        self.password = password
        self.nickname = nickname

    def add_route(self, route: list):
        """给用户添加历史查询记录

        :param route:包含用户查询路径对象（依次）的列表
        """
        self.query_time += 1
        self.routes_list.append(route)
