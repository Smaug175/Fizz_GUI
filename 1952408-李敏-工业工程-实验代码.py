# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 13:02:02 2023

@author: 22064
"""


###小球以一定速度朝着定点运动
###//////////////////////////////////////////////////////////////////////////////////////////
import pygame
import math
import random
import csv
import time

# 初始化 Pygame
pygame.init()

# 创建屏幕
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("小球运动")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 定义常量
FPS = 60
center_radius=10

SPEED = 3#速度为0、1、3
ball_radius=30 #半径为10、30
Distance=400  #距离为250、400

i=1
MAX_RUNTIME = 60  # 程序最长运行时间，单位秒
# 定义初始位置
center_x = screen_width // 2 
center_y = screen_height // 2
ball_x = center_x + Distance
ball_y = center_y

# 定义初始状态
moving = False

# 定义初始时间和距离
start_time = None
distance = None

header=('number','time','distance','ball_radius','speed','distance_after_moving')
with open('8data_kaojin.csv', mode='a',newline='') as data_file:
    data_writer = csv.writer(data_file)
    data_writer.writerow(header)

# 渲染动画
clock = pygame.time.Clock()
start = time.time()  # 记录程序启动时间
while True:
    # 判断程序运行时间是否超过最长运行时间
    if time.time() - start >= MAX_RUNTIME:
        pygame.quit()
        quit()
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2) < center_radius:
                moving = True
                start_time = time.time()
                distance = math.sqrt((ball_x - center_x) ** 2 + (ball_y - center_y) ** 2)
            elif math.sqrt((x - ball_x) ** 2 + (y - ball_y) ** 2) <= ball_radius:
                moving = False
                end_time = time.time()
                time_diff = round(end_time - start_time, 3)
                distance_after_moving = math.sqrt((ball_x - center_x) ** 2 + (ball_y - center_y) ** 2)
                with open('8data_kaojin.csv', mode='a', newline='') as data_file:
                    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    data_writer.writerow([i,time_diff, distance, ball_radius,SPEED,distance_after_moving])
                ball_x = center_x + Distance
                ball_y = center_y
                i=i+1

    # 计算小球位置
    if moving:
        vector_x = center_x - ball_x
        vector_y = center_y - ball_y
        vector_length = math.sqrt(vector_x ** 2 + vector_y ** 2)
        unit_vector_x = vector_x / vector_length
        unit_vector_y = vector_y / vector_length
        ball_x += int(SPEED * unit_vector_x)
        ball_y += int(SPEED * unit_vector_y)
        
        # 如果小球到达中心，则重新生成小球位置
        if math.sqrt((ball_x - center_x) ** 2 + (ball_y - center_y) ** 2) <= ball_radius + center_radius:
            moving=False
            ball_x = center_x + Distance
            ball_y = center_y
    # 绘制图形
    screen.fill(WHITE)
    pygame.draw.circle(screen, BLACK, (center_x, center_y), center_radius)
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)
    pygame.display.update()

    # 控制帧率
    clock.tick(FPS)


'''
###小球以一定速度远离定点运动
###/////////////////////////////////////////////////////////////////////////////////////////
import pygame
import math
import random
import csv
import time

# 初始化 Pygame
pygame.init()

# 创建屏幕
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("小球运动")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 定义常量
FPS = 60
center_radius=10

SPEED = 3 #速度为0、1、3
ball_radius=30 #半径为10、30
Distance=400  #距离为250、400

MAX_RUNTIME = 60  # 程序最长运行时间，单位秒
i=1

# 定义初始位置
center_x = screen_width // 2 
center_y = screen_height // 2
ball_x = center_x + Distance
ball_y = center_y

# 定义初始状态
moving = False

# 定义初始时间和距离
start_time = None
distance = None

header = ('number','time', 'distance', 'ball_radius', 'speed', 'distance_after_moving')

with open('1-data_yuanli.csv', mode='a', newline='') as data_file:
    data_writer = csv.writer(data_file)
    data_writer.writerow(header)

# 渲染动画
clock = pygame.time.Clock()
start = time.time()  # 记录程序启动时间
while True:
    # 判断程序运行时间是否超过最长运行时间
    if time.time() - start >= MAX_RUNTIME:
        pygame.quit()
        quit()
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2) < center_radius and not moving:
                moving = True
                start_time = time.time()
                distance = math.sqrt((ball_x - center_x) ** 2 + (ball_y - center_y) ** 2)
            elif math.sqrt((x - ball_x) ** 2 + (y - ball_y) ** 2) <= ball_radius and moving:
                moving = False
                end_time = time.time()
                time_diff = round(end_time - start_time, 3)
                distance_after_moving = math.sqrt((ball_x - center_x) ** 2 + (ball_y - center_y) ** 2)
                with open('1-data_yuanli.csv', mode='a', newline='') as data_file:
                    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    data_writer.writerow([i,time_diff, distance, ball_radius, SPEED, distance_after_moving])
                ball_x = center_x + Distance
                ball_y = center_y
                i=i+1

    # 计算小球位置
    if moving:
        if ball_x >= center_x:
            vector_x = ball_x - center_x
            vector_y = ball_y - center_y
            vector_length = math.sqrt(vector_x ** 2 + vector_y ** 2)
            unit_vector_x = vector_x / vector_length
            unit_vector_y = vector_y / vector_length
            ball_x += int(SPEED * unit_vector_x)
            ball_y += int(SPEED * unit_vector_y)
            if ball_x > screen_width or ball_x < 0 or ball_y > screen_height or ball_y < 0:
                moving = False
                ball_x = center_x + Distance
                ball_y = center_y
        else:
            ball_x = center_x
            ball_y = center_y


    # 绘制图形
    screen.fill(WHITE)
    pygame.draw.circle(screen, BLACK, (center_x, center_y), center_radius)
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)
    pygame.display.update()

    # 控制帧率
    clock.tick(FPS)
'''




'''
###测基准眼动数据
###//////////////////////////////////////////////////////////////////////////////////////////
import pygame
import math
import random
import csv
import time

# 初始化 Pygame
pygame.init()


# 获取屏幕大小
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("小球运动")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 定义常量
FPS = 60
center_radius=10
MAX_RUNTIME = 60  # 程序最长运行时间，单位秒

# 定义初始位置
center_x = screen_width // 2
center_y = screen_height // 2


# 定义初始状态
moving = False

# 渲染动画
clock = pygame.time.Clock()
start = time.time()  # 记录程序启动时间
while True:
    # 判断程序运行时间是否超过最长运行时间
    if time.time() - start >= MAX_RUNTIME:
        pygame.quit()
        quit()
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            quit()
    # 绘制图形
    screen.fill(WHITE)
    pygame.draw.circle(screen, BLACK, (center_x, center_y), center_radius)
    pygame.display.update()

    # 控制帧率
    clock.tick(FPS)
'''


'''
###瞳孔数据预处理第一步：删去置信度小于0.6的值
###/////////////////////////////////////////////////////////////////////////////////////////

import pandas as pd
import csv 

f=pd.read_csv(r'C:/Users/22064/Desktop/毕业设计/瞳孔数据/被试2瞳孔数据/2-2瞳孔数据.csv')
header = ('confidence','diameter')
with open('2-2_pupildata.csv', mode='a', newline='') as data_file:
    data_writer = csv.writer(data_file)
    data_writer.writerow(header)
    for i in range (f.shape[0]): 
        if f.iloc[i,0]>=0.6:
            data_writer.writerow([f.iloc[i,0],f.iloc[i,1]])
'''


'''
###瞳孔数据预处理第二步：移动平均滤波
###/////////////////////////////////////////////////////////////////////////////////////////

import pandas as pd
import numpy as np
import csv
def moving_average_filter(data, window_size):
    """定义移动平均滤波器函数，输入数据和窗口大小"""
    window = np.ones(int(window_size))/float(window_size)
    """创建窗口，窗口大小为window_size，元素值为1/window_size"""
    return np.convolve(data, window, 'valid')
    """使用np.convolve函数进行卷积操作，返回输出信号"""
f=pd.read_csv(r'C:/Users/22064/Desktop/毕业设计/瞳孔数据/被试2瞳孔数据1.0/2-2_pupildata.csv')
signal=f.iloc[:,1]
# 应用移动平均滤波器
filtered_signal = moving_average_filter(signal, 1000)

filtered_signal = np.reshape(filtered_signal, (-1, 1))
header=('diameter','')
with open('2-2_pupil.csv', mode='a', newline='') as data_file:
    data_writer = csv.writer(data_file)
    data_writer.writerow(header)
    data_writer.writerows(filtered_signal)

'''



'''
###基于多分类支持向量机识别认知模式
###//////////////////////////////////////////////////////////////////////////////////////////
# 导入所需库
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.svm import SVC
train_data=pd.read_csv(r'C:/Users/22064/Desktop/毕业设计/生成的数据.csv')
X=train_data.iloc[:,0:4]
y=train_data.iloc[:,4]
# 划分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
svm=SVC(kernel='linear',C=100,gamma=0.01) #构建svm分类器
svm.fit(X_train,y_train) #模型训练
print("训练集上准确度为：{:.2f}".format(svm.score(X_train,y_train)))
print("测试集上准确度为：{:.2f}".format(svm.score(X_test,y_test)))

#混淆矩阵

from sklearn.metrics import classification_report
y_pred = svm.predict(X_test)
#print(classification_report(y_test,y_pred))

with open('classification_report.txt', 'w') as f:
    f.write(classification_report(y_test,y_pred))

import seaborn as sns; sns.set()
from sklearn.metrics import confusion_matrix
mat = confusion_matrix(y_test,y_pred)
#labels= train_data['mode'].unique()#获取类别
labels =['认知难度1','认知难度2','认知难度3','认知难度4','认知难度5','认知难度6','认知难度7','认知难度8',
                '认知难度9','认知难度10','认知难度11','认知难度12','认知难度13','认知难度14','认知难度15',
                '认知难度16','认知难度17','认知难度18','认知难度19','认知难度20']
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
plt.figure(figsize=(9, 9))
sns.heatmap(mat.T, annot = True, cmap='Blues',fmt='d', cbar=True, xticklabels = labels ,yticklabels = labels)
plt.xlabel('true mode')
plt.ylabel('predicted mode')
plt.title('Confusion Matrix')
plt.savefig('confusion_matrix.svg', format='svg')
plt.show()
'''

'''
# 网格搜索交叉验证，返回最佳模型及其参数
from sklearn.model_selection import GridSearchCV
svm=SVC()
param_grid= {'kernel':['linear', 'rbf'], 'C':[0.1,1,10,100], 'gamma':[0.01,0.1,1]}
grid = GridSearchCV(svm,param_grid,cv=3)
grid.fit(X_train,y_train)
print(grid.best_params_) # 输出最佳参数组合
svm = grid.best_estimator_
print("训练集上准确度为：{:.2f}".format(svm.score(X_train,y_train)))
print("测试集上得分：{:.2f}".format(svm.score(X_test,y_test)))
# 在测试集上进行预测
y_pred = svm.predict(X_test)
# 计算分类准确度
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
'''
