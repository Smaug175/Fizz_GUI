from tkinter import *
from tkinter.messagebox import *
import winsound
import random

win = Tk()
win.geometry("1920x1080+0+0")
win.state("zoomed")
win.title("音乐机器人")


# 计时器
def count():
    global tim, countdown
    cav.delete(text)  # 删除气泡
    entry.destroy()  # 销毁秒数文本框
    cav.itemconfig(showTime, image=imgbox[tim + 1])
    tim -= 1
    countdown = win.after(1000, count)  # 定时器，每过1000毫秒就调用一次count
    if tim < 0:
        win.after_cancel(countdown)  # 倒计时结束，取消计时器
        play()  # 播放音乐


# 开始倒计时
def start(*arge):
    global tim, showTime
    tim = time1.get()  # 获取用户选择的时间
    if tim != "" and tim in "0123456789":
        tim = int(tim)
    else:
        showerror("提示", "请输入0到9之间的数字！")
        return
    showTime = cav.create_image(958, 228)
    if tim > 0 and tim < 10:  # 判断用户选择的时间是否大于0
        count()
    else:
        cav.delete(text)  # 删除气泡
        entry.destroy()  # 隐藏选择时间的组合框
        play()  # 播放音乐


# 随机播放音乐
def play():
    cav.itemconfig(showTime, image=imgbox[-1])
    cav.tag_bind(showTime, "<Button-1>", quitwin)
    music = ["m1.wav", "m2.wav", "m3.wav", "m4.wav", "m5.wav", "m6.wav"]
    one = "wav/" + random.choice(music)
    winsound.PlaySound(one, winsound.SND_ASYNC)


def quitwin(event="event"):
    win.quit()  # 功能：关闭窗口


imgbox = []
# 倒计时数字图片对象
for i in range(0, 11):
    img = PhotoImage(file="image/bg" + str(i) + ".png")
    imgbox.append(img)
quit1 = PhotoImage(file="image/quit.png")  # 关闭窗口图片对象
imgbox.append(quit1)  # 添加关闭按钮
pao = PhotoImage(file="image/pao.png")  # 聊天气泡图片对象

cav = Canvas(win, width=1920, height=1080, bg="yellow")
cav.place(x=0, y=0, relwidth=1, relheight=1)
bg = cav.create_image(960, 530, image=imgbox[0])  # 显示背景图片
# 用于显示倒计时
text = cav.create_image(470, 280, image=pao)
# 选择时间提示
# 创建文本框
time1 = StringVar()
entry = Entry(win, textvariable=time1, font=("宋体", 20, "normal"), relief="groove", bd=2)
entry.place(x=400, y=240, width=110, height=40)
# 当变量发生变化时，调用start方法
entry.bind("<Return>", start)  # 开始
entry.focus_set()  # 让文本框获得焦点
win.protocol("WM_DELETE_WINDOW", quitwin)
winsound.PlaySound("wav/1.wav", winsound.SND_ASYNC)  # 播放例计时提示
win.mainloop()
