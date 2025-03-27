import pygame, sys
from pygame.locals import *
import random, time

# Initialize pygame
pygame.init()

# Setting up FPS
FPS = 60  # Frames per second
FramePerSec = pygame.time.Clock()

# Colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5  # Initial speed of enemy movement
SCORE = 0  # Score counter
COINS = 0  # Number of collected coins

# Load background music
pygame.mixer.music.load("racer/background.wav")
pygame.mixer.music.play(-1)  # Loop indefinitely

# Fonts for displaying text
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load background image
background = pygame.image.load("racer/AnimatedStreet.png")

# Create game screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")  # Window title

# Enemy class 
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("racer/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)  # Random initial position
    
    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)  # Move enemy downward
        if self.rect.bottom > SCREEN_HEIGHT:  # If enemy moves past screen
            SCORE += 1  # Increase score
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)  # Reset enemy position

# Player class 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("racer/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)  # Initial position
    
    def move(self):
        pressed_keys = pygame.key.get_pressed()  # Get pressed keys
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)  # Move left
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:        
            self.rect.move_ip(5, 0)  # Move right
        if self.rect.top > 0 and pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)  # Move up
        if self.rect.bottom < SCREEN_HEIGHT and pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)  # Move down

# Coin class 
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.value = random.randint(1, 3)  # Random coin value (1 to 3)
        self.image = pygame.image.load("racer/coin.png")
        size = 20 + (self.value - 1) * 10  # Small: 20x20, Medium: 30x30, Large: 40x40
        self.image = pygame.transform.scale(self.image, (size, size))  # Resize coin based on value
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(40, SCREEN_HEIGHT - 40))  # Random position
    
    def respawn(self):
        self.value = random.randint(1, 3)  # New random value
        size = 20 + (self.value - 1) * 10  # Resize based on value
        self.image = pygame.transform.scale(pygame.image.load("racer/coin.png"), (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(40, SCREEN_HEIGHT - 40))  # Move coin to new position

# Setting up Sprites
P1 = Player()
E1 = Enemy()
coins = pygame.sprite.Group()
for _ in range(3):  # Generate 3 coins
    coins.add(Coin())

# Creating Sprite Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1)

# Adding a new User event to increase speed over time
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)  # Increase speed every second

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5  # Gradually increase enemy speed
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update display with background
    DISPLAYSURF.blit(background, (0, 0))
    
    # Display score and collected coins
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    coin_count = font_small.render(f"Coins: {COINS}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coin_count, (300, 10))
    
    # Move only player and enemies
    for entity in [P1, *enemies]:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)
    
    for coin_entity in coins:
        DISPLAYSURF.blit(coin_entity.image, coin_entity.rect)
    
    # Check for collisions between player and enemies (game over condition)
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('racer/crash.wav').play()  # Play crash sound
        time.sleep(1)
        DISPLAYSURF.fill(RED)  # Change screen color to red
        DISPLAYSURF.blit(game_over, (30, 250))  # Display game over message
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()
    
    # Check for collisions between player and coins
    for coin in coins:
        if pygame.sprite.collide_rect(P1, coin):
            COINS += coin.value  # Increase coin count by coin's value
            coin.respawn()  # Move the coin to a new random location
            
            # Increase enemy speed every 5 collected coins
            if COINS % 5 == 0:
                SPEED += 1
    
    pygame.display.update()  # Refresh the screen
    FramePerSec.tick(FPS)  # Control game speed
