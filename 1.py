import pygame
from pygame.locals import *  #  *  --> барлық функцияны импорттау 
import random 
import time
pygame.init()
FPS=120
FramePerSec = pygame.time.Clock()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED=5
SCORE=0
COINS_COLLECTED=0

coin_sound = pygame.mixer.Sound("/Users/zhambyldameli/Desktop/lab8/PYTHON_8 lab_звук монеты.mp3")

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Times New Roman", 20)
game_over = font.render("Game Over", True, (0,0,0)) # --> true болса тексттын жақтары әдемі болып шығады
background = pygame.image.load("/Users/zhambyldameli/Desktop/lab8/AnimatedStreet.png")

pygame.mixer.music.load("/Users/zhambyldameli/Desktop/lab8/PYTHON_8 lab_background.wav")
pygame.mixer.music.play(-1) # --> infinity

DISPLAY=pygame.display.set_mode((400,600))
DISPLAY.fill((255,255,255))
pygame.display.set_caption("GAME")

class Enemy(pygame.sprite.Sprite):   # --> pygame.sprite  модульінің ішінде Sprite деген клаасс бар 
    def __init__(self):    # __init__ --> конструктор
        super().__init__() # super() -->  (родительский класс) функциясын шақыру үшін қолданылады.
        self.image = pygame.image.load("/Users/zhambyldameli/Desktop/lab8/Enemy.png")
        self.image = pygame.transform.scale(self.image, (50,100))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if self.rect.bottom > 600:
            SCORE+=1
            self.rect.top = 0
            self.rect.center = (random.randint(20, SCREEN_WIDTH - 20) , 0)

class Player(pygame.sprite.Sprite): # --> pygame.sprite  модульінің ішінде Sprite деген клаасс бар 
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("/Users/zhambyldameli/Desktop/lab8/Player.png")
        self.image = pygame.transform.scale(self.image, (50,100 ))  
        self.rect = self.image.get_rect()
        self.rect.center = (207, 520)
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite): # --> pygame.sprite  модульінің ішінде Sprite деген клаасс бар 
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("/Users/zhambyldameli/Desktop/lab8/coin1.png")
        self.image = pygame.transform.scale(self.original_image, (40,40))
        self.rect = self.image.get_rect()
        self.respawn()
    def respawn(self):
        self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), 0)

    def move(self):
        self.rect.move_ip(0, SPEED // 2)
        if self.rect.top > SCREEN_HEIGHT:
            self.respawn()
P1=Player() # --> class
E1=Enemy() # --> class
C1=Coin() # --> class

enemies=pygame.sprite.Group()
enemies.add(E1)
coins=pygame.sprite.Group()
coins.add(C1)
all_sprites=pygame.sprite.Group()
all_sprites.add(P1,E1,C1)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.3
        if event.type == QUIT:
            pygame.quit()



    DISPLAY.blit(background, (0, 0))
    
    scores = font_small.render(str(SCORE), True, (0,0,0))
    DISPLAY.blit(scores, (10, 10))
    coins_collected_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, (0,0,0))
    DISPLAY.blit(coins_collected_text, (300, 10))
    
    for entity in all_sprites:
        if isinstance(entity,Enemy) or isinstance(entity , Player) or isinstance(entity, Coin):
            entity.move()
        DISPLAY.blit(entity.image, entity.rect)
    if pygame.sprite.spritecollideany(P1, enemies):  # --> Проверяешь, не столкнулся ли игрок P1 с каким-либо врагом из группы enemies.
        pygame.mixer.music.stop()
        pygame.mixer.Sound("/Users/zhambyldameli/Desktop/lab8/PYTHON_8 lab_crash.wav").play()
        time.sleep(0.7)  # --> ожидания до game over
        DISPLAY.fill((255,0,0))
        DISPLAY.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(1) # --> ойынның бітуі
        pygame.quit()

    if pygame.sprite.spritecollideany(P1, coins):       # spritecollideany -->  Если столкновение есть, возвращает первый найденный спрайт, с которым произошло столкновение. Если столкновения нет, возвращает None.
        COINS_COLLECTED += 1
        coin_sound.play()
        C1.respawn()
    
    pygame.display.update()
    FramePerSec.tick(FPS)
