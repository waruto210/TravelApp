class TravelRoute:
    def __init__(self, by: str, code: str, price: int, des: str, depart_time: int,
                 duration: int, is_tag: bool = False, stay: int = 0,
                 timelimit_satisfy: bool = True):
        """

        :param by: 交通工具
        :param code: 编号
        :param price: 价格
        :param des: 目的地
        :param depart_time: 出发时间
        :param duration: 时长
        :param is_tag: 标志该对象是否为标志
        :param stay: 停留多久
        :param timelimit_satisfy: 是否满足了用户的时间限制
        """
        # 参数分别为方式,为"A"或"T",车次航班编号，票价，到达地
        self.by = by
        self.code = code
        self.price = price
        self.des = des
        self.depart_time = depart_time
        self.duration = duration
        self.is_tag = is_tag
        self.stay = stay
        self.timelimit_satisfy = timelimit_satisfy
