# -*- coding: utf-8 -*-
import codecs
import datetime
import time
import random
from sys import exit

import matplotlib.pyplot as plt
import pyautogui as pyg  # 记录鼠标轨迹
import pygame  # 导入pygame库
from data_process import process_data, write_data
from plot import Plot
# 设置实验窗口大小
import xlwt
#导入两个类
from niukou import NiuKou

#3.0k
SCREEN_WIDTH = 3071
SCREEN_HEIGHT = 1919
#2.5k
#SCREEN_WIDTH = 2560
#SCREEN_HEIGHT = 1600

#实验参数
csd_speed = 15 # 移动速度
niukou_speed = 15 # 供给速度
niukou_num = 3 # 纽扣数量


# 初始化 pygame
pygame.init()

# 设置游戏界面大小
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# 游戏左上角界面标题
pygame.display.set_caption('动态视觉搜索实验')
# 设置左上角图标
ic_launcher = pygame.image.load('resources/image/ic_launcher.png').convert_alpha()
pygame.display.set_icon(ic_launcher)

# 游戏循环帧率设置
fps_clock = pygame.time.Clock()
#arg是发生事件
def startGame(arg,shu_biao_x, shu_biao_y):
    #开始坐标
    start_pos = (arg[0],SCREEN_HEIGHT-arg[1])
    #print('开始坐标',start_pos)

    #分段记录
    fd_index=1
    #只记录点击到物体后，之前的所有点，但是当被t记录之后会被清零，并且一直记录下去
    mouse_l = []
    #只记录点击到物体后，之前的所有点，选择性记录
    mouse_t = []
    # 纽扣生成数量足够后纽扣移动距离
    move_long = 0



    #展示出来的数量，
    desplay_num = 0
    clicked_right_num = 0  # 点击正确次数
    clicked_error_num = 0  # 点击错误次数


    #导入图片
    enemy_img1 = pygame.image.load('resources/image/扣子 (5).png')
    enemies1 = pygame.sprite.Group()



    # 判断游戏循环退出的参数
    running = True

    # 纽扣点击存储
    nk_destory = []

    # 使得每一次的THR都能够传进来
    T_H_R = []
    # 游戏主循环

    # 生成excel
    workbook = xlwt.Workbook(encoding = 'utf-8')
    #创建工作表二
    worksheet = workbook.add_sheet('轨迹数据')
    worksheet2 = workbook.add_sheet('THR数据')
    #在表二中加入相应的标题
    worksheet.write(0, 0, label='纽扣分段')
    worksheet.write(0, 1, label='时间')
    worksheet.write(0, 2, label='X坐标')
    worksheet.write(0, 3, label='Y坐标')
    worksheet.write(0, 4, label='备注')
    worksheet.write(0, 5, label='轨迹长度')
    worksheet.write(0, 6, label='直线距离')
    worksheet.write(0, 7, label='距离比例')
    #
    worksheet2.write(0, 0, label='Time')
    worksheet2.write(0, 1, label='H')
    worksheet2.write(0, 2, label='R')
    worksheet2.write(0, 3, label='log2(H/R)')
    worksheet2.write(0, 4, label='a')
    worksheet2.write(0, 5, label='b')
    #运行
    I=0
    while running:
        niukou_size = random.randint(30, 1000)

        enemy1_img = pygame.transform.scale(enemy_img1, (int(niukou_size), int(niukou_size)))
        #记录鼠标在整个屏幕中位置
        x, y = pyg.position()
        #print(x,y)
        #每一次都加进来了，所以一直都在记录数据
        shu_biao_x.append(x)
        shu_biao_y.append(SCREEN_HEIGHT-y)
        #time.sleep(0.05)
        #记录每一次循环的鼠标位置
        biao_qian = {
            'x':x,
            'y':SCREEN_HEIGHT-y,
            'time':datetime.datetime.now()
        }
        #print(biao_qian)
        #加入数组中
        mouse_l.append(biao_qian)

        #?
        click_kz = None
        # 绘制背景
        screen.fill('#C0C0C0')

        #绘制关闭按钮
        pygame.draw.rect(screen,(255, 0, 0),[2971,0,100,100],0)

        # 上一个纽扣出现的y坐标
        last_y = 0
        now_y = 0
        # 一次性创建实体，
        if I==0:

            #随机出现纽扣
            #使纽扣位置不超出屏幕,并且使得鼠标不会直接在图像上
            new_x=random.randint(0,SCREEN_WIDTH)
            new_y=random.randint(0, SCREEN_HEIGHT)
            while ((x-new_x)**2+(y-new_y)**2<=(niukou_size*1.5)**2) or (new_x+niukou_size >= SCREEN_WIDTH) or (new_y+niukou_size >= SCREEN_HEIGHT):
                new_x = random.randint(0, SCREEN_WIDTH)
                new_y = random.randint(0, SCREEN_WIDTH)


            #for an in enemies1:

            enemy1_pos = [new_x,new_y]
            enemy1 = NiuKou(enemy1_img, enemy1_pos, csd_speed)
            desplay_num += 1
            enemies1.add(enemy1)
            #print('12')
            I=1


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
                    running = False
                    # 最后的作图阶段

                    #pygame.quit()
                    #exit()


        for enemy in enemies1:
            # 移动扣子
            # print(enemy.__dict__)
            #pygame.draw.circle(screen, (0, 255, 0), [120, 120], 120, 120)
            #print("改变")
            #enemy.move()
            #print(click_kz)

            if click_kz is not None:
                #判断是否点到了位置上
                if (click_kz[0] - enemy.rect.centerx) ** 2 + (click_kz[1] - enemy.rect.centery) ** 2 < (int(niukou_size) / 2) ** 2:

                    enemy.destory_time = datetime.datetime.now()
                    I=0
                    nk_destory.append(enemy)
                    clicked_error_num += 1
                        #添加元素，加入从出现到点击，若没有点击到位置则没有数据
                    mouse_t.append({
                            'bz':'误点',
                            'start_mark':start_pos,
                            'fd_index':fd_index,
                            #将整个数组都加入其中
                            'fd_data':mouse_l,
                            'end_mark': (x,y),
                            'time':datetime.datetime.now()
                        })
                    start_pos=(x,y)
                    fd_index+=1
                        #将鼠标轨迹更新，这样就得到了点击前的数据，并移除一个实体吗，再在前面重新绘制
                    #print('qwe')
                    #plt.xlim(0, SCREEN_WIDTH)
                    #plt.ylim(0, SCREEN_HEIGHT)
                    #plt.xlabel("x")
                    #plt.ylabel("y")
                    #plt.title("the mouse log")
                    #a=[]
                    #b=[]
                    #for i in mouse_l:
                        #print(i['x'],i['y'])
                        #a.append(i['x'])
                        #b.append(i['y'])
                    #plt.plot(a,b) # 轨迹图
                    #plt.show()

                    t_h_r = process_data(mouse_l,niukou_size)
                    T_H_R.append(t_h_r)

                    mouse_l=[]
                    enemies1.remove(enemy)

    # 写入excel
    # 参数对应 行, 列, 值
    a, b =write_data(worksheet2,T_H_R)
    Plot(a,'a')
    Plot(b,'b')


    #row行
    row = 1
    for i8, t8 in enumerate(mouse_t):
        #print(t8['time'])
        #写入第一行，并计算初始的数据，现在写入的是初始点的数据，以及一些计算数据
        worksheet.write(row, 0, label=float(t8['fd_index']))
        #直接给出具体经过的时间
        worksheet.write(row, 1, label=t8['time'].strftime('%Y-%m-%d %H:%M:%S.%f'))
        #写x,y
        worksheet.write(row, 2, label=float(t8['start_mark'][0]))
        worksheet.write(row, 3, label=float(t8['start_mark'][1]))

        try:
            #计算直线距离
            direct_Long = round(((t8['end_mark'][1] - t8['start_mark'][1]) ** 2 + (
                        t8['end_mark'][0] - t8['start_mark'][0]) ** 2) ** 0.5, 0)
        except:
            direct_Long = ''

        #worksheet.write(row, 6, label=float(lll))
        #记录基准行，就是每一次，同一个字典里面的，不同字典则头一行用m_row来记录
        m_row = row

        row += 1

        #将之后的行都写进去，然后进行实际距离的计算，只要考虑数量就可以了
        Long = 0
        #print('zaizheli' + str(row)+'ss'+str(len(mouse_t)))
        #不严谨的判断方式，由于实际的数量远小于鼠标的数据，所以只有第一个for循环只进入一次
        if i8 < (len(mouse_t) - 1):
            for i, t1 in enumerate(t8['fd_data']):
                #遍历算法，为的是计算实际长度，下一次的初始点（mouse_t[i8 + 1]['start_mark'][0]，mouse_t[i8 + 1]['start_mark'][1]）
                #如果数据走到了下一个开始点就过
                if t1['x'] == mouse_t[i8 + 1]['start_mark'][0] and t1['y'] == mouse_t[i8 + 1]['start_mark'][1] :
                    pass
                #判t8['start_mark'][0]，t8['start_mark'][1]是这个字典的最初状态
                elif t1['x'] == t8['start_mark'][0] and t1['y'] == t8['start_mark'][1]  :
                    pass
                else:
                    #输出前面的？
                    #print(i)
                    worksheet.write(row, 1, label=t1['time'].strftime('%Y-%m-%d %H:%M:%S.%f'))
                    worksheet.write(row, 2, label=float(t1['x']))
                    worksheet.write(row, 3, label=float(t1['y']))

                    if i > 0:
                        Long += ((t1['y'] - t8['fd_data'][i - 1]['y']) ** 2 + (
                                    t1['x'] - t8['fd_data'][i - 1]['x']) ** 2) ** 0.5
                    row += 1
            #计算实际长度，输出实际长度
            worksheet.write(m_row, 5, label=float(round(Long, 0)))
            if direct_Long == 0 :
                rate = 0
            else :
                #计算比例,并写入
                rate = float(round(Long, 0)) / float(direct_Long)
                worksheet.write(m_row, 7, label= float(rate))
        else:
            for i, t1 in enumerate(t8['fd_data']):
                #判断开始相同则过
                if t1['x'] == t8['start_mark'][0] and t1['y'] == t8['start_mark'][1]:
                    pass
                else:
                    worksheet.write(row, 1, label=t1['time'].strftime('%Y-%m-%d %H:%M:%S.%f'))
                    worksheet.write(row, 2, label=float(t1['x']))
                    worksheet.write(row, 3, label=float(t1['y']))

                    if i > 0:
                        Long += ((t1['y'] - t8['fd_data'][i - 1]['y']) ** 2 + (
                                    t1['x'] - t8['fd_data'][i - 1]['x']) ** 2) ** 0.5
                    row+=1

            worksheet.write(m_row, 5, label=float(round(Long, 0)))
            if direct_Long != 0 :
                rate = float(round(Long, 0)) / float(direct_Long)
                worksheet.write(m_row, 7, label=float(rate))
            #输出最后一行
            worksheet.write(row, 0, label=float(t8['fd_index']+1))
            worksheet.write(row, 1, label=t8['time'].strftime('%Y-%m-%d %H:%M:%S.%f'))
            worksheet.write(row, 2, label=float(t8['end_mark'][0]))
            worksheet.write(row, 3, label=float(t8['end_mark'][1]))

    #下面都懂了

    workbook.save('实验数据.xls')

    # 绘制游戏结束背景
    game_over1 = pygame.transform.scale(pygame.image.load('resources/image/gameover.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(game_over1, (0, 0))
    # 使用系统字体
    xtfont = pygame.font.SysFont('华文中宋', 25)
    textstart = xtfont.render('当前试次结果如下，请确认并进行后续试次' , True, (0, 0, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery - 100
    screen.blit(textstart, text_rect)

    textstart = xtfont.render('正确数：' + str(clicked_right_num), True, (0, 0, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery - 20
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


from Second_page import di_er_ye
from First_page import sou_ye



def main():
    # 初始设定控制变量
    kai_shi = True
    jie_shu = False
    while True:
        #TRUE开始游戏进入循环
        if kai_shi:
            #创建鼠标的位置数组
            shu_biao_x, shu_biao_y = [], []
            #进入游戏主页
            sou_ye(SCREEN_WIDTH, SCREEN_HEIGHT)
        for event in pygame.event.get():
            # 关闭页面游戏退出
            if event.type == pygame.QUIT:
                #print('点击了退出按钮')
                pygame.quit()
                exit()
            # 判断是否有事件发生，直接判断鼠标点到哪里了
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #print('鼠标点击事件发生了')
                if  kai_shi:
                    # 点击了开始
                    #print('第一页')
                    if screen.get_rect().centerx - 80 <= event.pos[0] \
                            and event.pos[0] <= screen.get_rect().centerx + 80 \
                            and screen.get_rect().centery + 120 <= event.pos[1] \
                            and screen.get_rect().centery + 200 >= event.pos[1]:
                        #print('点到了按钮')
                        #绘制这个界面
                        di_er_ye(SCREEN_WIDTH, SCREEN_HEIGHT)
                        #print('第二页')
                        # print(shi_fou_kai_shi)
                        kai_shi = False
                        jie_shu = True

                elif not kai_shi:
                    if  jie_shu:

                        #print("点击任意位置，游戏正式开始，单击左键才能够开始")
                        # print(event.type==pygame.MOUSEBUTTONDOWN)
                        # print(event.button==1)
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            #正式进行游戏
                            startGame(event.pos,shu_biao_x, shu_biao_y)
                            jie_shu = False

                    else:
                        # 判断鼠标单击的位置是否为开始按钮位置范围内
                        if screen.get_rect().centerx - 70 <= event.pos[0] \
                                and event.pos[0] <= screen.get_rect().centerx + 50 \
                                and screen.get_rect().centery + 100 <= event.pos[1] \
                                and screen.get_rect().centery + 140 >= event.pos[1]:
                            #print('返回第二页')
                            di_er_ye(SCREEN_WIDTH, SCREEN_HEIGHT)
                            kai_shi = False
                            jie_shu = True

                        # 判断鼠标是否单击排行榜按钮
                        if screen.get_rect().centerx - 70 <= event.pos[0] \
                                and event.pos[0] <= screen.get_rect().centerx + 50 \
                                and screen.get_rect().centery + 160 <= event.pos[1] \
                                and screen.get_rect().centery + 200 >= event.pos[1]:
                            # 显示排行榜

                            kai_shi = True
                            pygame.quit()
                            exit()


        # 更新界面
        pygame.display.update()
        # 控制游戏最大帧率为 60
        fps_clock.tick(60)
#print()
if __name__ == '__main__':
    main()