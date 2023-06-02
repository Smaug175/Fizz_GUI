
from tkinter import *
import random
from tkinter.messagebox import showinfo

temp = 0  # 初始时间
timer = ""  # 定时器
boo = False  # 计时未开始
rans = [100, 80, 60, 40]  # 时间间隔
def anim():  # 计时
    global timer, temp
    num = random.choice(rans)
    print(num)
    temp += 0.02
    temp = round(temp, 2)  # 将时间格式化为两位小数的浮点数
    canvas.itemconfig(text, text=temp)  # 将时间显示在窗口中
    timer = win.after(num, anim)


def ready(event):  # 单击开始时，滚动显示昵称，再次单击时暂停
    global timer, boo, temp
    if boo:  # 挑战开始
        timer = win.after_cancel(timer)  # 挑战结束，关闭定时器
        if int(temp) == 10:  # 整数部分为10，则挑战成功，反之挑战失败
            showinfo("挑战成功", "恭喜，挑战成功，您在本店的消费课全部免单")
        else:
            showinfo("挑战失败", "啊哦！挑战失败，没有中奖")
        boo = False  # 重置boo,temp和窗口中显示的时间
        temp = 0
        canvas.itemconfig(text, text="0.00")
    else:
        anim()  # 调用倒计时函数
        boo = True  # 重置boo


win = Tk()
win.title("挑战10秒小程序")
win.geometry("527x751")  # 设置窗口大小
bg = PhotoImage(file="bg.png")
canvas = Canvas(win, width=527, height=751)  # 添加画布
canvas.create_image(0, 0, image=bg, anchor=NW)  # 绘制背景图像
text = canvas.create_text(210, 100, text="0.00", anchor=NW, font=("宋体", 40))  # 绘制文字，显示计时时间
canvas.pack()
win.bind("<Return>", ready)  # 为画布绑定键盘事件，单击回车键时挑战开始或者停止
win.mainloop()
