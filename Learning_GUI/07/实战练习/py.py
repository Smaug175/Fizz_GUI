#  _*_ coding:utf-8 _*_
# 开发团队：明日科技
# 开发人员：Administrator
# 文件名称：demo1.py
# 开发工具：PyCharm
#treeview的添加图标

from tkinter import *
from tkinter.ttk import *  # 导入内部包
win = Tk()
# 创建树菜单以及每一列的名称
tree = Treeview(win,columns=("score"))
#定义每一列的标题
tree.heading("#0",text="小组",anchor=W)
tree.heading("score",text="得分",anchor=W)
# 用字典存储各组队员的员工号以及得分
score1={"R001":"11","R002":"10","R003":"10","R004":"08"}
score2={"B001":"09","B002":"10","B003":"15","B004":"10"}
score3={"G001":"09","G002":"12","G003":"08","G004":"08"}
# 添加三黄队黄队与绿队，设置默认展开红队成员的得分
red=tree.insert("",END,text="红队",open=True)
blue=tree.insert("",END,text="蓝队")
green=tree.insert("",END,text="绿队")
# 通过遍历添加子菜单
for index,item in score1.items():
    tree.insert(red,END,text=index,values=(item))
for index,item in score2.items():
    tree.insert(blue,END,text=index,values=(item))
for index,item in score3.items():
    tree.insert(green,END,text=index,values=(item))
tree.pack()
win.mainloop()