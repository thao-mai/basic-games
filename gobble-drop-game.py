import sys
import pygame
import random

pygame.init()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gobble Drop")
clock = pygame.time.Clock()

catcher_width = 25
catcher_height = 15
catcher_x = SCREEN_WIDTH // 2 - catcher_width // 2
catcher_y = SCREEN_HEIGHT // 2 - catcher_height // 2
catcher_speed = 3  # you can adjust your catcher speed
original_catcher_size = (catcher_width, catcher_height)  # reset catcher size after collision

num_drops = 6
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

font = pygame.font.SysFont("Monospace Regular", 32)

# Color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
 
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
    # Walls
    pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, 5))  # upper wall
    pygame.draw.rect(screen, BLACK, (0, SCREEN_HEIGHT - 5, SCREEN_WIDTH, 5))  # lower wall
    pygame.draw.rect(screen, BLACK, (0, 0, 5, SCREEN_HEIGHT))  # left wall
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - 5, 0, 5, SCREEN_HEIGHT))  # right wall
    
    # Scoreboard
    text = font.render(f"Score: {score}", 1, BLUE)
    screen.blit(text, (SCREEN_WIDTH - 210, 30))
    
    # Catcher
    pygame.draw.rect(screen, GREEN, (catcher_x, catcher_y, catcher_width, catcher_height))
    
    # Drops
    for drop in drops:
        drop_x, drop_y = drop
        pygame.draw.rect(screen, RED, (drop_x, drop_y, drop_width, drop_height))

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
            drop_y += 3  # move drops downwards
            drops[idx][1] = drop_y
            
            if (catcher_x < drop_x + drop_width and
                catcher_x + catcher_width > drop_x and
                catcher_y < drop_y + drop_height and
                catcher_y + catcher_height > drop_y):
                
                score += drop_points  
                drops.pop(idx)
                
                catcher_width += drop_width // 2
                catcher_height += drop_height // 2
                break
            
            if drop_y > SCREEN_HEIGHT:
                drops[idx][1] = random.randint(-SCREEN_HEIGHT, -drop_height)
                drops[idx][0] = random.randint(5, SCREEN_WIDTH - drop_width - 5)
        
        if collision_with_walls(catcher_x, catcher_y, catcher_width, catcher_height):
            running = False
            break
        
        screen.fill(WHITE)
        draw_rectangles()  
        
        clock.tick(60)  # 60 FPS

    print("Game Over! Your score:", score)

game_loop()  