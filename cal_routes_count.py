def cal_routes_count(adj_matrix: list):
    """

    :param adj_matrix:
    :return:
    """
    ret: list = []
    for index in range(31):
        ret.append([])

    for index in range(31): 
        for j in range(31):
            route = adj_matrix[index][j]
            train: list = route['train']
            air: list = route['air']
            ret[index].append(len(train) + len(air))
    return ret
