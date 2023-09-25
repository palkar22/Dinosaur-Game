import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (WIDTH, HEIGHT)
BACKGROUND_COLOR = (0, 0, 0)  # Black

# Create the game window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Shooting Game")

# Game clock
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Screen/player1-fotor-bg-remover-20230924175337.jpg")
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 0, 0))  # Red bullet
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 0, 255))  # Blue enemy
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, WIDTH)
        self.rect.centery = random.randint(0, HEIGHT)
        self.speed = 2  # Adjust the speed as needed

    def update(self):
        # Implement enemy movement logic here
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
            self.rect.centerx = random.randint(0, WIDTH)

# Create player
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Create bullets
bullets = pygame.sprite.Group()

# Create enemies
enemies = pygame.sprite.Group()

# Create and add enemy sprites to the enemies group
for _ in range(5):  # Create 5 enemy sprites as an example
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Initialize the score
score = 0

# Create a font for the score display
font = pygame.font.Font(None, 36)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

    all_sprites.update()

    # Check for bullet collisions
    hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
    for hit in hits:
        score += 1

    # Add new enemy objects to the game
    if len(enemies) < 5:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Draw everything
    screen.fill(BACKGROUND_COLOR)
    all_sprites.draw(screen)

    # Display the score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
