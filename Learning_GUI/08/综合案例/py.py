# -*- coding: utf-8 -*-
# @Time    : 2020/5/27 14:31
# @Author  : 明日科技
# @File    : py.py
# @Software: PyCharm



from tkinter import *
from PIL import Image, ImageTk        # 需要旋转图片所以引入这两部分
import random                         #需要随机设置小球的初始位置
import math

wid = 500                  #画布的宽度
hig = 340                  #画布的高度

class ball():
    def __init__(self):
        btn.config(state="disabled")           #单击按钮后，将按钮设为禁用状态
        self.x1 = random.randint(50, 90)       #随机生成小球的初始坐标
        self.y1 = random.randint(50, 90)
        self.img1 = Image.open("balll1.png")
        self.dig = 0  # 初始角度
        self.img = ImageTk.PhotoImage(self.img1.rotate(self.dig))       #通过rotate()设置旋转角度
        self.speed_x = 5                  #小球的水平移动速度
        self.speed_y = 5                  #小球的垂直移动速度
        self.balls = canvas.create_image(self.x1, self.y1, image=self.img)        #绘制小球
        self.move()

#实现小球移动效果
    def move(self):
        canvas.delete(self.balls)    #删除绘制的小球
        self.dig += 5     #重新设置旋转角度
        #通过PhotoImage()将小球变形，然后再绘制
        self.img = ImageTk.PhotoImage(self.img1.rotate(self.dig))
        # 小球是否碰壁以及碰壁后的移动方向
        if self.dig >= 360:
            self.dig = 0
        if self.x1 < 60:
            self.speed_x = math.fabs(self.speed_x)
        if self.x1 + 65 > wid:
            self.speed_x = -self.speed_x
        if self.y1 < 60:
            self.speed_y = math.fabs(self.speed_y)
        if self.y1 + 65 > hig:
            self.speed_y = -self.speed_y
        self.x1 += self.speed_x
        self.y1 += self.speed_y
        # 重新绘制小球
        self.balls = canvas.create_image(self.x1, self.y1, image=self.img)
        win.after(50, self.move)


win = Tk()
win.geometry("500x380")
canvas = Canvas(win)
canvas.place(x=0, y=0, width=wid, height=hig)
bg = ImageTk.PhotoImage(file="bgball.png")        # 绘制背景图片
canvas.create_image(wid, hig, image=bg, anchor="se")
btn = Button(win, text="开始", command=ball)      #添加按钮
btn.place(x=200, y=hig + 10, width=60, height=30)
win.mainloop()
