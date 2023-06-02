import tkinter as tk
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
import time
import sys
import pickle

mouse_check_path=sys.path[0]+'\data\D=2000_W=100_mouse_check.bin'
mouse_move_path=sys.path[0]+'\data\D=2000_W=100_mouse_move.bin'
information_path=sys.path[0]+'\data\D=2000_W=100_information.bin'
track_path=sys.path[0]+'\data\D=2000_W=100_track.bin'

with open(information_path,'rb') as file:
    inf=pickle.load(file)
with open(track_path,'rb') as file:
    track=pickle.load(file)
with open(mouse_check_path,'rb') as file:
    mouse_check=pickle.load(file)

D=inf['D']
W=inf['W']

# 创建主窗口
root = tk.Tk()
root.title('记录鼠标的位置和时间')
# 获取屏幕尺寸
screen_width = inf['screen_width']
screen_height = inf['screen_height']

# 创建画布
canvas = tk.Canvas(root, width=screen_width, height=screen_height)
# 将画布置于主窗口
canvas.pack()

#绘制目标点

cir1=canvas.create_oval(inf['cir1'][0],inf['cir1'][1],inf['cir1'][2],inf['cir1'][3],outline='red',tags='cir1')
cir2=canvas.create_oval(inf['cir2'][0],inf['cir2'][1],inf['cir2'][2],inf['cir2'][3],outline='blue',tags='cir2')

for _,point in mouse_check:
    canvas.create_oval(point[0],point[1],point[0]+10,point[1]+10,outline='black')

line=0
times=0
def after_1s():
    global line,times,track
    if line==len(track):
        root.destroy()
    point=track[line][times][1]
    canvas.create_oval(point[0],point[1],point[0]+10,point[1]+10, fill='black',tags='point')
    root.after(1,after_1s)
    times+=1
    if times==len(track[line]):
        line+=1
        times=0
        canvas.delete('point')
    
    
    
after_1s()
# 隐藏窗口边框
root.attributes('-fullscreen', True)

#按1退出
root.bind('1', lambda event:root.destroy())

# 进入主循环
root.mainloop()
