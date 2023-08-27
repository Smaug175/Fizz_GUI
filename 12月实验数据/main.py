# -*- coding: utf-8 -*-
import math
import time
from sys import exit
import pyautogui as pyg  # 记录鼠标轨迹
import pygame  # 导入pygame库
import xlwt
import random
import datetime


global name,color1,color2,IDENX
name=''
color2=(255,0,0)
color1=(255,255,255)
IDENX=0
#3.0k

SCREEN_WIDTH = 3071
SCREEN_HEIGHT = 1919
RATE=3072/312

#创建实验模型
w=(40,25,13,7)
a=(70,120,200,250)
group=[]
for i in enumerate(w):
    for j in enumerate(a):
        group.append((int(i[1]*RATE),int(j[1]*RATE)))
random.shuffle(group)

pygame.init()

# 设置游戏界面大小
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# 游戏左上角界面标题
pygame.display.set_caption('XXX实验')
# 设置左上角图标
# 游戏循环帧率设置
fps_clock = pygame.time.Clock()
#arg是发生事件


def second_page(SCREEN_WIDTH, SCREEN_HEIGHT):
    #第二屏
    screen3 = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # 绘制背景
    screen3.fill([255,255,255])

    img = pygame.image.load('resources/red.png')
    img = pygame.transform.scale(img, (150, 150))
    xtfont = pygame.font.SysFont('华文中宋', 40)

    textstart = xtfont.render('请移动鼠标至起始点，点击左键后开始实验', True, (0, 0, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen3.get_rect().centerx  # 【横向位置，可根据自己需要调整】
    text_rect.centery = 50 + 30  # 【纵向位置，可根据自己需要调整】{注意：点击动作会受该参数影响，一下位置均可如此调整}
    screen3.blit(img, (100, (SCREEN_HEIGHT-1)/2))
    screen3.blit(textstart, text_rect)

class Rect_black(pygame.sprite.Sprite):
    def __init__(self, enemy_img,  init_pos):
        #print('init_pos', init_pos)
        pygame.sprite.Sprite.__init__(self)

        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_index = 0
        self.start_time = datetime.datetime.now()

    # 扣子移动，边界判断及删除在游戏主循环里处理
    def move(self):
        pass
        #self.rect.left -= self.speed

def startGame(arg):
    global name,color1,color2,IDENX
    #开始坐标
    #print('开始坐标',start_pos)
    #分段记录
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
    K=1#判断是第几次实验
    W_rect = group[0][0]
    D_between = group[0][1]
    #DW=2#初始的比值
    worksheet=None
    M=0
    CHI=0#第几次实验
    k = 1#控制游戏流程
    while running:

        #?
        click_kz = None
        # 绘制背景
        screen.fill((255,255,255))

        #绘制关闭按钮
        pygame.draw.rect(screen,(255, 0, 0),[2971,0,100,100],0)

        img= pygame.transform.scale(enemy_img2,  (10, 1919))
        #
        xtfont = pygame.font.SysFont('华文中宋', 50)
        textstart = xtfont.render('第'+str(CHI) + '次', True, (255, 0, 0))
        text_rect = textstart.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.centery = 100
        screen.blit(textstart, text_rect)
        #

        if CHI==9:
            if k<16:
                W_rect = group[k][0]
                D_between = group[k][1]
                #print(group[k])
                k+=1
            else:
                print()
                break
            CHI=0
            #pass
            #break

        if I==0 :
            if J==1 and M==0:
                #绘制初始位置
                cT = time.time()#创建时间即显示时间
                new_x = int((SCREEN_WIDTH - 1) / 2-75)
                new_y = int((SCREEN_HEIGHT - 1)/2-75)
                img1 = pygame.transform.scale(enemy_img2, (150, 150))
                enemy1_pos = [new_x,new_y]
                enemy1 = Rect_black(img1, enemy1_pos)
                enemies1.add(enemy1)
                I = 1
                J = 0
                M = 9
            elif J==0:

                worksheet = workbook.add_sheet('W=' + str(W_rect)+',A='+str(D_between))
                worksheet.write(0, 0, label='Time')
                worksheet.write(0, 1, label='X')
                worksheet.write(0, 2, label='Y')
                worksheet.write(0, 3, label='T or F')

                enemy1_img = pygame.transform.scale(enemy_img1, (int(W_rect), 1919))#改变图片的大小
                enemies1.draw(screen)
                pygame.display.update()
                pygame.time.wait(1000)#等待一秒计算中应该除去
                cT = time.time()
                # 实现了每一次等
                # 固定位置H
                new_x = int(SCREEN_WIDTH/2 +D_between/2- W_rect / 2)
                new_y = 0

                enemy1_pos = [new_x, new_y]
                enemy = Rect_black(enemy1_img, enemy1_pos)
                enemies1.add(enemy)#右边的圆形

                new_x1 = int(SCREEN_WIDTH/2 -D_between/2-W_rect / 2)
                new_y1 = 0

                enemy1_pos = [new_x1, new_y1]
                enemy1 = Rect_black(enemy1_img, enemy1_pos)
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
        Check=None#每次记录都是未点击的
        #每一次都加进来了，所以一直都在记录数据
        #time.sleep(0.05)
        #记录每一次循环的鼠标位置
        biao_qian = {
            'x':x,
            'y':y,
            'time':time.time(),
            'check':Check,
        }

        mouse_l.append(biao_qian)
        #将所有的长度都拿出来
        if click_kz is not None:
            if M==9 and J==0 and click_kz[0] >= (SCREEN_WIDTH - 1) / 2-75 and click_kz[0] <= (SCREEN_WIDTH - 1) / 2+75:
                #写入文件，作为第一页
                mouse_l=[]#重新设定
                for enemy in enemies1:
                    enemies1.remove(enemy)
                I = 0
                IDENX=0
            elif J==1 :
                if (click_kz[0] >= int(SCREEN_WIDTH/2 +D_between/2- W_rect / 2) and click_kz[0] <= int(SCREEN_WIDTH/2 +D_between/2+ W_rect / 2) )or \
                    (click_kz[0] >= int(SCREEN_WIDTH/2 -D_between/2- W_rect / 2) and click_kz[0] <= int(SCREEN_WIDTH/2 -D_between/2+ W_rect / 2)):
                    Check = True
                    # 总体速度
                    x, y = pyg.position()
                    # print(x,y)
                    # 每次记录都是未点击的
                    # 每一次都加进来了，所以一直都在记录数据
                    # 记录每一次循环的鼠标位置
                    biao_qian = {
                        'x': x,
                        'y': y,
                        'time': time.time(),
                        'check': Check,
                    }
                    mouse_l.append(biao_qian)
                    # 添加元素，加入从出现到点击，若没有点击到位置则没有数据

                    # print(len(mouse_l['time']))
                    for i in range(len(mouse_l)):
                        worksheet.write(i + 1 + IDENX, 0, label=str(mouse_l[i]['time'] - cT))
                        worksheet.write(i + 1 + IDENX, 1, label=mouse_l[i]['x'])
                        worksheet.write(i + 1 + IDENX, 2, label=mouse_l[i]['y'])
                        worksheet.write(i + 1 + IDENX, 3, label=mouse_l[i]['check'])

                    CHI += 1
                    K += 1
                    mouse_l = []
                    # enemies1.remove(enemy)
                    IDENX=i+IDENX+1
                    I = 0
                    M -= 1  # 点击的次数

                elif (click_kz[0] <= int(SCREEN_WIDTH/2 +D_between/2- W_rect / 2) and click_kz[0] >= int(SCREEN_WIDTH/2 -D_between/2+ W_rect / 2)) or (click_kz[0] >= int(SCREEN_WIDTH/2 +D_between/2+ W_rect / 2) and click_kz[0]<SCREEN_WIDTH) or \
                        (click_kz[0] <= int(SCREEN_WIDTH/2 -D_between/2- W_rect / 2) and click_kz[0]>0):
                    Check = False
                    x, y = pyg.position()
                    # print(x,y)
                    # 每次记录都是未点击的
                    # 每一次都加进来了，所以一直都在记录数据
                    # 记录每一次循环的鼠标位置
                    biao_qian = {
                        'x': x,
                        'y': y,
                        'time': time.time(),
                        'check': Check,
                    }
                    mouse_l.append(biao_qian)
                    # 添加元素，加入从出现到点击，若没有点击到位置则没有数据

                    # print(len(mouse_l['time']))
                    for i in range(len(mouse_l)):
                        worksheet.write(i + 1 + IDENX, 0, label=str(mouse_l[i]['time'] - cT))
                        worksheet.write(i + 1 + IDENX, 1, label=mouse_l[i]['x'])
                        worksheet.write(i + 1 + IDENX, 2, label=mouse_l[i]['y'])
                        worksheet.write(i + 1 + IDENX, 3, label=mouse_l[i]['check'])

                    CHI += 1
                    K += 1
                    mouse_l = []
                    # enemies1.remove(enemy)
                    IDENX = i+IDENX+1
                    I = 0
                    M -= 1  # 点击的次数

    pos=name+'-'+str(int(time.time()))+'-实验数据.xls'
    workbook.save(pos)

    # 绘制游戏结束背景
    # 使用系统字体
    # 重新开始按钮
    screen.fill((255, 255, 255))
    img = pygame.image.load('resources/1.jpg')
    img = pygame.transform.scale(img, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(img, (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 8))

    # 返回设置

    textstart = xtfont.render('感谢参与实验', True, (0, 255, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 380
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
    img = pygame.image.load('resources/2.jpg')
    img = pygame.transform.scale(img, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(img, (SCREEN_WIDTH/4, SCREEN_HEIGHT/8))

    textstart = font_40.render('开始', True, (0, 180, 60))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen2.get_rect().centerx
    text_rect.centery = screen2.get_rect().centery + 600
    screen2.blit(textstart, text_rect)


    textstart = font_40.render('请输入姓名拼音：', True, (255, 0, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen2.get_rect().centerx - 150
    # 【横向位置，可根据自己需要调整】
    text_rect.centery = 1400
    # 【纵向位置，可根据自己需要调整】{注意：点击动作会受该参数影响，一下位置均可如此调整}
    screen2.blit(textstart, text_rect)
    #以上代码插入了一个标签在里面，后面的代码是一样的意

    input_box1 = pygame.Rect(screen2.get_rect().centerx + 50, 1380, 200, 50)
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
            input_box1 = pygame.Rect(screen.get_rect().centerx + 50, 1380, 200, 50)
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
                            and screen.get_rect().centery + 520 <= event.pos[1] \
                            and screen.get_rect().centery + 700 >= event.pos[1]:
                        #print('点到了按钮')
                        #绘制这个界面
                        startGame(event.pos)
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
                            begin = True
                            pygame.quit()
                            exit()

                    else:
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