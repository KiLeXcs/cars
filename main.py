import pygame
from cryptography.fernet import Fernet
import time
import os
import random as rand
import json
import datetime

class Colors():
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 128, 255)
    gold = (255, 215, 0)
    silver = (192, 192, 192)
    bronze = (205, 127, 50)

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
key = b'es0XMVo30jLUso_mQU1PVmGh8RWnywv_arAPDENz9cU='
#reading top score file
if True:
    file_name = f'{game_dir}\score.txt'
    if not os.path.exists(file_name):
        file = open(file_name, "w")
        file.close()
    file = open(file_name, "rb+")
    content = file.read()
    f = Fernet(key)

    try:
        top_scores = json.loads((f.decrypt(content)).decode())
    except:
        top_scores = {
                    "high_scores": [{"score": 0, "date": "---"}, {"score": 0, "date": "---"}, {"score": 0, "date": "---"}, {"score": 0, "date": "---"}, {"score": 0, "date": "---"},
                                    {"score": 0, "date": "---"}, {"score": 0, "date": "---"}, {"score": 0, "date": "---"}, {"score": 0, "date": "---"}, {"score": 0, "date": "---"}]
                }
        write_data = f.encrypt(json.dumps(top_scores).encode())
        file.write(write_data)
    file.close()
clock = pygame.time.Clock()

def clearall():
    pygame.draw.rect(screen, Colors.black, pygame.Rect(0, 0, WIDTH, HEIGHT+MENU))

def save_score(score):
    global top_scores
    #check is a top 10 score
    if (top_scores["high_scores"][-1]["score"]) < score:
        top_scores["high_scores"][-1]["score"] = score
        top_scores["high_scores"][-1]["date"] = datetime.date.today().strftime('%Y-%m-%d')
        top_scores["high_scores"].sort(key=lambda x: x["score"], reverse = True)
        data_save = f.encrypt(json.dumps(top_scores).encode())
        file = open(file_name, "wb")
        file.write(data_save)
        file.close()

def mouse_coordinates():
    
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if mouse_x >= 142 and mouse_x <= 337 and mouse_y >= 390 and mouse_y <= 410:
        Menu.color_your_score_text = Colors.white
    else:
        Menu.color_your_score_text = Colors.blue
    
    if mouse_x >= 119 and mouse_x <= 361 and mouse_y >= 430 and mouse_y <= 450:
        Menu.color_world_score_text = Colors.white
    else:
        Menu.color_world_score_text = Colors.blue
        
    if mouse_x >= 178 and mouse_x <= 303 and mouse_y >= 470 and mouse_y <= 490:
        Menu.color_settings_text = Colors.white
    else:
        Menu.color_settings_text = Colors.blue

    if mouse_x >= 210 and mouse_x <= 270 and mouse_y >= 510 and mouse_y <= 530:
        Menu.color_exit_text = Colors.red
    else:
        Menu.color_exit_text = Colors.blue
    
    if mouse_x >= 180 and mouse_x <= 300 and mouse_y >= 150 and mouse_y <= 290:
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

def startgame():
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

