#  _*_ coding:utf-8 _*_

from tkinter import *
win=Tk()
win.title("为游戏窗口添加菜单")
menu1=Menu(win)          # 创建顶级菜单
menu1.add_command(label="游戏")   # 添加菜单项
menu1.add_command(label="帮助")  # 添加菜单项
menu1.add_command(label="退出")  # 添加菜单项
win.config(menu=menu1)         # 显示菜单
win.mainloop()
