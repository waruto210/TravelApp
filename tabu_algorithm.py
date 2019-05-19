from tabu import TabuSearch
from cal_routes_count import cal_routes_count
from label import label
import numpy as np
from routes import TravelRoute


def search_by_tabu(adj_matrix: list, from_to: list, depart_time: int, time_limit: int):
    """

    :param adj_matrix:
    :param from_to:
    :param depart_time:
    :param time_limit:
    :return:
    """
    max_iteration: int = 50
    candidates_num: int = 10
    tabu_length: int = 10
    routes_count = cal_routes_count(adj_matrix=adj_matrix)
    from_to = [label[from_to[0]], label[from_to[1]]]
    scores = []
    pass_cities = []
    routes_num = []
    result = []
    for route_length in range(1, 5):
        search = TabuSearch(adj_matrix=adj_matrix, from_to=from_to, depart_time=depart_time,
                            time_limit=time_limit, routes_count=routes_count,
                            max_iteration=max_iteration, candidates_num=candidates_num,
                            tabu_length=tabu_length, route_length=route_length)
        a, b, c = search.go()
        scores.append(a)
        pass_cities.append(b)
        routes_num.append(c)
    sorted_scores_index = np.argsort(scores)
    from_to = pass_cities[sorted_scores_index[0]]
    routes = routes_num[sorted_scores_index[0]]

    route_length = sorted_scores_index[0] + 1
    for i in range(route_length):
        f = from_to[i]
        t = from_to[i + 1]
        route_num = routes[i]
        real_routes: dict = adj_matrix[f][t]
        train: list = real_routes['train']
        air: list = real_routes['air']
        if route_num >= len(train):
            route_num = route_num - len(train)
            one_route: dict = air[route_num]
        else:
            one_route: dict = train[route_num]
        code: str = one_route['number']
        price: int = one_route['price']
        des: str = one_route['to']
        depart_time: int = one_route['depart_time']
        duration: int = one_route['length_time']
        if code[0].isalpha() and code[1].isalpha():
            by = 'A'
        else:
            by = 'T'
        seg = TravelRoute(by=by, code=code, price=price, des=des, depart_time=depart_time, duration=duration)
        result.append(seg)
    return result
