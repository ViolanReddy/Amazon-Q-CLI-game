import pygame
import random
import math

pygame.init()

# Game settings
WIDTH, HEIGHT = 640, 640
CELL_SIZE = 20
WALL_SIZE = 20
FPS = 10

# Enhanced pixel art colors
GRASS_LIGHT = (50, 180, 50)
GRASS_DARK = (30, 120, 30)
WALL_BROWN = (139, 90, 43)
WALL_DARK = (101, 67, 33)
WALL_LIGHT = (160, 110, 70)
SNAKE_YELLOW = (255, 215, 0)
SNAKE_GOLD = (255, 165, 0)
SNAKE_DARK = (184, 134, 11)
SNAKE_EYE = (0, 0, 0)
SNAKE_EYE_SHINE = (255, 255, 255)
APPLE_RED = (220, 20, 60)
APPLE_DARK = (139, 0, 0)
APPLE_SHINE = (255, 182, 193)
APPLE_LEAF = (34, 139, 34)
font = pygame.font.Font(None, 36)

# Initialize display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
GAME_WIDTH = WIDTH - 2 * WALL_SIZE
GAME_HEIGHT = HEIGHT - 2 * WALL_SIZE
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Snake initial position (inside walls)
snake = [(WIDTH//2, HEIGHT//2)]
direction = (CELL_SIZE, 0)

# Apple position (inside walls)
apple = (random.randint(1, (WIDTH-2*WALL_SIZE)//CELL_SIZE-1) * CELL_SIZE + WALL_SIZE, 
         random.randint(1, (HEIGHT-2*WALL_SIZE)//CELL_SIZE-1) * CELL_SIZE + WALL_SIZE)

running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                direction = (CELL_SIZE, 0)
    
    # Move snake
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    
    # Check wall collision
    if head[0] < WALL_SIZE or head[0] >= WIDTH-WALL_SIZE or head[1] < WALL_SIZE or head[1] >= HEIGHT-WALL_SIZE:
        game_over = True
    
    # Check self collision
    if head in snake:
        game_over = True
    
    if not game_over:
        snake.insert(0, head)
        
        # Check apple collision
        if head == apple:
            apple = (random.randint(1, (WIDTH-2*WALL_SIZE)//CELL_SIZE-1) * CELL_SIZE + WALL_SIZE, 
                     random.randint(1, (HEIGHT-2*WALL_SIZE)//CELL_SIZE-1) * CELL_SIZE + WALL_SIZE)
        else:
            snake.pop()
    
    # Draw everything
    screen.fill(WALL_BROWN)
    
    # Draw brown walls (pixelated)
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, WALL_SIZE, 4):
            color = WALL_BROWN if (x//4 + y//4) % 2 == 0 else WALL_DARK
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, 4))
            pygame.draw.rect(screen, color, (x, HEIGHT-WALL_SIZE+y, CELL_SIZE, 4))
    for y in range(0, HEIGHT, CELL_SIZE):
        for x in range(0, WALL_SIZE, 4):
            color = WALL_BROWN if (x//4 + y//4) % 2 == 0 else WALL_DARK
            pygame.draw.rect(screen, color, (x, y, 4, CELL_SIZE))
            pygame.draw.rect(screen, color, (WIDTH-WALL_SIZE+x, y, 4, CELL_SIZE))
    
    # Draw grass with checkerboard pattern
    for x in range(WALL_SIZE, WIDTH-WALL_SIZE, CELL_SIZE):
        for y in range(WALL_SIZE, HEIGHT-WALL_SIZE, CELL_SIZE):
            # Checkerboard pattern for grass blocks
            is_dark_block = ((x-WALL_SIZE)//CELL_SIZE + (y-WALL_SIZE)//CELL_SIZE) % 2 == 1
            base_color = GRASS_DARK if is_dark_block else GRASS_LIGHT
            
            # Fill block with base color and add texture
            for px in range(0, CELL_SIZE, 4):
                for py in range(0, CELL_SIZE, 4):
                    pygame.draw.rect(screen, base_color, (x+px, y+py, 4, 4))
    
    # Draw enhanced yellow snake
    for i, segment in enumerate(snake):
        # Snake body with gradient effect
        for px in range(0, CELL_SIZE, 4):
            for py in range(0, CELL_SIZE, 4):
                if px < 4 or px >= CELL_SIZE-4 or py < 4 or py >= CELL_SIZE-4:
                    pygame.draw.rect(screen, SNAKE_DARK, (segment[0]+px, segment[1]+py, 4, 4))
                elif px < 8 or py < 8:
                    pygame.draw.rect(screen, SNAKE_GOLD, (segment[0]+px, segment[1]+py, 4, 4))
                else:
                    pygame.draw.rect(screen, SNAKE_YELLOW, (segment[0]+px, segment[1]+py, 4, 4))
        
        # Enhanced snake head with better eyes
        if i == 0:
            pygame.draw.rect(screen, SNAKE_EYE, (segment[0]+6, segment[1]+6, 4, 4))
            pygame.draw.rect(screen, SNAKE_EYE, (segment[0]+14, segment[1]+6, 4, 4))
            pygame.draw.rect(screen, SNAKE_EYE_SHINE, (segment[0]+6, segment[1]+6, 2, 2))
            pygame.draw.rect(screen, SNAKE_EYE_SHINE, (segment[0]+14, segment[1]+6, 2, 2))
    
    # Draw enhanced pixelated apple
    for px in range(0, CELL_SIZE, 4):
        for py in range(4, CELL_SIZE, 4):
            if (px-CELL_SIZE//2)**2 + (py-CELL_SIZE//2)**2 <= (CELL_SIZE//2-1)**2:
                if px <= CELL_SIZE//2 and py <= CELL_SIZE//2+2:
                    pygame.draw.rect(screen, APPLE_SHINE, (apple[0]+px, apple[1]+py, 4, 4))
                elif px >= CELL_SIZE//2+4 or py >= CELL_SIZE//2+4:
                    pygame.draw.rect(screen, APPLE_DARK, (apple[0]+px, apple[1]+py, 4, 4))
                else:
                    pygame.draw.rect(screen, APPLE_RED, (apple[0]+px, apple[1]+py, 4, 4))
    
    pygame.draw.rect(screen, APPLE_LEAF, (apple[0]+CELL_SIZE//2-2, apple[1], 4, 8))
    
    # Draw score
    score_text = font.render(f'Score: {len(snake)-1}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
    # Draw game over screen with restart button
    if game_over:
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = font.render('GAME OVER!', True, (255, 255, 255))
        text_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2-50))
        screen.blit(game_over_text, text_rect)
        
        # Restart button
        button_rect = pygame.Rect(WIDTH//2-80, HEIGHT//2, 160, 50)
        pygame.draw.rect(screen, (100, 100, 100), button_rect)
        pygame.draw.rect(screen, (255, 255, 255), button_rect, 3)
        
        restart_text = font.render('RESTART', True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=button_rect.center)
        screen.blit(restart_text, restart_rect)
        
        # Check for restart button click
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        if button_rect.collidepoint(mouse_pos) and mouse_clicked:
            # Reset game
            snake = [(WIDTH//2, HEIGHT//2)]
            direction = (CELL_SIZE, 0)
            apple = (random.randint(1, (WIDTH-2*WALL_SIZE)//CELL_SIZE-1) * CELL_SIZE + WALL_SIZE, 
                     random.randint(1, (HEIGHT-2*WALL_SIZE)//CELL_SIZE-1) * CELL_SIZE + WALL_SIZE)
            game_over = False
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()