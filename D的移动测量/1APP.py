from ctypes import windll
#from sympy.physics.units.definitions.unit_definitions import ms
windll.shcore.SetProcessDpiAwareness(1)

from tkinter import *
import tkinter.font as tkFont
import time
import sys
import pickle
from tkinter import messagebox
import tkinter.ttk as ttk
import pandas as pd
import threading
import win32api
import pyautogui
import random
import os

class MouseTracker:
    def __init__(self, canvas):
        self.canvas = canvas
        self.thread = None
        self.is_tracking = False
        self.track=[]
        #真实的高采样频率的点击数据

    def start_tracking(self):
        self.track=[]
        self.is_tracking = True
        self.thread = threading.Thread(target=self.track_mouse)
        self.thread.start()

    def stop_tracking(self):
        self.is_tracking = False
        #print(len(self.track))
        #print('t3:',time.time())

    def track_mouse(self):
        while self.is_tracking:
            x1, y1 = pyautogui.position()
            x2, y2 = win32api.GetCursorPos()
            
            #x4, y4 = pyautogui.position()
            #x3, y3 = win32api.GetCursorPos()
            #print(f"Mouse position: ({x}, {y})")
            self.track.append((time.time(),(x1+x2)/2,(y1+y2)/2))
    
    def get_track(self):
        return self.track


