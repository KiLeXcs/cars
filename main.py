import pygame
import time
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
playing = False
score = -1
timer = 0
player_crash_x, player_crash_y, player_crush_length = 0, 0, 0
obstacle_crush_x, obstacle_crush_y, obstacle_crush_length = 0, 0, 0
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + MENU))
pygame.display.set_caption("Star slider")
game_dir = os.path.dirname(os.path.abspath(__file__))
font_nataliza = os.path.join(game_dir, 'nasaliza.ttf')
font_32 = pygame.font.Font(font_nataliza, 32)
font_64 = pygame.font.Font(font_nataliza, 64)
clock = pygame.time.Clock()

class Menu():
    
    color_play_sign = Colors.blue
    color_best_score_text = Colors.blue
    color_world_score_text= Colors.blue
    color_settings_text = Colors.blue
    color_score_text = Colors.black
    def refresh_menu():
        global timer
        
        #last crush
        global player_crash_x, player_crash_y, player_crush_length, obstacle_crush_x, obstacle_crush_y, obstacle_crush_length
        pygame.draw.rect(screen, Colors.blue, pygame.Rect(player_crash_x, player_crash_y, player_crush_length, player_crush_length))
        pygame.draw.rect(screen, Colors.red, pygame.Rect(obstacle_crush_x, obstacle_crush_y, obstacle_crush_length, obstacle_crush_length))
        
        #some texts
        text_menu_name = font_64.render("Star slider", True, Colors.blue)
        text_rect_menu_name = text_menu_name.get_rect(center = (WIDTH // 2, 110))
        screen.blit(text_menu_name, text_rect_menu_name)
        
        text_menu_your_score = font_32.render("Best score", True, Menu.color_best_score_text)
        text_rect_menu_your_score = text_menu_your_score.get_rect(center = (WIDTH // 2, 400))
        screen.blit(text_menu_your_score, text_rect_menu_your_score)
        
        text_menu_world_score = font_32.render("World records", True, Menu.color_world_score_text)
        text_rect_menu_world_score = text_menu_world_score.get_rect(center = (WIDTH // 2, 450))
        screen.blit(text_menu_world_score, text_rect_menu_world_score)
        
        text_menu_settings = font_32.render("Settings", True, Menu.color_settings_text)
        text_rect_menu_settings = text_menu_settings.get_rect(center = (WIDTH // 2, 500))
        screen.blit(text_menu_settings, text_rect_menu_settings)
        
        text_menu_score = font_32.render(f"Your score: {score}", True, Menu.color_score_text)
        text_rect_menu_score = text_menu_score.get_rect(center = (WIDTH // 2, 350))
        screen.blit(text_menu_score, text_rect_menu_score)
        
        if score != -1 and (time.time() - timer <= 0.4 or 0.8 <= time.time() - timer <= 1.2 or 1.6 <= time.time() - timer <= 2 or time.time() - timer >= 2.4):
            Menu.color_score_text = Colors.blue
        else:
            Menu.color_score_text = Colors.black
        
        #draw play sign
        pygame.draw.line(screen, Menu.color_play_sign, [(WIDTH - 100)//2, (HEIGHT - MENU)//2], [(WIDTH + 100)//2, (HEIGHT - MENU + 100)//2], 10)
        pygame.draw.line(screen, Menu.color_play_sign, [(WIDTH + 100)//2, (HEIGHT - MENU + 100)//2], [(WIDTH - 100)//2, (HEIGHT - MENU + 200)//2], 10)
        pygame.draw.line(screen, Menu.color_play_sign, [(WIDTH - 92)//2, (HEIGHT - MENU + 200)//2], [(WIDTH - 92)//2, (HEIGHT - MENU + 50)//2], 10)
        
        pygame.display.flip()
        clock.tick(FPS)

def mouse_coordinates():
    
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if mouse_x >= 157 and mouse_x <= 323 and mouse_y >= 390 and mouse_y <= 410:
        Menu.color_best_score_text = Colors.white
    else:
        Menu.color_best_score_text = Colors.blue
    
    if mouse_x >= 119 and mouse_x <= 361 and mouse_y >= 440 and mouse_y <= 460:
        Menu.color_world_score_text = Colors.white
    else:
        Menu.color_world_score_text = Colors.blue
        
    if mouse_x >= 178 and mouse_x <= 303 and mouse_y >= 490 and mouse_y <= 510:
        Menu.color_settings_text = Colors.white
    else:
        Menu.color_settings_text = Colors.blue
    
    if mouse_x >= 180 and mouse_x <= 300 and mouse_y >= 190 and mouse_y <= 320:
        Menu.color_play_sign = Colors.white
    else:
        Menu.color_play_sign = Colors.blue

def refresh_play():
    screen.fill(Colors.black)
    pygame.draw.rect(screen, Colors.blue, pygame.Rect(Player.x, Player.y, Player.length, Player.length))
    for obstacle in obstacles:
        pygame.draw.rect(screen, Colors.red, pygame.Rect(obstacle.x, obstacle.y, obstacle.length, obstacle.length))
    pygame.draw.rect(screen, Colors.black, pygame.Rect(0, HEIGHT, WIDTH, MENU))
    pygame.draw.rect(screen, Colors.blue, pygame.Rect(0, HEIGHT, WIDTH, 5))
    text_score = font_32.render(str(score), True, Colors.blue)
    text_rect_score = text_score.get_rect(center = (WIDTH // 2, HEIGHT + 30))
    screen.blit(text_score, text_rect_score)
    pygame.display.flip()
    clock.tick(FPS)

def mouse_button():
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    #best score button
    if mouse_x >= 157 and mouse_x <= 323 and mouse_y >= 390 and mouse_y <= 410:
        pass
    
    #world record button
    if mouse_x >= 119 and mouse_x <= 361 and mouse_y >= 440 and mouse_y <= 460:
        pass
    
    #settings button
    if mouse_x >= 178 and mouse_x <= 303 and mouse_y >= 490 and mouse_y <= 510:
        pass
    
    #play button
    if mouse_x >= 180 and mouse_x <= 300 and mouse_y >= 190 and mouse_y <= 320:
        global playing, obstacles, score
        playing = True
        pygame.mouse.set_visible(False)
        obstacles = []
        for i in range(num_enemy):
            obstacle = Obstacles()
            obstacles.append(obstacle)
        Player.x = 230
        Player.y = 230
        score = 0
        refresh_play()
        for i in range (3, 0, -1):
            pygame.draw.rect(screen, Colors.black, pygame.Rect(WIDTH//2 - 30, HEIGHT//2 + 50, 60, 60))
            timer_text = font_64.render(str(i), True, Colors.blue)
            timer_rect_text = timer_text.get_rect(center = (WIDTH // 2, HEIGHT // 2 + 80))
            screen.blit(timer_text, timer_rect_text)
            pygame.display.flip()
            pygame.time.wait(1000)
            
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
                score += self.length * abs(self.speed)
                self.spawn_obstacle()

while running:
    #quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #check mouse click
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_button()
    
    #get coordinate of mouse to change colors of texts
    mouse_coordinates()
    
    #draw
    Menu.refresh_menu()
    
    while playing:
        
        #quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os._exit()

        #obstacles moving
        for obstacle in obstacles:
            obstacle.move()
            if (Player.x < obstacle.x + obstacle.length and Player.x + Player.length > obstacle.x) and (Player.y < obstacle.y + obstacle.length and Player.y + Player.length > obstacle.y):
                playing = False
                player_crash_x, player_crash_y, player_crush_length = Player.x, Player.y, Player.length
                obstacle_crush_x, obstacle_crush_y, obstacle_crush_length = obstacle.x, obstacle.y, obstacle.length
                pygame.draw.rect(screen, Colors.black, pygame.Rect(0, 0, WIDTH, HEIGHT + MENU))
                pygame.mouse.set_visible(True)
                timer = time.time()
        
        if playing:
            #player moving
            Player.refresh()

            #draw
            refresh_play()

pygame.quit()