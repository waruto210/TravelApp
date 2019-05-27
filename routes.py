class TravelRoute:
    def __init__(self, by: str, code: str, price: int, des: str, depart_time: int,
                 duration: int, is_tag: bool = False, stay: int = 0,
                 timelimit_satisfy: bool = True):
        """

        :param by:
        :param code:
        :param price:
        :param des:
        :param depart_time:
        :param duration:
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