class App:

    #todo->    
    def __init__(self, root):
        folder_path=sys.path[0]+'\data'
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
            print(f"Folder '{folder_path}' created successfully.")
            
        #setting title
        self.root=root
        self.root.title("8-1")
        #setting window size
        self.width=1200
        self.height=400
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (self.width, self.height, (screenwidth - self.width) / 2, (screenheight - self.height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=True, height=False)
        
        #添加菜单栏目
        menubar=Menu(root,font=("Microsoft YaHei",12,"normal"))
        filemenu=Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=filemenu)#添加子菜单

        filemenu.add_command(label="New", command=self.newfile)
        filemenu.add_command(label="Open", command=self.openfile)
        filemenu.add_separator()#添加分割线
        filemenu.add_command(label="Save", command=self.savefile)
        filemenu.add_command(label="Save As", command=self.saveasfile)
        filemenu.add_separator()#添加分割线
        filemenu.add_command(label='exit', command=self.root.destroy)

        helpmenu=Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=helpmenu)#添加子菜单
        helpmenu.add_command(label="About", command=self.about)

        self.root.config(menu=menubar)#显示菜单

        #创建工具栏
        toolbar=Frame(self.root,relief=RAISED,borderwidth=1)
        toolbar.pack(side=TOP,fill=X,padx=5,pady=5)
        
        ft = tkFont.Font(family='Times',size=10)
        
        d1_label=Label(toolbar,bg="#f0f0f0",font=ft,fg="#000000",justify="center",text="D min ：")
        d1_label.pack(pady=5,side=LEFT)
        
        self.d1=StringVar()#d1,最小的D
        d1_cb=ttk.Combobox(toolbar,textvariable=self.d1,font=ft,width=4)
        d1_cb['value']=(3000,2500,2000,1500,1000,500,250,125)
        d1_cb.current(1)#设置默认值
        d1_cb.pack(pady=5,side=LEFT)
        
        d2_label=Label(toolbar,bg="#f0f0f0",font=ft,fg="#000000",justify="center",text="D max ：")
        d2_label.pack(pady=5,side=LEFT)
        
        self.d2=StringVar()#宽度
        d2_cb=ttk.Combobox(toolbar,textvariable=self.d2,font=ft,width=4)
        d2_cb['value']=(3000,2500,2000,1500,1000,500,250,125)
        d2_cb.current(1)#设置默认值
        d2_cb.pack(pady=5,side=LEFT)
        
        w1_label=Label(toolbar,bg="#f0f0f0",font=ft,fg="#000000",justify="center",text="W min ：")
        w1_label.pack(pady=5,side=LEFT)
        
        self.w1=StringVar()#直径
        w1_cb=ttk.Combobox(toolbar,textvariable=self.w1,font=ft,width=4)
        w1_cb['value']=(20,30,40,50,60,70,80)
        w1_cb.current(2)#设置默认值
        w1_cb.pack(pady=5,side=LEFT)
        
        w2_label=Label(toolbar,bg="#f0f0f0",font=ft,fg="#000000",justify="center",text="W max ：")
        w2_label.pack(pady=5,side=LEFT)
        
        self.w2=StringVar()#次数
        w2_cb=ttk.Combobox(toolbar,textvariable=self.w2,font=ft,width=4)
        w2_cb['value']=(20,30,40,50,60,70,80)
        w2_cb.current(2)#设置默认值
        w2_cb.pack(pady=5,side=LEFT)
        
        
        #添加空白标签,使得按钮居中
        spare_label=Label(toolbar,bg="#f0f0f0",font=ft,fg="#000000",justify="center",text="    ")
        spare_label.pack(pady=5,side=LEFT)
        
        begin_game_btn=Button(toolbar,bg="#f0f0f0",font=ft,fg="#000000",justify="center",text="开始游戏",command=self.begin_game)    
        begin_game_btn.pack(pady=5,side=LEFT)
        
        #创建底部栏,用于显示一些标签信息
        button_frame=Frame(self.root,relief=RAISED,borderwidth=1)
        button_frame.pack(side=BOTTOM,fill=BOTH,padx=5,pady=5)
        
        ft = tkFont.Font(family='Times',size=10)
        
        
        d1_label=Label(button_frame,bg="#f0f0f0",font=ft,fg="#000000",justify="center",text="在这里可以显示状态信息")
        d1_label.pack(pady=5,side=LEFT)
        
        
        notebook=ttk.Notebook(self.root)
        notebook.pack(fill=BOTH,expand=YES,padx=5,pady=0)
        # 创建画布
        canvas_frame1=Frame()
        self.canvas_1 = Canvas(canvas_frame1,width=self.width, height=self.height,bg='white')
        # 将画布置于主窗口
        self.canvas_1.configure(cursor="crosshair")
        self.canvas_1.pack(pady=5,side=LEFT,fill=BOTH,expand=YES)
        
        notebook.add(canvas_frame1,text='blank')
        
        notebook.add(Frame(),text='blank')
        
    #todo->      
    def newfile(self):
        messagebox.showinfo("New File", "New File")
    def openfile(self):
        messagebox.showinfo("Open File", "Open File")
    def savefile(self):
        messagebox.showinfo("Save File", "Save File")
    def saveasfile(self):
        messagebox.showinfo("Save As File", "Save As File") 
    def about(self):
        messagebox.showinfo("About", "构建菲兹定律的GUI界面")
 
    def begin_game(self):
        """
            开始游戏,初始化游戏界面，并进行保存数据。
        """
        # 保存数据并退出
        def clean(mouse_move):
            new1=[]
            for i in range(len(mouse_move)):
                new2=[]
                t=-1
                x=-1
                y=-1
                for j in range(len(mouse_move[i])):
                    
                    if t==mouse_move[i][j][0] and x==mouse_move[i][j][1] and y==mouse_move[i][j][2]:
                        t=mouse_move[i][j][0]
                        x=mouse_move[i][j][1]
                        y=mouse_move[i][j][2]
                        continue
                    else:
                        t=mouse_move[i][j][0]
                        x=mouse_move[i][j][1]
                        y=mouse_move[i][j][2]
                        new2.append(mouse_move[i][j])
                new1.append(new2)
            return new1
        
        def save_esc():
            #todo 保存数据的名字要改为方便的名字
            mouse_move_name = 'D='+str(self.d1.get())+'-'+str(self.d2.get())+'_W='+str(self.w1.get())+'-'+str(self.w2.get())+".bin"  # 文件路径和名称
            mouse_move_path=sys.path[0]+'\data\\'+mouse_move_name
            # 打开文件，以写入模式
            self.mouse_move =clean(self.mouse_move)
            with open(mouse_move_path, "wb") as file:
                pickle.dump(self.mouse_move, file)
            
            messagebox.showinfo("Save File", "保存路径为"+mouse_move_path)
              
        self.game_window = Toplevel(self.root)
        self.game_window.focus_set()
        # 获取屏幕尺寸
        screen_width = self.game_window.winfo_screenwidth()
        screen_height = self.game_window.winfo_screenheight()
        # 创建画布
        self.game_canvas = Canvas(self.game_window, width=screen_width, height=screen_height)
        # 将画布置于主窗口
        self.game_canvas.pack()
        self.game_window.attributes('-fullscreen', True)
        self.game_canvas.configure(cursor="crosshair")
        
        
        self.check=0#记录目标点是否已经出现，如果为0，说明要重新生成目标点
        
        tracker1 = MouseTracker(self.game_canvas)
        
        self.mouse_move=[]
        
        #删除被点击的控件
        def get_check(event):
            global T
            if tracker1.is_tracking:
                self.mouse_move.append(tracker1.get_track())
                tracker1.stop_tracking()
                print('t2:',time.time())
                print('time:',time.time()-T)
                self.check=0
            else:
                tracker1.start_tracking()
                print('t1:',time.time())
                T=time.time()
                self.check=1
        
        self.game_canvas.bind('<Button-1>', get_check)
        
        def create_cirs():
            if self.check==0:

                cir1=self.game_canvas.create_oval(screen_width/2-20,screen_height/2-20,screen_width/2+20,screen_height/2+20,fill='black',tags='cir1')
                #cir2=self.game_canvas.create_oval(200,200,400,400,fill='black',tags='cir2')
            
            else:
                self.game_canvas.delete('cir1')
                #self.game_canvas.delete('cir2')
        
            
            self.game_window.after(1, create_cirs)
            
        create_cirs()
        
        def exit_game(event):
            save_esc()
            self.game_window.destroy()
            return
        
        #按1退出
        self.game_window.bind('1', exit_game)


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
