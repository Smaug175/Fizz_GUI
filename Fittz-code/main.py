# -*- coding: utf-8 -*-
import codecs
import datetime
import time
import random
from sys import exit

import matplotlib.pyplot as plt
import pyautogui as pyg  # 记录鼠标轨迹
import pygame  # 导入pygame库


# 设置实验窗口大小
import xlwt
#导入两个类
from niukou import NiuKou

SCREEN_WIDTH = 3071
SCREEN_HEIGHT = 1919
#实验参数
csd_speed = 30  # 移动速度
niukou_speed = 150 # 供给速度
niukou_size = 120  # 纽扣大小
niukou_num = 1 # 纽扣数量


niukou_plfs = 1 # 排列方式
plfs_list = ['随机排列', '有序矩阵']
pai_lie_hang_shu = 6 #整齐排列行数
niukou_yichang = 0.08  #异常纽扣比例

mu_biao_lei_xing_su_zu = ['纽扣', 'C Ring']

#导出数据文件名  xls_name

# 初始化 pygame
pygame.init()

# 设置游戏界面大小
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# 游戏左上角界面标题
pygame.display.set_caption('动态视觉搜索实验')
# 设置左上角图标


#载入图片
ic_launcher = pygame.image.load('resources/image/ic_launcher.png').convert_alpha()
pygame.display.set_icon(ic_launcher)

# 红扣子
red_kouzi = pygame.image.load('resources/image/扣子.png')
red_kouzi = pygame.transform.scale(red_kouzi, (200, 200))
#黑扣子
black_kouzi = pygame.image.load('resources/image/icon-纽扣.png')
#加减图片
add_img = pygame.image.load('resources/image/加.png')
jian_img = pygame.image.load('resources/image/减.png')

#实验参数对应图片
bg_color_path_di_zhi = ['resources/image/单图排列 (5).png', 'resources/image/单图排列 (6).png', 'resources/image/单图排列 (7).png',
                      'resources/image/单图排列 (8).png', ]



