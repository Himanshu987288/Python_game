import pygame
import random
import sys


pygame.init()


WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
FPS = 10
FONT = pygame.font.SysFont('Arial', 30)


BG_COLOR = (20, 20, 30)
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 50, 50)
TEXT_COLOR = (255, 255, 255)


win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Professional Snake Game")


snake = [(ROWS//2, COLS//2)]
direction = (0, 0)
score = 0

def random_food():
    while True:
        pos = (random.randint(0, ROWS-1), random.randint(0, COLS-1))
        if pos not in snake:
            return pos

food = random_food()


def draw_window():
    win.fill(BG_COLOR)
    

    for block in snake:
        pygame.draw.rect(win, SNAKE_COLOR, (block[1]*CELL_SIZE, block[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.draw.rect(win, FOOD_COLOR, (food[1]*CELL_SIZE, food[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    score_text = FONT.render(f"Score: {score}", True, TEXT_COLOR)
    win.blit(score_text, (10, 10))
    
    pygame.display.update()


def game_over():
    over_text = FONT.render("GAME OVER! Press R to Restart", True, TEXT_COLOR)
    win.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2))
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                waiting = False


clock = pygame.time.Clock()
running = True

while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_DOWN and direction != (-1, 0):
                direction = (1, 0)
            elif event.key == pygame.K_LEFT and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_RIGHT and direction != (0, -1):
                direction = (0, 1)
    

    if direction != (0, 0):
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, head)
        
    
        if head == food:
            score += 1
            food = random_food()
        else:
            snake.pop()
    
    
    head = snake[0]
    if (head[0] < 0 or head[0] >= ROWS or head[1] < 0 or head[1] >= COLS or head in snake[1:]):
        game_over()
        
        snake = [(ROWS//2, COLS//2)]
        direction = (0, 0)
        score = 0
        food = random_food()
    
    draw_window()

pygame.quit()
