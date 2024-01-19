import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame.locals import *
from sys import exit
from random import randint
import time


pygame.init()
pygame.display.set_caption('Snake')
window_x = 800
window_y = 600
screen = pygame.display.set_mode((window_x, window_y))
clock = pygame.time.Clock()
start_time = time.time()
font = pygame.font.SysFont(None, 32)
pygame.mixer.init()
game_sound = pygame.mixer.Sound('gamesound.wav')
point_sound = pygame.mixer.Sound('Point.wav')


DISTANCE = 30
DIRECTION = [DISTANCE, 0]
COLOR = (255, 255, 255)
GAME_POINTS = 0
game_state = "start_menu"


def load_image(src, x, y):
    image = pygame.image.load(src).convert()
    image = pygame.transform.scale(image, (30, 30))
    rect = image.get_rect(center=(x, y))

    transparent = image.get_at((0, 0))
    image.set_colorkey(transparent)

    return image, rect


def move(head, snake):
    global DIRECTION, KEYS, DISTANCE, COLOR


    if KEYS[K_UP] and DIRECTION[1] == 0:
        DIRECTION = [0, -DISTANCE]
    elif KEYS[K_DOWN] and DIRECTION[1] == 0:
        DIRECTION = [0, DISTANCE]
    elif KEYS[K_RIGHT] and DIRECTION[0] == 0:
        DIRECTION = [DISTANCE, 0]
    elif KEYS[K_LEFT] and DIRECTION[0] == 0:
        DIRECTION = [-DISTANCE, 0]
    if head.bottom > 600:
        head.top = 0
    elif head.top < 0:
        head.bottom = 600
    elif head.left < 0:
        head.right = 800
    elif head.right > 800:
        head.left = 0
    for index in range(len(snake)-1, 0, -1):
        snake[index].x = snake[index-1].x
        snake[index].y = snake[index-1].y

    head.move_ip(DIRECTION)


def pickup():
    global apple_rect, head_rect, GAME_POINTS, snake

    if head_rect.colliderect(apple_rect):
        apple_rect.x = randint(40, 760)
        apple_rect.y = randint(40, 560)
        GAME_POINTS += 10
        snake.append(snake[-1].copy())
        point_sound.play()


def score():
    global GAME_POINTS
    global time_elapsed
    global start_time
    text = font.render(f'Score: {GAME_POINTS}', True, (255, 255, 255))
    text_rect = text.get_rect(center=(400, 500))
    screen.blit(text, text_rect)
    text1 = font.render(f"Time: {formatted_time} seconds", True, white)
    text1_rect = text.get_rect(center=(60, 10))
    screen.blit(text1, text1_rect)


def gameover():
    global snake, head_rect
    for segment in snake[1:]:
        if head_rect.colliderect(segment):
            return True
    return False


head_image, head_rect = load_image('head.png', 400, 300)
apple_image, apple_rect = load_image('apple.png', 200, 300)
body_image, body_rect = load_image('body.png', 370, 300)
snake = [head_rect, body_rect]
game_sound.play()
while True:
    screen.fill((0, 0, 0))
    current_time = time.time()
    time_elapsed = current_time - start_time
    time_elapsed = float(time_elapsed)
    formatted_time = "{:.1f}".format(time_elapsed)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    if gameover():
        my_font = pygame.font.SysFont('times new roman', 30)
        my_font1 = pygame.font.SysFont('times new roman', 50)
        text_surface = my_font1.render('Игра окончена!' , True, white)
        score_surface = my_font.render('Ваш конечный счет: ' + str(GAME_POINTS), True, white)
        game_time = my_font.render('Время игры: ' + str(formatted_time) + " секунд", True, white)
        text_rect = text_surface.get_rect(center=(window_x // 2, window_y // 4 - 50))
        score_rect = score_surface.get_rect(center=(window_x // 2 - 200, window_y // 2 + 50))
        time_rect = score_surface.get_rect(center=(window_x // 2 - 200, window_y // 2))
        screen.blit(text_surface, text_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(game_time, time_rect)
        pygame.display.flip()
        time.sleep(5)
        pygame.quit()
        quit()

    yellow = (255, 255, 0)
    white = (255, 255, 255)
    green = (118,238,0)
    blue = (0,255,255)
    pink = (255,114,86)

    if GAME_POINTS == 100:
        font = pygame.font.Font(None, 36)
        text = font.render(f"Мастер-укуситель. Набери {GAME_POINTS} очков.", True, yellow)
        text_rect = text.get_rect()
        text_rect.topright = (800, 0)
        screen.blit(text, text_rect)
        pygame.display.flip()

    if GAME_POINTS == 200:
        font = pygame.font.Font(None, 36)
        text = font.render(f"Гигантский голод. Набери {GAME_POINTS} очков.", True, white)
        text_rect = text.get_rect()
        text_rect.topright = (800, 0)
        screen.blit(text, text_rect)
        pygame.display.flip()

    if GAME_POINTS == 300:
        font = pygame.font.Font(None, 36)
        text = font.render(f"Укус успеха. Набери {GAME_POINTS} очков.", True, green)
        text_rect = text.get_rect()
        text_rect.topright = (800, 0)
        screen.blit(text, text_rect)
        pygame.display.flip()

    if GAME_POINTS == 400:
        font = pygame.font.Font(None, 36)
        text = font.render(f"Чемпион змейки: Достигнуть.{GAME_POINTS} очков в одной игре", True, blue)
        text_rect = text.get_rect()
        text_rect.topright = (800, 0)
        screen.blit(text, text_rect)
        pygame.display.flip()

    if GAME_POINTS == 500:
        font = pygame.font.Font(None, 36)
        text = font.render(f"Всемогущая змейка: Достигнуть.{GAME_POINTS} очков в одной игре", True, pink)
        text_rect = text.get_rect()
        text_rect.topright = (800, 0)
        screen.blit(text, text_rect)
        pygame.display.flip()

    screen.blit(head_image, head_rect)
    screen.blit(apple_image, apple_rect)

    for segment in snake[1:]:
        screen.blit(body_image, segment)

    KEYS = pygame.key.get_pressed()
    move(head_rect, snake)
    pickup()
    score()

    pygame.display.update()
    clock.tick(10)
