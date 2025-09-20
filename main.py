from tkinter import CENTER, W
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

# HighScore
high_score = 0
HIGH_SCORE_FILE = "highscore.txt"


def load_high_score():
    global high_score
    try:
        with open(HIGH_SCORE_FILE, 'r') as file:
            high_score = int(file.read().strip())
    except (FileNotFoundError, ValueError):
        high_score = 0


def save_high_score():
    with open(HIGH_SCORE_FILE, 'w') as file:
        file.write(str(high_score))


def show_score():
    txt_surf = test_font.render(f"Score: {score}", False, (255, 255, 0))
    txt_rect = txt_surf.get_rect(center=(WIDTH / 2, HEIGHT - 420))
    screen.blit(txt_surf, txt_rect)


    # FOOD
food = None


def spawn_food(snake_set):
    while True:
        p = (random.randrange(COLS), random.randrange(ROWS))
        if p not in snake_set:
            return p


food = spawn_food(set(snake))
# GameStates
game_state = "playing"


# GRID


def draw_grid():
    for x in range(0, WIDTH, BLOCK):
        pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK):
        pygame.draw.line(screen, GRID, (0, y), (WIDTH, y))


def move_snake():
    global snake, food, score, game_state, high_score
    # თავის პოზიცია
    head_x, head_y = snake[0]

    # ახალი თავის პოზიციის გამოთვლა
    new_head = (head_x + DIRECTION[0], head_y + DIRECTION[1])

    # ვამოწმებ ეხება თუ არა ბორდერს

    if (new_head[0] < 0 or new_head[0] >= COLS or
            new_head[1] < 0 or new_head[1] >= ROWS):
        game_state = "game_over"
        return False

    if new_head in snake:
        game_state = "game_over"
        if score > high_score:
            high_score = score
            save_high_score()
        return False

    snake.insert(0, new_head)

    if new_head == food:
        food = spawn_food(set(snake))

        score += 1

    else:
        snake.pop()

    return True


# GameOver
def draw_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Game Over text
    gameover_txt_surf = test_font.render("GAME OVER", False, (255, 100, 100))
    gameover_txt_rect = gameover_txt_surf.get_rect(
        center=(WIDTH//2, HEIGHT//2 - 60))
    screen.blit(gameover_txt_surf, gameover_txt_rect)

    # Final score text
    score_txt_surf = test_font.render(
        f"Final Score: {score}", False, (255, 255, 0))
    score_txt_rect = score_txt_surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 10))
    screen.blit(score_txt_surf, score_txt_rect)

    # High score text
    high_score_txt_surf = test_font.render(
        f"High Score: {high_score}", False, (0, 255, 255))
    high_score_txt_rect = high_score_txt_surf.get_rect(
        center=(WIDTH//2, HEIGHT//2 + 40))
    screen.blit(high_score_txt_surf, high_score_txt_rect)

    # Restart instruction
    restart_txt_surf = test_font.render(
        "Press R to Restart", False, (100, 255, 100))
    restart_txt_rect = restart_txt_surf.get_rect(
        center=(WIDTH//2, HEIGHT//2 + 90))
    screen.blit(restart_txt_surf, restart_txt_rect)

# ResetGame


def reset_game():

    global snake, food, score, DIRECTION, game_state
    snake = [(COLS//2, ROWS//2), (COLS//2, ROWS//2), (COLS//2, ROWS//2)]
    food = spawn_food(set(snake))
    score = 0
    DIRECTION = (0, 1)
    game_state = "playing"


while is_running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if game_state == "game_over":
                if e.key == pygame.K_r:
                    reset_game()
            elif game_state == "playing":
                if e.key in DIRECTION_MAP:
                    new_direction = DIRECTION_MAP[e.key]
                    if (new_direction[0] != -DIRECTION[0] or
                       new_direction[1] != -DIRECTION[1]):
                        DIRECTION = new_direction

    if game_state == "playing":
        if not move_snake():
            pass

    # Draw the game
    screen.fill(BG)
    for seg in snake:
        draw_cell(seg, SNAKE_COLOR)
    draw_cell(food, FOOD_COLOR)
    draw_grid()
    show_score()

    # Draw game over screen
    if game_state == "game_over":
        draw_game_over()

    pygame.display.flip()
    clock.tick(10)
