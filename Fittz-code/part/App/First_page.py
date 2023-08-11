import pygame


def sou_ye(SCREEN_WIDTH, SCREEN_HEIGHT):
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


    # 使用系统字体
    font_18 = pygame.font.SysFont('华文中宋', 18)
    #不同大小
    font_40 = pygame.font.SysFont('华文中宋', 40)
    # 重新开始按钮
    textstart = font_18.render('移动速度', True, (255, 0, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen2.get_rect().centerx - 100
    # 【横向位置，可根据自己需要调整】
    text_rect.centery = 50 + 30
    # 【纵向位置，可根据自己需要调整】{注意：点击动作会受该参数影响，一下位置均可如此调整}
    screen2.blit(textstart, text_rect)
    #以上代码插入了一个标签在里面，后面的代码是一样的意思

    textstart = font_18.render('供给速度', True, (255, 0, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen2.get_rect().centerx - 100
    text_rect.centery = 130 + 30
    screen2.blit(textstart, text_rect)


    # 纽扣数量输入框，数据输入框
    input_box1 = pygame.Rect(screen2.get_rect().centerx + 50, 180, 140, 32)
    font = pygame.font.Font(None, 32)
    txt_surface = font.render(str('niukou_num'), True, (255,0,0))
    width = max(100, txt_surface.get_width() + 10)
    input_box1.w = width
    screen2.blit(txt_surface, (input_box1.x + 5, input_box1.y + 5))
    pygame.draw.rect(screen2, (255,0,0), input_box1, 2)

