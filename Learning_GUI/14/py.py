
from tkinter import *
from tkinter.messagebox import *
import time
from PIL import Image, ImageTk, ImageSequence

'''界面设计中应用的全局变量'''
flyaction = []  # 飞行流程
entry_length = None
ifmodify = False
top = None
top1 = None
cav_t = None
flybox = None
plaine = None
posx = 250
posy = 300
posx1 = 250
posy1 = 300

step = 0
taskstep = 5  # 任务要求完成步骤，采用小于9的正整数
tempbg = []  # 临时用于保存PhotoImage对象，防止图片绘制完成被销毁，不显示的问题
p = 280
rem = 0
student_name = ""  # 学生姓名
screen_width = 1920  # 屏幕分辨率的宽度
screen_height = 1016  # 屏幕分辨率的高度


# 确定按钮事件
def submit(event):
    if entry.get() != "":
        global student_name
        student_name = entry.get()  # 获取名字
        print('你的名字是：', student_name)
        entry.delete(0, END)  # 清空文本框
        createTask()  # 打开新窗口
    else:
        showinfo('提示', '还没有输入名字呦！')
        return


# 弹出挑战任务新窗口
def createTask():
    global flyaction, p, ifmodify, rem, cav_t, entry_length, top  # 飞行流程， ** ，能否修改，**，画布，输入距离的文本框
    flyaction = []  # 飞行流程
    p = 250
    ifmodify = False
    rem = 0
    top = Toplevel()
    top.title('明日之星Pyhon版无人机挑战赛_任务')
    top.state("zoomed")
    top.iconbitmap(bitmap="picture/mr.ico")  # 设置图标
    cav_t = Canvas(top, width=screen_width, height=screen_height, bg="black")
    cav_t.place(width=screen_width, height=screen_height, relx=0, rely=0)

    img_v = PhotoImage(file="picture/bg-task.png")
    cav_t.create_image(screen_width // 2, (screen_height - 42) // 2, image=img_v)  # 显示背景图片

    # 显示XXX的任务
    cav_t.create_text(490, 170, text="【" + student_name + "】的任务：" + str(taskstep) + "步完成穿越风洞任务", justify="left",
                      fill="white",
                      font=("微软雅黑", 36, "bold"))
    # 显示任务描述
    pao = PhotoImage(file="picture/describe.png")
    text = cav_t.create_image(screen_width // 2 + 50, 386, image=pao)

    # 执行按钮
    fly = cav_t.create_text(1700, 927, text="确认执行", justify=RIGHT, fill="white", font=("微软雅黑", 37, "bold"))
    cav_t.tag_bind(fly, "<Button-1>", start)
    cav_t.create_text(330, 890, text="输入距离（11~400）：", justify="left", fill="black", font=("微软雅黑", 26, "bold"))
    # 输入距离的文本框
    entry_length = Entry(top, font=("宋体", 30, "normal"), relief="groove", bd=2)
    entry_length.place(x=142, y=937, width=287, height=51)
    entry_length.focus_set()  # 让文本框获得焦点
    cav_t.create_text(466, 962, text="cm", justify="left", fill="black", font=("微软雅黑", 30, "bold"))
    # 执行按钮
    btn_go = PhotoImage(file="picture/go.png")  # 前进按钮
    fly = cav_t.create_image(779, 943, image=btn_go)
    cav_t.tag_bind(fly, "<Button-1>", add_go)

    btn_up = PhotoImage(file="picture/up.png")  # 上升按钮
    fly = cav_t.create_image(1059, 943, image=btn_up)
    cav_t.tag_bind(fly, "<Button-1>", add_up)

    btn_fall = PhotoImage(file="picture/fall.png")  # 下降按钮
    fly = cav_t.create_image(1354, 943, image=btn_fall)
    cav_t.tag_bind(fly, "<Button-1>", add_fall)
    top.mainloop()


def add_go(event):  # 前进方法
    add('前进')


def add_up(event):  # 上升方法
    add('上升')


def add_fall(event):  # 下降方法
    add('下降')


# 添加执行流程
def add(action):
    number = entry_length.get()  # 获取值
    btnbg = PhotoImage(file="picture/btn_bg.png")  # 操作流程背景
    if number.strip() != "":
        try:
            if 20 <= int(number) <= 400:
                if action in ["上升", "下降"] and int(number) > 100:
                    showinfo('提示', '不是有效的数值！', parent=top)
                else:
                    global ifmodify
                    global rem
                    print("rem：", rem)
                    flyactionlen = len(flyaction)
                    print("flyactionlen:", flyactionlen)
                    entry_length.delete(0, END)  # 清空文本框
                    if rem != 0 and ifmodify:
                        cav_t.itemconfigure(rem, text=action + number + "cm")
                        for i in range(flyactionlen):
                            if flyaction[i][0] == rem:
                                flyaction[i] = (rem, action, number)  # 修改流程
                        rem = 0
                        ifmodify = False
                    else:  # 当绘制时
                        global p
                        p_y = 650  # y轴位置
                        if flyactionlen <= taskstep - 1:  # 小于限定步骤

                            if taskstep < 6:  # 步骤在一行可以显示时
                                p_y = 650  # y轴位置
                                if flyactionlen != taskstep - 1:  # 显示指示箭头
                                    btnline = PhotoImage(file="picture/btn_line.png")
                                    text = cav_t.create_image(p + 180, p_y, image=btnline)
                                draw(p, p_y, action, number, btnbg)  # 绘制一步
                                p += 350

                                if flyactionlen == taskstep - 1:  # 当最后一步时
                                    # 显示降落
                                    a_stop = PhotoImage(file="picture/stop.png")
                                    cav_t.create_image(screen_width - 230, 768, image=a_stop)
                            else:  # 步骤需2行显示时
                                p_y = 788  # y轴位置
                                if flyactionlen // 5 == 1:  # 显示第二行的内容
                                    p -= 350
                                    # 显示指示箭头
                                    if flyactionlen == 5:  # 第二行的第一步时显示竖向箭头
                                        btnlineb = PhotoImage(file="picture/btn_lineb.png")
                                        cav_t.create_image(p, 717, image=btnlineb)
                                    # 显示横向箭头
                                    btnline = PhotoImage(file="picture/btn_linel.png")
                                    cav_t.create_image(p - 180, p_y, image=btnline)
                                    draw(p, p_y, action, number, btnbg)  # 绘制一步
                                    if flyactionlen == taskstep - 1:
                                        # 显示降落
                                        a_stop = PhotoImage(file="picture/stop1.png")
                                        cav_t.create_image(p - 350, p_y, image=a_stop)
                                else:  # 显示两行中的第一行
                                    p_y = 650  # y轴位置
                                    if flyactionlen < 4:  # 显示指示箭头
                                        btnline = PhotoImage(file="picture/btn_line.png")
                                        text = cav_t.create_image(p + 180, p_y, image=btnline)
                                    draw(p, p_y, action, number, btnbg)  # 绘制一步
                                    p += 350
                            top.mainloop()

            else:
                showinfo('提示', '不是有效的数值！', parent=top)
        except Exception as e:
            showinfo('提示', '请输入正确的整数！', parent=top)
            print(e)
    else:
        showinfo('提示', '还没有输入距离！', parent=top)

    print("流程列表：", flyaction)


# 绘制一步
def draw(x, y, action, number, btnbg):
    # 显示操作流程背景
    cav_t.create_image(x, y, image=btnbg)
    # 显示操作流程文字
    fly = cav_t.create_text(x, y, text=action + number + "cm", justify=RIGHT, fill="white",
                            font=("微软雅黑", 27, "bold"))
    cav_t.tag_bind(fly, "<Button-1>", modify)
    flyaction.append((fly, action, number))  # 记录流程


# 修改执行流程
def modify(event):
    global rem
    rem = cav_t.find_closest(event.x, event.y)[0]
    global ifmodify
    ifmodify = True

# 任务执行
def start(event):
    global airplane, plaine, canvas_flyanim, flybox, fly_bg, flybg, gong, feng, shi
    print(flyaction)
    flybox = Toplevel()
    flybox.geometry("1920x498+0+0")
    canvas_flyanim = Canvas(flybox, width=1920, height=498, bg="#EFEFDA")
    canvas_flyanim.place(x=0, y=0, width=1920, height=498)
    airplane = PhotoImage(file="picture/airplane.png")
    fly_bg = PhotoImage(file="picture/showfly.png")
    gong = PhotoImage(file="picture/gong.png")
    feng = PhotoImage(file="picture/feng.png")
    shi = PhotoImage(file="picture/shi.png")
    flybg = canvas_flyanim.create_image(960, 229, image=fly_bg)
    canvas_flyanim.create_text(20, 20, text=student_name, font=("微软雅黑", 20, "bold"), fill="#f00", anchor=NW)
    canvas_flyanim.create_text(150, 20, text=" 的飞行轨迹", font=("微软雅黑", 20, "bold"), fill="#000", anchor=NW)
    plaine = canvas_flyanim.create_image(posx, posy, image=airplane)
    canvas_flyanim.create_image(498, 137, image=shi)
    canvas_flyanim.create_image(927, 163, image=feng)
    canvas_flyanim.create_image(1408, 220, image=gong)
    fly1(step, flyaction)
    flybox.mainloop()


def fly1(step, fly_ist):
    if step >= len(fly_ist):
        showresult()
    else:
        dire = fly_ist[step][1]  # 方向
        dis = int(fly_ist[step][2])  # 飞行距离
        if dire == "前进":
            go_head(dis, fly_ist)
        elif dire == "上升":
            go_up(dis, fly_ist)
        elif dire == "下降":
            go_down(dis, fly_ist)


def go_head(dis, fly_ist):  # 向前移动
    global posx, posy, plaine, posx1, posy1, step, canvas_flyanim, flybox
    if posx1 < posx + dis * 2.5:  # 判断是否移动了指定距离
        posx1 += 2
        canvas_flyanim.coords(plaine, posx1, posy1)  # 使用coords(0方法移动无人机
        flybox.after(50, lambda: go_head(dis, fly_ist))
    else:
        posx += dis * 2.5
        step += 1  # 当前运行的步数加1
        flybox.after(1000, lambda: fly1(step, fly_ist))


def go_up(dis, fly_ist):  # 向上移动
    global posx, posy, plaine, posx1, posy1, step
    if posy1 > posy - dis * 1.5:
        posy1 -= 2
        canvas_flyanim.coords(plaine, posx1, posy1)
        flybox.after(50, lambda: go_up(dis, fly_ist))
    else:
        posy -= dis * 1.5
        step += 1
        flybox.after(1000, lambda: fly1(step, fly_ist))


def go_down(dis, fly_ist):  # 向上移动
    global posx, posy, plaine, posx1, posy1, step
    if posy1 < posy + dis * 1.5:
        posy1 += 2
        canvas_flyanim.coords(plaine, posx1, posy1)
        flybox.after(50, lambda: go_down(dis, fly_ist))
    else:
        posy += dis * 1.5
        step += 1
        flybox.after(1000, lambda: fly1(step, fly_ist))


def showresult():  # 显示挑战结果
    global top1
    top1 = Toplevel()
    top1.state("zoomed")
    # 弹出任务完成的图片
    global cav_s
    cav_s = Canvas(top1, width=screen_width, height=screen_height, bg="black")
    cav_s.place(width=screen_width, height=screen_height, relx=0, rely=0)
    img_s = PhotoImage(file="picture/successbg.png")
    cav_s.create_image(screen_width // 2, (screen_height - 42) // 2, image=img_s)  # 显示背景图片

    # 重新开始按钮
    close_s = cav_s.create_text(screen_width // 2, (screen_height + 500) // 2, text="重新开始", justify=RIGHT, fill="white",
                                font=("微软雅黑", 37, "bold"))
    cav_s.tag_bind(close_s, "<Button-1>", close2)
    # 恢复上次操作按钮
    close_r = cav_s.create_text(screen_width // 2, (screen_height + 650) // 2, text="恢复上次", justify=RIGHT, fill="white",
                                font=("微软雅黑", 37, "bold"))
    cav_s.tag_bind(close_r, "<Button-1>", close3)
    im = Image.open('picture/success.gif')  # gif动图路径
    while True:
        for frame in ImageSequence.Iterator(im):  # ImageSequence.Iterator(im) 将gif动画分解为每一帧
            pic = ImageTk.PhotoImage(frame)
            cav_s.create_image(screen_width // 2, (screen_height - 42) // 3,
                               image=pic)  # 设置动画的位置，代码中的坐标为动图的中心点的坐标，而不是左上角坐标
            top1.update()
            time.sleep(0.1)  # 控制动画的播放速度
    top1.mainloop()


def close2(event):
    '''重新开始'''
    global step, posy1, posx1, posx, posy
    cav_t.delete("all")
    cav_s.delete("all")
    canvas_flyanim.delete("all")
    top1.destroy()
    top.destroy()
    flybox.destroy()
    step = 0
    posx = 250
    posy = 300
    posx1 = 250
    posy1 = 300


def close3(event):
    global step, posy1, posx1, posx, posy
    '''恢复上次操作'''
    cav_s.delete("all")
    canvas_flyanim.delete("all")
    step = 0
    posx = 250
    posy = 300
    posx1 = 250
    posy1 = 300
    flybox.destroy()
    top1.destroy()



'''根窗口——登录'''
win = Tk()
win.state("zoomed")
win.iconbitmap('picture/mr.ico')
win.title("明日之星Pyhon版无人机挑战赛")
cav = Canvas(win, width=screen_width, height=screen_height, bg="black")
cav.place(width=screen_width, height=screen_height, relx=0, rely=0)

img = PhotoImage(file="picture/bg-3.png")
bg = cav.create_image(screen_width // 2, screen_height // 2, image=img)  # 显示背景图片
# 问题
question = '请输入挑战者名字？'
cav.create_text(890, 330, text=question, justify="left", fill="white", font=("微软雅黑", 36, "bold"))
# 确定按钮
fly = cav.create_text(962, 775, text="确定", justify=RIGHT, fill="white", font=("微软雅黑", 37, "bold"))
cav.tag_bind(fly, "<Button-1>", submit)
# 输入名字的文本框
entry = Entry(win, textvariable="", font=("宋体", 30, "normal"), relief="groove", bd=2)
entry.place(x=712, y=407, width=287, height=51)
entry.bind("<Return>", submit)
entry.focus_set()  # 让文本框获得焦点

win.mainloop()
