# 这是一个示例 Python 脚本。
import numpy as np
import pygame, sys
from pygame.locals import *
import pandas as pd
# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

def Plot(a,str):
    #排序
    for i in range(1, len(a)):
        for j in range(0, len(a) - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]

    #切分，计数
    k = (a[-1]-a[0])/1000
    M=[]
    m=0
    for i in range(1000):
        for j in range(len(a)):
            if a[j]>=(a[0]+k*i)and a[j]<=(a[0]+k*(i+1)):
                m +=1
                n = j
            l=0
        while l <int(m*1000/len(a)):
            M.append(a[n])
            l +=1
        m=0

    #画出正太分布图

    x =np.mean(M)
    s =np.std(M)
    #去除异常值
    N = []
    for i in range(len(M)):
        # print(i)
        if M[i] >= (x - 3 * s) and M[i] <= (x + 3 * s):
            N.append(M[i])
    x = np.mean(N)
    s = np.std(N)
    # 从均值为x，标准差为s的正态分布上 产生100000000个数
    x = np.random.normal(x, s, 1000)

    #print(N)
    #print(len(N))

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.set(font='SimHei', font_scale=1.0)  # 解决Seaborn中文显示问题并调整字体大小
    sns.histplot(N, bins=100,kde=True, stat='probability', color='red', label='test')
    sns.histplot(x, bins=100,kde=True, stat='probability', color='blue', label='std')
    ax.set_title('P_'+str)
    ax.legend()

    plt.savefig("D:\Desk\一元固定\一维\XXX\\"+str+".png")

    # 3.图像展示
    #plt.show()
