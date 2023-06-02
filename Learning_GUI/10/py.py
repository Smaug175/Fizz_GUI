# -*- coding: utf-8 -*-
# @Author  : 明日科技
# @File    : py.py
# @Software: PyCharm

from tkinter import *
import random

win = Tk()  # 根窗口
win.geometry("380x270")

bg_img = PhotoImage(file="bg.png")  # 背景图片对象
btn_img = PhotoImage(file="button.png")  # 按钮图片对象

temp = ""  # 当前昵称
timer = ""  # 定时器
boo = False  # 抽奖未开始
with open("all.txt", "r", encoding="utf-8") as file1:  # 读取原文件
    text1 = file1.readlines()  # 读取文件
    box = text1[0].split(" ")  # 将名称以空格分割，然后存储为列表


def comeon():  # 滚动抽奖
    global timer, temp
    i = random.randint(0, len(box) - 1)
    temp = box[i]
    canvas.itemconfigure(re, text=temp)
    timer = win.after(100, comeon)


def callback(event):  # 单击开始时，滚动显示昵称，再次单击时暂停
    global timer, boo, re3, box, i, temp
    if not boo:
        comeon()
        boo = True
    else:
        timer = win.after_cancel(timer)
        box.remove(temp)
        with open("all.txt", "w", encoding="utf-8") as file1:  # 从all文件中删除中奖人
            for k in box:
                file1.write(" " + k)
        with open("lucky.txt", "a", encoding="utf-8") as file2:  # 将中奖昵称写入lucky.txt
            file2.write(temp + " ")
        boo = False


canvas = Canvas(win, width=380, height=270)
canvas.pack()
bg = canvas.create_image(190, 135, image=bg_img)  # 添加背景
btn = canvas.create_image(190, 215, image=btn_img)  # 添加按钮
re = canvas.create_text(190, 110, text="", font="宋体 08 bold")  # 显示结果
canvas.tag_bind(btn, "<Button-1>", callback)
win.mainloop()
