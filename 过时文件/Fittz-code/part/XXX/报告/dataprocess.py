import numpy as np
import pandas as pd
import xlwt
from matplotlib import pyplot as plt
import os,shutil
file_path='实验数据.xls'
file_path1='1.xls'
raw_data=pd.read_excel(file_path,header=0)
data= raw_data.values
#print(len(data))
k1=[]
k2=[]
for i in range(len(data)):
    if data[i][0]>=0:
        k1.append(data[i][0])
        k2.append(data[i][1])
raw_data = pd.read_excel(file_path1, header=0)
data = raw_data.values
for i in range(len(data)):
    if data[i][0]>=0:
        k1.append(data[i][0])
        k2.append(data[i][1])

plt.xlim(np.min(k1),np.max(k1))
plt.ylim(np.min(k2),np.max(k2))
plt.xlabel("W/D")
plt.ylabel("S/D")
plt.scatter(k1,k2,marker='.')

plt.draw()
plt.savefig('p.png')

plt.show()



