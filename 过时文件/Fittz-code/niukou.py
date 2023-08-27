import pygame
import datetime
import random

class NiuKou(pygame.sprite.Sprite):
    def __init__(self, enemy_img,  init_pos, speed):
        #print('init_pos', init_pos)
        pygame.sprite.Sprite.__init__(self)

        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = int(speed)
        self.down_index = 0
        self.start_time = datetime.datetime.now()

    # 扣子移动，边界判断及删除在游戏主循环里处理
    def move(self):
        pass
        #self.rect.left -= self.speed

