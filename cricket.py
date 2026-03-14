import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade Cricket Game")

clock = pygame.time.Clock()
FPS = 60


GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BROWN = (210, 180, 140)
BLUE = (0, 0, 200)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0,0,0)

font = pygame.font.SysFont("Arial", 28)


score = 0
balls = 0
max_balls = 12
over = 0


bat_x = WIDTH//2 - 40
bat_y = HEIGHT - 120
bat_width, bat_height = 80, 20
bat_speed = 7


ball_x = random.randint(100, WIDTH-100)
ball_y = -50
ball_speed = 6
ball_in_play = False


result_text = ""


move_lock = False

def draw_ground():
    screen.fill(GREEN)
    pygame.draw.rect(screen, BROWN, (80, HEIGHT-200, WIDTH-160, 180))
    pygame.draw.circle(screen, WHITE, (WIDTH//2, HEIGHT//2+60), 120, 5)
    pygame.draw.line(screen, WHITE, (WIDTH//2-120, HEIGHT//2+60), (WIDTH//2+120, HEIGHT//2+60), 5)

def draw_score():
    score_text = font.render(f"Score: {score}  Overs: {over}.{balls%6}", True, BLACK)
    screen.blit(score_text, (20,20))

def display_result(text):
    res = font.render(text, True, RED)
    screen.blit(res, (WIDTH//2 - res.get_width()//2, 80))

def reset_ball():
    global ball_x, ball_y, ball_in_play
    ball_x = random.randint(100, WIDTH-100)
    ball_y = -50
    ball_in_play = False


running = True
while running:
    clock.tick(FPS)
    draw_ground()
    draw_score()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and bat_x>80:
        bat_x -= bat_speed
    if keys[pygame.K_RIGHT] and bat_x<WIDTH-80-bat_width:
        bat_x += bat_speed

   
    if not ball_in_play:
        ball_in_play = True
        ball_x = random.randint(100, WIDTH-100)
        ball_y = -50

    ball_y += ball_speed

  
    pygame.draw.rect(screen, BLUE, (bat_x, bat_y, bat_width, bat_height))
    pygame.draw.rect(screen, YELLOW, (bat_x+10, bat_y-20, bat_width-20, 20))

 
    pygame.draw.circle(screen, RED, (ball_x, int(ball_y)), 12)

    
    if ball_y >= bat_y and ball_y <= bat_y + 30:
        if bat_x < ball_x < bat_x + bat_width:
            hit = random.choice([0,1,2,4,6])
            score += hit
            result_text = f"Hit: {hit} runs!"
        else:
            result_text = "Missed!"
        ball_y = HEIGHT + 50
        balls += 1

    if ball_y > HEIGHT:
        reset_ball()

    if result_text:
        display_result(result_text)

    if balls >= max_balls:
        over = balls//6
        display_result(f"Match Over! Final Score: {score}")
        pygame.display.update()
        pygame.time.delay(3000)
        break

    pygame.display.update()
