import sys
import numpy as np


def cal_weight_by_price(train_route: list, air_route: list, bullet_route: list, vehicle: str = ''):
    """

    :param train_route:
    :param air_route:
    :param bullet_route:
    :param vehicle:
    :return:
    """
    min_price = [sys.maxsize] * 3
    min_dict = [{}] * 3
    # 找到权最小火车班次
    if vehicle == '' or vehicle == 'train':
        for way in train_route:
            price: int = way['price']
            if price < min_price[0]:
                min_price[0] = price
                min_dict[0] = way
    # 找到权最小飞机班次
    if vehicle == '' or vehicle == 'air':
        for way in air_route:
            price: int = way['price']
            if price < min_price[1]:
                min_price[1] = price
                min_dict[1] = way
    # 找到权最小动车班次
    if vehicle == '' or vehicle == 'bullet':
        for way in bullet_route:
            price: int = way['price']
            if price < min_price[2]:
                min_price[2] = price
                min_dict[2] = way
    # 返回二者中小者
    min_index: int = int(np.argmin(min_price))
    return min_dict[min_index], min_price[min_index]


def cal_weight_by_time(d_time: int, train_route: list, air_route: list, bullet_route: list, vehicle: str = ''):
    """

    :param d_time:
    :param train_route:
    :param air_route:
    :param bullet_route:
    :param vehicle:
    :return:
    """
    
    min_time = [sys.maxsize] * 3
    min_dict = [{}] * 3
    # 找到权最小火车班次
    if vehicle == '' or vehicle == 'train':
        for way in train_route:
            depart_time: int = way['depart_time']
            length_time: int = way['length_time']

            if depart_time >= d_time:   # 当天可乘该班次
                length = length_time + depart_time - d_time
            else:                       # 当天不可乘该班次
                length = length_time + depart_time + (24 - d_time)
            if length < min_time[0]:
                min_time[0] = length
                min_dict[0] = way

    # 找到权最小的飞机班次
    if vehicle == '' or vehicle == 'air':
        for way in air_route:
            depart_time: int = way['depart_time']
            length_time: int = way['length_time']
            if depart_time >= d_time:   # 当天可乘该班次
                length = length_time + depart_time - d_time
            else:                       # 当天不可乘该班次
                length = length_time + depart_time + (24 - d_time)

            if length < min_time[1]:
                min_time[1] = length
                min_dict[1] = way

    # 找到权最小的飞机班次
    if vehicle == '' or vehicle == 'bullet':
        for way in bullet_route:
            depart_time: int = way['depart_time']
            length_time: int = way['length_time']
            if depart_time >= d_time:   # 当天可乘该班次
                length = length_time + depart_time - d_time
            else:                       # 当天不可乘该班次
                length = length_time + depart_time + (24 - d_time)

            if length < min_time[2]:
                min_time[2] = length
                min_dict[2] = way
    min_index: int = int(np.argmin(min_time))
    # 返回三者中权小者班次
    return min_dict[min_index], min_time[min_index]

