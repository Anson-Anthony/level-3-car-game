######################
## By Anson Anthony ##
## Car Game         ##
######################

# Import necessary libraries
import pygame  # For game functionality
import random  # For random enemy positioning

# Initialize Pygame modules
pygame.init()


# Game Settings


# Display configuration
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 720
FPS = 60  # Frames per second

# Player configuration
PLAYER_START_X = 250  # Initial X position
PLAYER_START_Y = 600  # Initial Y position
CAR_WIDTH = 100       # Vehicle dimensions
CAR_HEIGHT = 100

# Road configuration
ROAD_WIDTH = 420       # Width of drivable area
LANE_MARKER_WIDTH = 10  # Lane line dimensions
LANE_MARKER_HEIGHT = 50
LANE_POSITIONS = [50, 150, 250, 350]  # X positions for lanes
ROAD_MARKER_INTERVAL = 200  # Vertical spacing between lane markers
BASE_SPEED = 5         # Base scroll speed

# Enemy configuration
ENEMY_MIN_Y = -800     # Spawn range vertical boundaries
ENEMY_MAX_Y = -100
ENEMY_MIN_SPEED = 5    # Speed variation
ENEMY_MAX_SPEED = 8

# UI configuration
FONT_SIZE = 36          # Regular text size
GAME_OVER_FONT_SIZE = 74  # Game over text size
TEXT_OFFSET_X = 10      # Score positions
SCORE_TEXT_Y = 10
HIGH_SCORE_TEXT_Y = 50
GAME_OVER_Y_OFFSET = -100  # Game over text positioning
RESTART_TEXT_Y_OFFSET = 0

# Color RGB
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)



# Score Tracking Class

class Score:
    def __init__(self):
        self.current = 0
        self.high = self.load_high_score()
    
    def load_high_score(self):
        # Load high score from file or return 0 if not found
        try:
            with open("highscore.txt", "r") as file:
                return int(file.read())
        except:
            return 0
    
    def save_high_score(self):
        # Persist high score to file
        with open("highscore.txt", "w") as file:
            file.write(str(self.high))
    
    def increment(self):
        # Increase current score
        self.current += 1
    
    def reset(self):
        # Reset current score for new game
        self.current = 0
    
    def update_high_score(self):
        # Update high score if current exceeds previous record
        if self.current > self.high:
            self.high = self.current
            self.save_high_score()


# Game Initialization


# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car_Game")
game_icon = pygame.image.load('game_icon.png')
pygame.display.set_icon(game_icon)

# Load and scale game assets
#collision scale
player_car = pygame.image.load("car_1.png")
player_car = pygame.transform.scale(player_car, (CAR_WIDTH, CAR_HEIGHT))
Normal_car = pygame.image.load("car_3.png")
Normal_car = pygame.transform.scale(Normal_car, (CAR_WIDTH, CAR_HEIGHT))

# Initialize road markers
road_markers = []
for lane_x in LANE_POSITIONS + [450]:  # Includes right boundary
    for i in range(5):
        road_markers.append([lane_x - LANE_MARKER_WIDTH//2, i * ROAD_MARKER_INTERVAL])

# Game control variables
clock = pygame.time.Clock()
score = Score()
game_over = False


# Game Logic Functions


def initialize_enemies():
    #Create initial enemy cars with random positions and speeds
    enemies = []
    for _ in range(4):
        x = random.choice(LANE_POSITIONS)
        y = random.randint(ENEMY_MIN_Y, ENEMY_MAX_Y)
        speed = random.randint(ENEMY_MIN_SPEED, ENEMY_MAX_SPEED)
        enemies.append([x, y, speed])
    return enemies

def update_enemies(enemies):
    #Update enemy positions and handle respawning
    for enemy in enemies:
        enemy[1] += enemy[2]  # Move down the screen
        # Respawn enemies that exit bottom of screen
        if enemy[1] > SCREEN_HEIGHT:
            enemy[1] = random.randint(ENEMY_MIN_Y, ENEMY_MAX_Y)
            enemy[0] = random.choice(LANE_POSITIONS)
            enemy[2] = random.randint(ENEMY_MIN_SPEED, ENEMY_MAX_SPEED)
            score.increment()  # Increase score for avoided cars

def check_collision(player_rect, enemies):
    #Check collision between player and any enemy
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], CAR_WIDTH, CAR_HEIGHT)
        if player_rect.colliderect(enemy_rect):
            return True
    return False


# Drawing Functions


def draw_road(player_x, player_y, enemies):
    # Draw all road elements and vehicles
    # Draw road background
    pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH//2 - ROAD_WIDTH//2, 0, ROAD_WIDTH, SCREEN_HEIGHT))
    
    # Animate and draw lane markers
    for marker in road_markers:
        pygame.draw.rect(screen, WHITE, (marker[0], marker[1], LANE_MARKER_WIDTH, LANE_MARKER_HEIGHT))
        marker[1] += BASE_SPEED  # Move markers down
        # Reset markers that exit screen
        if marker[1] > SCREEN_HEIGHT:
            marker[1] = -LANE_MARKER_HEIGHT
            
    # Draw player and enemy cars
    screen.blit(player_car, (player_x, player_y))
    for enemy in enemies:
        screen.blit(Normal_car, (enemy[0], enemy[1]))

def draw_scores():
    #Display current and high scores
    font = pygame.font.Font(None, FONT_SIZE)
    score_text = font.render(f"Score: {score.current}", True, WHITE)
    screen.blit(score_text, (TEXT_OFFSET_X, SCORE_TEXT_Y))
    high_score_text = font.render(f"High Score: {score.high}", True, WHITE)
    screen.blit(high_score_text, (TEXT_OFFSET_X, HIGH_SCORE_TEXT_Y))

def draw_game_over():
    # Display game over message and restart prompt
    font = pygame.font.Font(None, GAME_OVER_FONT_SIZE)
    text = font.render("GAME OVER", True, RED)
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 + GAME_OVER_Y_OFFSET))
    
    font = pygame.font.Font(None, FONT_SIZE)
    text = font.render("Press R to restart", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 + RESTART_TEXT_Y_OFFSET))


# Game Loop

# Initialize game objects
enemies = initialize_enemies()
player_x = PLAYER_START_X
player_y = PLAYER_START_Y
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if not game_over:
                # Player movement
                if event.key == pygame.K_LEFT and player_x > LANE_POSITIONS[0]:
                    player_x -= 100  # Move left one lane
                if event.key == pygame.K_RIGHT and player_x < LANE_POSITIONS[-1]:
                    player_x += 100  # Move right one lane
            
            # Restart mechanism
            if event.key == pygame.K_r and game_over:
                game_over = False
                player_x = PLAYER_START_X
                player_y = PLAYER_START_Y
                score.reset()
                enemies = initialize_enemies()

    # Clear screen
    screen.fill(BLACK)
    
    # Draw game elements
    draw_road(player_x, player_y, enemies)

    # Game logic
    if not game_over:
        update_enemies(enemies)
        player_rect = pygame.Rect(player_x, player_y, CAR_WIDTH, CAR_HEIGHT)
        if check_collision(player_rect, enemies):
            game_over = True
            score.update_high_score()

    # Draw UI elements
    draw_scores()
    if game_over:
        draw_game_over()

    # Update display and maintain FPS
    pygame.display.update()
    clock.tick(FPS)

# Clean up when loop exits
pygame.quit()