from schedule_window import Ui_ScheduleWindow
from traveler import TravelRoute
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, pyqtSignal
from drawer import Drawer
import time as now
import datetime

class TravelScheduleWindow (QWidget, Ui_ScheduleWindow):
    """
    子窗口的存储&逻辑结构和基本功能
        schedule 旅行日程，是一个包含若干TravelRoute的list
        cost 旅行开销
        start_position 启程地点
    """

    simulate_start = pyqtSignal()

    def __init__(self):
        super().__init__()

        # 存储结构初始化
        self.schedule = []
        self.cost = 0
        self.stay_time = 0
        self.start_day = 0
        self.start_date = datetime.datetime.now()
        self.parts = []
        self.timer = QTimer()
        self.speed = 10000
        self.start_position = '北京'

        # 显示&按键逻辑初始化
        self.setupUi(self)
        self.retranslateUi(self)
        self.drawer = Drawer()
        self.drawer.setParent(self.map)
        self.drawer.show()
        self.stackedWidget.setCurrentIndex(0)
        self.ScheduleTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ScheduleTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ScheduleTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.CloseButton.clicked.connect(self.close)
        self.sim_btn.clicked.connect(self.into_map)
        self.back_btn.clicked.connect(self.into_list)
        self.start_btn.clicked.connect(self.simulator)
        self.timer.timeout.connect(self.simulate)
        self.speed_btn.clicked.connect(self.speeder)
        self.progress.valueChanged.connect(self.check)
