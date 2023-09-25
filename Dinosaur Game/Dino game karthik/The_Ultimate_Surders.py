# import pygame
# import sys
# import random

# # Initialize Pygame
# pygame.init()

# # Constants
# WIDTH, HEIGHT = 800, 400
# BACKGROUND_COLOR = (0, 0, 0)
# PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
# PLAYER_COLOR = (255, 0, 0)
# GROUND_HEIGHT = 50
# GROUND_COLOR = (0, 255, 0)
# FPS = 60
# GRAVITY = 1
# JUMP_STRENGTH = -15
# OBSTACLE_WIDTH = 30
# OBSTACLE_HEIGHT = 40
# OBSTACLE_COLOR = (0, 0, 255)
# OBSTACLE_GAP = 200
# OBSTACLE_SPEED = 5
# SCORE_FONT_SIZE = 36

# # Initialize the screen
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Endless Runner")

# # Initialize clock
# clock = pygame.time.Clock()

# # Player attributes
# player_x = WIDTH // 4
# player_y = HEIGHT - PLAYER_HEIGHT - GROUND_HEIGHT
# player_velocity_y = 0
# on_ground = True

# # Ground
# ground_rect = pygame.Rect(0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT)

# # Obstacles
# obstacle_width = OBSTACLE_WIDTH
# obstacle_height = OBSTACLE_HEIGHT
# obstacle_x = WIDTH
# obstacle_y = HEIGHT - obstacle_height - GROUND_HEIGHT

# # Score
# score = 0

# # Game loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Handle player input (one-button control)
#     keys = pygame.key.get_pressed()
#     if on_ground and keys[pygame.K_SPACE]:
#         player_velocity_y = JUMP_STRENGTH
#         on_ground = False

#     # Update player physics
#     player_velocity_y += GRAVITY
#     player_y += player_velocity_y

#     # Check if player is on the ground
#     if player_y >= HEIGHT - PLAYER_HEIGHT - GROUND_HEIGHT:
#         player_y = HEIGHT - PLAYER_HEIGHT - GROUND_HEIGHT
#         on_ground = True

#     # Update obstacles
#     obstacle_x -= OBSTACLE_SPEED

#     # Check for collision with obstacle
#     player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
#     obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

#     if player_rect.colliderect(obstacle_rect):
#         print("Game Over")
#         running = False

#     # Check if the obstacle has passed the player
#     if obstacle_x + OBSTACLE_WIDTH < player_x:
#         obstacle_x = WIDTH
#         obstacle_y = HEIGHT - obstacle_height - GROUND_HEIGHT
#         score += 1

#     # Clear the screen
#     screen.fill(BACKGROUND_COLOR)

#     # Draw ground
#     pygame.draw.rect(screen, GROUND_COLOR, ground_rect)

#     # Draw player
#     pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))

#     # Draw obstacle
#     pygame.draw.rect(screen, OBSTACLE_COLOR, (obstacle_x, obstacle_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

#     # Draw score
#     font = pygame.font.Font(None, SCORE_FONT_SIZE)
#     score_text = font.render(f"Score: {score}", True, (255, 255, 255))
#     screen.blit(score_text, (10, 10))

#     # Update the display
#     pygame.display.flip()

#     # Control frame rate
#     clock.tick(FPS)

# # Quit the game
# pygame.quit()
# sys.exit()
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
BACKGROUND_COLOR = (0, 0, 0)
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
PLAYER_COLOR = (255, 0, 0)
GROUND_HEIGHT = 50
GROUND_COLOR = (0, 255, 0)
FPS = 60
GRAVITY = 1
JUMP_STRENGTH = -15
SLIDE_DURATION = 30
OBSTACLE_WIDTH = 30
OBSTACLE_HEIGHT = 40
OBSTACLE_COLOR = (0, 0, 255)
OBSTACLE_GAP = 200
OBSTACLE_SPEED = 5
SCORE_FONT_SIZE = 36

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Runner")

# Initialize clock
clock = pygame.time.Clock()

# Player attributes
player_x = WIDTH // 4
player_y = HEIGHT - PLAYER_HEIGHT - GROUND_HEIGHT
player_velocity_y = 0
on_ground = True
is_sliding = False
slide_count = 0

# Ground
ground_rect = pygame.Rect(0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT)

# Obstacles
obstacle_width = OBSTACLE_WIDTH
obstacle_height = OBSTACLE_HEIGHT
obstacle_x = WIDTH
obstacle_y = HEIGHT - obstacle_height - GROUND_HEIGHT

# Score
score = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player input (arrow keys)
    keys = pygame.key.get_pressed()

    if on_ground:
        if keys[pygame.K_UP]:
            player_velocity_y = JUMP_STRENGTH
            on_ground = False
        elif keys[pygame.K_DOWN]:
            is_sliding = True

    # Slide duration
    if is_sliding:
        slide_count += 1
        if slide_count >= SLIDE_DURATION:
            is_sliding = False
            slide_count = 0

    # Update player physics
    player_velocity_y += GRAVITY
    player_y += player_velocity_y

    # Check if player is on the ground
    if player_y >= HEIGHT - PLAYER_HEIGHT - GROUND_HEIGHT:
        player_y = HEIGHT - PLAYER_HEIGHT - GROUND_HEIGHT
        on_ground = True

    # Update obstacles
    obstacle_x -= OBSTACLE_SPEED

    # Check for collision with obstacle
    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

    if player_rect.colliderect(obstacle_rect):
        print("Game Over")
        running = False

    # Check if the obstacle has passed the player
    if obstacle_x + OBSTACLE_WIDTH < player_x:
        obstacle_x = WIDTH
        obstacle_y = HEIGHT - obstacle_height - GROUND_HEIGHT
        score += 1

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw ground
    pygame.draw.rect(screen, GROUND_COLOR, ground_rect)

    # Draw player
    pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))

    # Draw obstacle
    pygame.draw.rect(screen, OBSTACLE_COLOR, (obstacle_x, obstacle_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

    # Draw score
    font = pygame.font.Font(None, SCORE_FONT_SIZE)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()
 