def player_score_menu():
    player_score_menu_open = True
    clearall()
    while player_score_menu_open:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                os._exit()
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                    clearall()
                    player_score_menu_open = False
        
        if player_score_menu_open:
            #some text
            text = font_32.render("Your best scores", True, Colors.blue)
            text_rect = text.get_rect(center = (WIDTH // 2, 40))
            screen.blit(text, text_rect)

            text = font_32.render("score", True, Colors.blue)
            text_rect = text.get_rect(center = (WIDTH // 2 - 55, 80))
            screen.blit(text, text_rect)

            text = font_32.render("date", True, Colors.blue)
            text_rect = text.get_rect(center = (WIDTH // 2 + 130, 80))
            screen.blit(text, text_rect)

            for i in range(0, 10):
                if i == 0:
                    Color = Colors.gold
                elif i == 1:
                    Color = Colors.silver
                elif i == 2:
                    Color = Colors.bronze
                else:
                    Color = Colors.blue

                #number
                text = font_32.render(str(i+1), True, Color)
                text_rect = text.get_rect(center = (WIDTH // 2 - 170, 80 + 40 * (i+1)))
                screen.blit(text, text_rect)
                
                #score
                text = font_32.render(str(top_scores["high_scores"][i]["score"]), True, Color)
                text_rect = text.get_rect(center = (WIDTH // 2 - 55, 80 + 40 * (i+1)))
                screen.blit(text, text_rect)

                #date
                text = font_32.render(str(top_scores["high_scores"][i]["date"]), True, Color)
                text_rect = text.get_rect(center = (WIDTH // 2 + 130, 80 + 40 * (i+1)))
                screen.blit(text, text_rect)


            pygame.display.flip()

def mouse_button():
    
    mouse_x, mouse_y = pygame.mouse.get_pos()

    #your score button
    if mouse_x >= 142 and mouse_x <= 337 and mouse_y >= 390 and mouse_y <= 410:
        player_score_menu()
    
    #world record button
    if mouse_x >= 119 and mouse_x <= 361 and mouse_y >= 430 and mouse_y <= 450:
        pass
    
    #settings button
    if mouse_x >= 178 and mouse_x <= 303 and mouse_y >= 470 and mouse_y <= 490:
        pass
    
    #exit button
    if mouse_x >= 210 and mouse_x <= 270 and mouse_y >= 510 and mouse_y <= 530:
        os._exit()

    #play button
    if mouse_x >= 180 and mouse_x <= 300 and mouse_y >= 150 and mouse_y <= 290:
        startgame()
            
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
                score += self.length * abs(self.speed)
                self.spawn_obstacle()
        else:
            self.y += self.speed
            if self.y > HEIGHT or self.y < -self.length:
                score += self.length * abs(self.speed)
                self.spawn_obstacle()

class Menu():
    
    color_play_sign = Colors.blue
    color_your_score_text = Colors.blue
    color_world_score_text= Colors.blue
    color_settings_text = Colors.blue
    color_exit_text = Colors.blue
    color_score_text = Colors.blue
    
    def refresh_menu():
        global timer

        #last crush
        global player_crash_x, player_crash_y, player_crush_length, obstacle_crush_x, obstacle_crush_y, obstacle_crush_length

        if score != -1 and (time.time() - timer <= 0.4 or 0.8 <= time.time() - timer <= 1.2 or 1.6 <= time.time() - timer <= 2 or time.time() - timer >= 2.4):
            pygame.draw.rect(screen, Colors.blue, pygame.Rect(player_crash_x, player_crash_y, player_crush_length, player_crush_length))
            pygame.draw.rect(screen, Colors.red, pygame.Rect(obstacle_crush_x, obstacle_crush_y, obstacle_crush_length, obstacle_crush_length))
            text_menu_score = font_32.render(f"Your score: {score}", True, Menu.color_score_text)
            text_rect_menu_score = text_menu_score.get_rect(center = (WIDTH // 2, 330))
            screen.blit(text_menu_score, text_rect_menu_score)
        else:
            pygame.draw.rect(screen, Colors.black, pygame.Rect(0, 305, WIDTH, 50))
            pygame.draw.rect(screen, Colors.blue, pygame.Rect(player_crash_x, player_crash_y, player_crush_length, player_crush_length))
            pygame.draw.rect(screen, Colors.red, pygame.Rect(obstacle_crush_x, obstacle_crush_y, obstacle_crush_length, obstacle_crush_length))

        
        #some texts
        text_menu_name = font_64.render("Star slider", True, Colors.blue)
        text_rect_menu_name = text_menu_name.get_rect(center = (WIDTH // 2, 80))
        screen.blit(text_menu_name, text_rect_menu_name)
        
        text_menu_your_score = font_32.render("Your scores", True, Menu.color_your_score_text)
        text_rect_menu_your_score = text_menu_your_score.get_rect(center = (WIDTH // 2, 400))
        screen.blit(text_menu_your_score, text_rect_menu_your_score)
        
        text_menu_world_score = font_32.render("World records", True, Menu.color_world_score_text)
        text_rect_menu_world_score = text_menu_world_score.get_rect(center = (WIDTH // 2, 440))
        screen.blit(text_menu_world_score, text_rect_menu_world_score)
        
        text_menu_settings = font_32.render("Settings", True, Menu.color_settings_text)
        text_rect_menu_settings = text_menu_settings.get_rect(center = (WIDTH // 2, 480))
        screen.blit(text_menu_settings, text_rect_menu_settings)

        text_menu_settings = font_32.render("Exit", True, Menu.color_exit_text)
        text_rect_menu_settings = text_menu_settings.get_rect(center = (WIDTH // 2, 520))
        screen.blit(text_menu_settings, text_rect_menu_settings)
        
        #draw play sign
        pygame.draw.line(screen, Menu.color_play_sign, [(WIDTH - 100)//2, (HEIGHT - MENU - 60)//2], [(WIDTH + 100)//2, (HEIGHT - MENU + 40)//2], 10)
        pygame.draw.line(screen, Menu.color_play_sign, [(WIDTH + 100)//2, (HEIGHT - MENU + 40)//2], [(WIDTH - 100)//2, (HEIGHT - MENU + 140)//2], 10)
        pygame.draw.line(screen, Menu.color_play_sign, [(WIDTH - 92)//2, (HEIGHT - MENU + 140)//2], [(WIDTH - 92)//2, (HEIGHT - MENU - 10)//2], 10)
        
        pygame.display.flip()
        clock.tick(FPS)

while running:
    #quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #check mouse click
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_button()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                startgame()
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
                #cleaning screen
                pygame.draw.rect(screen, Colors.black, pygame.Rect(0, 0, WIDTH, HEIGHT + MENU))
                pygame.mouse.set_visible(True)
                save_score(score)
                timer = time.time()
        
        if playing:
            #player moving
            Player.refresh()

            #draw
            refresh_play()
