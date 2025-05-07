import pygame
import random

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car_Game")
game_icon=pygame.image.load('game_icon.png')
pygame.display.set_icon(game_icon)

BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
GREEN = (188, 227, 199)
BLUE = (32, 32, 200)
RED = (0, 255, 0)

ROAD_WIDTH = 600
LANE_MARKER_WIDTH = 10
LANE_MARKER_HEIGHT = 50

#where player spawns
washing_machine_X = 250
washing_machine_Y = 600
#player score
score = 0
#player high score
high_score = 0
#speed of road, how fast it goes down, and how fast enemie car comes
speed = 5
game_over = False

washing_machine = pygame.image.load("Player_washing_machine.png")
washing_machine = pygame.transform.scale(washing_machine, (100, 100))


try:
    with open("highscore.txt") as file:
        high_score = int(file.read())
except:
    high_score = 0


road_markers = []
for lane_x in [100, 250, 400]:
    for i in range(5):
        road_markers.append([lane_x - LANE_MARKER_WIDTH//2, i * 200])
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




running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))
    text = font.render(f"High_score: {high_score}", True, WHITE)
    screen.blit(text, (10, 50))

    screen.fill(BLACK)
    draw_road()
    pygame.display.update()
    clock.tick(60)

pygame.quit()