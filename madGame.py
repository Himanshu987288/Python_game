import pygame
import random
import sys

pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mad Game - Lane Cars")

clock = pygame.time.Clock()
FPS = 60



WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
ROAD_COLOR = (60, 60, 60)
LINE_COLOR = (255, 255, 255)
BLUE = (0, 0, 200)   # Player car
RED = (200,0,0)    # Enemy car
YELLOW = (255, 255, 0)  # Optional highlights


road_left = 150
road_right = WIDTH - 150
lane_count = 3
lane_width = (road_right - road_left)// lane_count
lanes = [road_left + i*lane_width + lane_width//2 for i in range(lane_count)]


player_width, player_height = 50,100
player_lane = 1  
player_y = HEIGHT - player_height - 20


enemy_width, enemy_height = 50, 100
enemy_speed = 6
enemy_count = 2 
enemies = []

for _ in range(enemy_count):
    lane = random.randint(0, lane_count - 1)
    y = random.randint(-600, -100)
    enemies.append([lane, y])

score = 0
high_score = 0
font = pygame.font.SysFont(None, 40)


move_lock = False

def draw_score(score, high_score):
    text = font.render(f"Score: {score}  High Score: {high_score}", True,WHITE)
    screen.blit(text, (10, 10))

def draw_background():
    screen.fill(GRAY) 
    pygame.draw.rect(screen, ROAD_COLOR, (road_left, 0, road_right-road_left, HEIGHT))  
    for i in range(1, lane_count):
        x = road_left + i*lane_width
        pygame.draw.line(screen, LINE_COLOR, (x, 0), (x, HEIGHT), 5)

def game_over():
    global high_score
    if score > high_score:
        high_score = score
    screen.fill(ROAD_COLOR)
    text1 = font.render("GAME OVER", True, RED)
    text2 = font.render(f"Score: {score}  High Score: {high_score}", True, WHITE)
    screen.blit(text1, (WIDTH//2 - 100, HEIGHT//2 - 40))
    screen.blit(text2, (WIDTH//2 - 150, HEIGHT//2 + 10))
    pygame.display.update()
    pygame.time.delay(3000)
    reset_game()

def reset_game():
    global player_lane, score, enemies, enemy_speed
    player_lane = 1
    score = 0
    enemy_speed = 5
    enemies.clear()
    for _ in range(enemy_count):
        lane = random.randint(0, lane_count - 1)
        y = random.randint(-600, -100)
        enemies.append([lane, y])

running = True
while running:
    draw_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
      
        if event.type == pygame.KEYDOWN and not move_lock:
            if event.key == pygame.K_LEFT and player_lane > 0:
                player_lane -= 1
                move_lock = True  
            if event.key == pygame.K_RIGHT and player_lane < lane_count - 1:
                player_lane += 1
                move_lock = True
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                move_lock = False 

   
    for i in range(enemy_count):
        enemies[i][1] += enemy_speed
        if enemies[i][1] > HEIGHT:
            enemies[i][1] = random.randint(-600, -100)
            enemies[i][0] = random.randint(0, lane_count - 1)
            score += 1
            enemy_speed += 0.1

       
        enemy_x = lanes[enemies[i][0]] - enemy_width//2
        enemy_y = enemies[i][1]
      
        pygame.draw.rect(screen, RED, (enemy_x, enemy_y, enemy_width, enemy_height))
        pygame.draw.rect(screen, YELLOW, (enemy_x+10, enemy_y+20, enemy_width-20, 30)) 

      
        player_rect = pygame.Rect(lanes[player_lane]-player_width//2, player_y, player_width, player_height)
        enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        if player_rect.colliderect(enemy_rect):
            game_over()

 
    player_x = lanes[player_lane] - player_width//2
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))
    pygame.draw.rect(screen, YELLOW, (player_x+10, player_y+20, player_width-20, 30))

    draw_score(score, high_score)

    pygame.display.update()
    clock.tick(FPS)
