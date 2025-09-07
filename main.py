from tkinter import CENTER
from turtle import left
import pygame
import sys
import random


BLOCK = 20
COLS, ROWS = 32, 24
WIDTH, HEIGHT = COLS*BLOCK, ROWS*BLOCK

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
is_running = True

BG = (10, 10, 10)
GRID = (30, 30, 30)

# PLAYER
SNAKE_COLOR = (80, 220, 100)
FOOD_COLOR = (220, 70, 60)

DIRECTION = (0, 1)
DIRECTION_MAP = {
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
}
move_event = pygame.USEREVENT + 1


def draw_cell(pos, color):
    x, y = pos
    pygame.draw.rect(screen, color, (x*BLOCK, y*BLOCK, BLOCK, BLOCK))


snake = [(COLS//2, ROWS//2), (COLS//2, ROWS//2), (COLS//2, ROWS//2)]

# Score
score = 0
test_font = pygame.font.Font('Minecraft.ttf', 50)


def show_score():
    txt_surf = test_font.render(f"Score: {score}", False, (255, 255, 0))
    txt_rect = txt_surf.get_rect(center=(350, 50))
    screen.blit(txt_surf, txt_rect)


    # FOOD
food = None


def spawn_food(snake_set):
    while True:
        p = (random.randrange(COLS), random.randrange(ROWS))
        if p not in snake_set:
            return p


food = spawn_food(set(snake))

# GRID


def draw_grid():
    for x in range(0, WIDTH, BLOCK):
        pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK):
        pygame.draw.line(screen, GRID, (0, y), (WIDTH, y))


def move_snake():
    global snake, food, score
    # თავის პოზიცია
    head_x, head_y = snake[0]

    # ახალი თავის პოზიციის გამოთვლა
    new_head = (head_x + DIRECTION[0], head_y + DIRECTION[1])

    # ვამოწმებ ეხება თუ არა ბორდერს

    if (new_head[0] < 0 or new_head[0] >= COLS or
            new_head[1] < 0 or new_head[1] >= ROWS):
        return False
    if new_head in snake:
        return False

    snake.insert(0, new_head)

    if new_head == food:
        food = spawn_food(set(snake))
        score += 1
    else:
        snake.pop()

    return True


while is_running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key in DIRECTION_MAP:
                new_direction = DIRECTION_MAP[e.key]

                if (new_direction[0] != -DIRECTION[0] or
                   new_direction[1] != -DIRECTION[1]):
                    DIRECTION = new_direction

    if not move_snake():
        pygame.quit()
        sys.exit()
    screen.fill(BG)
    for seg in snake:
        draw_cell(seg, SNAKE_COLOR)
    draw_cell(food, FOOD_COLOR)
    draw_grid()
    show_score()
    pygame.display.flip()
    clock.tick(10)
