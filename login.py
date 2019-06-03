from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from login_window import Ui_Login_Window
from user import User
import save
import journal


class TravelLoginWindow(QDialog, Ui_Login_Window):
    """
    登录窗口的存储、逻辑结构和基本功能
        user: 登录用户
        login_success: 登录成功信号
        simulate_start: 模拟开始信号
    """
    user: User
    login_success = pyqtSignal()
    simulate_start = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.user = False
        self.setupUi(self)
        self.retranslateUi(self)
        self.invalid_name.hide()
        self.failed.hide()
        self.signin_btn2.setDisabled(True)
        self.login_btn.setDefault(True)

        self.login_btn.clicked.connect(self.login)
        self.signin_btn.clicked.connect(self.into_sign_in)
        self.signin_btn2.clicked.connect(self.sign_in)
        self.back_btn.clicked.connect(self.into_login)
        self.show_btn.pressed.connect(self.show_pw)
        self.show_btn.clicked.connect(self.hide_pw)
        self.close_btn.clicked.connect(self.quit)
        self.name_sign.textChanged.connect(self.is_empty)
        self.name_sign_2.textChanged.connect(self.is_empty)
        self.simulate_start.connect(self.sim_log)

        journal.journal.init()

    def login(self):
        """
        登录，获取用户，储存到self.user
        """
        self.user = save.save_unit.log_in(self.name_log.text(), self.pw_log.text())
        if self.user == 'logged':
            self.failed.setText('不能重复登录咯')
            self.failed.show()
        elif self.user == 'error':
            self.failed.setText('用户名或密码错误')
            self.failed.show()
        elif self.user == 'nonexistent':
            self.failed.setText('未注册用户')
            self.failed.show()
        else:
            # 登录成功
            self.failed.hide()
            journal.journal.login(self.user.account)
            self.login_success.emit()
            print(self.user.account, self.user.nickname,self.user.password)
            print(self.user.query_time, self.user.routes_list.__len__())
        self.pw_log.clear()

    def sign_in(self):
        """
        注册
        """
        if save.save_unit.register(self.name_sign.text(), self.pw_sign.text(), self.name_sign_2.text()):
            self.name_log.setText(self.name_sign.text())
            self.invalid_name.hide()
            journal.journal.register(self.name_sign.text())
            self.into_login()
        else:
            self.invalid_name.show()
        self.pw_sign.clear()

    def is_empty(self):
        """
        判断注册用户名是否为空，若空则禁止注册
        :return:
        """
        if self.name_sign.text() == '' or self.name_sign_2.text() == '':
            self.signin_btn2.setDisabled(True)
        else:
            self.signin_btn2.setEnabled(True)

    def into_login(self):
        """
        进入登录窗口
        :return:
        """
        self.stackedWidget.setCurrentIndex(0)

    def into_sign_in(self):
        """
        进入注册窗口
        :return:
        """
        self.stackedWidget.setCurrentIndex(1)

    def add(self, start: list, routes: list):
        """
        添加历史记录
        :param start 历史记录头
        :param routes 历史记录数据
        :return:
        """
        routes.insert(0, start)
        self.user.add_route(routes)
        save.save_unit.update_user(self.user)

    def logout(self):
        """
        登出
        :return:
        """
        journal.journal.logout(self.user.account)
        save.save_unit.log_out(self.user)
        self.show()

    def show_pw(self):
        """
        显示密码
        :return:
        """
        self.pw_sign.setEchoMode(QLineEdit.Normal)

    def hide_pw(self):
        """
        隐藏密码
        :return:
        """
        self.pw_sign.setEchoMode(QLineEdit.Password)

    def sim_log(self):
        """
        模拟日志输出
        :return:
        """
        journal.journal.simulate(self.user.account)

    def quit(self):
        """
        退出日志输出
        :return:
        """
        journal.journal.quit()
        exit()

    def query(self):
        """
         查询日志输出
         :return:
         """
        journal.journal.query(self.user.account)



