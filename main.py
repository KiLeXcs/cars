import pygame
import random as rand

class Colors():
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 128, 255)

#params
WIDTH = 480
HEIGHT = 480
FPS = 60
running = True
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cars")
font = pygame.font.SysFont("Arial", 32)
clock = pygame.time.Clock()

class Player():
    x = 230
    y = 230
    speed = 3
    length = 20
    
class Obstacles():
    length = rand.randint(5,45)
    speed = 0
    while speed == 0:
        speed = rand.randint(-6, 6)
    direction = rand.randint(0,1)
    if direction:
        y = rand.randint(0,HEIGHT-length)
        if speed > 0:
            x = -length
        else:
            x = WIDTH
    else:
        x = rand.randint(0,WIDTH-length)
        if speed > 0:
            y = -length
        else:
            y = HEIGHT

while running:
    #quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(Colors.black)

    #obstacles moving
    if Obstacles.direction:
        if Obstacles.x + Obstacles.speed > -Obstacles.length and Obstacles.x + Obstacles.speed < WIDTH:
            Obstacles.x += Obstacles.speed
        else:
            Obstacles.x = WIDTH//2
    else:
        if Obstacles.y + Obstacles.speed > -Obstacles.length and Obstacles.y + Obstacles.speed < HEIGHT:
            Obstacles.y += Obstacles.speed
        else:
            Obstacles.y = HEIGHT//2
    
    #player moving
    pressed = pygame.key.get_pressed()
    if (pressed[pygame.K_UP] or pressed[pygame.K_w]):
        if Player.y - Player.speed > 5: 
            Player.y -= Player.speed
        else:
            Player.y = 5
    if (pressed[pygame.K_DOWN] or pressed[pygame.K_s]): 
        if Player.y + Player.speed < HEIGHT - Player.length - 5: 
            Player.y += Player.speed
        else:
            Player.y = HEIGHT - Player.length - 5
    if (pressed[pygame.K_LEFT] or pressed[pygame.K_a]): 
        if Player.x - Player.speed > 5: 
            Player.x -= Player.speed
        else:
            Player.x = 5
    if (pressed[pygame.K_RIGHT] or pressed[pygame.K_d]): 
        if Player.x + Player.speed < WIDTH - Player.length - 5: 
            Player.x += Player.speed
        else:
            Player.x = WIDTH - Player.length - 5

    #draw
    pygame.draw.rect(screen, Colors.blue, pygame.Rect(Player.x, Player.y, Player.length, Player.length))
    pygame.draw.rect(screen, Colors.red, pygame.Rect(Obstacles.x, Obstacles.y, Obstacles.length, Obstacles.length))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()