#        self.start_btn.clicked.connect(self.paint)

    def show_schedule(self, start_time: int = 0, day: int = 1):
        """
        在列表ScheduleTable中显示旅行日程
        :param start_time 起始时刻
        :param day 起始相对日期
        :return: 无
        """
        i = 0
        hour = start_time
        self.parts = [start_time]
        self.start_day = day
        by = '航班'
        position = self.start_position
        self.stackedWidget.setCurrentIndex(0)

        # 空计划检测
        if not self.schedule:
            self.save_btn.setDisabled(True)
            self.sim_btn.setDisabled(True)
            QMessageBox.information(self, u'计划失败', u'未能找到符合要求的方案')
            self.ScheduleTable.setRowCount(1)
            self.ScheduleTable.setItem(0, 0, QTableWidgetItem("找"))
            self.ScheduleTable.setItem(0, 1, QTableWidgetItem("不"))
            self.ScheduleTable.setItem(0, 2, QTableWidgetItem("到"))
            self.ScheduleTable.setItem(0, 3, QTableWidgetItem("可"))
            self.ScheduleTable.setItem(0, 4, QTableWidgetItem("用"))
            self.ScheduleTable.setItem(0, 5, QTableWidgetItem("路"))
            self.ScheduleTable.setItem(0, 6, QTableWidgetItem("线"))
            self.ScheduleTable.setItem(0, 7, QTableWidgetItem("！！！"))
            return

        # 读取并显示旅行计划
        for step in self.schedule:
            print(step.by, step.code, step.price, step.des, step.depart_time, step.duration, step.stay)
            self.ScheduleTable.setRowCount(i + 1)

            # 标志位检测
            if step.is_tag:
                stay_hour = step.stay
                if i and self.ScheduleTable.item(i-1, 9).text() == "经停":
                    if step.timelimit_satisfy:
                        self.ScheduleTable.setItem(i-1, 9, QTableWidgetItem("到达"))
                    else:
                        self.ScheduleTable.setItem(i-1, 9, QTableWidgetItem("到达,本段超时"))

                if stay_hour:
                    self.ScheduleTable.setItem(i, 4, QTableWidgetItem(position))
                    self.ScheduleTable.setItem(i, 5, QTableWidgetItem(position))
                    self.ScheduleTable.setItem(i, 9, QTableWidgetItem("停留"))
                    self.stay_time += stay_hour
                    hour += stay_hour
                    self.parts.append(hour)
                    self.ScheduleTable.setItem(i, 6, QTableWidgetItem(str(stay_hour // 24) + "天"
                                                                      + str(stay_hour % 24) + "时"))
                    i += 1
                else:
                    self.ScheduleTable.setRowCount(i)
                continue

            # 获取出发日期&时间
            if step.depart_time < hour % 24:
                hour += 24 - (hour % 24) + step.depart_time
            else:
                hour += step.depart_time - (hour % 24)

            if step.by == 'air':
                by = '航班'
            elif step.by == 'train':
                by = '绿皮火车'
            elif step.by == 'bullet':
                by = '高铁/动车'

            # 出发信息显示
            self.ScheduleTable.setItem(i, 0, QTableWidgetItem("Day" + str(hour // 24 + day)))
            self.ScheduleTable.setItem(i, 1, QTableWidgetItem(str(hour % 24) + ":00"))
            self.ScheduleTable.setItem(i, 2, QTableWidgetItem(by))
            self.ScheduleTable.setItem(i, 3, QTableWidgetItem(step.code))
            self.ScheduleTable.setItem(i, 4, QTableWidgetItem(position))

            # 获取到达地点&日期&时间
            position = step.des
            hour = hour + step.duration
            self.parts.append(hour)

            # 到达信息显示
            self.ScheduleTable.setItem(i, 5, QTableWidgetItem(position))
            self.ScheduleTable.setItem(i, 6, QTableWidgetItem(str(step.duration) + "个小时"))
            self.ScheduleTable.setItem(i, 7, QTableWidgetItem("Day" + str(hour // 24 + day)))
            self.ScheduleTable.setItem(i, 8, QTableWidgetItem(str(hour % 24) + ":00"))
            self.ScheduleTable.setItem(i, 9, QTableWidgetItem("经停"))
            self.ScheduleTable.setItem(i, 10, QTableWidgetItem(str(step.price) + "元"))
            self.cost += step.price
            i += 1

        # 计划结束
        if self.schedule[-1].stay:
            i -= 1
            self.parts.pop()
        else:
            self.ScheduleTable.setRowCount(i + 1)
            self.ScheduleTable.setItem(i, 9, QTableWidgetItem("停留"))
        self.ScheduleTable.setItem(i, 3, QTableWidgetItem("旅"))
        self.ScheduleTable.setItem(i, 4, QTableWidgetItem("途"))
        self.ScheduleTable.setItem(i, 5, QTableWidgetItem("结"))
        self.ScheduleTable.setItem(i, 6, QTableWidgetItem("束"))

        # 模拟窗口初始化
        for p in range(len(self.parts)):
            self.parts[p] += (day - 1) * 24
        print(self.parts)
        self.progress.valueChanged.disconnect(self.check)
        self.progress.setMinimum(self.parts[0])
        self.progress.setMaximum(self.parts[-1])
        self.progress.setValue(self.parts[0])
        self.progress.valueChanged.connect(self.check)
        self.drawer.schedule = self.ScheduleTable
        self.drawer.parts = self.parts
        self.check(self.progress.value())

    def simulator(self):
        """
        模拟起止控制
        :return: 无
        """
        if self.start_btn.isChecked():
            self.timer.start(self.speed)
            self.simulate_start.emit()
        else:
            self.timer.stop()

    def speeder(self):
        """
        模拟速度控制
        :return: 无
        """
        self.timer.stop()
        if self.speed_btn.isChecked():
            self.speed //= 10
        else:
            self.speed *= 10
        self.simulator()

    def simulate(self):
        """
        推进模拟进程
        :return: 无
        """
        if self.progress.value() == self.progress.maximum():
            self.progress.setValue(self.progress.minimum())
        else:
            self.progress.setValue(self.progress.value() + 1)

    def check(self, time: int):
        """
        查询当前状态并绘制路线图
        :param time: 当前模拟时间
        :return: 无
        """
        str_a = ''
        str_b = ''
        code = ''
        method = ''
        way = ''
        state = 0

        # 获取当前阶段
        for i in range(len(self.parts)):
            if self.parts[i] >= time:
                state = i - 1
                break

        # 根据阶段判断状态
        if state == -1:
            way = "起点 ：" + self.start_position
            str_b = "准备出发"
        else:
            str_a = self.ScheduleTable.item(state, 9).text()
            if state != len(self.parts) - 2 and self.ScheduleTable.item(state + 1, 9).text() != "停留":
                if self.drawer.get_time(self.ScheduleTable.item(state + 1, 0).text(),
                                        self.ScheduleTable.item(state + 1, 1).text()) == time:
                    str_b = "出发"
                elif str_a != "停留":
                    str_b = "准备出发"
                method = self.ScheduleTable.item(state + 1, 2).text()
                code = self.ScheduleTable.item(state + 1, 3).text()
                way = self.ScheduleTable.item(state + 1, 4).text() + " 至 " +self.ScheduleTable.item(state + 1, 5).text()
            else:
                way = self.ScheduleTable.item(state, 5).text()
            if str_a != "停留":
                if self.drawer.get_time(self.ScheduleTable.item(state, 7).text(),
                                        self.ScheduleTable.item(state, 8).text()) != time:
                    method = self.ScheduleTable.item(state, 2).text()
                    code = self.ScheduleTable.item(state, 3).text()
                    way = self.ScheduleTable.item(state, 4).text() + " 至 " +self.ScheduleTable.item(state, 5).text()
                    str_a = ""
                if self.drawer.get_time(self.ScheduleTable.item(state, 7).text(),
                                        self.ScheduleTable.item(state, 8).text()) > time > \
                        self.drawer.get_time(self.ScheduleTable.item(state, 0).text(),
                                             self.ScheduleTable.item(state, 1).text()):
                    str_b = "旅程中"
                elif time < self.drawer.get_time(self.ScheduleTable.item(state, 0).text(),
                                             self.ScheduleTable.item(state, 1).text()):
                    str_b = "准备出发"
                elif time == self.drawer.get_time(self.ScheduleTable.item(state, 0).text(),
                                             self.ScheduleTable.item(state, 1).text()):
                    str_b = "出发"
            elif str_b != "出发":
                method = ''
                code = ''
                way = self.ScheduleTable.item(state, 5).text()

        # 显示
        self.code.setText(code)
        self.method.setText(method)
        self.posi.setText(way)
        self.state.setText(str_a + ' ' + str_b)
        self.day.setNum(time // 24 + 1)
        date = self.start_date + datetime.timedelta(days=time//24)
        self.date.setText(date.strftime("%Y-%m-%d"))
        self.time.setText(str(time % 24) + ":00")

        # 作图
        self.drawer.time = time
        self.drawer.state = state
        self.drawer.update()

    def into_list(self):
        """
        返回列表页
        :return: 无
        """
        self.stackedWidget.setCurrentIndex(0)
        if self.start_btn.isChecked():
            self.start_btn.click()
        if self.speed_btn.isChecked():
            self.speed_btn.click()

    def into_map(self):
        """
        进入模拟页
        :return: 无
        """
        self.stackedWidget.setCurrentIndex(1)

    def close(self):
        """
        关闭后自杀
        :return: 无
        """
        self.deleteLater()
