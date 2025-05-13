import pygame
import random

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car_Game")
game_icon = pygame.image.load('game_icon.png')
pygame.display.set_icon(game_icon)

BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
GREEN = (188, 227, 199)
BLUE = (32, 32, 200)
RED = (0, 255, 0)

# lane varable
ROAD_WIDTH = 400
LANE_MARKER_WIDTH = 10
LANE_MARKER_HEIGHT = 50

# player varable
washing_machine_X = 250
washing_machine_Y = 600
score = 0
high_score = 0
speed = 5
game_over = False

# import images
washing_machine = pygame.image.load("Player_washing_machine.png")
washing_machine = pygame.transform.scale(washing_machine, (100, 100))
Normal_car = pygame.image.load("Lemon_car.png")
Normal_car = pygame.transform.scale(Normal_car, (100, 100))

# high score save file
try:
    with open("highscore.txt") as file:
        high_score = int(file.read())
except:
    high_score = 0

# Create 4 lane 
road_markers = [] #empnty list varable
for lane_x in [50, 150, 250, 350, 450]:
    for i in range(5):
        road_markers.append([lane_x - LANE_MARKER_WIDTH//2, i * 200])


#Enemy cars where they spawn and speed and how ramdon it spawn
enemies = []
for _ in range(4):
    Normal_car_x = random.choice([50, 150, 250, 350, 450])
    Normal_car_y = random.randint(-1500, -100)
    enemies.append([Normal_car_x, Normal_car_y, random.randint(3, 6)])

#clock tick varable
clock = pygame.time.Clock()

def draw_road():
    pygame.draw.rect(screen, GRAY, 
                    (SCREEN_WIDTH//2 - ROAD_WIDTH//2, 0, ROAD_WIDTH, SCREEN_HEIGHT))
    
    for marker in road_markers:
        pygame.draw.rect(screen, WHITE, 
                        (marker[0], marker[1], LANE_MARKER_WIDTH, LANE_MARKER_HEIGHT))
        marker[1] += speed
        if marker[1] > SCREEN_HEIGHT:
            marker[1] = -LANE_MARKER_HEIGHT

    screen.blit(washing_machine, (washing_machine_X, washing_machine_Y))
    
    for enemy in enemies:
        screen.blit(Normal_car, (enemy[0], enemy[1]))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Prevent movement if game over
            if event.key == pygame.K_LEFT and not game_over:
                if washing_machine_X > 50:
                    washing_machine_X -= 100
            if event.key == pygame.K_RIGHT and not game_over:
                if washing_machine_X < 350:
                    washing_machine_X += 100

            if event.key == pygame.K_r and game_over:
                game_over = False
                washing_machine_X = 250
                washing_machine_Y = 600
                score = 0
                enemies = []
                for _ in range(4):
                    Normal_car_x = random.choice([50, 150, 250, 350, 450])
                    Normal_car_y = random.randint(-1500, -100)
                    enemies.append([Normal_car_x, Normal_car_y, random.randint(3, 6)])

        
    screen.fill(BLACK)
    draw_road()


    if not game_over:
        for enemy in enemies:
            enemy[1] += enemy[2]
            if enemy[1] > SCREEN_HEIGHT:
                enemy[1] = random.randint(-1500, -100)
                enemy[0] = random.choice([50, 150, 250, 350, 450])
                enemy[2] = random.randint(3, 6)
                score += 1 

        player_rect = pygame.Rect(washing_machine_X, washing_machine_Y, 100, 100)
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], 100, 100)
            if player_rect.colliderect(enemy_rect):
                game_over = True
                if score > high_score:
                    high_score = score
                    with open("highscore.txt", "w") as file:
                        file.write(str(high_score))
    if game_over:
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, RED)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 100))
        font = pygame.font.Font(None, 36)
        text = font.render("Press R to restart", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2))

    
    
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))
    text = font.render(f"High_score: {high_score}", True, WHITE)
    screen.blit(text, (10, 50))
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()