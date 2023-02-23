import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random
from os import listdir

pygame.init()
# pygame.font.init()

FPS = pygame.time.Clock()
# print(pygame.font.get_fonts())

screen = width, height = 1200, 800

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
BLUE = 0, 0, 255

# font = pygame.font.SysFont('Verdana', 20)
main_surface = pygame.display.set_mode(screen)

IMGS_PATCH = 'goose'
ball_image = [pygame.transform.scale(pygame.image.load(IMGS_PATCH + '/' + file).convert_alpha(),(80, 60)) for file in listdir(IMGS_PATCH)]
# ball = pygame.image.load('player.png').convert_alpha()
ball = ball_image[0]
ball_rect = ball.get_rect()  # currentPoint
ball_speed = 5  # movePointSpeed

def create_enemy():
    enemy = pygame.transform.scale(pygame.image.load('sprite/enemy.png').convert_alpha(), (90, 30))
    enemy_rect = pygame.Rect(width, random.randint(0, height), *enemy.get_size())  # enemyPointCreation
    enemy_speed = random.randint(2, 5)
    return [enemy, enemy_rect, enemy_speed]

def create_bonus():
    bonus = pygame.transform.scale(pygame.image.load('sprite/bonus.png').convert_alpha(), (150, 140))
    bonus_rect = pygame.Rect(random.randint(0, width), 0, *bonus.get_size())  # bonusPointCreation
    bonus_speed = random.randint(4, 6)
    return [bonus, bonus_rect, bonus_speed]

bg = pygame.transform.scale(pygame.image.load('sprite/background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 125)

img_index = 0
enemies = []
bonuses = []
scores = 0

is_working = True

while is_working:
    FPS.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            img_index += 1
            if img_index == len(ball_image):
                img_index = 0
            ball = ball_image[img_index]

    pressed_keys = pygame.key.get_pressed()

    bgX -= bg_speed
    bgX2 -= bg_speed
    if bgX < -bg.get_width():  # if the sceenX has borders update
        bgX = bg.get_width()
    if bgX2 < -bg.get_width():  # if the sceenX2 has borders update
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bgX, 0))  # painOnXBg
    main_surface.blit(bg, (bgX2, 0))  # painOnXBgDisplaced

    main_surface.blit(ball, ball_rect)
    # main_surface.blit(font.render(str(scores), True, WHITE), (width - 30, 0))  # paintPlayingFieldText (x,y)

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
        if ball_rect.colliderect(enemy[1]):
            is_working = False
            # enemies.pop(enemies.index(enemy))
    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])  # move!!!!!0
        main_surface.blit(bonus[0], bonus[1])
        if bonus[1].bottom >= height:
            bonuses.pop(bonuses.index(bonus))
        if ball_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1

    if pressed_keys[K_DOWN] and not ball_rect.bottom >= height:
        ball_rect = ball_rect.move(0, ball_speed)  # changePositionUp

    if pressed_keys[K_UP] and not ball_rect.top <= 0:
        ball_rect = ball_rect.move(0, -ball_speed)  # changePositionDown

    if pressed_keys[K_RIGHT] and not ball_rect.right >= width:
        ball_rect = ball_rect.move(ball_speed, 0)  # changePosition

    if pressed_keys[K_LEFT] and not ball_rect.left <= 0:
        ball_rect = ball_rect.move(-ball_speed, 0)  # changePosition

    pygame.display.flip()
