import pygame
import math

# 初始化 Pygame 的显示、字体、声音等模块
pygame.init()


# =========================================================
# 窗口与时间控制
# =========================================================

# 创建一个 800 × 600 的游戏窗口
screen = pygame.display.set_mode((800, 600))

# 设置窗口标题
pygame.display.set_caption("Day 9")

# Clock 用来控制游戏帧率
clock = pygame.time.Clock()


# =========================================================
# 颜色常量
# RGB 格式：(红, 绿, 蓝)，每个数字范围为 0～255
# =========================================================

BLACK = (0, 0, 0)
GREEN = (80, 180, 100)
DARK_GREEN = (40, 120, 60)
GRAY = (120, 120, 120)
BLUE = (80, 160, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


# 每个地图格子的宽和高都是 60 像素
TILE_SIZE = 60


# =========================================================
# 地图数据
#
# 1 = 道路，敌人可以走，不能建塔
# 0 = 草地，可以建塔
#
# MAP[row][col]
# row 是行，也就是 y 方向
# col 是列，也就是 x 方向
# =========================================================

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


# =========================================================
# 敌人路径
#
# 每一个元组格式都是：
# (列 col, 行 row)
#
# 这些点只写路径的拐点，不需要把每一个格子都列出来
# =========================================================

PATH = [
    (0, 0),     # 出生点
    (11, 0),    # 向右
    (11, 3),    # 向下
    (1, 3),     # 向左
    (1, 6),     # 向下
    (11, 6),    # 向右
    (11, 9),    # 向下
    (1, 9)      # 向左，到达终点
]


# =========================================================
# Enemy 类
#
# 每一个 Enemy 对象都有自己的：
# x、y、血量、速度、半径、当前路径目标
# =========================================================

class Enemy:

    def __init__(self):
        """
        __init__ 会在 Enemy() 被创建时自动运行。
        用于给敌人设置初始数据。
        """

        # PATH[0] 是敌人的出生格子
        start_col = PATH[0][0]
        start_row = PATH[0][1]

        # 把格子坐标转换成像素坐标
        # + TILE_SIZE // 2 是为了让敌人出现在格子中心
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2

        # 敌人的初始血量
        self.hp = 100

        # 每一帧移动 2 个像素
        self.speed = 2

        # 敌人圆形的半径
        self.radius = 15

        # PATH[0] 是出生点，所以第一个目标是 PATH[1]
        self.target = 1

        # 是否已经走完整条路径
        self.finished = False

    def update(self):
        """
        每一帧更新敌人的位置。
        敌人会朝 PATH 中当前的目标点移动。
        """

        # 如果已经走到终点，就不再移动
        if self.finished:
            return

        # 如果目标编号已经超过 PATH 的长度，
        # 说明敌人走完整条路径了
        if self.target >= len(PATH):
            self.finished = True
            return

        # 取出当前目标格子的列和行
        target_col = PATH[self.target][0]
        target_row = PATH[self.target][1]

        # 把目标格子转换成屏幕像素坐标
        target_x = target_col * TILE_SIZE + TILE_SIZE // 2
        target_y = target_row * TILE_SIZE + TILE_SIZE // 2

        # 目标位置与敌人当前位置之间的差值
        dx = target_x - self.x
        dy = target_y - self.y

        # 使用勾股定理计算敌人与目标点之间的直线距离
        distance = math.sqrt(dx * dx + dy * dy)

        # 如果剩余距离已经小于或等于一步的移动距离，
        # 就直接把敌人放到目标点上，防止越过目标
        if distance <= self.speed:
            self.x = target_x
            self.y = target_y

            # 切换到 PATH 中的下一个目标点
            self.target += 1

        else:
            # dx / distance 是 x 方向的单位方向
            # dy / distance 是 y 方向的单位方向
            #
            # 再乘 speed，就得到这一帧应该移动多少
            self.x += dx / distance * self.speed
            self.y += dy / distance * self.speed

    def draw(self, screen):
        """
        把敌人画到屏幕上。
        """

        pygame.draw.circle(
            screen,                         # 画到哪个 Surface 上
            RED,                            # 敌人的颜色
            (int(self.x), int(self.y)),      # 敌人的圆心坐标
            self.radius                     # 敌人半径
        )

    def take_damage(self, damage):
        """
        敌人受到伤害。
        """

        self.hp -= damage

    def is_dead(self):
        """
        判断敌人是否死亡。

        返回 True：敌人血量小于或等于 0
        返回 False：敌人还活着
        """

        return self.hp <= 0

    def reached_end(self):
        """
        判断敌人是否已经走到路径终点。
        """

        return self.finished


# =========================================================
# Tower 类
#
# 每一个 Tower 对象都有自己的：
# 位置、攻击范围、伤害、攻击速度和冷却时间
# =========================================================

class Tower:

    def __init__(self, x, y):
        """
        创建塔时传入塔在屏幕上的 x、y 像素坐标。
        """

        # 塔的中心位置
        self.x = x
        self.y = y

        # 塔的攻击范围，单位是像素
        self.range = 150

        # 每次攻击造成的伤害
        self.damage = 20

        # 每次攻击之后需要等待多少帧
        # 游戏是 60 FPS，所以 60 帧大约是 1 秒
        self.fire_delay = 60

        # 当前剩余冷却时间
        # 0 表示现在可以攻击
        self.cooldown = 0

        # 塔在画面中的圆形半径
        self.radius = 20

    def find_target(self, enemies):
        """
        从 enemies 列表里寻找攻击范围内最近的敌人。

        返回：
        找到了 -> 返回那个 Enemy 对象
        没找到 -> 返回 None
        """

        # 一开始还没有找到敌人
        closest_enemy = None

        # 最近距离先设置为攻击范围
        # 只有比这个距离更近的敌人才会被选中
        closest_distance = self.range

        # 一个一个检查敌人
        for enemy in enemies:

            # 如果敌人已经死亡，就跳过这个敌人
            if enemy.is_dead():
                continue

            # 敌人与塔之间的 x、y 距离
            dx = enemy.x - self.x
            dy = enemy.y - self.y

            # 使用勾股定理算出实际距离
            distance = math.sqrt(dx * dx + dy * dy)

            # 如果这个敌人在攻击范围内，
            # 并且比之前找到的敌人更近
            if distance <= closest_distance:
                closest_distance = distance
                closest_enemy = enemy

        # 把找到的敌人返回给 update()
        # 如果没找到，返回的就是 None
        return closest_enemy

    def attack(self, enemy):
        """
        对指定的 enemy 造成伤害。
        """

        enemy.take_damage(self.damage)

        # 调试时可以打开这一句观察攻击结果
        print(f"Tower attacked! Enemy HP: {enemy.hp}")

    def update(self, enemies):
        """
        每一帧更新塔。

        主要负责：
        1. 减少攻击冷却
        2. 寻找敌人
        3. 冷却结束后攻击
        """

        # 如果还在冷却，就每一帧减 1
        if self.cooldown > 0:
            self.cooldown -= 1

        # 寻找攻击范围内最近的敌人
        target = self.find_target(enemies)

        # 必须同时满足：
        # 1. 找到了敌人
        # 2. 冷却时间已经归零
        if target is not None and self.cooldown == 0:

            # 攻击目标
            self.attack(target)

            # 攻击后重新进入冷却
            self.cooldown = self.fire_delay

    def draw(self, screen):
        """
        把塔画到屏幕上。
        """

        # 画塔本体
        pygame.draw.circle(
            screen,
            BLUE,
            (int(self.x), int(self.y)),
            self.radius
        )

        # 画攻击范围圈
        # 最后一个参数 1 表示只画 1 像素宽的圆边框
        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.x), int(self.y)),
            self.range,
            1
        )


