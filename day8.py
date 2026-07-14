from turtle import distance

import pygame
import math
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Day 8 - Grid Map")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
GREEN = (80, 180, 100)
DARK_GREEN = (40, 120, 60)
GRAY = (120, 120, 120)
BLUE = (80, 160, 255)
WHITE = (255, 255, 255)
TILE_SIZE = 60
MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
]
PATH = [
    (0,0),
    (11,0),
    (11,3),
    (1,3),
    (1,6),
    (11,6),
    (11,9),
    (1,9)
]
class Enemy:

    def __init__(self):
        # 出生点
        self.x = PATH[0][0] * TILE_SIZE + TILE_SIZE // 2
        self.y = PATH[0][1] * TILE_SIZE + TILE_SIZE // 2
        # 血量
        self.hp = 100
        # 移动速度
        self.speed = 2
        # 半径
        self.radius = 15

        # 正在前往 PATH 的第几个点
        self.target = 1

        # 是否到终点
        self.finished = False

    def update(self):

        # 已经到终点
        if self.finished:
            return

        # 已经走完整条路
        if self.target >= len(PATH):
            self.finished = True
            return

        target_x = PATH[self.target][0] * TILE_SIZE + TILE_SIZE // 2
        target_y = PATH[self.target][1] * TILE_SIZE + TILE_SIZE // 2

        dx = target_x - self.x
        dy = target_y - self.y

        distance = math.sqrt(dx * dx + dy * dy)

        # 到达当前目标点
        if distance < self.speed:

            self.x = target_x
            self.y = target_y

            self.target += 1

        else:

            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed

    # ==========================
    # 绘制
    # ==========================
    def draw(self, screen):

        pygame.draw.circle(
            screen,
            (255,0,0),
            (int(self.x), int(self.y)),
            self.radius
        )

    # ==========================
    # 扣血
    # ==========================
    def take_damage(self, damage):

        self.hp -= damage

    # ==========================
    # 是否死亡
    # ==========================
    def is_dead(self):

        return self.hp <= 0

    # ==========================
    # 是否走到终点
    # ==========================
    def reached_end(self):

        return self.finished
def draw_map():
    for row in range(len(MAP)):
        for col in range(len(MAP[row])):
            x = col * TILE_SIZE
            y = row * TILE_SIZE

            if MAP[row][col] == 0:
                color = GREEN
            else:
                color = GRAY

            pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, DARK_GREEN, (x, y, TILE_SIZE, TILE_SIZE), 1)
def draw_towers(towers):
    for col, row in towers:
        center_x = col * TILE_SIZE + TILE_SIZE // 2
        center_y = row * TILE_SIZE + TILE_SIZE // 2

        pygame.draw.circle(screen, BLUE, (center_x, center_y), 20)
towers = []
running = True
enemy = Enemy()
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 鼠标左键点击放塔
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos

                col = mouse_x // TILE_SIZE
                row = mouse_y // TILE_SIZE

                # 防止点到地图外
                if 0 <= row < len(MAP) and 0 <= col < len(MAP[row]):

                    # 只能在草地放塔
                    if MAP[row][col] == 0 and (col, row) not in towers:
                        towers.append((col, row))
    screen.fill(BLACK)

    draw_map()
    draw_towers(towers)
    enemy.update()
    enemy.draw(screen)
    pygame.display.flip()

pygame.quit()