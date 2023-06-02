from PyQt5 import QtWidgets
from untitled import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.open)
    def open(self):
        import untitled2,untitled3,untitled4
        self.second = untitled2.Ui_MainWindow()  # 创建第2个窗体对象
        self.second.show()  # 显示窗体
        self.third = untitled3.Ui_MainWindow()  # 创建第3个窗体对象
        self.third.show()  # 显示窗体
        self.fouth = untitled4.Ui_MainWindow()  # 创建第4个窗体对象
        self.fouth.show()  # 显示窗体

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())