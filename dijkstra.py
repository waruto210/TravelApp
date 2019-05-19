from label import label
from cal_wqeight import cal_weight_by_price, cal_weight_by_time
import sys
from routes import TravelRoute


def my_dijkstra(adj_matrix: list, mode: str = "best_time", cities: list = [], depart_time: int = 10):
    """
    根据模式返回两地最优线路
    :param adj_matrix； 邻接矩阵,存储i -> j的所有班次
    :param mode: 模式，best_time表最优时间，best_price表最优价格
    :param cities: 起点和终点城市
    :param depart_time: 最早可出发时间
    :return: 包含TravelRoute对象的列表,以及最优开销
    """
    # 从城市i最早可出发时间
    d_time_list: list = [-1] * 31
    # 城市列表为空
    if not list:
        return None, None
    depart = depart_time
    # 起点，终点
    start: int = label[cities[0]]
    destination: int = label[cities[1]]
    # 一定确定距离的城市集合
    already_certain: list = [bool] * 31
    # 从起点的时间或价格开销
    distance: list = [int] * 31
    # 路径
    path: list = [dict] * 31
    # 求出个点到起点的开销
    for city in range(31):
        weight_dict: dict = {}
        weight: int = 0
        already_certain[city] = False
        train_route = adj_matrix[start][city]['train']
        air_route = adj_matrix[start][city]['air']
        if mode == "best_time":
            weight_dict, weight = cal_weight_by_time(d_time=depart, train_route=train_route, air_route=air_route)
        elif mode == "best_price":
            weight_dict, weight = cal_weight_by_price(train_route=train_route, air_route=air_route)
        if not weight_dict:
            distance[city] = sys.maxsize
        else:
            if mode == "best_time":
                distance[city] = weight
                d_time_list[city] = (weight_dict['depart_time'] + weight_dict['length_time']) % 24
            else:
                distance[city] = weight_dict['price']
        if distance[city] < sys.maxsize:
            path[city] = weight_dict
        else:
            path[city] = {}
    # 确认起点距离，到自身距离为0
    already_certain[start] = True
    distance[start] = 0

    for city in range(30):
        weight: int = 0
        weight_dict: dict = {}
        new_city: int = 0
        min_cost: int = sys.maxsize
        # 选出目前离起点开销最短的城市
        for j in range(31):
            if not already_certain[j] and (distance[j] < min_cost):
                new_city = j
                min_cost = distance[j]
        # 确定该城市距离
        already_certain[new_city] = True
        for j in range(31):
            if not already_certain[j]:  # 该城市距离未确定
                # 获取班次列表
                train_route: list = adj_matrix[new_city][j]['train']
                air_route: list = adj_matrix[new_city][j]['air']
                if mode == "best_time":
                    depart = d_time_list[new_city]
                    weight_dict, weight = cal_weight_by_time(d_time=depart, train_route=train_route,
                                                             air_route=air_route)
                elif mode == "best_price":
                    weight_dict, weight = cal_weight_by_price(train_route=train_route, air_route=air_route)

                if weight_dict:
                    if distance[j] > (distance[new_city] + weight):
                        # 如果从new_city到j开销小于原开销,更新
                        distance[j] = distance[new_city] + weight
                        if mode == "best_time":
                            # 最优时间模式还需更新到j城市后的最早可出发时间
                            d_time_list[j] = (weight_dict['depart_time'] + weight_dict['length_time']) % 24
                        # 加入路径
                        path[j] = weight_dict
    # 将path的记录改为正序
    order: list = []
    rou = path[destination]
    while rou:
        order.insert(0, rou)
        c_from = rou['from']
        num: int = label[c_from]
        rou = path[num]
    # 返回结果
    result: list = []
    for r in order:
        code: str = r['number']
        price: int = r['price']
        des: str = r['to']
        depart_time: int = r['depart_time']
        duration: int = r['length_time']
        if code[0].isalpha() and code[1].isalpha():
            by = 'A'
        else:
            by = 'T'
        seg = TravelRoute(by=by, code=code, price=price, des=des, depart_time=depart_time, duration=duration)
        result.append(seg)

    return result, distance[destination]
