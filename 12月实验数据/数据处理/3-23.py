#创建同一组的z-x数据进行合并

import numpy as np
import pandas as pd
import xlwt
from matplotlib import pyplot as plt
import os, shutil
from matplotlib.font_manager import FontProperties
import os
from PyPDF2 import PdfMerger


# 加载中文字体
font = FontProperties(fname="./data/SimHei.ttf", size=14)

class DataProcessV2():
    def __init__(self, path):
        self.path = path
        # 长宽比
        self.RATE = 3072 / 312
        # 创建实验模型
        self.w = (7, 13, 25, 40)
        self.a = (70, 120, 200, 250)
        self.group = []#每一组名字的集合
        self.dir = ''
        for i in enumerate(self.w):
            for j in enumerate(self.a):
                strs = 'W=' + str(int(i[1] * self.RATE)) + ',A=' + str(int(j[1] * self.RATE))
                self.group.append(strs)

    # 创建一个读取函数
    def changedataset(self, data):
        Data = []
        data1 = []
        j = 0
        #print(data)
        for i in range(len(data)):
            if np.isnan(data[i][3]):
                data1.append((data[i][0], data[i][1], data[i][2]))
            else:
                j += 1
                Data.append(data1)
                data1 = []
        #print(Data)
        del Data[0]
        return Data

    # 由一个数据组输出其中的t,x,y数组
    def getdatasignal(self, data):
        long = len(data)
        t = []
        x = []
        y = []
        for i in range(long):
            t.append(data[i][0])
            x.append(3071 - data[i][1])
            y.append(1919 - data[i][2])
        return t, x, y

    # 创建一个由定义的函数画出轨迹图
    def plotdata1(self, data, i, dir):
        #print('轨迹图--' + self.group[i])
        plt.figure(figsize=(160, 20), dpi=160)

        for j in range(len(data)):
            #print(j)
            # 每一组中的数据
            t, x, y = self.getdatasignal(self.data[j])

            # >>>屏幕轨迹图

            plt.subplot(1, 8, j+1)
            plt.xlim(0, 3071)
            plt.ylim(0, 1919)
            plt.xlabel("x")
            plt.ylabel("y")
            plt.title('screen track')
            # plt.scatter(x, y, marker='.')
            point_numbers = list(range(len(x)))
            plt.scatter(x, y, c=point_numbers, cmap=plt.cm.Blues,
                        edgecolor='none', s=5)
            plt.legend()
        plt.draw()
        plt.savefig(dir + '\\' + '1.pdf')
        # plt.show()

    # 创建一个由定义的函数画出有向速度图
    def plotdata2(self, data, i, dir):
        def speed(t, x):
            v = []
            for i in range(len(x) - 1):
                # print(x[i])

                m = (x[i + 1] - x[i]) / (t[i + 1] - t[i]) / 100
                # print(m,np.isfinite(m))
                if not np.isfinite(m):
                    m = v[-1]
                v.append(m)

            return v
        def smooth(data, facter=0.8):
            sp = []
            for i in data:
                if sp:
                    p = sp[-1]
                    sp.append(p * facter + i * (1 - facter))
                else:
                    sp.append(i)
            return sp

        #print('有方向速度图--' + self.group[i])
        plt.figure(figsize=(160, 20), dpi=160)

        for j in range(len(data)):
            t, x, y = self.getdatasignal(self.data[j])
            v_x = speed(t, x)
            v_y = speed(t, y)
            # 总体速度
            z = []
            for i in range(len(v_x)):
                m = (v_x[i] ** 2 + v_y[i] ** 2) ** 0.5
                z.append(m)

            del t[-1]
            '''v_x = smooth(v_x)
                   v_y = smooth(v_y)
                   z = smooth(z)'''

            plt.subplot(1, 9, j+1)
            plt.xlim(np.min(t), np.max(t))
            plt.ylim(np.min((np.min(v_x), np.min(v_y))) - 10, np.max((np.max(v_x), np.max(v_y))) + 10)
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
            # print(j)
            # 每一组中的数据
            plt.legend()
        plt.draw()
        plt.savefig(dir + '\\' + '2.pdf')

    # 创建一个由定义的函数画出z-t
    def plotdata3(self, data, i, dir):
        def speed(t, x):
            v = []
            for i in range(len(x) - 1):
                # print(x[i])

                m = (x[i + 1] - x[i]) / (t[i + 1] - t[i]) / 100
                # print(m,np.isfinite(m))
                if not np.isfinite(m):
                    m = v[-1]
                v.append(m)

            return v

        def smooth(data, facter=0.8):
            sp = []
            for i in data:
                if sp:
                    p = sp[-1]
                    sp.append(p * facter + i * (1 - facter))
                else:
                    sp.append(i)
            return sp

        #print('无方向速度图--' + self.group[i])
        plt.figure(figsize=(160, 20), dpi=160)

        for j in range(len(data)):
            t, x, y = self.getdatasignal(self.data[j])
            v_x = speed(t, x)
            v_y = speed(t, y)
            # 总体速度
            z = []
            for i in range(len(v_x)):
                m = (v_x[i] ** 2 + v_y[i] ** 2) ** 0.5
                z.append(m)

            del t[-1]
            '''v_x = smooth(v_x)
                   v_y = smooth(v_y)
                   z = smooth(z)'''

            plt.subplot(1, 9, j+1)
            # >>>总体速度图，标量,
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
            plt.legend()
        plt.draw()
        plt.savefig(dir + '\\' + '3.pdf')

    # 创建一个由定义的函数画出z-x
    def plotdata4(self, data, i, dir):
        def speed(t, x):
            v = []
            for i in range(len(x) - 1):
                # print(x[i])

                m = (x[i + 1] - x[i]) / (t[i + 1] - t[i]) / 100
                # print(m,np.isfinite(m))
                if not np.isfinite(m):
                    m = v[-1]
                v.append(m)

            return v

        def smooth(data, facter=0.8):
            sp = []
            for i in data:
                if sp:
                    p = sp[-1]
                    sp.append(p * facter + i * (1 - facter))
                else:
                    sp.append(i)
            return sp

        #print('无方向速度图--' + self.group[i])
        plt.figure(figsize=(160, 20), dpi=160)

        for j in range(len(data)):
            t, x, y = self.getdatasignal(self.data[j])
            v_x = speed(t, x)
            v_y = speed(t, y)
            # 总体速度
            z = []
            for i in range(len(v_x)):
                m = (v_x[i] ** 2 + v_y[i] ** 2) ** 0.5
                z.append(m)

            del t[-1]
            '''v_x = smooth(v_x)
                   v_y = smooth(v_y)
                   z = smooth(z)'''

            plt.subplot(1, 9, j + 1)
            del x[-1]
            del y[-1]
            plt.xlim(np.min(x) - 10, np.max(x) + 10)
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
            plt.legend()
        plt.draw()
        plt.savefig(dir + '\\' + '4.pdf')


    def __call__(self):
        # 总数据中的每一组
        print(len(self.group))

        for i in range(len(self.group)):
            self.raw_data = pd.read_excel(self.path, sheet_name=self.group[i], header=0)
            self.data = self.raw_data.values
            self.data = self.changedataset(self.data)
            #每一组数据单独创建文件夹
            try:
                os.mkdir('3-23')
            except:
                pass
            self.dir = '3-23'+'\\'+str(self.group[i])
            try:
                print(self.dir)
                os.mkdir(self.dir)
            except:
                pass
            #self.plotdata1(data=self.data, i=i ,dir=self.dir)
            #self.plotdata2(data=self.data, i=i, dir=self.dir)
            self.plotdata3(data=self.data, i=i, dir=self.dir)
            self.plotdata4(data=self.data, i=i, dir=self.dir)
            #self.merge_pdf(pdf_path=self.dir,name=self.group[i])

    def merge_pdf(self,pdf_path,name):
        pdf_lst = [f for f in os.listdir(pdf_path) if f.endswith('.pdf')]
        pdf_lst = [os.path.join(pdf_path, pdf_name) for pdf_name in pdf_lst]

        pdf_merger = PdfMerger()  # 实例化

        for pdf in pdf_lst:  # 逐个读取需要合并的pdf文件
            with open(pdf, 'rb') as input:
                pdf_merger.append(input)

        with open(name+'.pdf', 'wb') as output:
            pdf_merger.write(output)  # 将多个pdf文件合并后保存为output.pdf



a = DataProcessV2('liuyu-实验数据.xls')
a()
