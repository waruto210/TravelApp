class TravelRoute:
    def __init__(self, by: str, code: str, price: int, des: str, depart_time: int, duration: int):
        # 参数分别为方式,为"A"或"T",车次航班编号，票价，到达地
        self.by = by
        self.code = code
        self.price = price
        self.des = des
        self.depart_time = depart_time
        self.duration = duration

