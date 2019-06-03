from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from traveler import Traveler
from main_window import Ui_TravelMainWindow
from schedue import TravelScheduleWindow
from login import TravelLoginWindow
import journal
import copy
import time
import datetime
from PyQt5.QtGui import QPainter, QPen





class TravelMainWindow(QMainWindow, Ui_TravelMainWindow):
    """
    主窗口的存储&逻辑结构和基本功能

        plan 旅行路线计划
        strategy 寻路模式：best_time, best_price, three
        start_time 出发时间：range 23
        time_limit Three模式下的时间限制
        start_time 开始时间
        self.start_day 开始日期
        ScheduleWindow 子窗口，用于显示旅行日程
        LoadWindow 子窗口，用于读取旅行历史记录
        LoginWindow 子窗口，登录窗口
    """

    def __init__(self):
        """
        存储&逻辑结构初始化
        """
        # 存储结构初始化
        super().__init__()
        self.plan = []
        self.strategy = 'best_time'
        self.transport = ''
        self.start_time = 0
        self.start_day = 0
        self.time_limit = 0
        self.T = Traveler()
        self.load_window: TravelScheduleWindow
        self.load_windows = []

        # 显示初始化
        self.setupUi(self)
        self.retranslateUi(self)
        self.ScheduleWindow = TravelScheduleWindow()
        self.LoginWindow = TravelLoginWindow()
        self.StartButton.setDisabled(True)
        self.editor.hide()
        self.best_time.click()
        self.PathList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.PathList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.PathList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabWidget.setTabText(0, '新的')
        self.tabWidget.setTabText(1, '我的')
        self.hide()
        self.LoginWindow.show()

        # 设定按键逻辑
        self.confirm_btn.clicked.connect(self.init_editor)
        self.Add_btn.clicked.connect(self.add_to_path)
        self.StartButton.clicked.connect(self.get_schedule)
        self.ClearButton.clicked.connect(self.clear)
        self.CloseButton.clicked.connect(self.close)
        self.PathList.itemChanged.connect(self.ready)
        self.air.clicked.connect(self.air_checked)
        self.train.clicked.connect(self.train_checked)
        self.bullet.clicked.connect(self.bullet_checked)
        self.check_btn.clicked.connect(self.load)
        self.logout_btn.clicked.connect(self.logout)
        self.LoginWindow.login_success.connect(self.login_success)
        self.LoginWindow.close_btn.clicked.connect(self.close)

    def login_success(self):
        """
        登陆成功，显示用户信息
        :return:
        """
        self.LoginWindow.hide()
        self.nickname1.setText(self.LoginWindow.user.nickname)
        self.nickname2.setText(self.LoginWindow.user.nickname)
        self.read()
        self.show()

    def logout(self):
        """
        退出登录，存储用户信息
        :return:
        """
        self.hide()
        self.clear()
        self.LoginWindow.logout()

    def init_editor(self):
        """
        根据模拟策略初始化路径编辑器
        """

        # 是否为策略三
        if self.three.isChecked():
            self.Time_limit.show()
            self.time_lab.show()
            self.PathList.setColumnCount(3)
            self.PathList.setHorizontalHeaderItem(2, QTableWidgetItem('本段旅途时限'))
            self.is_order.hide()
        else:
            self.Time_limit.hide()
            self.time_lab.hide()
            self.is_order.show()
        self.settings.setDisabled(True)
        self.ClearButton.setEnabled(True)
        self.is_order.setChecked(True)
        self.editor.show()

    def add_to_path(self):
        """
        将添加途径下拉菜单(PBox)中的数据添加到路径存储
        :return: 无
        """
        i = self.PathList.rowCount()
        des = self.PBox.currentText()
        stay = self.TBox.currentText()
        self.PathList.setRowCount(i+1)
        self.PathList.setItem(i, 0, QTableWidgetItem(des))
        self.PathList.setItem(i, 1, QTableWidgetItem(stay))
        if self.three.isChecked():
            during = self.Time_limit.text()
            self.PathList.setItem(i, 2, QTableWidgetItem(during))

    def get_schedule(self):
        """
        获取旅行方案并在子窗口中显示之
        :return: 无
        """
        # 设定旅行偏好
        self.strategy = self.Strategy.checkedButton().objectName()
        self.start_time = self.time_set.value() + int(time.strftime("%H", time.localtime()))
        self.start_day = self.day_set.value() + self.start_time // 23 + 1
        self.start_time %= 23
        if self.air.isChecked():
            self.transport = 'air'
        elif self.train.isChecked():
            self.transport = 'train'
        elif self.bullet.isChecked():
            self.transport = 'bullet'

        # 读取窗口中的旅行计划
        self.plan = []
        self.plan.append(self.SBox.currentText())
        for i in range(self.PathList.rowCount()):
            stay = self.PathList.item(i, 1).text()
            if stay == '2小时':
                stay = 2
            elif stay == '不停留':
                stay = 0
            elif stay == '4小时':
                stay = 4
            elif stay == '8小时':
                stay = 8
            elif stay == '12小时':
                stay = 12
            elif stay == '18小时':
                stay = 18
            elif stay == '一天':
                stay = 24
            elif stay == '两天':
                stay = 48
            elif stay == '三天':
                stay = 72
            elif stay == '一周':
                stay = 168
            else:
                stay = 0
            path = [self.PathList.item(i, 0).text()]
            if self.three.isChecked():
                path.append(int(self.PathList.item(i, 2).text()))
            path.append(stay)
            self.plan.append(path)

        # 获取日程并转入子窗口处理
        print(self.strategy, self.start_time, self.transport, self.plan, self.is_order.isChecked())

        self.ScheduleWindow = TravelScheduleWindow()
        self.ScheduleWindow.save_btn.clicked.connect(self.save)
        self.ScheduleWindow.CloseButton.clicked.connect(self.show)
        self.ScheduleWindow.start_position = self.plan[0]
        self.ScheduleWindow.schedule = self.T.search_plan(self.plan, self.start_time, self.transport, self.strategy,
                                                          self.is_order.isChecked())
        self.ScheduleWindow.save_btn.setEnabled(True)
        self.ScheduleWindow.sim_btn.setEnabled(True)
        self.ScheduleWindow.show_schedule(self.start_time, self.start_day)
        self.ScheduleWindow.show()
        self.LoginWindow.query()
        self.ScheduleWindow.simulate_start.connect(self.LoginWindow.simulate_start.emit)
        self.hide()

    def ready(self):
        """
        判断是否满足开始模拟的条件
        :return:
        """
        if self.PathList.rowCount() > 0:
            self.StartButton.setEnabled(True)
        else:
            self.StartButton.setDisabled(True)

    def save(self):
        """
        保存本次结果
        :return:
        """

        # head:保存本次结果的概要信息
        head = [self.plan[0], self.start_time, self.transport, self.strategy,
                self.PathList.item(self.PathList.rowCount() - 1, 0).text(), self.start_day,
                datetime.datetime.now()]
        self.LoginWindow.add(head, self.ScheduleWindow.schedule)
        self.read()
        self.ScheduleWindow.save_btn.setDisabled(True)
        #QMessageBox.information(self, u'鞋程', u'已保存')

    def read(self):
        """
        读取用户历史记录并显示
        :return:
        """
        i = 0
        routes_list = self.LoginWindow.user.routes_list
        self.history.clearContents()
        self.history.setRowCount(0)
        for r in routes_list:
            self.history.setRowCount(i + 1)
            self.history.setItem(i, 0, QTableWidgetItem(r[0][0]))
            self.history.setItem(i, 1, QTableWidgetItem('Day' + str(r[0][5]) + ' ' + str(r[0][1]) + ':00'))
            self.history.setItem(i, 2, QTableWidgetItem(r[0][2]))
            self.history.setItem(i, 3, QTableWidgetItem(r[0][3]))
            self.history.setItem(i, 4, QTableWidgetItem(r[0][4]))
            self.history.setItem(i, 5, QTableWidgetItem(r[0][6].strftime("%y %m %d")))
            i += 1
        self.his_num.setNum(i)
        if self.history.rowCount() == 0:
            self.check_btn.setDisabled(True)
        else:
            self.history.selectRow(0)
            self.check_btn.setEnabled(True)

    def load(self):
        """
        载入选中的历史记录
        :return:
        """
        route = copy.copy(self.LoginWindow.user.routes_list[self.history.currentRow()])
        start = route[0][1]
        day = route[0][5]
        self.load_window = TravelScheduleWindow()
        self.load_windows.append(self.load_window)
        self.load_window.start_position = route[0][0]
        self.load_window.start_date = route[0][6]
        route.pop(0)
        self.load_window.schedule = route
        self.load_window.save_btn.setDisabled(True)
        self.load_window.show_schedule(start, day)
        self.load_window.CloseButton.clicked.connect(self.load_windows.pop)
        self.load_window.sim_btn.clicked.connect(self.LoginWindow.sim_log)
        self.LoginWindow.query()
        self.load_window.show()

    def clear(self):
        """
        清空旅行计划并复位
        :return: 无
        """
        self.plan = []
        self.PathList.clearContents()
        self.PathList.setRowCount(0)
        self.settings.setEnabled(True)
        self.StartButton.setDisabled(True)
        self.PathList.setColumnCount(2)
        self.editor.hide()
        self.best_time.click()
        self.air.setChecked(False)
        self.train.setChecked(False)
        self.bullet.setChecked(False)
        print(self.bullet.isChecked())
        self.transport = ''

    def air_checked(self):
        """
        交通方式偏好选择判断
        :return:
        """
        if self.air.isChecked:
            self.train.setChecked(False)
            self.bullet.setChecked(False)

    def train_checked(self):
        """
        交通方式偏好选择判断
        :return:
        """
        if self.train.isChecked:
            self.bullet.setChecked(False)
            self.air.setChecked(False)

    def bullet_checked(self):
        """
        交通方式偏好选择判断
        :return:
        """
        if self.bullet.isChecked:
            self.train.setChecked(False)
            self.air.setChecked(False)

    def close(self):
        """
        安全退出
        :return:
        """
        self.LoginWindow.logout()
        self.LoginWindow.quit()
