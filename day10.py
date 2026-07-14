from turtle import distance

import pygame
import math
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Day 10")
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

        # 水平移动
        if self.x < target_x:
            self.x += self.speed

        elif self.x > target_x:
            self.x -= self.speed

        # x 到了以后再移动 y
        elif self.y < target_y:
            self.y += self.speed

        elif self.y > target_y:
            self.y -= self.speed

        # 到达目标点
        if self.x == target_x and self.y == target_y:
            self.target += 1

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
    

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.range = 150
        self.damage = 20

        self.fire_delay = 60
        self.cooldown = 0

        self.radius = 20

    def find_target(self, enemies):
        closest_enemy = None
        closest_distance = self.range

        for enemy in enemies:
            if enemy.is_dead():
                continue

            dx = enemy.x - self.x
            dy = enemy.y - self.y

            distance = math.sqrt(dx * dx + dy * dy)

            if distance <= closest_distance:
                closest_distance = distance
                closest_enemy = enemy

        return closest_enemy

    def attack(self, enemy):
        enemy.take_damage(self.damage)

    def update(self, enemies):
        if self.cooldown > 0:
            self.cooldown -= 1

        target = self.find_target(enemies)

        if target is not None and self.cooldown == 0:
            self.attack(target)
            self.cooldown = self.fire_delay

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (0, 100, 255),
            (int(self.x), int(self.y)),
            self.radius
        )



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
class WaveManager:
    def __init__(self):

        self.wave_number = 0


        self.enemies_to_spawn = 0


        self.spawn_timer = 0


        self.spawn_interval = 60


        self.wave_complete = True


        self.between_wave_timer = 180

        self.between_wave_delay = 180

    def start_next_wave(self):
        # 波数加一
        self.wave_number += 1


        self.enemies_to_spawn = 3 + self.wave_number * 2

        self.wave_complete = False

        self.spawn_timer = 0

        print(
            f"Wave {self.wave_number} started! "
            f"Enemies: {self.enemies_to_spawn}"
        )

    def update(self, enemies):
        if self.wave_complete:
            self.between_wave_timer -= 1

            if self.between_wave_timer <= 0:
                self.start_next_wave()
                self.between_wave_timer = self.between_wave_delay

            return

        if self.enemies_to_spawn > 0:
            self.spawn_timer -= 1

            if self.spawn_timer <= 0:
                enemies.append(Enemy())

                self.enemies_to_spawn -= 1
                self.spawn_timer = self.spawn_interval

        elif len(enemies) == 0:
            self.wave_complete = True
            self.between_wave_timer = self.between_wave_delay

            print(f"Wave {self.wave_number} complete!")
towers = []
running = True
enemies = []
wave_manager = WaveManager()
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

                if MAP[row][col] == 0:
                    tower_x = col * TILE_SIZE + TILE_SIZE // 2
                    tower_y = row * TILE_SIZE + TILE_SIZE // 2

                    towers.append(Tower(tower_x, tower_y))
    wave_manager.update(enemies)
    for enemy in enemies:
        enemy.update()
    for tower in towers:
        tower.update(enemies)   
    enemies = [
        enemy for enemy in enemies
        if not enemy.is_dead()
    ]
    screen.fill(BLACK)   
    draw_map()
    for enemy in enemies:
        enemy.draw(screen)
    for tower in towers:
        tower.draw(screen)
    pygame.display.flip()

pygame.quit()