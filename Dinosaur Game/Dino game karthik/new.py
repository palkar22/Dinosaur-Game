
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
INTRO_IMAGE = "Screen/WhatsApp Image 2023-09-25 at 11.38.01.jpg"  # Specify your intro image file (PNG)
OUTRO_IMAGE = "Screen/WhatsApp Image 2023-09-25 at 11.39.05.jpg"  # Specify your outro image file (PNG)
INTRO_MUSIC = 'music/wc.mp3' # Specify your intro music file
GAME_MUSIC = "music/bgm.mp3"    # Specify your in-game music file
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
PLAYER_COLOR = (255, 0, 0)
GROUND_HEIGHT = 50
FPS = 60
GRAVITY = 1
JUMP_STRENGTH = -15
LANE_WIDTH = WIDTH // 3
PLAYER_INITIAL_X = LANE_WIDTH  # Start in the left lane
PLAYER_INITIAL_Y = HEIGHT - PLAYER_HEIGHT - GROUND_HEIGHT
PLAYER_SPEED = 5
OBSTACLE_GAP = 200
OBSTACLE_SPEED = 5
COIN_WIDTH, COIN_HEIGHT = 30, 30
COIN_COLOR = (255, 255, 0)
SCORE_FONT_SIZE = 36
GAME_OVER_FONT_SIZE = 72
COIN_FONT_SIZE = 48

# Load the intro and outro images
intro_image = pygame.image.load(INTRO_IMAGE)
intro_image = pygame.transform.scale(intro_image, (WIDTH, HEIGHT))

outro_image = pygame.image.load(OUTRO_IMAGE)
outro_image = pygame.transform.scale(outro_image, (WIDTH, HEIGHT))

# Load the background image
background = pygame.Surface((WIDTH, HEIGHT))  # Create an empty surface for the background

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Train Inspector Runner")

# Initialize clock
clock = pygame.time.Clock()

# Initialize intro music
pygame.mixer.music.load(INTRO_MUSIC)

# Initialize in-game music
pygame.mixer.music.load(GAME_MUSIC)

# Player attributes
player_x = PLAYER_INITIAL_X
player_y = PLAYER_INITIAL_Y
player_velocity_y = 0
on_ground = True
current_lane = 1  # Start in the middle lane (0: left, 1: middle, 2: right)

# Ground
ground_rect = pygame.Rect(0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT)

# Obstacles
obstacle_width = 30
obstacle_height = 40
obstacle_x = random.choice([0, LANE_WIDTH, 2 * LANE_WIDTH])
obstacle_y = HEIGHT - obstacle_height - GROUND_HEIGHT

# Coins
coin_x = random.choice([0, LANE_WIDTH, 2 * LANE_WIDTH])
coin_y = HEIGHT - obstacle_height - GROUND_HEIGHT
coin_collected = False
coins_collected_count = 0  # Count of collected coins

# Score
score = 0

# Game state
game_over = False
game_started = False
restart_game = False  # Flag to control game restart

# Function to reposition coin if it's too close to the obstacle
def reposition_coin():
    new_coin_x = random.choice([0, LANE_WIDTH, 2 * LANE_WIDTH])
    new_coin_y = HEIGHT - obstacle_height - GROUND_HEIGHT
    return new_coin_x, new_coin_y

# Function to display game over screen with score and prompt to restart
def show_game_over():
    pygame.mixer.music.stop()  # Stop in-game music

    screen.blit(outro_image, (0, 0))

    game_over_font = pygame.font.Font(None, GAME_OVER_FONT_SIZE)
    score_font = pygame.font.Font(None, SCORE_FONT_SIZE)
    press_enter_font = pygame.font.Font(None, GAME_OVER_FONT_SIZE // 2)

    game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    press_enter_text = press_enter_font.render("Press Enter to Restart", True, (255, 255, 255))

    game_over_text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    score_text_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    press_enter_text_rect = press_enter_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

    screen.blit(game_over_text, game_over_text_rect)
    screen.blit(score_text, score_text_rect)
    screen.blit(press_enter_text, press_enter_text_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Reset game state
                    restart_game = False
                    pygame.mixer.music.load(INTRO_MUSIC)
                    pygame.mixer.music.play(-1)  # Play intro music in a loop
                    return

# Main game loop
pygame.mixer.music.play(-1)  # Play intro music in a loop

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_started and not game_over:
        # Handle player input (arrow keys)
        keys = pygame.key.get_pressed()

        if on_ground:
            if keys[pygame.K_UP]:
                player_velocity_y = JUMP_STRENGTH
                on_ground = False

            if keys[pygame.K_LEFT] and current_lane > 0:
                current_lane -= 1
                player_x -= LANE_WIDTH
            elif keys[pygame.K_RIGHT] and current_lane < 2:
                current_lane += 1
                player_x += LANE_WIDTH

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
        obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)

        if player_rect.colliderect(obstacle_rect):
            print("Game Over")
            game_over = True

        # Check if the obstacle has passed the player
        if obstacle_x + obstacle_width < player_x:
            obstacle_x = WIDTH
            obstacle_y = HEIGHT - obstacle_height - GROUND_HEIGHT
            score += 1

        # Update coins
        coin_x -= OBSTACLE_SPEED

        # Check for collision with coin
        coin_rect = pygame.Rect(coin_x, coin_y, COIN_WIDTH, COIN_HEIGHT)

        if player_rect.colliderect(coin_rect) and not coin_collected:
            coin_collected = True
            coins_collected_count += 1  # Increase coin count
            score += 10  # Increase score for collecting coins
            coin_x, coin_y = reposition_coin()  # Respawn coin
            coin_collected = False

        # Check if the coin has passed the player
        if coin_x + COIN_WIDTH < player_x:
            coin_x, coin_y = reposition_coin()  # Respawn coin
            coin_collected = False

        # Draw background
        screen.blit(background, (0, 0))

        # Draw ground
        pygame.draw.rect(screen, (0, 255, 0), ground_rect)

        # Draw player
        pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))

        # Draw obstacle
        pygame.draw.rect(screen, (0, 0, 255), (obstacle_x, obstacle_y, obstacle_width, obstacle_height))

        # Draw coin
        pygame.draw.rect(screen, COIN_COLOR, (coin_x, coin_y, COIN_WIDTH, COIN_HEIGHT))

        # Draw score and coin count
        font = pygame.font.Font(None, SCORE_FONT_SIZE)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        coin_text = font.render(f"Coins: {coins_collected_count}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(coin_text, (10, 50))

        # Check for game over condition
        if game_over:
            show_game_over()

        # Update the display
        pygame.display.flip()

        # Control frame rate
        clock.tick(FPS)
    else:
        # Display "Press Enter to Start" screen
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            game_started = True
            restart_game = False
            pygame.mixer.music.stop()  # Stop intro music
            pygame.mixer.music.load(GAME_MUSIC)  # Switch to in-game music
            pygame.mixer.music.play(-1)  # Play in-game music in a loop

        screen.blit(intro_image, (0, 0))

        font = pygame.font.Font(None, GAME_OVER_FONT_SIZE)
        press_enter_text = font.render("Press Enter to Start", True, (255, 255, 255))
        press_enter_text_rect = press_enter_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        screen.blit(press_enter_text, press_enter_text_rect)
        pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()
