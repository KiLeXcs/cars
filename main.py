import pygame
import random as rand

WIDTH = 480
HEIGHT = 480
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cars")
clock = pygame.time.Clock()

class Player():
    x = 230
    y = 230
    length = 20

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(BLACK)

    pressed = pygame.key.get_pressed()
    if (pressed[pygame.K_UP] or pressed[pygame.K_w]) and Player.y > 5: 
        Player.y -= 3
    if (pressed[pygame.K_DOWN] or pressed[pygame.K_s]) and Player.y < HEIGHT - Player.length - 5: 
        Player.y += 3
    if (pressed[pygame.K_LEFT] or pressed[pygame.K_a]) and Player.x > 5: 
        Player.x -= 3
    if (pressed[pygame.K_RIGHT] or pressed[pygame.K_d]) and Player.x < WIDTH - Player.length - 5: 
        Player.x += 3

    pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(Player.x, Player.y, Player.length, Player.length))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()