#from startgame import startGame
#arg是发生事件
def startGame(arg):
    xz_b=0
    shubiao_x = arg[0]
    shubiao_y = arg[1]
    #print(arg)
    #开始坐标
    start_pos = (arg[0],SCREEN_HEIGHT-arg[1])
    print('开始坐标',start_pos)

    #分段记录
    fd_index=1
    #鼠标轨迹记录
    mouse_l = []
    #鼠标总体记录
    mouse_t = []
    # 纽扣生成数量足够后纽扣移动距离
    move_long = 0
    # 纽扣每秒生成多少个的辅助变量#
    numi = 1
    # 上一个纽扣出现的y坐标
    last_y = 0
    now_y = 0

    desplay_num = 0
    desplay_yc_num = 0
    clicked_num = 0  # 点击总次数
    clicked_right_num = 0  # 点击正确次数
    clicked_error_num = 0  # 点击错误次数


    #导入图片
    enemy_img1 = pygame.image.load('resources/image/扣子 (5).png')
    enemy_img2 = pygame.image.load('resources/image/扣子 (5).png')

    enemy1_img = pygame.transform.scale(enemy_img1, (int(niukou_size), int(niukou_size)))
    enemy2_img = pygame.transform.scale(enemy_img2, (int(niukou_size), int(niukou_size)))

    enemy1_rect = enemy1_img.get_rect()
    enemy1_down_imgs = []

    enemy1_down_imgs.append(enemy_img1)
    enemy1_down_imgs.append(enemy_img2)
    #print(enemy1_down_imgs[0],enemy1_down_imgs[1])
    # 储存纽扣
    enemies1 = pygame.sprite.Group()
    # 存储删除纽扣，用来渲染击毁动画
    enemies_down = pygame.sprite.Group()

    enemy_frequency = 0

    score = 0
    # 游戏循环帧率设置
    clock = pygame.time.Clock()

    # 判断游戏循环退出的参数
    running = True

    # 纽扣点击存储
    nk_destory = []

    # 规则记录
    gz_mark = 0

    # 游戏主循环

    # 生成excel
    workbook = xlwt.Workbook(encoding = 'utf-8')
    #创建工作表二
    worksheet = workbook.add_sheet('轨迹数据')
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
    #纽扣随机排序？
    #首先生成异常的数量，然后用总数减去异常的数量，最后对数组进行洗牌
    nk_rongqi = []
    for i in range(int(niukou_yichang * int(niukou_num))):
        nk_rongqi.append(1)
    for j in range(int(niukou_num) - int(niukou_yichang * int(niukou_num))):
        nk_rongqi.append(0)
    random.shuffle(nk_rongqi)
    #运行
    while running:
        #记录鼠标在整个屏幕中位置
        x, y = pyg.position()
        print(x,y)

        shu_biao_x.append(x)
        shu_biao_y.append(SCREEN_HEIGHT-y)
        #time.sleep(0.05)
        #记录每一次循环的鼠标位置
        biao_qian = {
            'x':x,
            'y':y,
            'time':datetime.datetime.now()
        }
        print(biao_qian)
        #加入数组中
        mouse_l.append(biao_qian)


        posite_mark = True
        #?
        click_kz = None
        # 绘制背景
        screen.fill('#C0C0C0')
        # 控制游戏最大帧率为 60
        clock.tick(120)

        # 生成扣子，需要控制生成频率
        if desplay_num < int(niukou_num):
            if enemy_frequency == (int(numi * 60 / int(niukou_speed))):
                if numi >= int(niukou_speed):
                    numi = 1
                else:
                    numi += 1
                # 判断排列方式
                if niukou_plfs == 0:

                    while posite_mark:
                        now_y = random.randint(0, SCREEN_HEIGHT - enemy1_rect.height)
                        if now_y - last_y > 0:
                            if now_y - last_y > enemy1_rect.height:
                                posite_mark = False
                        else:
                            if last_y - now_y > enemy1_rect.height:
                                posite_mark = False

                    last_y = now_y

                    enemy1_pos = [SCREEN_WIDTH, now_y]
                    if nk_rongqi[desplay_num] == 0:
                        enemy1 = NiuKou(enemy1_img, enemy1_down_imgs, enemy1_pos, csd_speed)
                    elif nk_rongqi[desplay_num] == 1:
                        enemy1 = NiuKou_err(enemy2_img, enemy1_down_imgs, enemy1_pos, csd_speed)
                        desplay_yc_num += 1
                    desplay_num += 1
                    enemies1.add(enemy1)
                elif niukou_plfs == 1:
                    gz_mark += 1
                    if (int(pai_lie_hang_shu)) == gz_mark / 1:
                        for i in range(pai_lie_hang_shu):
                            if desplay_num < int(niukou_num):
                                enemy1_pos = [SCREEN_WIDTH,
                                              (i + 0.5) * ((SCREEN_HEIGHT) / (pai_lie_hang_shu)) - 0.5 * enemy1_rect.height]
                                if nk_rongqi[desplay_num] == 0:
                                    enemy1 = NiuKou(enemy1_img, enemy1_down_imgs, enemy1_pos, csd_speed)
                                elif nk_rongqi[desplay_num] == 1:
                                    enemy1 = NiuKou_err(enemy2_img, enemy1_down_imgs, enemy1_pos, csd_speed)
                                    desplay_yc_num += 1  # 异常纽扣生成数量统计
                                desplay_num += 1
                                enemies1.add(enemy1)
                        gz_mark = 0
                    else:
                        pass

                    pass
            else:
                pass

        enemy_frequency += 1
        if enemy_frequency > 60:
            enemy_frequency = 0
        # print(len(enemies1))

        # 敌机被子弹击中效果显示
        for enemy_down in enemies_down:
            if enemy_down.down_index == 0:
                pass
            if enemy_down.down_index > 7:
                enemies_down.remove(enemy_down)
                score += 100
                continue
            # 显示碰撞图片
            screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
            enemy_down.down_index += 1
        # 显示精灵
        enemies1.draw(screen)

        # 更新屏幕
        pygame.display.update()
        # 处理游戏退出
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == 1025:
                click_kz = event.pos
                clicked_num += 1

        for enemy in enemies1:
            # 移动扣子
            # print(enemy.__dict__)
            enemy.move()
            # print(click_kz)

            if click_kz is not None:

                if (click_kz[0] - enemy.rect.centerx) ** 2 + (click_kz[1] - enemy.rect.centery) ** 2 < (
                        int(niukou_size) / 2) ** 2:
                    enemy.destory_time = datetime.datetime.now()
                    # print(enemy.__dict__)
                    # print('-----------------')
                    nk_destory.append(enemy)
                    if enemy.name == 0:
                        clicked_error_num += 1
                        mouse_t.append({
                            'bz':'误点',
                            'start_mark':start_pos,
                            'fd_index':fd_index,
                            'fd_data':mouse_l,
                            'end_mark': (x,y),
                            'time':datetime.datetime.now()
                        })
                        start_pos=(x,y)
                        fd_index+=1
                        mouse_l=[]
                    elif enemy.name == 1:
                        clicked_right_num += 1
                        mouse_t.append({
                            'bz': '',
                            'start_mark': start_pos,
                            'fd_index': fd_index,
                            'fd_data': mouse_l,
                            'end_mark': (x,y),
                            'time':datetime.datetime.now()
                        })
                        start_pos = (x, y)
                        fd_index += 1
                        mouse_l = []
                    enemies1.remove(enemy)
                else:
                    bbbb = {
                        'bz': '空点',
                        'x': x,
                        'y': y,
                        'time': datetime.datetime.now()
                    }
                    if bbbb not in mouse_l:
                        mouse_l.append(bbbb)

                # click_kz=None


            # 移动出屏幕后删除纽扣
            if enemy.rect.top < 0:
                enemies1.remove(enemy)

        # 游戏结束
        if desplay_num == int(niukou_num):
            move_long += int(csd_speed)
            #可以有更好的解决方法
            if move_long > SCREEN_WIDTH + int(niukou_size):
                #当移动距离大于屏幕大小加上自身大小时结束
                #print(move_long,SCREEN_WIDTH + int(niukou_size))
                #设置结束
                running = False
                #最后的作图阶段
                plt.xlim(0, SCREEN_WIDTH)
                plt.ylim(0, SCREEN_HEIGHT)
                plt.xlabel("x")
                plt.ylabel("y")
                plt.title("the mouse log")
                plt.plot(shu_biao_x, shu_biao_y) # 轨迹图
                #plt.scatter(xs, ys)  # 散点图
                #plt.hist(xs) #直方图
                plt.show()
    #上面的循环是游戏的进程

    click_null = desplay_yc_num - clicked_right_num


    # 写入excel
    # 参数对应 行, 列, 值


    for i in range(len(nk_destory)):
        if nk_destory[i].name == 0:
            nk_type = '正常纽扣'
        elif nk_destory[i].name == 1:
            nk_type = '异常纽扣'

        # print(nk_destory[i].__dict__)
        action_time= str((nk_destory[i].destory_time)- (nk_destory[i].start_time))[6: ]
    row = 1
    for ii, tt in enumerate(mouse_t):
        worksheet.write(row, 0, label=float(tt['fd_index']))
        worksheet.write(row, 1, label=tt['time'].strftime('%Y-%m-%d %H:%M:%S.%f'))
        worksheet.write(row, 2, label=float(tt['start_mark'][0]))
        worksheet.write(row, 3, label=float(tt['start_mark'][1]))

        if row == 1:
            worksheet.write(row, 4, label=str(tt['start_mark']))
        else:
            worksheet.write(row, 4, label=tt['bz'])

        try:
            lll = round(((tt['end_mark'][1] - tt['start_mark'][1]) ** 2 + (
                        tt['end_mark'][0] - tt['start_mark'][0]) ** 2) ** 0.5, 0)
        except:
            lll = ''

        worksheet.write(row, 6, label=float(lll))

        m_row = row
        row += 1
        real_l = 0
        if ii < (len(mouse_t) - 1):
            for i, t1 in enumerate(tt['fd_data']):
                if t1['x'] == mouse_t[ii + 1]['start_mark'][0] and t1['y'] == mouse_t[ii + 1]['start_mark'][1] and t1[
                    'bz'] == '空点':
                    pass
                elif t1['x'] == tt['start_mark'][0] and t1['y'] == tt['start_mark'][1] and t1['bz'] == '空点':
                    pass
                else:
                    worksheet.write(row, 1, label=t1['time'].strftime('%Y-%m-%d %H:%M:%S.%f'))
                    worksheet.write(row, 2, label=float(t1['x']))
                    worksheet.write(row, 3, label=float(t1['y']))
                    worksheet.write(row, 4, label=t1['bz'])
                    if i > 0:
                        real_l += ((t1['y'] - tt['fd_data'][i - 1]['y']) ** 2 + (
                                    t1['x'] - tt['fd_data'][i - 1]['x']) ** 2) ** 0.5
                    row += 1
            worksheet.write(m_row, 5, label=float(round(real_l, 0)))
            if lll == 0 :
                bili = 0
            else :
                bili = float(round(real_l, 0)) / float(lll)
                worksheet.write(m_row, 7, label= float(bili))
        else:
            for i, t1 in enumerate(tt['fd_data']):
                if t1['x'] == tt['start_mark'][0] and t1['y'] == tt['start_mark'][1] and t1['bz'] == '空点':
                    pass
                else:
                    worksheet.write(row, 1, label=t1['time'].strftime('%Y-%m-%d %H:%M:%S.%f'))
                    worksheet.write(row, 2, label=float(t1['x']))
                    worksheet.write(row, 3, label=float(t1['y']))
                    worksheet.write(row, 4, label=t1['bz'])
                    if i > 0:
                        real_l += ((t1['y'] - tt['fd_data'][i - 1]['y']) ** 2 + (
                                    t1['x'] - tt['fd_data'][i - 1]['x']) ** 2) ** 0.5
                    row+=1
            worksheet.write(m_row, 5, label=float(round(real_l, 0)))
            if lll == 0 :
                bili = 0
            else :
                bili = float(round(real_l, 0)) / float(lll)
                worksheet.write(m_row, 7, label=float(bili))

            worksheet.write(row, 0, label=float(tt['fd_index']+1))
            worksheet.write(row, 1, label=tt['time'].strftime('%Y-%m-%d %H:%M:%S.%f'))
            worksheet.write(row, 2, label=float(tt['end_mark'][0]))
            worksheet.write(row, 3, label=float(tt['end_mark'][1]))

    #下面都懂了

    # 导出数据文件名
    xls_name = str('实验数据')
    workbook.save(xls_name + '.xls')

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
    textstart = xtfont.render("返回第二页", True, (0, 255, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 120
    screen.blit(textstart, text_rect)

    # 返回设置
    textstart = xtfont.render('返回第一页 ', True, (0, 255, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 180
    screen.blit(textstart, text_rect)


from Second_page import di_er_ye
from First_page import sou_ye

#初始设定控制变量
kai_shi = True
jie_shu = False

#完全看懂
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
                        startGame(event.pos)
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