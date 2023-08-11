# -*- coding: utf-8 -*-
import math
import os
import time
import random
from sys import exit
import numpy as np
import pyautogui as pyg  # 记录鼠标轨迹
import pygame  # 导入pygame库
import xlwt
#导入两个类
from 一维.App.niukou import NiuKou
import matplotlib as mpl
import matplotlib.pyplot as plt
from 一维.App.Second_page import second_page

global name,color1,color2
name=''
color2=(255,0,0)
color1=(255,255,255)
#3.0k
SCREEN_WIDTH = 3071
SCREEN_HEIGHT = 1919
#2.5k
#SCREEN_WIDTH = 2560
#SCREEN_HEIGHT = 1600

# 初始化 pygame
pygame.init()

# 设置游戏界面大小
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# 游戏左上角界面标题
pygame.display.set_caption('XXX实验')
# 设置左上角图标
# 游戏循环帧率设置
fps_clock = pygame.time.Clock()
#arg是发生事件

def speed(t, x):#计算速度
    v = []
    for i in range(len(x) - 1):
        # print(x[i])

        m = (x[i + 1] - x[i]) / (t[i + 1] - t[i])

        v.append(m)
    return v
def angle(x,y):#计算角度
    a = []
    for i in range(len(x) - 1):
        # print(x[i])

        m = math.atan((y[i ] - y[i+1]) / (x[i + 1] - x[i]+1e-5))

        a.append(m)
    return a
def waylong(x,y):#计算路径长度
    s=0
    for i in range (len(x)-1):
        s=s+((x[i]-x[i+1])**2+(y[i]-y[i+1])**2)**0.5
    return s
def smooth(data,facter=0.8):#实现平滑指数
        sp=[]
        for i in data:
            if sp:
                p=sp[-1]
                sp.append(p*facter+i*(1-facter))
            else:
                sp.append(i)
        return sp
