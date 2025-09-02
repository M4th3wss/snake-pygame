import pygame
import sys
import random


BLOCK = 20
COLS, ROWS = 32, 24
WIDTH, HEIGHT = COLS*BLOCK, ROWS*BLOCK

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

BG = (10, 10, 10)
GRID = (30, 30, 30)

# PLAYER
SNAKE_COLOR = (80, 220, 100)
FOOD_COLOR = (220, 70, 60)


def draw_cell(pos, color):
    x, y = pos
    pygame.draw.rect(screen, color, (x*BLOCK, y*BLOCK, BLOCK, BLOCK))


snake = [(COLS//2, ROWS//2), (COLS//2, ROWS//2), (COLS//2, ROWS//2)]

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


while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BG)
    for seg in snake:
        draw_cell(seg, SNAKE_COLOR)
    draw_cell(food, FOOD_COLOR)
    draw_grid()
    pygame.display.flip()
    clock.tick(10)
