import numpy as np
import pandas as pd
import xlwt
from matplotlib import pyplot as plt
import os,shutil


def draw(name,file_path,I,R):

    raw_data=pd.read_excel(file_path,sheet_name=name,header=0)

    data= raw_data.values
    #print(len(data))
    t=[]
    x=[]
    y=[]
    for i in range(len(data)):
        if data[i][0]>=0:
            t.append(data[i][0]-1)
            x.append(data[i][1])
            y.append(data[i][2])
    #print(t)
    #求速度大小
    def Eliminate_outliers(t,x):
        v=[]
        for i in range(len(x)-1):
            #print(x[i])

            m = (x[i + 1] - x[i]) / (t[i + 1] - t[i]) / 100

            v.append(m)
        return v

    v_x=Eliminate_outliers(t,x)
    v_y=Eliminate_outliers(t,y)
    #总体速度
    z=[]
    for i in range (len(v_x)):
        if v_x[i]>=0:
            m=(v_x[i]**2+v_y[i]**2)**0.5
        else:
            m = (v_x[i] ** 2 + v_y[i] ** 2) ** 0.5*(-1)
        z.append(m)
    del t[-1]

    def smooth(data,facter=0.8):
        sp=[]
        for i in data:
            if sp:
                p=sp[-1]
                sp.append(p*facter+i*(1-facter))
            else:
                sp.append(i)
        return sp

    v_x=smooth(v_x)
    v_y=smooth(v_y)
    z=smooth(z)
    try:
        dir='D:\Desk\一元固定\一维\XXX\img\\'+'R='+str(R)
        os.mkdir(dir)
    except:
        pass
    '''
    plt.xlim(t[0], t[-1])
    plt.ylim(np.min(v_x),np.max(v_x))
    plt.xlabel("t")
    plt.ylabel("vx")
    plt.title("the mouse log")
    plt.scatter(t,v_x) # 轨迹图
    #plt.scatter(xs, ys)  # 散点图
    #plt.hist(xs)
    plt.figure()
    
    plt.xlim(t[0], t[-1])
    plt.ylim(np.min(v_y),np.max(v_y))
    plt.xlabel("t")
    plt.ylabel("vy")
    plt.title("the mouse log")
    plt.scatter(t,v_y) # 轨迹图
    #plt.scatter(xs, ys)  # 散点图
    #plt.hist(xs)
    plt.figure()
    '''
    plt.xlim(t[0], t[-1])
    plt.ylim(np.min(z),np.max(z))
    plt.xlabel("t")
    plt.ylabel("vz")
    plt.title(name)
    plt.scatter(t,z,marker='.')
    #plt.scatter(xs, ys)  # 散点图
    #plt.hist(xs)
    plt.draw()
    plt.savefig('./img/'+'R='+str(R)+'/pic'+str(R)+'-{}.png'.format(I + 1))

    plt.show()


def plot(N,file_path,R):
    for i in range(N):
        name='轨迹数据'+str(i)
        draw(name,file_path,i,R)

