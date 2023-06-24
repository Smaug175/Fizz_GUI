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