def startGame(arg):
    global name,color1,color2
    #开始坐标
    #print('开始坐标',start_pos)
    #分段记录
    fd_index=1
    #只记录点击到物体后，之前的所有点，但是当被t记录之后会被清零，并且一直记录下去
    mouse_l = []

    #展示出来的数量，
    #导入图片
    enemy_img1 = pygame.image.load('resources/yellow.png')
    enemy_img2 = pygame.image.load('resources/red.png')
    enemies1 = pygame.sprite.Group()

    # 生成excel
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建工作表二

    # 在表二中加入相应的标
    #

    # 判断游戏循环退出的参数
    running = True

    # 纽扣点击存储
    nk_destory = []

    # 游戏主循环
    #I控制循环只进行一次J控制左边还是右边
    I=0
    J=1
    K=1
    W = 250
    #DW=2#初始的比值
    WD=0
    M=1
    CHI=1
    D=0
    K1=[]
    K2=[]
    while running:

        #?
        click_kz = None
        # 绘制背景
        screen.fill((255,255,255))

        #绘制关闭按钮
        pygame.draw.rect(screen,(255, 0, 0),[2971,0,100,100],0)

        img= pygame.transform.scale(enemy_img2,  (50, 50))

        xtfont = pygame.font.SysFont('华文中宋', 50)
        textstart = xtfont.render('第'+str(CHI) + '次，还剩'+str(10-CHI)+'次', True, (0, 255, 255))
        text_rect = textstart.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.centery = 100
        screen.blit(textstart, text_rect)

        if CHI==11:
            break

        if I==0 :
            if J==1 and M==1:
                #绘制初始位置
                cT = time.time()

                new_x = int((SCREEN_WIDTH - 1) / 2)
                new_y = int((SCREEN_HEIGHT - 1) / 2 )

                enemy1_pos = [new_x,new_y]
                enemy1 = NiuKou(img ,enemy1_pos)
                enemies1.add(enemy1)
                I = 1
                J = 0
                M=3
            elif J==0:

                W = random.uniform(30., 500.)
                WD = random.uniform(0.01, 1.)
                D = W / WD
                while  W + D >  SCREEN_WIDTH or D<3*W:
                    #print(D)
                    W = random.uniform(30., 500.)
                    WD = random.uniform(0.01, 1.)
                    D = W / WD
                enemy1_img = pygame.transform.scale(enemy_img1, (int(W), int(W)))
                enemies1.draw(screen)
                pygame.display.update()
                pygame.time.wait(1000)#等待一秒计算中应该除去
                cT = time.time()
                # 实现了每一次等
                # 固定位置H
                new_x = int(SCREEN_WIDTH/2 +D/2- W / 2)
                new_y = int((SCREEN_HEIGHT - 1) / 2 -W/2)

                enemy1_pos = [new_x, new_y]
                enemy = NiuKou(enemy1_img, enemy1_pos)
                enemies1.add(enemy)#右边的圆形

                new_x1 = int(SCREEN_WIDTH/2 -D/2-W / 2)
                new_y1 = int((SCREEN_HEIGHT - 1) / 2 - W / 2)

                enemy1_pos = [new_x1, new_y1]
                enemy1 = NiuKou(enemy1_img, enemy1_pos)
                enemies1.add(enemy1)#左边的圆形

                I = 1
                J = 1

        # 显示精灵# 更新屏幕
        enemies1.draw(screen)
        pygame.display.update()
        # 处理游戏退出
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                #1025按下1026抬起1024移动
            if event.type == 1025:
                #给kz赋值，为事件发生的位置
                click_kz = event.pos
                #print('qwe',click_kz)
                # 点到结束键
                if 2971 < event.pos[0] < 3071 and 0 < event.pos[1] < 100:
                    #跳出循环
                    running = False

        #记录鼠标在整个屏幕中位置
        x, y = pyg.position()
        #print(x,y)
        #每一次都加进来了，所以一直都在记录数据

        #time.sleep(0.05)
        #记录每一次循环的鼠标位置
        biao_qian = {
            'x':x,
            'y':y,
            'time':time.time()
        }

        mouse_l.append(biao_qian)
        for enemy in enemies1:
            if click_kz is not None:
                #print(enemy.rect.centerx,enemy.rect.centery)
                #判断是否点到了位置上
                #print(click_kz)
                if J==1 and (click_kz[0] - enemy.rect.centerx) ** 2 + (click_kz[1] - enemy.rect.centery) ** 2 < (int(W) / 2) ** 2:
                    if M==2:
                        '''
                            #添加元素，加入从出现到点击，若没有点击到位置则没有数据
                        worksheet = workbook.add_sheet('轨迹数据'+str(K))
                        worksheet.write(0, 0, label='Time')
                        worksheet.write(0, 1, label='X')
                        worksheet.write(0, 2, label='Y')
                        #print(len(mouse_l['time']))
                        for i in range(len(mouse_l)):
                            worksheet.write(i+1, 0, label=str(mouse_l[i]['time']-cT))
                            worksheet.write(i+1, 1, label=mouse_l[i]['x'])
                            worksheet.write(i+1, 2, label=mouse_l[i]['y'])
                        '''
                        CHI+=1

                        t = []
                        x = []
                        y = []
                        a=[]
                        for i in range(len(mouse_l)):
                                t.append(mouse_l[i]['time']-cT)
                                x.append(mouse_l[i]['x'])
                                y.append(mouse_l[i]['y'])
                        v_x = speed(t, x)
                        v_y = speed(t, y)
                        a = angle(x,y)
                        # 总体速度
                        K1.append(WD)
                        K2.append(waylong(x,y)/D)
                        z = []
                        for i in range(len(v_x)):

                            m = (v_x[i] ** 2 + v_y[i] ** 2) ** 0.5
                            z.append(m)
                        try:
                            del t[-1]
                        except:
                            pass
                        try:
                            dir = 'D:\Desk\一元固定\一维\XXX\img\\' + 'R=' + str(W)
                            os.mkdir(dir)
                        except:
                            pass

                        #https://blog.csdn.net/u013185349/article/details/122618862?utm_term=plt%E7%BB%98%E5%88%B6%E4%B8%89%E7%BB%B4%E5%9B%BE&utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~all~sobaiduweb~default-1-122618862-null-null&spm=3001.4430
                        #v_x = smooth(v_x)
                        #v_y = smooth(v_y)
                        z = smooth(z)
                        a = smooth(a)
                        #绘制三维图
                        mpl.rcParams['legend.fontsize'] = 10

                        fig = plt.figure()
                        ax = fig.add_subplot(111,projection = '3d')
                        ax.set_xlim(np.min(t), np.max(t))
                        ax.set_ylim(np.min(z), np.max(z))
                        ax.set_zlim(np.min(a), np.max(a))
                        ax.set_xlabel("t")
                        ax.set_ylabel("z")
                        ax.set_zlabel("a")
                        plt.title(str(W) + '-{}.png'.format(K))
                        ax.plot(t, z,a,label='parametric curve')
                        ax.scatter(t, z,a,s=5, c='r',label='parametric curve')
                        #ax.legend()
                        plt.savefig('./img/' + 'R=' + str(W) + '/pic-z-a' + str(W) + '-{}.png'.format(K))
                        #plt.show()

                        plt.clf()
                        for i in range (len(y)):
                            y[i]=SCREEN_HEIGHT-y[i]

                        #print(len(x),len(y))
                        plt.xlabel("x")
                        plt.ylabel("y")
                        plt.title(str(W) + '-{}.png'.format(K))
                        plt.plot(x,y)
                        plt.scatter(x, y, marker='.')
                        #plt.draw()
                        #ax.legend()
                        plt.savefig('./img/' + 'R=' + str(W) + '/pic-x-y' + str(W) + '-{}.png'.format(K))

                        '''
                        plt.xlim(t[0], t[-1])
                        plt.ylim(np.min(z), np.max(z))
                        plt.xlabel("t")
                        plt.ylabel("vz")
                        plt.title(str(R) + '-{}.png'.format(K))
                        plt.scatter(t, z, marker='.')
                        plt.draw()
                        plt.savefig('./img/' + 'R=' + str(R) + '/pic' + str(R) + '-{}.png'.format(K))
                        if K%3==0:
                            plt.clf()
                        #plt.show()
                        '''
                        if K%3==0:
                            W/=2
                        K += 1


                    mouse_l = []
                    enemies1.remove(enemy)
                    I = 0
                    M-=1#点击的次数

                elif M==3 and J==0 and (click_kz[0] - enemy.rect.centerx) ** 2 + (click_kz[1] - enemy.rect.centery) ** 2 < (int(W) / 2) ** 2:

                    mouse_l=[]
                    enemies1.remove(enemy)
                    I = 0

    worksheet = workbook.add_sheet('轨迹数据')
    worksheet.write(0, 0, label='WD')
    worksheet.write(0, 1, label='SD')
    for i in range(len(K1)):
        worksheet.write(i + 1, 0, label=K1[i])
        worksheet.write(i + 1, 1, label=K2[i])
    pos=name+'-实验数据.xls'
    workbook.save(pos)

    plt.xlim(np.min(K1), np.max(K1))
    plt.ylim(np.min(K2), np.max(K2))
    plt.xlabel("W/D")
    plt.ylabel("S/D")
    plt.scatter(K1, K2, marker='.')
    plt.draw()
    plt.savefig('相比.png')
    # plt.show()
    # 绘制游戏结束背景
    # 使用系统字体

    screen.fill((255, 255, 255))
    xtfont = pygame.font.SysFont('华文中宋', 25)
    textstart = xtfont.render('当前试次结果如下，请确认并进行后续试次' , True, (0, 0, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery - 100
    screen.blit(textstart, text_rect)

    # 重新开始按钮
    textstart = xtfont.render('返回第二页', True, (0, 255, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 120
    screen.blit(textstart, text_rect)

    # 返回设置
    textstart = xtfont.render('退出游戏 ', True, (0, 255, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 180
    screen.blit(textstart, text_rect)


def first_page(SCREEN_WIDTH, SCREEN_HEIGHT):
    global color2,color1,name
    #创建一个新背景
    screen2 = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # 绘制背景
    screen2.fill([230, 230, 230])
    #不同大小
    font_40 = pygame.font.SysFont('华文中宋', 40)
    # 重新开始按钮
    #以上代码插入了一个标签在里面，后面的代码是一样的意思
    # 开始按钮
    textstart = font_40.render('开始', True, (0, 180, 60))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen2.get_rect().centerx
    text_rect.centery = screen2.get_rect().centery + 160
    screen2.blit(textstart, text_rect)


    textstart = font_40.render('请输入姓名拼音：', True, (255, 0, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen2.get_rect().centerx - 150
    # 【横向位置，可根据自己需要调整】
    text_rect.centery = 800
    # 【纵向位置，可根据自己需要调整】{注意：点击动作会受该参数影响，一下位置均可如此调整}
    screen2.blit(textstart, text_rect)
    #以上代码插入了一个标签在里面，后面的代码是一样的意

    input_box1 = pygame.Rect(screen2.get_rect().centerx + 50, 780, 200, 50)
    font = pygame.font.Font(None, 32)
    txt_surface = font.render(name, True, color1)
    width = max(100, txt_surface.get_width() + 10)
    input_box1.w = width
    screen2.blit(txt_surface, (input_box1.x + 5, input_box1.y + 5))
    pygame.draw.rect(screen2, color1, input_box1, 2)

def main():
    global name,color1,color2
    # 初始设定控制变量
    begin = True
    end = False
    while True:
        #TRUE开始游戏进入循环
        if begin:
            #创建鼠标的位置数组
            #进入游戏主页
            input_box1 = pygame.Rect(screen.get_rect().centerx + 50, 780, 200, 50)
            first_page(SCREEN_WIDTH, SCREEN_HEIGHT)
        for event in pygame.event.get():
            # 关闭页面游戏退出
            if event.type == pygame.QUIT:
                #print('点击了退出按钮')
                pygame.quit()
                exit()
            # 判断是否有事件发生，直接判断鼠标点到哪里了
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #print('鼠标点击事件发生了')
                if  begin:
                    # 点击了开始
                    #print('第一页')
                    if screen.get_rect().centerx - 80 <= event.pos[0] \
                            and event.pos[0] <= screen.get_rect().centerx + 80 \
                            and screen.get_rect().centery + 120 <= event.pos[1] \
                            and screen.get_rect().centery + 200 >= event.pos[1]:
                        #print('点到了按钮')
                        #绘制这个界面
                        second_page(SCREEN_WIDTH, SCREEN_HEIGHT)
                        #print('第二页')
                        # print(shi_fou_kai_shi)
                        begin = False
                        end = True

                elif not begin:
                    if  end:

                        #print("点击任意位置，游戏正式开始，单击左键才能够开始")
                        # print(event.type==pygame.MOUSEBUTTONDOWN)
                        # print(event.button==1)
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            #正式进行游戏
                            startGame(event.pos)
                            end = False

                    else:
                        # 判断鼠标单击的位置是否为开始按钮位置范围内
                        if screen.get_rect().centerx - 70 <= event.pos[0] \
                                and event.pos[0] <= screen.get_rect().centerx + 50 \
                                and screen.get_rect().centery + 100 <= event.pos[1] \
                                and screen.get_rect().centery + 140 >= event.pos[1]:
                            #print('返回第二页')
                            second_page(SCREEN_WIDTH, SCREEN_HEIGHT)
                            begin = False
                            end = True

                        # 判断鼠标是否单击排行榜按钮
                        if screen.get_rect().centerx - 70 <= event.pos[0] \
                                and event.pos[0] <= screen.get_rect().centerx + 50 \
                                and screen.get_rect().centery + 160 <= event.pos[1] \
                                and screen.get_rect().centery + 200 >= event.pos[1]:
                            # 显示排行榜

                            begin = True
                            pygame.quit()
                            exit()
            if begin:
                #  判断事件是否是鼠标放下
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    # 纽扣数量
                    if input_box1.collidepoint(event.pos):
                        # Toggle the active variable.
                        active1 = True
                    else:
                        active1 = False
                    # Change the current color of the input box.
                    color1 = color2 if active1 else color1

                if event.type == pygame.KEYDOWN:
                    if active1:

                        if event.key == pygame.K_RETURN:
                            name = ''
                        elif event.key == pygame.K_BACKSPACE:
                            name = str(name)[:-1]
                        else:
                            name += event.unicode
        # 更新界面
        pygame.display.update()
        # 控制游戏最大帧率为 60
        fps_clock.tick(60)



#print()
if __name__ == '__main__':
    main()