# =========================================================
# 地图绘制函数
# =========================================================

def draw_map():
    """
    遍历二维 MAP，把每一个格子画到屏幕上。
    """

    # 遍历每一行
    for row in range(len(MAP)):

        # 遍历这一行中的每一列
        for col in range(len(MAP[row])):

            # 把格子编号转换成像素坐标
            x = col * TILE_SIZE
            y = row * TILE_SIZE

            # 0 是草地，1 是道路
            if MAP[row][col] == 0:
                color = GREEN
            else:
                color = GRAY

            # 画格子的背景颜色
            pygame.draw.rect(
                screen,
                color,
                (x, y, TILE_SIZE, TILE_SIZE)
            )

            # 画格子的边框
            # 最后的 1 表示边框宽度为 1 像素
            pygame.draw.rect(
                screen,
                DARK_GREEN,
                (x, y, TILE_SIZE, TILE_SIZE),
                1
            )


# =========================================================
# 游戏初始数据
# =========================================================

# 存放所有塔对象
towers = []

# 存放所有敌人对象
# 现在先生成一个敌人
enemies = [Enemy()]

# 控制游戏主循环
running = True




while running:

    # 把游戏限制为每秒最多 60 帧
    clock.tick(60)

    # -----------------------------------------------------
    # 处理事件
    # -----------------------------------------------------

    for event in pygame.event.get():

        # 点击窗口右上角 X
        if event.type == pygame.QUIT:
            running = False

        # 检测鼠标按下事件
        if event.type == pygame.MOUSEBUTTONDOWN:


            if event.button == 1:


                mouse_x, mouse_y = event.pos

                # 把鼠标像素坐标转换成地图格子坐标
                col = mouse_x // TILE_SIZE
                row = mouse_y // TILE_SIZE

                # 确保鼠标点击的位置没有超出 MAP
                if (
                    0 <= row < len(MAP)
                    and 0 <= col < len(MAP[row])
                ):

                    # 只有草地格子才能建塔
                    if MAP[row][col] == 0:

                        tower_x = col * TILE_SIZE + TILE_SIZE // 2
                        tower_y = row * TILE_SIZE + TILE_SIZE // 2

                        # 创建一个新的 Tower 对象，
                        # 然后加入 towers 列表
                        towers.append(Tower(tower_x, tower_y))


    for enemy in enemies:
        enemy.update()

    # 更新每一座塔，让塔自动寻找并攻击敌人
    for tower in towers:
        tower.update(enemies)

    # 删除已经死亡或者已经走到终点的敌人
    enemies = [
        enemy
        for enemy in enemies
        if not enemy.is_dead() and not enemy.reached_end()
    ]


    screen.fill(BLACK)

    draw_map()

    # 画所有敌人
    for enemy in enemies:
        enemy.draw(screen)

    # 画所有塔
    for tower in towers:
        tower.draw(screen)

    # 把这一帧真正显示到窗口上
    pygame.display.flip()


# 结束 Pygame，释放资源
pygame.quit()