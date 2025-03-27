import pygame
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400  # Screen dimensions
CELL_SIZE = 10  # Size of each grid cell
WHITE = (255, 255, 255)  # Wall color
GREEN = (0, 255, 0)  # Snake color
RED = (255, 0, 0)  # Food color (weight 1)
ORANGE = (255, 165, 0)  # Food color (weight 3)
YELLOW = (255, 255, 0)  # Food color (weight 2)
BLACK = (0, 0, 0)  # Background color

# Initialize screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Snake properties
snake = [(100, 100), (90, 100), (80, 100)]  # Initial snake position
snake_dir = (CELL_SIZE, 0)  # Initial movement direction
score = 0  # Player score
level = 1  # Game level
speed = 10  # Initial game speed (frames per second)

# Define the walls (borders of the game area)
walls = [(0, i) for i in range(0, HEIGHT, CELL_SIZE)] + [(WIDTH - CELL_SIZE, i) for i in range(0, HEIGHT, CELL_SIZE)] + \
        [(i, 0) for i in range(0, WIDTH, CELL_SIZE)] + [(i, HEIGHT - CELL_SIZE) for i in range(0, WIDTH, CELL_SIZE)]

# Food properties
food = None  # Position of the food
food_weight = 1  # Default weight of food
food_timer = 300  # Timer for food expiration (5 seconds at speed=10)
food_size = CELL_SIZE  # Default food size

# Function to generate food at a random position
def generate_food():
    global food_weight, food_timer, food_size
    while True:
        x = random.randint(1, (WIDTH // CELL_SIZE) - 2) * CELL_SIZE
        y = random.randint(1, (HEIGHT // CELL_SIZE) - 2) * CELL_SIZE
        
        # Ensure food does not spawn inside the snake or walls
        if (x, y) not in snake and (x, y) not in walls:
            food_weight = random.randint(1, 3)  # Randomize food value (1-3)
            food_timer = 300  # Reset food timer
            
            # Adjust food size based on its weight
            food_size = CELL_SIZE + (food_weight - 1) * 5
            return (x, y)

food = generate_food()  # Generate initial food position

# Main game loop
running = True
while running:
    screen.fill(BLACK)  # Clear screen
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit event
            running = False
        elif event.type == pygame.KEYDOWN:  # Key press event
            if event.key == pygame.K_UP and snake_dir != (0, CELL_SIZE):
                snake_dir = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and snake_dir != (0, -CELL_SIZE):
                snake_dir = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and snake_dir != (CELL_SIZE, 0):
                snake_dir = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and snake_dir != (-CELL_SIZE, 0):
                snake_dir = (CELL_SIZE, 0)
    
    # Move snake
    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
    
    # Check for collision with walls or itself
    if new_head in walls or new_head in snake:
        running = False
        continue
    
    snake.insert(0, new_head)  # Add new head position
    
    # Check if snake eats food
    if new_head == food:
        score += food_weight  # Increase score based on food weight
        food = generate_food()  # Generate new food
        
        # Increase level and speed every 3 points
        if score % 3 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()  # Remove last segment to maintain length
    
    # Handle food expiration
    food_timer -= 1
    if food_timer <= 0:
        food = generate_food()
    
    # Draw snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    
    # Draw food with different sizes and colors based on weight
    food_color = RED if food_weight == 1 else (YELLOW if food_weight == 2 else ORANGE)
    pygame.draw.rect(screen, food_color, (food[0] + (CELL_SIZE - food_size) // 2, food[1] + (CELL_SIZE - food_size) // 2, food_size, food_size))
    
    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, WHITE, (wall[0], wall[1], CELL_SIZE, CELL_SIZE))
    
    # Display score, level, and food expiration timer
    font = pygame.font.Font(None, 30)
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Level: {level}", True, WHITE), (10, 40))
    screen.blit(font.render(f"Food Timer: {food_timer//60} s", True, WHITE), (10, 70))  # Display remaining time in seconds
    
    pygame.display.flip()  # Update display
    clock.tick(speed)  # Control game speed

pygame.quit()  # Quit game when loop exits
