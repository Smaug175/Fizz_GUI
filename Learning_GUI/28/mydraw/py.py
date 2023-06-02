
from tkinter import *
import tkinter.ttk
from PIL import Image
import tkinter.colorchooser
import tkinter.filedialog
from PIL import Image, ImageTk, ImageGrab
import time


root = Tk()
root.title('我的画图')
root.geometry("1000x600")
root.resizable(0, 0)
# 控制是否允许画图的变量，1：允许，0：不允许
canDraw = IntVar(value=0)
# 控制画图类型的变量，1：曲线，2：直线，3：矩形，4：文本，5：橡皮 6：圆形
type1 = IntVar(value=1)
# 记录鼠标位置的变量
X = IntVar(value=0)
Y = IntVar(value=0)
colorbar = 0  # colorbar=0表示当前设置的是边框颜色，反之设置填充颜色
fillColor = '#000000'  # 填充颜色
strokeColor = '#FFFFFF'  # 边框颜色

# 记录最后绘制图形的id
lastDraw = 0
end = [0]  # 每次抬起鼠标时，最后一组图形的编号

# 保存画布
def getter():
    app_x = root.winfo_x()
    app_y = root.winfo_y()
    canvas_x = canvas.winfo_x()
    canvas_y = canvas.winfo_y()
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    x1 = app_x + canvas_x + 7
    y1 = app_y + canvas_y + 52
    x2 = x1 + canvas_width
    y2 = y1 + canvas_height - 2
    time.sleep(0.5)  # 等待一会，否则会把点击“保存”那一刻也存进去
    filename = tkinter.filedialog.asksaveasfilename(filetypes=[('.jpg', 'JPG')],
                                                    initialdir='C:\\Users\\Public\\Desktop')
    ImageGrab.grab().crop((x1, y1, x2, y2)).save(filename)


# 鼠标左键单击，允许画图
def mouseDown(event):
    canDraw.set(1)
    X.set(event.x)
    Y.set(event.y)
    if type1.get() == 4:
        canvas.create_text(event.x, event.y, font=font1, text=text, fill=fillColor)
        type1.set(1)


# 按住鼠标左键移动，画图
def mouseMove(event):
    global lastDraw
    if canDraw.get() == 0:
        return
    if type1.get() == 1:
        # 使用当前选择的前景色绘制曲线
        lastDraw = canvas.create_line(X.get(), Y.get(), event.x, event.y,
                                      fill=fillColor, width=linWid.get())  # 返回值就是对图形的计数，直接delete这个数字就能删除该图形
        X.set(event.x)
        Y.set(event.y)
    elif type1.get() == 2:
        try:
            canvas.delete(lastDraw)
        except Exception as e:
            pass
        # 绘制直线，先删除刚刚画过的直线，再画一条新的直线
        lastDraw = canvas.create_line(X.get(), Y.get(), event.x, event.y,
                                      fill=fillColor, width=linWid.get())
    elif type1.get() == 3:
        # 绘制矩形，先删除刚刚画过的矩形，再画一个新的矩形
        try:
            canvas.delete(lastDraw)
        except Exception as e:
            pass
        lastDraw = canvas.create_rectangle(X.get(), Y.get(), event.x, event.y,
                                           outline=strokeColor, fill=fillColor, width=linWid.get())

    elif type1.get() == 5:
        lastDraw = canvas.create_rectangle(event.x - 5, event.y - 5, event.x + 5, event.y + 5,
                                           outline="#fff")
    elif type1.get() == 6:
        # 绘制圆形，先删除刚刚画过的矩形，再画一个新的矩形
        try:
            canvas.delete(lastDraw)
        except Exception as e:
            pass
        lastDraw = canvas.create_oval(X.get(), Y.get(), event.x, event.y,
                                      fill=fillColor, outline=strokeColor, width=linWid.get())


# 鼠标左键抬起，不允许画图
def mouseUp(event):
    global lastDraw
    if type1.get() == 2:
        # 绘制直线
        lastDraw = canvas.create_line(X.get(), Y.get(), event.x, event.y, fill=fillColor)
    elif type1.get() == 3:

        lastDraw = canvas.create_rectangle(X.get(), Y.get(), event.x, event.y, outline=strokeColor)
    elif type1.get() == 6:

        lastDraw = canvas.create_oval(X.get(), Y.get(), event.x, event.y, outline=strokeColor)
    canDraw.set(0)
    end.append(lastDraw)


