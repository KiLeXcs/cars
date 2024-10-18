import pygame
import os
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
MENU = 75
FPS = 60
num_enemy = 12
running = True
score = 0
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + MENU))
pygame.display.set_caption("Cars")
game_dir = os.path.dirname(os.path.abspath(__file__))
font_nataliza = os.path.join(game_dir, 'nasaliza.ttf')
font = pygame.font.Font(font_nataliza, 32)
clock = pygame.time.Clock()

def refresh():
    screen.fill(Colors.black)
    pygame.draw.rect(screen, Colors.blue, pygame.Rect(Player.x, Player.y, Player.length, Player.length))
    for obstacle in obstacles:
        pygame.draw.rect(screen, Colors.red, pygame.Rect(obstacle.x, obstacle.y, obstacle.length, obstacle.length))
    pygame.draw.rect(screen, Colors.black, pygame.Rect(0, HEIGHT, WIDTH, MENU))
    pygame.draw.rect(screen, Colors.blue, pygame.Rect(0, HEIGHT, WIDTH, 5))
    text_score = font.render(str(score), True, Colors.blue)
    text_rect_score = text_score.get_rect(center = (WIDTH // 2, HEIGHT + 30))
    screen.blit(text_score, text_rect_score)
    pygame.display.flip()
    clock.tick(FPS)

class Player():
    x = 230
    y = 230
    speed = 3
    length = 20

    def refresh():
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

class Obstacles():

    def __init__(self):
        self.spawn_obstacle()

    def spawn_obstacle(self):
        self.length = rand.randint(5, 45)
        self.speed = 0
        while self.speed == 0:
            self.speed = rand.randint(-6, 6)
        self.direction = rand.randint(0, 1)
        if self.direction:
            self.y = rand.randint(0, HEIGHT - self.length)
            if self.speed > 0:
                self.x = -self.length
            else:
                self.x = WIDTH
        else:
            self.x = rand.randint(0, WIDTH - self.length)
            if self.speed > 0:
                self.y = -self.length
            else:
                self.y = HEIGHT

    def move(self):
        global score
        if self.direction:
            self.x += self.speed
            if self.x > WIDTH or self.x < -self.length:
                score += self.length * 10
                self.spawn_obstacle()
        else:
            self.y += self.speed
            if self.y > HEIGHT or self.y < -self.length:
                score += self.length * 10
                self.spawn_obstacle()


obstacles = []
for i in range(num_enemy):
    obstacle = Obstacles()
    obstacles.append(obstacle)

while running:
    #quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #obstacles moving
    for obstacle in obstacles:
        obstacle.move()
    
    #player moving
    Player.refresh()

    #draw
    refresh()

pygame.quit()