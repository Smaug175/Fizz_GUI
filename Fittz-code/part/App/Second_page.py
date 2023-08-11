import pygame


def second_page(SCREEN_WIDTH, SCREEN_HEIGHT):
    #第二屏
    screen3 = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # 绘制背景
    screen3.fill([255,255,255])

    img = pygame.image.load('../XXX/resources/red.png')
    img = pygame.transform.scale(img, (150, 150))
    xtfont = pygame.font.SysFont('华文中宋', 40)

    textstart = xtfont.render('请移动鼠标至起始点，点击左键后开始实验', True, (0, 0, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen3.get_rect().centerx  # 【横向位置，可根据自己需要调整】
    text_rect.centery = 50 + 30  # 【纵向位置，可根据自己需要调整】{注意：点击动作会受该参数影响，一下位置均可如此调整}
    screen3.blit(img, (100, (SCREEN_HEIGHT-1)/2))
    screen3.blit(textstart, text_rect)
