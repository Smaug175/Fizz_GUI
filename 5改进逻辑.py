from ctypes import windll
from sympy.physics.units.definitions.unit_definitions import ms
windll.shcore.SetProcessDpiAwareness(1)

from tkinter import *
import tkinter.font as tkFont
import time
import sys
import pickle
from tkinter import messagebox
import tkinter.ttk as ttk


class App:
    def read_data(self,D,W):
        '''
        通过D,和W的大小来区分和读取数据，，并返回四个数据结果。
        '''
        name=sys.path[0]+'\data\\'+'D='+str(D)+'_W='+str(W)
        
        with open(name+'_mouse_check.bin','rb') as file:
            check_datas=pickle.load(file)
        with open(name+'_mouse_move.bin','rb') as file:
            move_datas=pickle.load(file)
        with open(name+'_track.bin','rb') as file:
            track_datas=pickle.load(file)
        with open(name+'_information.bin','rb') as file:
            inf=pickle.load(file)
        
        return move_datas,check_datas,track_datas,inf
    
    
    
    def __init__(self, root):
        #setting title
        self.root=root
        self.root.title("undefined")
        #setting window size
        self.width=1600
        self.height=1200
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (self.width, self.height, (screenwidth - self.width) / 2, (screenheight - self.height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)
        
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
        
        id_label=Label(toolbar,bg="#f0f0f0",font=ft,fg="#000000",justify="center",text="ID：")
        id_label.pack(pady=5,side=LEFT)
        
        self.ID=StringVar()#难度系数，设置全局的变量
        ID_cb=ttk.Combobox(toolbar,textvariable=self.ID,font=ft,width=2)
        ID_cb['value']=(2,3,4,5,6,7,8)
        ID_cb.current(2)#设置默认值
        ID_cb.bind("<<ComboboxSelected>>",lambda event:self.W.set(int(int(self.D.get())*2/(2**int(self.ID.get())))))
        ID_cb.pack(pady=5,side=LEFT)
        
        D_label=Label(toolbar,bg="#f0f0f0",font=ft,fg="#000000",justify="center",text="D：")
        D_label.pack(pady=5,side=LEFT)
        
        self.D=StringVar()#宽度
        D_cb=ttk.Combobox(toolbar,textvariable=self.D,font=ft,width=4)
        list_D=[]
        for i in range(100,screenwidth,100):
            list_D.append(i)
        D_cb['value']=list_D
        D_cb.current(15)#设置默认值
        D_cb.bind("<<ComboboxSelected>>",lambda event:self.W.set(int(int(self.D.get())*2/(2**int(self.ID.get())))))
        D_cb.pack(pady=5,side=LEFT)
        
        W_label=Label(toolbar,bg="#f0f0f0",font=ft,fg="#000000",justify="center",text="W：")
        W_label.pack(pady=5,side=LEFT)
        
        self.W=StringVar()#直径
        W_cb=ttk.Combobox(toolbar,textvariable=self.W,font=ft,width=4)
        list_W=[]
        for i in range(0,screenwidth,1):
            list_W.append(i)
        W_cb['value']=list_W
        W_cb.current(200)#设置默认值
        W_cb.bind("<<ComboboxSelected>>",lambda event:self.D.set(int(self.W.get())*2**(int(self.ID.get())-1)))
        W_cb.pack(pady=5,side=LEFT)
        
        #添加空白标签,使得按钮居中
        spare_label=Label(toolbar,bg="#f0f0f0",font=ft,fg="#000000",justify="center",text="    ")
        spare_label.pack(pady=5,side=LEFT)
        
        #根据设计的初始值加载数据
        #将要保存的四个数据结构初始化为0，以便后续进行读取和处理
        self.mouse_move,self.mouse_check,self.track,self.inf=self.read_data(self.D.get(),self.W.get())
        
        
        begin_game_btn=Button(toolbar,bg="#f0f0f0",font=ft,fg="#000000",justify="center",text="开始游戏",command=self.begin_game)    
        begin_game_btn.pack(pady=5,side=LEFT)
        show_trace_btn=Button(toolbar,bg="#f0f0f0",font=ft,fg="#000000",justify="center",text="显示动画",command=self.show_trace)
        show_trace_btn["bg"] = "#f0f0f0"
        show_trace_btn.pack(pady=5,side=LEFT)
        
        #创建底部栏,用于显示一些标签信息
        button_frame=Frame(self.root,relief=RAISED,borderwidth=1)
        button_frame.pack(side=BOTTOM,fill=BOTH,padx=5,pady=5)
        
        ft = tkFont.Font(family='Times',size=10)
        
        
        id_label=Label(button_frame,bg="#f0f0f0",font=ft,fg="#000000",justify="center",text="在这里可以显示状态信息")
        id_label.pack(pady=5,side=LEFT)
        
        
        notebook=ttk.Notebook(self.root)
        notebook.pack(fill=BOTH,expand=YES,padx=5,pady=0)
        # 创建画布
        canvas_frame1=Frame()
        self.canvas = Canvas(canvas_frame1,width=self.width, height=self.height,bg='white')
        # 将画布置于主窗口
        self.canvas.pack(pady=5,side=LEFT,fill=BOTH,expand=YES)
        
        notebook.add(canvas_frame1,text='轨迹动画')
        
        notebook.add(Frame(),text='轨迹分析')
        
        
        
        
        
        
        
        
        
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
        def save_esc():
            #保存实验的关键信息
            information_name = 'D='+str(self.inf['D'])+'_W='+str(self.inf['W'])+"_information.bin"  # 文件路径和名称
            information_path=sys.path[0]+'\data\\'+information_name
            # 打开文件，以写入模式
            with open(information_path, "wb") as file:
                pickle.dump(self.inf, file)
            
            mouse_move_name = 'D='+str(self.inf['D'])+'_W='+str(self.inf['W'])+"_mouse_move.bin"  # 文件路径和名称
            mouse_move_path=sys.path[0]+'\data\\'+mouse_move_name
            # 打开文件，以写入模式
            with open(mouse_move_path, "wb") as file:
                pickle.dump(self.mouse_move, file)
            
            mouse_check_name='D='+str(self.inf['D'])+'_W='+str(self.inf['W'])+"_mouse_check.bin"
            mouse_check_path=sys.path[0]+'\data\\'+mouse_check_name
            with open(mouse_check_path, "wb") as file:
                pickle.dump(self.mouse_check, file)
            
            track_name='D='+str(self.inf['D'])+'_W='+str(self.inf['W'])+"_track.bin"
            track_path=sys.path[0]+'\data\\'+track_name
            
            divide_index=[]#记录鼠标移动和鼠标点击的分界点
            print('点击点的个数为：',len(self.mouse_check))
            for i in range(len(self.mouse_check)):
                for j in range(len(self.mouse_move)):
                    if self.mouse_check[i][0]<self.mouse_move[j][0]:
                        divide_index.append(j)
                        break
            #得到切片的索引
            self.track=[]
            for i in range(0,len(divide_index)-1,2):
                self.track.append(self.mouse_move[divide_index[i]:divide_index[i+1]])
            
            print('总的轨迹长度为：',len(self.mouse_move))
            
            for i in range(len(self.track)):
                print(len(self.track[i]))

            with open(track_path, "wb") as file:
                pickle.dump(self.track, file)
            
            messagebox.showinfo("Save File", "数据保存成功")
              
        self.geme_window = Toplevel(self.root)
        self.geme_window.focus_set()
        # 获取屏幕尺寸
        screen_width = self.geme_window.winfo_screenwidth()
        screen_height = self.geme_window.winfo_screenheight()
        
        self.inf={}
        self.inf['screen_width']=screen_width
        self.inf['screen_height']=screen_height

        D=int(self.D.get())
        W=int(self.W.get())
        self.inf['D']=D
        self.inf['W']=W
        
        # 创建画布
        self.game_canvas = Canvas(self.geme_window, width=screen_width, height=screen_height)
        # 将画布置于主窗口
        self.game_canvas.pack()
        self.geme_window.attributes('-fullscreen', True)
        
        
        #绘制目标点
        x1=(screen_width-D-W)/2
        x2=(screen_width+D-W)/2
        y1=(screen_height-W)/2
        y2=(screen_height-W)/2
        self.cir=0#记录目标点是否已经出现，如果为0，说明要重新生成目标点
        self.show_times=-1#记录目标点出现的次数，如果为3，说明测试结束
        
        
        #删除被点击的控件
        def delete_widget(event):
            item_id = self.game_canvas.find_closest(event.x, event.y)[0]  # 获取与鼠标事件位置最接近的项的ID
            self.cir-=1
            self.game_canvas.delete(item_id)  # 删除该项
            self.mouse_check.append((time.time(),(event.x,event.y)))#只记录点击到的点的位置和时间
        
        
        def create_cirs():
            if self.cir==0:
                cir1=self.game_canvas.create_oval(x1,y1,x1+W,y1+W,fill='red',tags='cir1')
                cir2=self.game_canvas.create_oval(x2,y2,x2+W,y2+W,fill='blue',tags='cir2')
                self.inf['cir1']=(x1,y1,x1+W,y1+W)
                self.inf['cir2']=(x2,y2,x2+W,y2+W)
                self.game_canvas.tag_bind(cir1, '<Button-1>', delete_widget)
                self.game_canvas.tag_bind(cir2, '<Button-1>', delete_widget)
                self.cir+=2
                self.show_times+=1
                
            else:
                pass
            #是否结束测试
            if self.show_times==2:
                    save_esc()
                    self.geme_window.destroy()
                    return
            self.geme_window.after(1000, create_cirs)
            
        create_cirs()
       
        def exit_game(event):
            save_esc()
            self.geme_window.destroy()
            return
        
        #按1退出
        self.geme_window.bind('1', exit_game)

        # 绑定鼠标事件
        self.mouse_move=[]
        self.mouse_check=[]
        def record_mouse_position():
            x = self.geme_window.winfo_pointerx()  # 获取鼠标当前的x坐标
            y = self.geme_window.winfo_pointery()  # 获取鼠标当前的y坐标
            current_time = time.time()  # 获取当前时间
            #print(f"Mouse position: ({x}, {y}), time: {current_time}")
            self.mouse_move.append((current_time,(x,y)))
            self.geme_window.after(1, record_mouse_position)  # 每隔一秒调用一次函数
            #canvas.create_oval(x,y,x+10,y+10,fill='black')

        record_mouse_position()

    def show_trace(self):
        self.canvas.delete('all')
        try:
            self.mouse_move,self.mouse_check,self.track,self.inf=self.read_data(self.D.get(),self.W.get())
        except:
            messagebox.showerror(title='错误',message='没有找到数据')
            return None
        
        inf=self.inf

        track=self.track

        mouse_check=self.mouse_check
    
        D=inf['D']
        W=inf['W']
        screen_width=inf['screen_width']
        screen_height=inf['screen_height']
        
        k_x=self.canvas.winfo_width()/screen_width
        k_y=self.canvas.winfo_height()/screen_height
        
        cir1=self.canvas.create_oval(inf['cir1'][0]*k_x,inf['cir1'][1]*k_y,inf['cir1'][2]*k_x,inf['cir1'][3]*k_y,outline='red',tags='cir1')
        cir2=self.canvas.create_oval(inf['cir2'][0]*k_x,inf['cir2'][1]*k_y,inf['cir2'][2]*k_x,inf['cir2'][3]*k_y,outline='blue',tags='cir2')

        for _,point in mouse_check:
            self.canvas.create_oval(point[0]*k_x,point[1]*k_y,(point[0]+10)*k_x,(point[1]+10)*k_y,outline='black')

        self.line=0
        self.times=0
        colors=('blue','red','green','yellow','black','gray','pink','purple','orange','brown','cyan','magenta','tan','olive','maroon','navy','aquamarine','turquoise','silver','lime','teal','indigo','violet','pink','wheat','thistle','plum','orchid','moccasin','mistyrose','linen','lavender','ivory','honeydew','hotpink','gold','ghostwhite','gainsboro','floralwhite','firebrick','darkviolet','darkturquoise','darkslategray','darkslateblue','darkseagreen','darkred','darkorchid','darkorange','darkolivegreen','darkmagenta','darkkhaki','darkgreen','darkgray','darkgoldenrod','darkcyan','darkblue','crimson','cornsilk','chocolate','chartreuse','burlywood','blueviolet','blanchedalmond','bisque','beige','azure','antiquewhite','aliceblue')
        def after_1s():         
            if self.line==len(track):
                #self.canvas.delete('all')
                self.line=0
                return 
            point=track[self.line][self.times][1]
            self.canvas.create_oval(point[0]*k_x,point[1]*k_y,(point[0]+5)*k_x,(point[1]+5)*k_y, fill=colors[self.line],tags='point',)
            self.root.after(1,after_1s)
            self.times+=1
            #print(times,len(track[line]))
            if self.times==len(track[self.line]):
                self.line+=1
                self.times=0
                #self.canvas.delete('point')
        after_1s()
              
        self.root.bind('1', lambda event:self.canvas.delete('all'))

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