# 打开图像文件
def Open():
    filename = tkinter.filedialog.askopenfilename(title='导入图片',
                                                  filetypes=[('image', '*.jpg *.png *.gif')])
    if filename:
        global image
        image = Image.open(filename)
        img_width0=image.size[0]
        img_height0=image.size[1]
        if img_width0>img_height0:
            img_width1=1000
            img_height1=img_height0*img_width1//img_width0
        else:
            img_height1 = 550
            img_width1 = img_width0 * img_height1 // img_height0
        image = image.resize((img_width1, img_height1), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        canvas.create_image(img_width1/2, img_height1/2, image=image)



# 清除
def Clear():
    global lastDraw, end
    canvas.delete("all")
    # for item in canvas.find_all():
    #     canvas.delete(item)
    end = [0]
    lastDraw = 0


# 撤销
def Back():
    global end
    try:
        for i in range(end[-2], end[-1] + 1):  # 要包含最后一个点，否则无法删除图形
            canvas.delete(i)
        end.pop()  # 弹出末尾元素
    except:
        end = [0]


def selType(event, num):
    global type1
    type1.set(num)


# 文本框
def drawText(event):
    global text, size, font_Style, font_size, top, entry
    top = Toplevel()
    top.title("输入文本")
    Label(top, text="请输入文本：").pack(side=LEFT)
    entry = Entry(top)
    entry.pack(side=LEFT)
    entry.focus_set()
    font_family = ("宋体", "黑体", "方正舒体", "楷体", "隶书", "方正姚体", "微软雅黑")
    font_Style = StringVar()
    font_Style.set("宋体")  # 初始字体
    family = tkinter.ttk.Combobox(top, textvariable=font_Style, values=font_family).pack(side=LEFT)
    font_size = Spinbox(top, from_=12, to=30, increment=2, width=10)  # 选择字号
    font_size.pack(side=LEFT)
    Button(top, text="确定", command=showText).pack(side=LEFT)


def showText():
    global font1, text
    text = entry.get()
    font1 = (font_Style.get(), font_size.get())
    type1.set(4)
    top.destroy()


# 选择颜色
def colorSel(event, boo):
    global fillColor, strokeColor
    if boo:  # boo=1,表示从鼠标单击的位置获取颜色值，boo=1表示要打开颜色版选择位置
        colorTag = canvasTool.find_closest(event.x, event.y)  # 鼠标单击位置的颜色色块
        theColor = canvasTool.itemcget(colorTag, "fill")  # 获取该色块的颜色值
        if colorbar:  # 判断应该设置为边框颜色还是填充颜色
            fillColor = theColor
            canvasTool.itemconfig(fgrect, fill=theColor)
        else:
            strokeColor = theColor
            canvasTool.itemconfig(bgrect, fill=theColor)
    else:
        if colorbar:
            fillColor = tkinter.colorchooser.askcolor()[1]
            canvasTool.itemconfig(fgrect, fill=fillColor)
        else:
            strokeColor = tkinter.colorchooser.askcolor()[1]
            canvasTool.itemconfig(bgrect, fill=strokeColor)


def colorType(event, bar):
    global colorbar
    if bar:
        colorbar = 0
        canvasTool.moveto(colrect, 60, 5)
    else:
        colorbar = 1
        canvasTool.moveto(colrect, 5, 5)


# 创建画布（用于画图）
image = PhotoImage()
canvas = Canvas(root, bg='white', width=1000, height=550, relief=SOLID)
canvas.create_image(1000, 550, image=image)
canvas.bind('<Button-1>', mouseDown)  # 单击左键
canvas.bind('<B1-Motion>', mouseMove)  # 按住并移动左键
canvas.bind('<ButtonRelease-1>', mouseUp)  # 释放左键

canvas.place(x=0, y=50)

'''主菜单及其关联的函数'''
menu = Menu(root, tearoff=0)
menu.add_command(label='保存', command=getter)
menu.add_command(label='打开', command=Open)
menu.add_command(label='清屏', command=Clear)
menu.add_command(label='撤销', command=Back)
menu.add_command(label='橡皮擦', command=lambda: selType("", 5))
root.config(menu=menu)

'''该canvas用于显示工具栏'''
canvasTool = Canvas(root, width=1000, height=50, bg="#f0f0f0")
canvasTool.place(x=0, y=0)
colrect = canvasTool.create_rectangle(60, 5, 110, 50, fill="#c9e0f7")
fgrect = canvasTool.create_rectangle(20, 10, 40, 30, fill="#000")
canvasTool.create_text(30, 40, text="填充颜色")
bgrect = canvasTool.create_rectangle(75, 10, 95, 30, fill="#fff")
canvasTool.create_text(85, 40, text="边框颜色")
canvasTool.tag_bind(fgrect, "<Button-1>", lambda event: colorType(event, 0))
canvasTool.tag_bind(bgrect, "<Button-1>", lambda event: colorType(event, 1))
colorcust = canvasTool.create_rectangle(335, 5, 385, 50, fill="#fff")
colortext = canvasTool.create_text(360, 30, text="选择\n颜色")
canvasTool.tag_bind(colorcust, "<Button-1>", lambda event: colorSel(event, 0))
canvasTool.tag_bind(colortext, "<Button-1>", lambda event: colorSel(event, 0))

# 批量添加颜色色块

colorbox = ["#000", "#fff", "#7f7f7f", "#c3c3c3", "#880015", "#b97a57", "#ed1c24", "#ffaec9", "#ff7f27", "#ffc90e",
            "#fff200", "#efe480", "#22b14c", "#b6e61d", "#00a2eb", "#99d9ea", "#3f48cc", "#7092be", "#a349a4",
            "#c88fe7"]

for item in colorbox:
    index = colorbox.index(item)
    if index % 2 == 0:
        color1 = canvasTool.create_rectangle(135 + 20 * index // 2, 7, 150 + 20 * index // 2, 22, fill=item)
    else:
        color1 = canvasTool.create_rectangle(135 + 20 * (index - 1) // 2, 28, 150 + 20 * (index - 1) // 2, 43,
                                             fill=item)
    canvasTool.tag_bind(color1, "<Button-1>", lambda event: colorSel(event, 1))


'''绘制工具栏'''
# 绘制圆形工具
img1 = PhotoImage(file="D:\Desk\Fizz_GUI\Learning_GUI\\28\mydraw\image/circle.png")
circleIcon = canvasTool.create_rectangle(400, 10, 434, 44, fill="#fff")
circle1 = canvasTool.create_image(420, 27, image=img1)
canvasTool.tag_bind(circleIcon, "<Button-1>", lambda event: selType(event, 6))
canvasTool.tag_bind(circle1, "<Button-1>", lambda event: selType(event, 6))
# 绘制矩形工具
img2 = PhotoImage(file="D:\Desk\Fizz_GUI\Learning_GUI\\28\mydraw\image/rect.png")
rectIcon = canvasTool.create_rectangle(440, 10, 474, 44, fill="#fff")
rect1 = canvasTool.create_image(460, 27, image=img2)
canvasTool.tag_bind(rectIcon, "<Button-1>", lambda event: selType(event, 3))
canvasTool.tag_bind(rect1, "<Button-1>", lambda event: selType(event, 3))

# 绘制直线工具
img3 = PhotoImage(file="D:\Desk\Fizz_GUI\Learning_GUI\\28\mydraw\image/line.png")
lineIcon = canvasTool.create_rectangle(480, 10, 514, 44, fill="#fff")
line1 = canvasTool.create_image(500, 27, image=img3)
canvasTool.tag_bind(lineIcon, "<Button-1>", lambda event: selType(event, 2))
canvasTool.tag_bind(line1, "<Button-1>", lambda event: selType(event, 2))
# 绘制文字工具
img4 = PhotoImage(file="D:\Desk\Fizz_GUI\Learning_GUI\\28\mydraw\image/text.png")
textIcon = canvasTool.create_rectangle(520, 10, 554, 44, fill="#fff")
text1 = canvasTool.create_image(540, 27, image=img4)
canvasTool.tag_bind(textIcon, "<Button-1>", drawText)
canvasTool.tag_bind(text1, "<Button-1>", drawText)
# 铅笔工具工具
img5 = PhotoImage(file="D:\Desk\Fizz_GUI\Learning_GUI\\28\mydraw\image/pen.png")
penIcon = canvasTool.create_rectangle(560, 10, 594, 44, fill="#fff")
pen1 = canvasTool.create_image(580, 27, image=img5)
canvasTool.tag_bind(penIcon, "<Button-1>", lambda event: selType(event, 1))
canvasTool.tag_bind(pen1, "<Button-1>", lambda event: selType(event, 1))

# 设置文字粗细
canvasTool.create_text(630, 30, text="粗细:", font=10)
linWid = IntVar()
spin = tkinter.ttk.OptionMenu(canvasTool, linWid, *range(1, 11))
linWid.set(1)
canvasTool.create_window(670, 30, window=spin)
root.mainloop()

