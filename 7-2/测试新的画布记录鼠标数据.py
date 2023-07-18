import tkinter as tk

import subprocess

# 运行另一个Python文件


RUN=False    
process=None

def chick(event):
    global RUN,process
    if RUN:
        RUN=False
        process.kill()
    else:
        RUN=True
        process=subprocess.run(['python', 'D:\\Desk\\Fizz_GUI\\todo\\autotrack.py'])   
    print(RUN)
    
    x, y = event.x, event.y
    canvas.create_oval(x, y, x+1, y+1, fill='black')  # 绘制一个小点
root = tk.Tk()
canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()


canvas.bind('<Button-1>', chick)  # 绑定鼠标移动事件
root.mainloop()

