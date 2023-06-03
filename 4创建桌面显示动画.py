from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

import tkinter as tk
import tkinter.font as tkFont
import time
import sys
import pickle

def save_track(mouse_check_path,mouse_move_path,track_path):
    '''
    模拟轨迹
    mouse_check_path:鼠标点击的位置和时间的二进制文件
    mouse_move_path:鼠标移动的位置和时间的二进制文件
    track_path:鼠标轨迹的二进制文件
    鼠标点击和移动是列表，(t,(x,y))
    
    鼠标轨迹，是一个列表，包含每一段轨迹的列表，每一段列表由一个元组组成，
    元组的第一个元素是记录时间，第二个元素是鼠标的x坐标，第三个元素是鼠标的y坐标(t,(x,y))
    '''
    divide_index=[]#记录鼠标移动和鼠标点击的分界点
    with open(mouse_check_path,'rb') as file:
        check_datas=pickle.load(file)
    with open(mouse_move_path,'rb') as file:
        move_datas=pickle.load(file)
    print('点击点的个数为：',len(check_datas))
    for i in range(len(check_datas)):
        for j in range(len(move_datas)):
            if check_datas[i][0]<move_datas[j][0]:
                divide_index.append(j)
                break
    #得到切片的索引
    track=[]
    for i in range(0,len(divide_index)-1,2):
        track.append(move_datas[divide_index[i]:divide_index[i+1]])
    
    print('总的轨迹长度为：',len(move_datas))
    
    for i in range(len(track)):
        print(len(track[i]))
    with open(track_path, "wb") as file:
        pickle.dump(track, file)
    #print(track)
    print('轨迹保存成功')

class App:
    def __init__(self, root):
        #setting title
        self.root=root
        self.root.title("undefined")
        #setting window size
        self.width=1800
        self.height=1200
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (self.width, self.height, (screenwidth - self.width) / 2, (screenheight - self.height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        begin_game_btn=tk.Button(self.root)
        begin_game_btn["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        begin_game_btn["font"] = ft
        begin_game_btn["fg"] = "#000000"
        begin_game_btn["justify"] = "center"
        begin_game_btn["text"] = "开始游戏"
        begin_game_btn.place(x=0,y=0,width=80,height=25)
        begin_game_btn["command"] = self.begin_game

        show_trace_btn=tk.Button(self.root)
        show_trace_btn["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        show_trace_btn["font"] = ft
        show_trace_btn["fg"] = "#000000"
        show_trace_btn["justify"] = "center"
        show_trace_btn["text"] = "显示动画"
        show_trace_btn.place(x=85,y=0,width=80,height=25)
        show_trace_btn["command"] = self.show_trace
        
        # 创建画布
        self.canvas = tk.Canvas(self.root,width=self.width, height=self.height)
        # 将画布置于主窗口
        self.canvas.place(x=0, y=25)

    def begin_game(self):
        
        self.geme_window = tk.Toplevel(self.root)
        self.geme_window.focus_set()
        # 获取屏幕尺寸
        screen_width = self.geme_window.winfo_screenwidth()
        screen_height = self.geme_window.winfo_screenheight()
        
        self.inf={}
        self.inf['screen_width']=screen_width
        self.inf['screen_height']=screen_height

        D=2000
        W=100
        self.inf['D']=D
        self.inf['W']=W
        
        # 创建画布
        self.game_canvas = tk.Canvas(self.geme_window, width=screen_width, height=screen_height)
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
        
        # 保存数据并退出
        def save_esc(event):
            #保存实验的关键信息
            information_name = 'D='+str(D)+'_W='+str(W)+"_information.bin"  # 文件路径和名称
            information_path=sys.path[0]+'\data\\'+information_name
            # 打开文件，以写入模式
            with open(information_path, "wb") as file:
                pickle.dump(self.inf, file)
            
            mouse_move_name = 'D='+str(D)+'_W='+str(W)+"_mouse_move.bin"  # 文件路径和名称
            mouse_move_path=sys.path[0]+'\data\\'+mouse_move_name
            # 打开文件，以写入模式
            with open(mouse_move_path, "wb") as file:
                pickle.dump(self.mouse_move, file)
            
            mouse_check_name='D='+str(D)+'_W='+str(W)+"_mouse_check.bin"
            mouse_check_path=sys.path[0]+'\data\\'+mouse_check_name
            with open(mouse_check_path, "wb") as file:
                pickle.dump(self.mouse_check, file)
            
            track_name='D='+str(D)+'_W='+str(W)+"_track.bin"
            track_path=sys.path[0]+'\data\\'+track_name
            
            divide_index=[]#记录鼠标移动和鼠标点击的分界点
            print('点击点的个数为：',len(self.mouse_check))
            for i in range(len(self.mouse_check)):
                for j in range(len(self.mouse_move)):
                    if self.mouse_check[i][0]<self.mouse_move[j][0]:
                        divide_index.append(j)
                        break
            #得到切片的索引
            track=[]
            for i in range(0,len(divide_index)-1,2):
                track.append(self.mouse_move[divide_index[i]:divide_index[i+1]])
            
            print('总的轨迹长度为：',len(self.mouse_move))
            
            for i in range(len(track)):
                print(len(track[i]))
   
            with open(track_path, "wb") as file:
                pickle.dump(track, file)
            
            self.geme_window.destroy()
        
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
            if self.show_times==3:
                    save_esc(1)
            self.geme_window.after(1000, create_cirs)
            
        create_cirs()
        # 隐藏窗口边框
        
        #按1退出
        self.geme_window.bind('1', save_esc)

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
        screen_width=inf['screen_width']
        screen_height=inf['screen_height']
        
        k_x=self.width/screen_width
        k_y=self.height/screen_height
        
        cir1=self.canvas.create_oval(inf['cir1'][0]*k_x,inf['cir1'][1]*k_y,inf['cir1'][2]*k_x,inf['cir1'][3]*k_y,outline='red',tags='cir1')
        cir2=self.canvas.create_oval(inf['cir2'][0]*k_x,inf['cir2'][1]*k_y,inf['cir2'][2]*k_x,inf['cir2'][3]*k_y,outline='blue',tags='cir2')

        for _,point in mouse_check:
            self.canvas.create_oval(point[0]*k_x,point[1]*k_y,(point[0]+10)*k_x,(point[1]+10)*k_y,outline='black')

        self.line=0
        self.times=0
        
        def after_1s():         
            if self.line==len(track):
                self.canvas.delete('all')
            point=track[self.line][self.times][1]
            self.canvas.create_oval(point[0]*k_x,point[1]*k_y,(point[0]+10)*k_x,(point[1]+10)*k_y, fill='black',tags='point')
            self.root.after(1,after_1s)
            self.times+=1
            #print(times,len(track[line]))
            if self.times==len(track[self.line]):
                self.line+=1
                self.times=0
                self.canvas.delete('point')
        after_1s()
              
        self.root.bind('1', lambda event:self.canvas.delete('all'))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
