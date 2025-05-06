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




running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()