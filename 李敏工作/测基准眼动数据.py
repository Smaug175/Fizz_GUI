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