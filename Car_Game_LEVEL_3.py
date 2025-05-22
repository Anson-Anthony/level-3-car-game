######################
## By Anson Anthony ##
## Car Game         ##
######################


import pygame
import random

pygame.init()
# screen size and icon of game
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car_Game")
game_icon = pygame.image.load('game_icon.png')
pygame.display.set_icon(game_icon)

# Colors
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Lane variables
ROAD_WIDTH = 420
LANE_MARKER_WIDTH = 10
LANE_MARKER_HEIGHT = 50

# Player variables
player_car_X = 250  # Starting position
player_car_Y = 600  # Starting position
score = 0
high_score = 0
speed = 5  # Base speed for road movement
game_over = False

# Load assets
player_car = pygame.image.load("car_1.png")
player_car = pygame.transform.scale(player_car, (100, 100))
Normal_car = pygame.image.load("car_3.png")
Normal_car = pygame.transform.scale(Normal_car, (100, 100))

# Initialize game elements eg road/lanes
road_markers = []
for lane_x in [50, 150, 250, 350, 450]:
    for i in range(5):
        road_markers.append([lane_x - LANE_MARKER_WIDTH//2, i * 200])

clock = pygame.time.Clock()


def initialize_enemies():
    enemies = []
    for _ in range(4):
        x = random.choice([50, 150, 250, 350])
        y = random.randint(-1500, -100)
        s = random.randint(3, 6)
        enemies.append([x, y, s])
    return enemies

def update_enemies(enemies, current_score):
    for enemy in enemies:
        enemy[1] += enemy[2]
        if enemy[1] > SCREEN_HEIGHT:
            enemy[1] = random.randint(-1500, -100)
            enemy[0] = random.choice([50, 150, 250, 350])
            enemy[2] = random.randint(3, 6)
            current_score += 1
    return current_score

def check_collision(player_rect, enemies):
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], 100, 100)
        if player_rect.colliderect(enemy_rect):
            return True
    return False

def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except:
        return 0

def save_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))

def draw_scores(surface, score, high_score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(text, (10, 10))
    text = font.render(f"High Score: {high_score}", True, WHITE)
    surface.blit(text, (10, 50))

def draw_road():
    pygame.draw.rect(screen, GRAY, 
                    (SCREEN_WIDTH//2 - ROAD_WIDTH//2, 0, ROAD_WIDTH, SCREEN_HEIGHT))
    
    for marker in road_markers:
        pygame.draw.rect(screen, WHITE, 
                        (marker[0], marker[1], LANE_MARKER_WIDTH, LANE_MARKER_HEIGHT))
        marker[1] += speed
        if marker[1] > SCREEN_HEIGHT:
            marker[1] = -LANE_MARKER_HEIGHT
            
    screen.blit(player_car, (player_car_X, player_car_Y))
    for enemy in enemies:
        screen.blit(Normal_car, (enemy[0], enemy[1]))

# Initialize game state
high_score = load_high_score()
enemies = initialize_enemies()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_LEFT and player_car_X > 50:
                    player_car_X -= 100
                if event.key == pygame.K_RIGHT and player_car_X < 350:
                    player_car_X += 100
            
            if event.key == pygame.K_r and game_over:
                game_over = False
                player_car_X = 250
                player_car_Y = 600
                score = 0
                enemies = initialize_enemies()

    screen.fill(BLACK)
    draw_road()

    if not game_over:
        score = update_enemies(enemies, score)
        player_rect = pygame.Rect(player_car_X, player_car_Y, 100, 100)
        if check_collision(player_rect, enemies):
            game_over = True
            if score > high_score:
                high_score = score
                save_high_score(high_score)

    if game_over:
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, RED)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 100))
        font = pygame.font.Font(None, 36)
        text = font.render("Press R to restart", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2))

    draw_scores(screen, score, high_score)
    pygame.display.update()
    clock.tick(60)

pygame.quit()