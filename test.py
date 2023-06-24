import pygame
import random

# 初始化游戏
pygame.init()

# 定义游戏窗口的宽度和高度
window_width = 800
window_height = 600

# 定义贪吃蛇和食物的大小
snake_size = 20
food_size = 20

# 定义颜色
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# 创建游戏窗口
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('贪吃蛇游戏')

clock = pygame.time.Clock()

# 定义贪吃蛇的初始位置和速度
snake_head = [window_width / 2, window_height / 2]
snake_body = [[window_width / 2, window_height / 2], [window_width / 2, window_height / 2], [window_width / 2, window_height / 2]]
snake_speed = 20
direction = 'RIGHT'

# 定义食物的初始位置
food_pos = [random.randrange(1, (window_width // food_size)) * food_size,
            random.randrange(1, (window_height // food_size)) * food_size]

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 监听键盘事件，改变贪吃蛇的方向
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'

    # 根据方向移动贪吃蛇的头部
    if direction == 'UP':
        snake_head[1] = snake_head[1]-snake_speed
    elif direction == 'DOWN':
        snake_head[1] += snake_speed
    elif direction == 'LEFT':
        snake_head[0] -= snake_speed
    elif direction == 'RIGHT':
        snake_head[0] += snake_speed

    # 检查贪吃蛇是否吃到了食物
    if snake_head[0] == food_pos[0] and snake_head[1] == food_pos[1]:
        food_pos = [random.randrange(1, (window_width // food_size)) * food_size,
                    random.randrange(1, (window_height // food_size)) * food_size]
    else:
        snake_body.pop()

    # 将贪吃蛇的新头部加入到身体中
    snake_body.insert(0, list(snake_head))

    # 绘制游戏窗口
    window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(window, white, pygame.Rect(pos[0], pos[1], snake_size, snake_size))
    pygame.draw.rect(window, red, pygame.Rect(food_pos[0], food_pos[1], food_size, food_size))

    # 检查贪吃蛇是否碰到了边界或自身
    if snake_head[0] < 0 or snake_head[0] >= window_width or snake_head[1] < 0 or snake_head[1] >= window_height:
        running = False
    if snake_head in snake_body[1:]:
        running = False

    pygame.display.flip()
    clock.tick(10)

# 退出游戏
pygame.quit()
