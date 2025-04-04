import sys
import pygame
import random

# Initialize
pygame.init()

# Set screen size/dimensions
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create your screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gobble Drop")
clock = pygame.time.Clock()
screen_perimeter_color = BLACK
FPS_AMT = 60

# Catcher attributes
catcher_width = 25
catcher_height = 15
catcher_color = GREEN
catcher_x = SCREEN_WIDTH // 2 - catcher_width // 2
catcher_y = SCREEN_HEIGHT // 2 - catcher_height // 2
catcher_speed = 3  # you can adjust your catcher speed
original_catcher_size = (catcher_width, catcher_height)  # To reset catcher size after collision

# Drop attributes
num_drops = 6
drop_color = RED
drop_width = 20
drop_height = 20
drop_spacing = 25
drop_points = 10
drops = []

def spawn_drops():
    drop_x = (SCREEN_WIDTH - (drop_width + drop_spacing) * num_drops) // 2 + drop_spacing
    for _ in range(num_drops):
        drop_y = random.randint(-SCREEN_HEIGHT, -drop_height)
        drops.append([drop_x, drop_y])
        drop_x += drop_width + drop_spacing

spawn_drops()

# Font for displaying score
font = pygame.font.SysFont("Monospace Regular", 32)
 
# Moving direction of catcher
moving_right = False
moving_left = False
moving_up = False
moving_down = False

score = 0

def collision_with_walls(catcher_x, catcher_y, catcher_width, catcher_height):
    if catcher_x < 0 or catcher_x + catcher_width > SCREEN_WIDTH:
        return True
    if catcher_y < 0 or catcher_y + catcher_height > SCREEN_HEIGHT:
        return True
    return False

def draw_rectangles():
    # Walls in black
    pygame.draw.rect(screen, screen_perimeter_color, (0, 0, SCREEN_WIDTH, 5))  # upper wall
    pygame.draw.rect(screen, screen_perimeter_color, (0, SCREEN_HEIGHT - 5, SCREEN_WIDTH, 5))  # lower wall
    pygame.draw.rect(screen, screen_perimeter_color, (0, 0, 5, SCREEN_HEIGHT))  # left wall
    pygame.draw.rect(screen, screen_perimeter_color, (SCREEN_WIDTH - 5, 0, 5, SCREEN_HEIGHT))  # right wall
    
    # Scoreboard in blue
    text = font.render(f"Score: {score}", 1, BLUE)
    screen.blit(text, (SCREEN_WIDTH - 210, 30))
    
    # Draw the green catcher
    pygame.draw.rect(screen, catcher_color, (catcher_x, catcher_y, catcher_width, catcher_height))
    
    # Drops in red
    for drop in drops:
        # Ensure drop is a tuple or list with 2 coordinate elems: [x, y]
        drop_x, drop_y = drop
        pygame.draw.rect(screen, drop_color, (drop_x, drop_y, drop_width, drop_height))

    pygame.display.flip()

def game_loop():
    global catcher_x, catcher_y, catcher_width, catcher_height, moving_right, moving_left,  moving_up, moving_down, score
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit(0)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moving_left = True
                if event.key == pygame.K_RIGHT:
                    moving_right = True
                if event.key == pygame.K_UP:
                    moving_up = True
                if event.key == pygame.K_DOWN:
                    moving_down = True
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    moving_left = False
                if event.key == pygame.K_RIGHT:
                    moving_right = False
                if event.key == pygame.K_UP:
                    moving_up = False
                if event.key == pygame.K_DOWN:
                    moving_down = False

        # Update catcher position
        if moving_right:
            catcher_x += catcher_speed
        if moving_left:
            catcher_x -= catcher_speed
        if moving_up:
            catcher_y -= catcher_speed
        if moving_down:
            catcher_y += catcher_speed
        
        # Game logic
        for idx, drop in enumerate(drops):
            drop_x, drop_y = drop
            drop_y += 3  # Move drops downwards
            drops[idx][1] = drop_y
            
            # Check for collision with catcher and drops
            if (catcher_x < drop_x + drop_width and
                catcher_x + catcher_width > drop_x and
                catcher_y < drop_y + drop_height and
                catcher_y + catcher_height > drop_y):
                
                # Increase score
                score += drop_points  
                drops.pop(idx)  # Remove drop from the list
                
                # Increase catcher size on collision
                catcher_width += drop_width // 2
                catcher_height += drop_height // 2
                break
            
            # Reset drops randomly if they move off the screen
            if drop_y > SCREEN_HEIGHT:
                drops[idx][1] = random.randint(-SCREEN_HEIGHT, -drop_height)
                drops[idx][0] = random.randint(5, SCREEN_WIDTH - drop_width - 5)
        
        # Check for collision with walls (game ends)
        if collision_with_walls(catcher_x, catcher_y, catcher_width, catcher_height):
            running = False
            break
        
        # Draw everything
        screen.fill(WHITE)
        draw_rectangles()  
        clock.tick(FPS_AMT)  # 60 FPS

    # Touch the walls to end the game
    print("Game Over! Your score:", score)

game_loop()
