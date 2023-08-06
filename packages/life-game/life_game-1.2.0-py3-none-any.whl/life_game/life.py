#!python3
# -*- coding: utf-8 -*-
'''
@name: life
@author: Memory
@date: 2018/11/19
@document: {"F11": 全屏,
            "空格": 暂停游戏,
            "点击": 复活或者杀死一个生命
            }
'''
import pygame
from sys import exit
from random import randint

SCREEN_SIZE = (500, 500)                                                # 屏幕的尺寸
NEIGH = [(0, 1), (1, 0), (0, -1), (-1, 0),                              # 八个相邻点
        (1, 1), (1, -1), (-1, 1), (-1, -1)]
FPS = 20                                                                # 帧率
COLOR = [0xff0000, 0x00ff00, 0x0000ff, 0xffff00, 0xff00ff, 0x00ffff]    # 颜色


class World(object):
    def __init__(self, screen, rows):
        self.screen = screen                                            # 屏幕
        self.rows = rows                                                # 一条边小格子数量
        self.side = screen.get_width() // rows                          # 小格子的边长
        self.lifes = [[False for i in range(rows)] for j in range(rows)]# 生命，True 是活，False 是死
        self.init_lifes()

    def init_lifes(self):                                               # 初始化，随机生成一些生命
        t = self.rows // 3                                              # 控制范围
        for i in range(t, 2*t):
            for j in range(t, 2*t):
                if randint(1, 5) == 1:
                    self.lifes[i][j] = True                             # 设置为活的

    def reverse(self, x, y):                                            # 翻转，死的活，活的死
        i = x // self.side
        j = y // self.side
        if i < 0 or j < 0 or i >= self.rows or j >= self.rows:
            return
        self.lifes[i][j] = not self.lifes[i][j]
        rect = pygame.Rect(i*self.side, j*self.side, self.side, self.side)
        if self.lifes[i][j]:
            self.screen.fill(COLOR[randint(0, len(COLOR)-1)], rect)
        else:
            self.screen.fill((0, 0, 0), rect)
        pygame.display.update(rect)

    def neigh_num(self, x, y):                                          # 有几个邻居
        num = 0
        for i in NEIGH:
            tx = x + i[0]
            ty = y + i[1]
            if tx > 0 and ty > 0 and tx < self.rows and ty < self.rows:
                if self.lifes[tx][ty]:
                    num += 1
        return num

    def update(self):                                                   # 根据有几个邻居更新生命
        temp_lifes = [[False for i in range(self.rows)] for j in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.rows):
                num = self.neigh_num(i, j)
                if num == 3:                                            # 3个邻居为活
                    temp_lifes[i][j] = True
                elif num == 2:                                          # 两个邻居保持现状
                    temp_lifes[i][j] = self.lifes[i][j]                 # 其他情况全死

        self.lifes = temp_lifes

    def draw(self):                                                     # 绘制
        self.screen.fill((0, 0, 0))                                     # 背景
        for i in range(self.rows):
            for j in range(self.rows):
                if self.lifes[i][j]:                                    # 绘制活的
                    rect = pygame.Rect(i*self.side, j*self.side, self.side, self.side)
                    self.screen.fill(COLOR[randint(0, len(COLOR)-1)], rect)

        pygame.display.update()                                         # 刷新屏幕


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    pygame.display.set_caption("life")

    world = World(screen, 50)
    fps = pygame.time.Clock()
    Fullscreen = False
    pause = False
    num = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                               # 退出游戏
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:                           # F11全屏
                    Fullscreen = not Fullscreen
                    if Fullscreen:
                        screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN, 32)
                    else:
                        screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
                elif event.key == pygame.K_SPACE:                       # 空格暂停
                    pause = not pause
            if event.type == pygame.MOUSEBUTTONDOWN:                    # 左键点击，翻转生命
                if event.button == 1:
                    world.reverse(*event.pos)                           # 传入鼠标的坐标

        if num == 0 and not pause:                                      # 更新状态
            world.update()
            world.draw()
        fps.tick(FPS)
        num = (num + 1) % int((1.5 * FPS))                              # 控制更新速度，目前是1.5秒


if __name__ == '__main__':
    main()
