import random
import time
import pygame

# Initialize Pygame
pygame.init()

# Game settings
maze_size = 8
cell_size = 100  # Each cell in the maze will be 100x100 pixels
screen_width = maze_size * cell_size
screen_height = maze_size * cell_size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze of Fortune")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (169, 169, 169)

# Load the background image
background_image = pygame.image.load('cave.jpg')  # Replace with your image file
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Load the player image (replace 'player.png' with your image file)
player_image = pygame.image.load('runner.png')  # Replace with the path to your player image
player_image = pygame.transform.scale(player_image, (cell_size // 2, cell_size // 2))  # Resize it to fit within the cell

# Maze setup
maze_size = 8
maze = [['.' for _ in range(maze_size)] for _ in range(maze_size)]
lasers = []
start_pos = (0, 0)
end_pos = (maze_size - 1, maze_size - 1)
reward = 20000
time_limit = 3600  # 1 hour in seconds

# Player setup
player_pos = start_pos

# Place lasers randomly
while len(lasers) < 5:
    x, y = random.randint(0, maze_size - 1), random.randint(0, maze_size - 1)
    if (x, y) != start_pos and (x, y) != end_pos and (x, y) not in lasers:
        lasers.append((x, y))

# Game timer setup
start_time = time.time()

# Font setup
font = pygame.font.Font(None, 36)

# Function to draw the maze and player
def draw_maze():
    for i in range(maze_size):
        for j in range(maze_size):
            # Draw grid cells
            rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
            if (i, j) in lasers:
                pygame.draw.rect(screen, RED, rect)  # Draw laser as red square
            else:
                pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 3)  # Draw the grid lines
           
            # Draw the player image at the player's position
            if (i, j) == player_pos:
                # Center the image inside the cell
                player_rect = player_image.get_rect(center=rect.center)
                screen.blit(player_image, player_rect)  # Draw the player image
            # Draw the goal
            elif (i, j) == end_pos:
                pygame.draw.circle(screen, (0, 0, 255), rect.center, cell_size // 3)

# Function to handle time and display remaining time
def draw_time_left(time_left):
    time_text = font.render(f"Time Left: {time_left} seconds", True, BLACK)
    screen.blit(time_text, (10, 10))

# Function to check for laser collision
def check_collision():
    if player_pos in lasers:
        return True
    return False

# Function to handle game over (win or lose)
def game_over(message):
    game_over_text = font.render(message, True, BLACK)
    screen.blit(game_over_text, (screen_width // 4, screen_height // 2))

# Main game loop
running = True
while running:
    # Calculate remaining time
    elapsed_time = time.time() - start_time
    time_left = time_limit - int(elapsed_time)

    if time_left <= 0:
        game_over("Time's up! You failed to complete the maze in time.")
        pygame.display.update()
        pygame.time.wait(3000)
        break

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_pos[0] > 0:
        player_pos = (player_pos[0] - 1, player_pos[1])
    elif keys[pygame.K_DOWN] and player_pos[0] < maze_size - 1:
        player_pos = (player_pos[0] + 1, player_pos[1])
    elif keys[pygame.K_LEFT] and player_pos[1] > 0:
        player_pos = (player_pos[0], player_pos[1] - 1)
    elif keys[pygame.K_RIGHT] and player_pos[1] < maze_size - 1:
        player_pos = (player_pos[0], player_pos[1] + 1)

    # Collision check
    if check_collision():
        game_over("You've hit a laser! Game Over!")
        pygame.display.update()
        pygame.time.wait(3000)
        break

    # Check for win
    if player_pos == end_pos:
        game_over(f"Congratulations! You win ${reward}")
        pygame.display.update()
        pygame.time.wait(3000)
        break

    # Drawing everything
    screen.blit(background_image, (0, 0))  # Draw the background image first
    draw_maze()
    draw_time_left(time_left)

    # Update the display
    pygame.display.update()

    # Frame rate
    pygame.time.Clock().tick(30)  # 30 frames per second

# Quit Pygame
pygame.quit()
