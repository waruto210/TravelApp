from label import *
from dijkstra_algorithm import my_dijkstra
from routes import TravelRoute
from tabu_algorithm import  search_by_tabu


class Map:
    """地点的数据结构

    用于生成地点的数据结构，以邻接表形式储存。
    adj_matrix为二维数组，matrix[i][j]为城市i到j的Routes，
    Route中含有train、air两个列表，每个列表中含有多个字典格式的行程方式，
    train、格式：{"depart_time": 出发时刻, "from": "出发地", "number": "序号",
    "price": 230, "to": "目的地", "length_time": 总时长}
    """

    def __init__(self, train_filepath: str, air_filepath: str):
        """Map类的生成函数。

        通过文件导入并生成整个地图。
        :param train_filepath: 火车车次数据，json格式
        :param air_filepath: 飞机航班数据，json格式
        """
        self.adj_matrix = self.load_matrix(train_filepath, air_filepath)

    def get_way(self, mode: str = "best_time", cities: list = [], depart_time: str = "morning"):
        """
        根据城市列表得到路线
        :param mode: 寻路模式,best_time,best_price
        :param cities:  途径城市列表
        :param depart_time: 最早可出发时间
        :return: 返回包含TravelRoute对象的列表以及最优开销
        """
        if not cities:
            return None, None

        if depart_time == "morning":
            d_time = 10
        elif depart_time == "afternoon":
            d_time = 14
        else:
            d_time = 20
        count: int = len(cities)
        result: list = []
        total: int = 0
        for index in range(count - 1):
            ret_tmp, cost_tmp = my_dijkstra(self.adj_matrix, mode=mode, cities=cities[index: index + 2], depart_time=d_time)
            for item in ret_tmp:
                result.append(item)
            total = total + cost_tmp
            d_time = (d_time + cost_tmp) % 24

        return result, total

    def get_way2(self, cities: list, depart_time: int, time_limit: int):
        # search_by_ga(adj_matrix=self.adj_matrix, cities=cities, depart_time=depart_time, time_limit=time_limit, epoch=100
        #              , route_length=2, pop_size=50, p_mutation=0.8)
        ret: list[TravelRoute] = search_by_tabu(adj_matrix=self.adj_matrix, from_to=cities, depart_time=depart_time,
                                                time_limit=time_limit)
        for router in ret:
            print(router.by, router.depart_time, router.duration, router.des, router.price, router.code)

    def load_matrix(self, train_filepath: str, air_filepath: str):
        """通过文件返回地图的数据结构。

        matrix为二维数组，matrix[i][j]为城市i到j的Routes，
        Route中含有train、air两个列表，每个列表中含有多个字典格式的行程方式，

        :param train_filepath:火车车次数据，json格式
        :param air_filepath:飞机航班数据，json格式
        :return:地图邻接表
        """

        # 初始化地图并载入label
        adj_matrix = []
        for i in range(31):
            adj_matrix.append([])
            for j in range(31):
                adj_matrix[i].append({'train': [], 'air': []})

        # 将火车数据载入
        train_list_file = open(train_filepath, 'r', encoding='utf-8')
        train_list = train_list_file.read()
        train_list_file.close()
        train_list = json.loads(train_list)
        for train in train_list:
            self.load_traffic(adj_matrix, train=train)

        # 将飞机信息载入
        air_list_file = open(air_filepath, 'r', encoding='utf-8')
        air_list = air_list_file.read()
        air_list_file.close()
        air_list = json.loads(air_list)
        for air in air_list:
            self.load_traffic(adj_matrix, air=air)

        return adj_matrix

    @staticmethod
    def load_traffic(adj_matrix, train=None, air=None):
        """导入单个交通信息

        根据信息中的起点、终点及方式导入到地图中
        :param adj_matrix:地图邻接矩阵
        :param train:车次信息
        :param air:航班信息
        """
        if train is None:
            traffic = air
            traffic_name = 'air'
        else:
            traffic = train
            traffic_name = 'train'

        start = label[traffic['from']]
        destination = label[traffic['to']]
        state = adj_matrix[start][destination]
        state[traffic_name].append(traffic)


the_map = Map('train_new.json', 'flight.json')
the_map.get_way2(cities=["重庆", "乌鲁木齐"], time_limit=20, depart_time=12)
# tmp1: list = the_map.adj_matrix[17][1]['train']
# tmp2: list = the_map.adj_matrix[17][1]['air']
# print(tmp1)
# print(tmp2)
# 下面为测试代码
# for index in range(31):
#     if index != 25:
#         tmp1: list = the_map.adj_matrix[index][25]['train']
#         tmp2: list = the_map.adj_matrix[index][25]['air']
#         print("trainlen: " + str(len(tmp1)) + "airlen: " + str(len(tmp2)))
# ret, cost = the_map.get_way(mode="best_price", cities=["北京", "重庆"])
# for i in ret:
#     print("交通方式:" + i.by + " 班次:" + i.code + " 价格:" + str(i.price) + " 目的:" + i.des + " 出发时间:" \
#           + str(i.depart_time) + " 时长:" + str(i.duration))
#
# print("Cost is " + str(cost))
# ret = get_routes_count(the_map.adj_matrix)
# print(ret[25][12])
# a = [1, 2]
# a.insert(1, 3)
# print(a)