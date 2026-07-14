import pygame
import random
# 初始化 Pygame
pygame.init()
font=pygame.font.Font(None, 36)
# 创建窗口
screen = pygame.display.set_mode((800, 600))
a=0
# 设置窗口标题
pygame.display.set_caption("Tower Defense")
key=pygame.key.get_pressed()
# 游戏是否继续运行
running = True

# 游戏主循环
while running:
    color = (
    random.randint(0,255),
    random.randint(0,255),
    random.randint(0,255)
    )
    # 检测事件
    for event in pygame.event.get():
        pygame.draw.rect(screen, (0, 0, 0), (100, 100, 50, 50))
        text = font.render(str(a), True, (255,255,255))
        screen.blit(text, (100,100))
        # 点击右上角 X
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                a+=1
                x, y = event.pos
                pygame.draw.circle(screen, color, (x, y), 20)
            elif event.button == 3:
                a=0
                screen.fill((0, 0, 0))

    # 更新屏幕
    
    pygame.display.flip()

# 退出
pygame.quit()