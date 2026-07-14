import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("弹球游戏")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
xl=0
yl=250
xr=800
yr=250
xb=400
yb=300
xdx=2
ydy=2
ball_radius=20
score=0
running = True
while running:
    clock.tick(60)  # FPS
    xb+=xdx
    yb+=ydy
    if yb>=580 or yb<=20:
        ydy *= -1
    ball_rect = pygame.Rect(xb - 10, yb - 10, 20, 20)
    left_paddle = pygame.Rect(10, yl, 10, 100)
    right_paddle = pygame.Rect(790, yr, 10, 100)
    if ball_rect.colliderect(left_paddle):
        xdx = abs(xdx)
        score += 1
    if ball_rect.colliderect(right_paddle):
        xdx = -abs(xdx)
        score += 1
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if keys[pygame.K_w] and yl>0:
            yl -= 10
        if keys[pygame.K_s] and yl<500:
            yl += 10
        if keys[pygame.K_i] and yr>0:
            yr -= 10
        if keys[pygame.K_k] and yr<500:
            yr += 10
        if keys[pygame.K_r]:
            score=0
            xl=0
            yl=250
            xr=800
            yr=250
            xb=400
            yb=300
    screen.fill((0, 0, 0))  # 清屏，黑色背景
    if xb < 0 or xb > 800:
        score=0
        line1 = font.render("You Lose!", True, (255,255,255))
        line2 = font.render(f"Score: {score}", True, (255,255,255))
        line3 = font.render("Press 'R' to Restart", True, (255,255,255))
        screen.blit(line1, (300,250))
        screen.blit(line2, (300,300))
        screen.blit(line3, (300,350))
    else:
        text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        pygame.draw.circle(screen, (255, 255, 255), (xb, yb), ball_radius)
        pygame.draw.rect(screen, (255, 0, 0), (xl, yl, 10, 100))
        pygame.draw.rect(screen, (255, 0, 0), (xr-10, yr, 10, 100))
    pygame.display.update()


pygame.quit()