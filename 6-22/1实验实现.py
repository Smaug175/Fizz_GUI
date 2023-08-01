import tkinter as tk
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
import time
import sys
import pickle


inf={}

D=2000
W=100
inf['D']=D
inf['W']=W

#删除被点击的控件
def delete_widget(event):
    global cir,mouse_check
    item_id = canvas.find_closest(event.x, event.y)[0]  # 获取与鼠标事件位置最接近的项的ID
    cir-=1
    canvas.delete(item_id)  # 删除该项
    mouse_check.append((time.time(),(event.x,event.y)))#只记录点击到的点的位置和时间
    

# 保存数据并退出
def save_esc(event):
    global mouse_move,W,D,mouse_check,inf
    #保存实验的关键信息
    file_name0 = 'D='+str(D)+'_W='+str(W)+"_information.bin"  # 文件路径和名称
    file_path0=sys.path[0]+'\data\\'+file_name0
    # 打开文件，以写入模式
    with open(file_path0, "wb") as file:
        pickle.dump(inf, file)
    
    file_name1 = 'D='+str(D)+'_W='+str(W)+"_mouse_move.bin"  # 文件路径和名称
    file_path1=sys.path[0]+'\data\\'+file_name1
    # 打开文件，以写入模式
    with open(file_path1, "wb") as file:
        pickle.dump(mouse_move, file)
    
    file_name2='D='+str(D)+'_W='+str(W)+"_mouse_check.bin"
    file_path2=sys.path[0]+'\data\\'+file_name2
    with open(file_path2, "wb") as file:
        pickle.dump(mouse_check, file)
        
    root.destroy()
    
# 创建主窗口
root = tk.Tk()
root.title('记录鼠标的位置和时间')
# 获取屏幕尺寸
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
inf['screen_width']=screen_width
inf['screen_height']=screen_height

# 创建画布
canvas = tk.Canvas(root, width=screen_width, height=screen_height)
# 将画布置于主窗口
canvas.pack()

#绘制目标点
x1=(screen_width-D-W)/2
x2=(screen_width+D-W)/2
y1=(screen_height-W)/2
y2=(screen_height-W)/2
cir=0#记录目标点是否已经出现，如果为0，说明要重新生成目标点
show_times=-1#记录目标点出现的次数，如果为3，说明测试结束
def create_cirs():
    global cir,show_times,inf
    
    if cir==0:
        cir1=canvas.create_oval(x1,y1,x1+W,y1+W,fill='red',tags='cir1')
        cir2=canvas.create_oval(x2,y2,x2+W,y2+W,fill='blue',tags='cir2')
        inf['cir1']=(x1,y1,x1+W,y1+W)
        inf['cir2']=(x2,y2,x2+W,y2+W)
        canvas.tag_bind(cir1, '<Button-1>', delete_widget)
        canvas.tag_bind(cir2, '<Button-1>', delete_widget)
        cir+=2
        show_times+=1
        
    else:
        pass
    #是否结束测试
    if show_times==3:
            save_esc(1)
    root.after(1000, create_cirs)
    
create_cirs()
# 隐藏窗口边框
root.attributes('-fullscreen', True)

#按1退出
root.bind('1', save_esc)

# 绑定鼠标事件
mouse_move=[]
mouse_check=[]
def record_mouse_position():
    global mouse_move
    x = root.winfo_pointerx()  # 获取鼠标当前的x坐标
    y = root.winfo_pointery()  # 获取鼠标当前的y坐标
    current_time = time.time()  # 获取当前时间
    #print(f"Mouse position: ({x}, {y}), time: {current_time}")
    mouse_move.append((current_time,(x,y)))
    root.after(1, record_mouse_position)  # 每隔一秒调用一次函数
    #canvas.create_oval(x,y,x+10,y+10,fill='black')

record_mouse_position()

# 进入主循环
root.mainloop()
