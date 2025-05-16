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

# color
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
GREEN = (188, 227, 199)
BLUE = (32, 32, 200)
RED = (255, 0, 0)

# lane varable
ROAD_WIDTH = 400
LANE_MARKER_WIDTH = 10
LANE_MARKER_HEIGHT = 50

# player varable
player_car_X = 250 #starting pision
player_car_Y = 600 #starting pision
score = 0
high_score = 0
speed = 5 #speed of the cars coming down or road moving
game_over = False 

# import images
player_car = pygame.image.load("Player_washing_machine.png")
player_car = pygame.transform.scale(player_car, (100, 100))
Normal_car = pygame.image.load("jesus_with_baskball.png")
Normal_car = pygame.transform.scale(Normal_car, (100, 100))

# high score save file open as read
try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
except:
    high_score = 0 #high score is set to zero if no high score

# Create 4 lane 
road_markers = [] #empnty list varable
for lane_x in [50, 150, 250, 350, 450]: #placement of the white lanes on the road
    for i in range(5): #markers for the lane
        road_markers.append([lane_x - LANE_MARKER_WIDTH//2, i * 200])


#Enemy cars where they spawn and speed and how ramdon it spawn
enemies = []
for _ in range(4):
    Normal_car_x = random.choice([50, 150, 250, 350]) #where te eneny spawn
    Normal_car_y = random.randint(-1500, -100)
    enemies.append([Normal_car_x, Normal_car_y, random.randint(3, 6)])

#clock tick varable
clock = pygame.time.Clock()

def draw_road(): #draw the element of the road and put the normal car on it
    pygame.draw.rect(screen, GRAY, 
                    (SCREEN_WIDTH//2 - ROAD_WIDTH//2, 0, ROAD_WIDTH, SCREEN_HEIGHT))
    
    for marker in road_markers:
        pygame.draw.rect(screen, WHITE, 
                        (marker[0], marker[1], LANE_MARKER_WIDTH, LANE_MARKER_HEIGHT))
        marker[1] += speed
        if marker[1] > SCREEN_HEIGHT:
            marker[1] = -LANE_MARKER_HEIGHT
            #draw the mornal car and the player car 
    screen.blit(player_car, (player_car_X, player_car_Y))
    
    for enemy in enemies:
        screen.blit(Normal_car, (enemy[0], enemy[1]))

# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            #event
        if event.type == pygame.KEYDOWN:
            # Prevent movement if game over
            if event.key == pygame.K_LEFT and not game_over:
                if player_car_X > 50:
                    player_car_X -= 100 #move one lane left
            if event.key == pygame.K_RIGHT and not game_over:
                if player_car_X < 350:
                    player_car_X += 100 #move one lane right
            #restart game
            if event.key == pygame.K_r and game_over:
                game_over = False
                player_car_X = 250
                player_car_Y = 600
                score = 0
                enemies = []
                for _ in range(4): #reset the normal car after end of game
                    Normal_car_x = random.choice([50, 150, 250, 350])
                    Normal_car_y = random.randint(-1500, -100)
                    enemies.append([Normal_car_x, Normal_car_y, random.randint(3, 6)])

     #make screen black and clear all element   
    screen.fill(BLACK)
    draw_road()

    # when game havent dectect any colloision and hasent ended
    if not game_over:
        for enemy in enemies:
            #enemy moving down
            enemy[1] += enemy[2]
            #reset enemy when not on screen
            if enemy[1] > SCREEN_HEIGHT:
                enemy[1] = random.randint(-1500, -100)
                enemy[0] = random.choice([50, 150, 250, 350])
                enemy[2] = random.randint(3, 6)
                score += 1 
        #collision detection
        player_rect = pygame.Rect(player_car_X, player_car_Y, 100, 100)
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], 100, 100)
            if player_rect.colliderect(enemy_rect):
                game_over = True
                #update high score
                if score > high_score:
                    high_score = score
                    #open high score
                    with open("highscore.txt", "w") as file:
                        file.write(str(high_score))
    #game over display
    if game_over:
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, RED)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 100))
        font = pygame.font.Font(None, 36)
        text = font.render("Press R to restart", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2))

    
    #display score infomation
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))
    text = font.render(f"High_score: {high_score}", True, WHITE)
    screen.blit(text, (10, 50))
    #60 fps
    pygame.display.update()
    clock.tick(60)
#quit
pygame.quit()