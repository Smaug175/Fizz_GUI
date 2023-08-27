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
