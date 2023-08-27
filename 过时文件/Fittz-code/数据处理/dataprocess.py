import numpy as np
import pandas as pd
import xlwt

file_path='数据处理_前.xls'

raw_data=pd.read_excel(file_path,header=0)

data= raw_data.values
print(len(data))
a=[]
b=[]
for i in range(len(data)):
    a.append(data[i][0])
    b.append(data[i][1])

def Eliminate_outliers(data):
    while True:
        x = np.mean(data)
        s = np.std(data)
        N = []
        # 去除异常值
        for i in range(len(data)):
            # print(i)
            if data[i] >= (x - 3 * s) and data[i] <= (x + 3 * s):
                N.append(data[i])

        if len(data) != len(N):
            data=N
        else:
            return N


a=Eliminate_outliers(a)
b=Eliminate_outliers(b)

print(a)
print(len(a))

workbook = xlwt.Workbook(encoding = 'utf-8')
worksheet = workbook.add_sheet('1')
worksheet.write(0, 0, label='a')
worksheet.write(0, 1, label='b')
for i in range(len(a)):
    worksheet.write(i + 1, 0, label=a[i])
for i in range(len(b)):
    worksheet.write(i + 1, 1, label=b[i])

workbook.save('数据处理_后.xls')
print(len(a))
print(len(b))