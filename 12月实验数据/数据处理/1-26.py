#创建的是每一个实验的各次移动，其中的轨迹以及数据的相关性图表

import numpy as np
import pandas as pd
import xlwt
from matplotlib import pyplot as plt
import os,shutil

class DataProcessV1():
    def __init__(self, path):
        self.path=path
        # 长宽比
        self.RATE = 3072 / 312
        # 创建实验模型
        self.w = (7, 13, 25, 40)
        self.a = (70, 120, 200, 250)
        self.group = []
        self.strs=''
        for i in enumerate(self.w):
            for j in enumerate(self.a):
                self.strs = 'W=' + str(int(i[1] * self.RATE)) + ',A=' + str(int(j[1] * self.RATE))
                self.group.append(self.strs)

    #创建一个读取函数
    def changedataset(self,data):
        Data = []
        data1 = []
        j = 0
        print(data)
        for i in range(len(data)):
            if np.isnan(data[i][3]):
                data1.append((data[i][0], data[i][1], data[i][2]))
            else:
                j += 1
                Data.append(data1)
                data1 = []
        print(Data)
        return Data

    #由一个数据组输出其中的t,x,y数组
    def getdatasignal(self,data):
        long=len(data)
        t=[]
        x=[]
        y=[]
        for i in range(long):
            t.append(data[i][0])
            x.append(3071-data[i][1])
            y.append(1919-data[i][2])
        return t,x,y

    #创建一个由定义的函数画出轨迹图
    def plotdata(self,t,x,y,I,J):
        #>>>屏幕轨迹图
        plt.figure(figsize=(15,20), dpi=160)
        plt.subplot(3, 2, 1)
        plt.xlim(0, 3071)
        plt.ylim(0, 1919)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title('screen track')
        #plt.scatter(x, y, marker='.')
        point_numbers = list(range(len(x)))
        plt.scatter(x,y, c=point_numbers, cmap=plt.cm.Blues,
                    edgecolor='none', s=5)
        #>>>时间速度图
        #>>>>>有向xy图
        # 求速度大小
        def speed(t, x):
            v = []
            for i in range(len(x) - 1):
                # print(x[i])

                m = (x[i + 1] - x[i]) / (t[i + 1] - t[i]) /100
                #print(m,np.isfinite(m))
                if not np.isfinite(m):
                    m=v[-1]
                v.append(m)

            return v

        v_x = speed(t, x)
        v_y = speed(t, y)
        # 总体速度
        z = []
        for i in range(len(v_x)):
            m = (v_x[i] ** 2 + v_y[i] ** 2) ** 0.5
            z.append(m)

        del t[-1]

        def smooth(data, facter=0.8):
            sp = []
            for i in data:
                if sp:
                    p = sp[-1]
                    sp.append(p * facter + i * (1 - facter))
                else:
                    sp.append(i)
            return sp

        '''v_x = smooth(v_x)
        v_y = smooth(v_y)
        z = smooth(z)'''

        plt.legend()
        plt.subplot(3, 2, 2)
        plt.xlim(np.min(t), np.max(t))
        plt.ylim(np.min((np.min(v_x),np.min(v_y)))-10, np.max((np.max(v_x),np.max(v_y)))+10)
        plt.xlabel("t")
        plt.ylabel("x_y")
        plt.title('speed_x-speed_y-t')
        # plt.scatter(x, y, marker='.')
        point_numbers = list(range(len(v_x)))
        plt.scatter(t, v_x, c=point_numbers, cmap=plt.cm.Reds,
                    edgecolor='none', s=5)

        plt.plot(t, v_x, c='r', linestyle='-', linewidth=1,
                 marker='>', markersize=8, fillstyle='left',
                 markerfacecolor='y', markeredgecolor='m', )

        plt.scatter(t, v_y, c=point_numbers, cmap=plt.cm.Greens,
                    edgecolor='none', s=5)

        plt.plot(t, v_y, c='b', linestyle='-', linewidth=1,
                 marker='>', markersize=8, fillstyle='left',
                 markerfacecolor='y', markeredgecolor='m', )
        # >>>总体速度图，标量,
        plt.legend()
        plt.subplot(3, 2, 3)
        plt.xlim(np.min(t), np.max(t))
        plt.ylim(np.min(z) - 10, np.max(z) + 10)
        plt.xlabel("t")
        plt.ylabel("z")
        plt.title('speed_z-t')
        # plt.scatter(x, y, marker='.')
        point_numbers = list(range(len(z)))
        plt.scatter(t, z, c=point_numbers, cmap=plt.cm.Reds,
                    edgecolor='none', s=5)

        plt.plot(t, z, c='r', linestyle='-', linewidth=1,
                 marker='>', markersize=8, fillstyle='left',
                 markerfacecolor='y', markeredgecolor='m', )
        # >>>总体速度图，标量,
        plt.legend()
        plt.subplot(3, 2, 4)
        del x[-1]
        del y[-1]
        plt.xlim(np.min(x)-10, np.max(x)+10)
        plt.ylim(np.min(z) - 10, np.max(z) + 10)
        plt.xlabel("x")
        plt.ylabel("z")
        plt.title('speed_z-x')
        # plt.scatter(x, y, marker='.')
        point_numbers = list(range(len(z)))
        plt.scatter(x, z, c=point_numbers, cmap=plt.cm.Reds,
                    edgecolor='none', s=5)

        plt.plot(x, z, c='r', linestyle='-', linewidth=1,
                 marker='>', markersize=8, fillstyle='left',
                 markerfacecolor='y', markeredgecolor='m', )

        # >>>总体速度图，标量
        plt.legend()
        plt.subplot(3, 2, 5)
        plt.xlim(np.min(y) - 10, np.max(y) + 10)
        plt.ylim(np.min(z) - 10, np.max(z) + 10)
        plt.xlabel("y")
        plt.ylabel("z")
        plt.title('speed_z-y')
        # plt.scatter(x, y, marker='.')
        point_numbers = list(range(len(z)))
        plt.scatter(y, z, c=point_numbers, cmap=plt.cm.Reds,
                    edgecolor='none', s=5)

        plt.plot(y, z, c='r', linestyle='-', linewidth=1,
                 marker='>', markersize=8, fillstyle='left',
                 markerfacecolor='y', markeredgecolor='m', )

        # >>>总体速度图，标量
        plt.legend()
        plt.subplot(3, 2, 6)
        plt.xlim(np.min(v_x) - 1, np.max(v_x) + 1)
        plt.ylim(np.min(v_y) - 1, np.max(v_y) + 1)
        plt.xlabel("v_x")
        plt.ylabel("v_y")
        plt.title('speed_x-speed_y')
        # plt.scatter(x, y, marker='.')
        point_numbers = list(range(len(v_x)))
        plt.scatter(v_x, v_y, c=point_numbers, cmap=plt.cm.Reds,
                    edgecolor='none', s=5)

        '''plt.plot(v_x, v_y, c='r', linestyle='-', linewidth=1,
                 marker='>', markersize=8, fillstyle='left',
                 markerfacecolor='y', markeredgecolor='m', )'''
        plt.draw()
        self.dir =str( self.group[I])
        try:
            os.mkdir(self.dir)
        except:
            pass
        if J!=0:
            plt.savefig(self.dir+'\\'+str(J)+'.png')
        else:
            pass
        #plt.show()

    def __call__(self):
        #总数据中的每一组
        print(len(self.group))
        for i in range(len(self.group)):
            self.raw_data = pd.read_excel(self.path, sheet_name=self.group[i], header=0)
            self.data = self.raw_data.values
            self.data = self.changedataset(self.data)
            for j in range(len(self.data)):
                #每一组中的数据
                self.t, self.x, self.y = self.getdatasignal(self.data[j])
                print(self.group[i]+' '+str(i)+' - '+str(j))
                self.plotdata(self.t,self.x,self.y,i,j)

a=DataProcessV1('liuyu-实验数据.xls')
a()
