from label import *


class Map:
    """地点的数据结构。

    用于生成地点的数据结构，以邻接表形式储存。
    adj_matrix为二维数组，matrix[i][j]为城市i到j的Routes，
    Route中含有train、air、bullet三个列表，每个列表中含有多个字典格式的行程方式，
    格式：{"depart_time": 出发时刻, "from": "出发地", "number": "序号",
    "price": 230, "to": "目的地", "length_time": 总时长, "type": 出行方式}
    """

    def __init__(self, train_filepath: str, air_filepath: str, bullet_filepath: str):
        """Map类的生成函数。

        通过文件导入并生成整个地图。
        :param train_filepath: 火车车次数据，json格式
        :param bullet_filepath: 动车/城际车次数据，json格式
        :param air_filepath: 飞机航班数据，json格式
        """
        self.adj_matrix = self.load_matrix(train_filepath, air_filepath, bullet_filepath)

    def load_matrix(self, train_filepath: str, air_filepath: str, bullet_filepath: str):
        """通过文件返回地图的数据结构。

        matrix为二维数组，matrix[i][j]为城市i到j的Routes，
        Route中含有train、air、bullet三个列表，每个列表中含有多个字典格式的行程方式，

        :param train_filepath:火车车次数据，json格式
        :param bullet_filepath:动车车次数据，json格式
        :param air_filepath:飞机航班数据，json格式
        :return:地图邻接表
        """

        # 初始化地图并载入label
        adj_matrix = []
        for i in range(31):
            adj_matrix.append([])
            for j in range(31):
                adj_matrix[i].append({'train': [], 'air': [], 'bullet': []})

        # 将火车数据载入
        train_list_file = open(train_filepath, 'r', encoding='utf-8')
        train_list = train_list_file.read()
        train_list_file.close()
        train_list = json.loads(train_list)
        for train in train_list:
            self.load_traffic(adj_matrix, train=train)

        # 将动车数据载入
        bullet_list_file = open(bullet_filepath, 'r', encoding='utf-8')
        bullet_list = bullet_list_file.read()
        bullet_list_file.close()
        bullet_list = json.loads(bullet_list)
        for bullet in bullet_list:
            self.load_traffic(adj_matrix, bullet=bullet)

        # 将飞机信息载入
        air_list_file = open(air_filepath, 'r', encoding='utf-8')
        air_list = air_list_file.read()
        air_list_file.close()
        air_list = json.loads(air_list)
        for air in air_list:
            self.load_traffic(adj_matrix, air=air)

        return adj_matrix

    @staticmethod
    def load_traffic(adj_matrix, train=None, air=None, bullet=None):
        """导入单个交通信息

        根据信息中的起点、终点及方式导入到地图中
        :param adj_matrix:地图邻接矩阵
        :param train:车次信息
        :param air:航班信息
        """
        if (train is None) & (bullet is None):
            traffic = air
            traffic_name = 'air'
        elif bullet is None:
            traffic = train
            traffic_name = 'train'
        else:
            traffic = bullet
            traffic_name = 'bullet'

        start = label[traffic['from']]
        destination = label[traffic['to']]
        state = adj_matrix[start][destination]
        state[traffic_name].append(traffic)


