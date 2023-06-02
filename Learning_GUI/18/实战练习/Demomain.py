# -*- coding: utf-8 -*-
# 开发团队   ：明日科技
# 开发人员   ：小科
# 开发时间   ：2021/8/9  10:14
# 文件名称   ：Demomain.py
# 开发工具   ：PyCharm

from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import *
from Demo import Ui_MainWindow
from Login import Ui_Form
import os

class LoginWindow(QMainWindow,Ui_Form):
    def __init__(self):
        super(LoginWindow,self).__init__()
        self.setupUi(self)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton.clicked.connect(self.login) # 登录

    # 打开主窗体
    def login(self):
        if  self.lineEdit.text()== "mr" and self.lineEdit_2.text()== "mrsoft":
            self.main=MainWindow()
            self.hide()
            self.main.statusbar.addPermanentWidget(QLabel("当前登录用户："+self.lineEdit.text()),1)
            self.main.show()

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("note.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNote.setIcon(icon)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("calc.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCalc.setIcon(icon2)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("paint.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPaint.setIcon(icon3)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("idle.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionIDLE.setIcon(icon4)

        self.menu.triggered[QAction].connect(self.openTool) # 打开工具
        self.actionExit.triggered.connect(self.close) # 退出
    # 打开各种工具
    def openTool(self, m):
        if m.text() == "Note":
            os.system("notepad") # 打开记事本
        elif m.text() == "Calc":
            os.system("calc")  # 打开计算器
        elif m.text() == "Paint":
            os.system("mspaint") # 打开画图工具
        elif m.text() == "IDLE": # 由于路径中有空格，所以使用startfile方式
            os.startfile(r"C:\Program Files\Python39\Lib\idlelib\idle.bat")

import sys
if __name__=="__main__":
    app=QApplication(sys.argv)
    main=LoginWindow()
    main.show()
    sys.exit(app.exec_())