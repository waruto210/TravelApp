from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPoint


class Drawer(QLabel):
    """
    绘图蒙版
    """
    def __init__(self):
        super().__init__()
        # 设置蒙版大小和图片一致
        self.setGeometry(0, 0, 1350, 900)
        # 计划表
        self.schedule = QTableWidget()
        self.parts = []
        # 当前时间、状态
        self.state = -1
        self.time = 0
        # 点序列
        self.__coord = {"北京": QPoint(964, 244),
                        "天津": QPoint(986, 278),
                        "石家庄": QPoint(913, 310),
                        "济南": QPoint(985, 358),
                        "哈尔滨": QPoint(1240, 28),
                        "长春": QPoint(1207, 103),
                        "沈阳": QPoint(1156, 179),
                        "上海": QPoint(1103, 534),
                        "杭州": QPoint(1067, 566),
                        "南京": QPoint(1030, 508),
                        "福州": QPoint(1044, 694),
                        "合肥": QPoint(987, 515),
                        "南昌": QPoint(951, 616),
                        "郑州": QPoint(890, 421),
                        "武汉": QPoint(907, 554),
                        "长沙": QPoint(871, 628),
                        "广州": QPoint(877, 779),
                        "太原": QPoint(859, 315),
                        "呼和浩特": QPoint(837, 211),
                        "海口": QPoint(796, 869),
                        "西安": QPoint(763, 436),
                        "银川": QPoint(688, 295),
                        "重庆": QPoint(697, 586),
                        "贵阳": QPoint(697, 676),
                        "南宁": QPoint(745, 790),
                        "兰州": QPoint(623, 379),
                        "成都": QPoint(628, 556),
                        "昆明": QPoint(596, 730),
                        "西宁": QPoint(597, 360),
                        "拉萨": QPoint(277, 584),
                        "乌鲁木齐": QPoint(182, 103)}

    def paintEvent(self, event):
        """
            重写绘图事件
        """
        # 初始化画笔
        qp = QPainter(self)
        point_pen = QPen(Qt.red, 8, Qt.SolidLine)
        line_pen = QPen(Qt.red, 3, Qt.SolidLine)
        qp.begin(self)

        # 起始点
        point_a = self.schedule.item(0, 4).text()
        point_b: str
        qp.setPen(point_pen)
        qp.drawPoint(self.__coord[point_a])
        qp.setPen(line_pen)
        qp.drawEllipse(self.__coord[point_a], 10, 10)

        # 已完成过程绘制
        if self.state != -1:
            arrive = 0
            go = 0
            point_flag = True
            for i in range(self.state):
                point_b = self.schedule.item(i, 5).text()
                if self.schedule.item(i, 9).text() == "经停":
                    qp.setPen(point_pen)
                    qp.drawPoint(self.__coord[point_b])
                    point_flag = False
                elif self.schedule.item(i, 9).text() == "到达" or self.schedule.item(i, 9).text() == "到达,本段超时":
                    qp.setPen(line_pen)
                    qp.drawEllipse(self.__coord[point_b], 10, 10)
                    point_flag = True
                qp.setPen(line_pen)
                qp.drawLine(self.__coord[point_a], self.__coord[point_b])
                point_a = point_b

            # 当前过程绘制----蓝色
            point_pen = QPen(Qt.blue, 8, Qt.SolidLine)
            line_pen = QPen(Qt.blue, 3, Qt.SolidLine)
            point_b = self.schedule.item(self.state, 5).text()

            # 若停留，只绘制一点，否则进入过程判断
            if self.schedule.item(self.state, 9).text() == "停留":
                if point_flag:
                    qp.setPen(line_pen)
                    qp.drawEllipse(self.__coord[point_a], 10, 10)
                else:
                    qp.setPen(point_pen)
                    qp.drawPoint(self.__coord[point_a])
            else:
                arrive = self.get_time(self.schedule.item(self.state, 7).text(),
                                       self.schedule.item(self.state, 8).text())
                go = self.get_time(self.schedule.item(self.state, 0).text(),
                                   self.schedule.item(self.state, 1).text())
            # 过程判断，根据当前事件判断如何绘制
            if self.time <= go:
                if point_flag:
                    qp.setPen(line_pen)
                    qp.drawEllipse(self.__coord[point_a], 10, 10)
                else:
                    qp.setPen(point_pen)
                    qp.drawPoint(self.__coord[point_a])
            elif self.time == arrive:
                if self.schedule.item(self.state, 9).text() != "经停":
                    qp.setPen(line_pen)
                    qp.drawEllipse(self.__coord[point_b], 10, 10)
                else:
                    qp.setPen(point_pen)
                    qp.drawPoint(self.__coord[point_b])
                qp.setPen(line_pen)
                qp.drawLine(self.__coord[point_a], self.__coord[point_b])
            elif go < self.time < arrive:
                x = self.__coord[point_a].x()
                x += round((self.__coord[point_b].x() - self.__coord[point_a].x()) * ((self.time - go) / (arrive - go)))
                y = self.__coord[point_a].y()
                y += round((self.__coord[point_b].y() - self.__coord[point_a].y()) * ((self.time - go) / (arrive - go)))
                qp.setPen(line_pen)
                qp.drawLine(self.__coord[point_a], QPoint(x, y))

        qp.end()

    @staticmethod
    def get_time(day: str, hour: str):
        """
            重写绘图事件
            :param day 日期：Dayx
            :param hour 时刻： 12：00
            :return 模拟时间戳
        """
        return (int(day[3:]) - 1) * 24 + int(hour[:-3])

