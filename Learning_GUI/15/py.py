# -*- coding: utf-8 -*-
# @Time    : 2020/5/21 10:08
# @Author  : 明日科技
# @File    : index.py
# @Software: PyCharm

from tkinter import *
from PIL import Image, ImageTk
import random
from tkinter.messagebox import *


class poker():

    def __init__(self):
        self.win = Tk()
        self.win.geometry("930x500-200-200")
        self.win.title("斗地主")
        self.pkBox_num = []  # 所有扑克牌编号
        self.pkBox = []
        self.moveCenter = True
        self.pb = []  # 底牌
        self.pb_box = []  # 玩家手里的牌
        self.pb_num = []  # 底牌编号
        self.pb1_num = []  # 左边玩家牌的编号
        self.pb2_num = []  # 右边玩家牌的编号
        self.pb3_num = []  # 中间玩家牌的编号
        self.pbback = []  # 为发牌时，显示牌背面
        self.temp = 0  # 所发出去的牌的数量
        self.backbox = []  # 将绘制的扑克背面存储在该列表中
        self.boo = 0  # 判断谁是地主，0表示没人叫地主，左侧表示第一位玩家，2表示第中间为玩家，3表示右侧玩家

        self.imgback1 = Image.open("border/back.png")  # 牌背面
        self.imgback2 = self.imgback1.resize((70, 120))  # 设置扑克牌大小

        for i in range(1, 55):
            self.img1 = Image.open("border/" + str(i) + ".png")
            self.img2 = self.img1.resize((70, 120))
            self.img = ImageTk.PhotoImage(self.img2)
            self.pkBox.append(self.img)  # 初始状态时，显示54张牌的背面
        self.imgback = ImageTk.PhotoImage(self.imgback2)
        self.p1 = PhotoImage(file="border/people1.png")
        self.p2 = PhotoImage(file="border/people2.png")
        self.p3 = PhotoImage(file="border/people3.png")
        self.p4 = PhotoImage(file="border/people4.png")

        self.canvas = Canvas(self.win, bg="#DDF3FF")
        self.canvas.place(x=0, y=0, width=930, height=500)

        self.call1 = Button(self.win, text="叫地主", command=lambda: self.dizhu(1), wraplength=20, bg="#efefda",
                            relief="groove")  # 左侧的叫地主
        self.call2 = Button(self.win, text="叫地主", command=lambda: self.dizhu(2), bg="#efefda",
                            relief="groove")  # 中间的叫地主
        self.call3 = Button(self.win, text="叫地主", command=lambda: self.dizhu(3), wraplength=20, bg="#efefda",
                            relief="groove")  # 右侧的叫地主
        self.dizhubox = [self.call1, self.call2, self.call3]
        self.btn1 = Button(self.win, text="发牌", command=self.fapai, relief="groove", bg="#E8E8FF")
        self.btn2 = Button(self.win, text="码牌", command=self.mapai, relief="groove", bg="#bdbdec")
        self.btn3 = Button(self.win, text="重新开始", command=self.reset, relief="groove", bg="#66cccc")
        self.btn1.place(x=360, y=180, width=80, height=30)
        self.btn2.place(x=500, y=180, width=80, height=30)
        self.btn3.place(x=400, y=230, width=150, height=30)
        self.reset()
        self.win.mainloop()

    def dizhu(self, who):
        if who == 1:
            self.canvas.itemconfig(self.left, image=self.p1)
        elif who == 2:
            self.canvas.itemconfig(self.center, image=self.p1)
            self.moveCenter = False
        elif who == 3:
            self.canvas.itemconfig(self.right, image=self.p2)
        self.boo = who

        for it in self.dizhubox:
            it.place_forget()

    # 发牌
    def fapai(self):
        # self.btn2.config(state="normal")
        if self.boo == 0:
            showerror("错误", "请先确定地主")
            return False
        a = random.randint(0, len(self.pkBox) - 1)
        if (a not in self.pb2_num) and (a not in self.pb3_num) and (a not in self.pb1_num):
            if self.temp % 3 == 0:
                lt = self.canvas.create_image(150, 70 + self.temp // 3 * 20, image=self.pkBox[a])
                self.pb1_num.append(a)
                self.pb_box.append(lt)
            elif self.temp % 3 == 1:
                rt = self.canvas.create_image(335 + self.temp // 3 * 20, 400, image=self.pkBox[a])
                self.pb2_num.append(a)
                self.pb_box.append(rt)
            else:
                ct = self.canvas.create_image(770, 70 + self.temp // 3 * 20, image=self.pkBox[a])
                self.pb3_num.append(a)
                self.pb_box.append(ct)
            self.pb.remove(a)
            self.canvas.delete(self.backbox[-1])
            del self.backbox[-1]
        else:
            self.temp -= 1
        self.temp += 1
        if self.temp < len(self.pkBox) - 3:
            self.win.after(30, self.fapai)
        else:

            self.canvas.create_image(360, 100, image=self.pkBox[self.pb[0]])
            self.canvas.create_image(460, 100, image=self.pkBox[self.pb[1]])
            self.canvas.create_image(560, 100, image=self.pkBox[self.pb[2]])
            for i in self.backbox:
                self.canvas.delete(self.backbox[-1])
                del self.backbox[-1]

            self.canvas.delete(self.backbox[-1])
            del self.backbox[-1]
            print(len(self.backbox))

    # 码牌
    def mapai(self):
        self.btn2.config(state="disabled")
        # self.canvas.delete("all")
        for it in self.pb_box:
            self.canvas.delete(it)
            self.pb_box.remove(it)
        if self.boo == 1:
            self.pb1_num.extend(self.pb)
        elif self.boo == 2:
            self.pb2_num.extend(self.pb)
        else:
            self.pb3_num.extend(self.pb)
        self.pb1_num.sort()
        self.pb2_num.sort()
        self.pb3_num.sort()
        for i in range(len(self.pb1_num)):
            self.canvas.create_image(150, 70 + i * 20, image=self.pkBox[self.pb1_num[i]])

        for i in range(len(self.pb3_num)):
            self.canvas.create_image(770, 70 + i * 20, image=self.pkBox[self.pb3_num[i]])
        if self.moveCenter:
            for i in range(len(self.pb2_num)):
                self.canvas.create_image(335 + i * 20, 400, image=self.pkBox[self.pb2_num[i]])
        else:
            for i in range(len(self.pb2_num)):
                self.canvas.create_image(310 + i * 20, 400, image=self.pkBox[self.pb2_num[i]])

    def reset(self):
        self.temp = 0
        self.canvas.delete("all")
        self.pb = []
        self.boo = 0
        self.pb1_num = []
        self.pb2_num = []
        self.pb3_num = []
        self.moveLeft = True
        self.left = self.canvas.create_image(70, 80, image=self.p3)
        self.right = self.canvas.create_image(850, 80, image=self.p4)
        self.center = self.canvas.create_image(225, 400, image=self.p3)

        for it in self.dizhubox:
            it.config(state="normal")
        for i in range(54):
            self.back1 = self.canvas.create_image(160 + i * 11, 90, image=self.imgback)
            self.backbox.append(self.back1)
            self.pb.append(i)

        self.call1.place(x=275, y=160, width=30, height=100)  # 左侧的叫地主
        self.call2.place(x=415, y=290, width=120, height=30)  # 中间的叫地主
        self.call3.place(x=650, y=160, width=30, height=100)  # 右侧的叫地主


poker()
