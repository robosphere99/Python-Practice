import pygame
import random

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set clock
clock = pygame.time.Clock()
FPS = 60  # Frames per second

# Balloon settings
balloon_radius = 30
balloon_speed = 2
balloon_list = []
pop_radius = 35

# Score
score = 0
font = pygame.font.SysFont("Arial", 30)

# Create a function to generate a new balloon at a random position
def create_balloon():
    x = random.randint(balloon_radius, screen_width - balloon_radius)
    y = screen_height + balloon_radius
    return [x, y]

# Create multiple balloons
for _ in range(5):
    balloon_list.append(create_balloon())

# Game loop
running = True
while running:
    screen.fill(WHITE)
    
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for mouse click to pop balloons
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for balloon in balloon_list:
                balloon_x, balloon_y = balloon
                distance = ((balloon_x - mouse_x) ** 2 + (balloon_y - mouse_y) ** 2) ** 0.5
                if distance < pop_radius:
                    balloon_list.remove(balloon)
                    balloon_list.append(create_balloon())  # Replace the popped balloon
                    score += 1

    # Update balloon positions and draw them
    for balloon in balloon_list:
        balloon[1] -= balloon_speed  # Move the balloon upwards
        if balloon[1] < -balloon_radius:
            balloon[1] = screen_height + balloon_radius  # Reset balloon position

        # Draw balloons
        pygame.draw.circle(screen, RED, (balloon[0], balloon[1]), balloon_radius)

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Set FPS
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
