from ui_init import *
import sys

if __name__ == '__main__':
    # 实例化主窗口
    app = QApplication(sys.argv)
    SettingWindow = TravelMainWindow()
    sys.exit(app.exec_())
