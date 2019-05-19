import sys


def cal_weight_by_price(train_route: list, air_route: list):
    """获取两地间价格权，传入火车和飞机路线

    :param train_route: 火车班次列表，内含dict
    :param air_route: 自解释
    :return: 返回权最短的班次以及权
    """
    # 找到权最小火车班次
    min_train_price: int = sys.maxsize
    min_train_dict: dict = {}
    for way in train_route:
        price: int = way['price']
        if price < min_train_price:
            min_train_price = price
            min_train_dict = way
    # 找到权最小飞机班次
    min_air_price: int = sys.maxsize
    min_air_dict: dict = {}
    for way in air_route:
        price: int = way['price']
        if price < min_air_price:
            min_air_price = price
            min_air_dict = way
    # 返回二者中小者
    if min_air_price < min_train_price:
        return min_air_dict, min_air_price
    else:
        return min_train_dict, min_train_price


def cal_weight_by_time(d_time: int, train_route: list, air_route: list):
    """
    获取两地间时间权，传入火车和飞机路线
    :param d_time: 最早可出发时间
    :param train_route: 火车班次列表
    :param air_route:   飞机班次；列表
    :return: 返回权最短班次及权
    """

    # 找到权最小火车班次
    min_train_time: int = sys.maxsize
    min_train_dict: dict = {}
    for way in train_route:
        depart_time: int = way['depart_time']
        length_time: int = way['length_time']

        if depart_time >= d_time:   # 当天可乘该班次
            length = length_time + depart_time - d_time
        else:                       # 当天不可乘该班次
            length = length_time + depart_time + (24 - d_time)
        if length < min_train_time:
            min_train_time = length
            min_train_dict = way

    # 找到权最小的飞机班次
    min_air_time: int = sys.maxsize
    min_air_dict: dict = {}
    for way in air_route:
        depart_time: int = way['depart_time']
        length_time: int = way['length_time']
        if depart_time >= d_time:   # 当天可乘该班次
            length = length_time + depart_time - d_time
        else:                       # 当天不可乘该班次
            length = length_time + depart_time + (24 - d_time)

        if length < min_air_time:
            min_air_time = length
            min_air_dict = way
    # 返回二者中权小者班次
    if min_air_time < min_train_time:
        return min_air_dict, min_air_time
    else:
        return min_train_dict, min_train_time

