import tkinter as tk
from PIL import Image, ImageTk
import tkinter.filedialog
import tkinter.messagebox


# 单击选择图片按钮，预览图片
def select_button():
    global a
    fileType=[("png文件","*.png"),("jpg文件","*.jpg")]
    a = tk.filedialog.askopenfilename(title="选择图片",filetypes=fileType)
    # 预览图片
    img = Image.open(a)
    image_width = img.size[0]  # 获取原图像的宽度
    image_height = img.size[1]  # 获取原图像的高度
    if image_width > image_height:  # 如果原图像的宽度大于高度，那么设置预览图的宽度为310，高度等比例缩小
        image_height = int(image_height * 310 / image_width)
        image_width = 310
    else:  # 如果原图的高度大于宽度，那么设置预览图的高度为280，宽度等比例缩小
        image_width = int(image_width * 280 / image_height)
        image_height = 280
    out = img.resize((image_width, image_height))  # 设置图片大小，缩放显示
    img = ImageTk.PhotoImage(out)
    label_image.config(image=img)  # 将图像显示在窗口中
    label_image.place(x=120, y=80)  # 设置图像容器label组件的位置
    txt.set(a)  # 显示图片文件路径    # 将图像路径显示在文本框中


# 单击切分图片按钮，调用切图和保存图片的函数
def cut_button():
    file_path = txt.get()
    if file_path == "":
        tk.messagebox.showerror("错误", "所选文件为空，请重新选择文件")
    else:
        image = Image.open(file_path)
        image_list = cut_image(image)
        save_images(image_list)
        tk.messagebox.showinfo("切图成功", "切图成功，请在程序所在的目录查看")


# 切图（切成9张图）
def cut_image(image):
    width, height = image.size
    colWidth = int(width / 3)  # 一行3张
    colHeight = int(height / 3)
    image_grid = []
    for i in range(0, 3):
        for j in range(0, 3):
            row = (j * colWidth, i * colHeight, (j + 1) * colWidth, (i + 1) * colHeight)
            image_grid.append(row)
    image_list = [image.crop(row) for row in image_grid]
    return image_list


# 保存图片
def save_images(image_list):
    index = 1
    for image in image_list:
        image.save(str(index) + '.png', 'PNG')
        index += 1


# 设置窗口
main = tk.Tk()
# 设置窗口的大小
# F2F1D7    #E8FFE8"
main.configure(bg="#F2F1D7")
main.geometry('550x400')
main.title('明日九宫格切图器')  # 设置标题栏
label1 = tk.Label(main, text='选择文件：', font=("bold", 14), fg='#f00', bg="#F2F1D7")
label1.place(x=20, y=25)
txt = tkinter.StringVar()
txt_entry = tkinter.Entry(main, width=55, textvariable=txt, relief=tk.GROOVE)
txt_entry.place(x=120, y=20, width=220, height=30)
button1 = tk.Button(main, text='浏览', fg="#f00", bg='#E8FFE8', font=14, command=select_button, relief=tk.GROOVE, )
button1.place(x=350, y=20, width=60, height=32)
button2 = tk.Button(main, text='我选好了', fg="#f00", bg='#DDF3FF', font=13, relief=tk.GROOVE, command=cut_button)
button2.place(x=430, y=20, width=90, height=32)
# 添加显示图片的Label
label_image = tkinter.Label(main, bg="#F2F1D7")
main.mainloop()  # 执行主循环
