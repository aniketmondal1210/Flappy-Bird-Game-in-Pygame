import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 70)

# Bird properties
bird_x = 50
bird_y = 300
bird_radius = 20
bird_velocity = 0
gravity = 0.5
jump_strength = -10

# Pipe properties
pipe_width = 70
pipe_gap = 150
pipe_velocity = 3
pipe_frequency = 1500  # milliseconds

# Score
score = 0

# Event for adding pipes
ADD_PIPE = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_PIPE, pipe_frequency)

# Pipes list: each pipe is represented by [x, height_of_top_pipe]
pipes = []

# Game state
game_over = False


def draw_bird(x, y):
    pygame.draw.circle(screen, RED, (int(x), int(y)), bird_radius)


def draw_pipe(x, height):
    # Top pipe
    pygame.draw.rect(screen, GREEN, pygame.Rect(x, 0, pipe_width, height))
    # Bottom pipe
    bottom_pipe_y = height + pipe_gap
    pygame.draw.rect(screen, GREEN, pygame.Rect(x, bottom_pipe_y, pipe_width, SCREEN_HEIGHT - bottom_pipe_y))


def display_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    screen.blit(surface, rect)


def check_collision(bird_y, pipes):
    # Bird rectangle
    bird_rect = pygame.Rect(bird_x - bird_radius, bird_y - bird_radius, bird_radius * 2, bird_radius * 2)

    if bird_y - bird_radius <= 0 or bird_y + bird_radius >= SCREEN_HEIGHT:
        return True

    for pipe in pipes:
        pipe_x = pipe[0]
        pipe_top_height = pipe[1]

        top_pipe_rect = pygame.Rect(pipe_x, 0, pipe_width, pipe_top_height)
        bottom_pipe_rect = pygame.Rect(pipe_x, pipe_top_height + pipe_gap, pipe_width, SCREEN_HEIGHT - (pipe_top_height + pipe_gap))

        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
            return True

    return False


def main():
    global bird_y, bird_velocity, pipes, score, game_over

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird_velocity = jump_strength
                if event.key == pygame.K_r and game_over:
                    # Reset game
                    bird_y = 300
                    bird_velocity = 0
                    pipes = []
                    score = 0
                    game_over = False

            if event.type == ADD_PIPE and not game_over:
                pipe_height = random.randint(50, SCREEN_HEIGHT - pipe_gap - 50)
                pipes.append([SCREEN_WIDTH, pipe_height])

        if not game_over:
            # Update bird
            bird_velocity += gravity
            bird_y += bird_velocity

            # Move pipes
            for pipe in pipes:
                pipe[0] -= pipe_velocity

            # Remove off-screen pipes
            pipes = [pipe for pipe in pipes if pipe[0] + pipe_width > 0]

            # Check for score update
            for pipe in pipes:
                if pipe[0] + pipe_width < bird_x and not pipe.count('scored'):
                    score += 1
                    pipe.append('scored')  # mark pipe as scored

            # Collision detection
            if check_collision(bird_y, pipes):
                game_over = True

        # Drawing
        screen.fill(SKY_BLUE)

        # Draw pipes
        for pipe in pipes:
            draw_pipe(pipe[0], pipe[1])

        # Draw bird
        draw_bird(bird_x, bird_y)

        # Draw score
        display_text(f"Score: {score}", font, BLACK, SCREEN_WIDTH // 2, 50)

        if game_over:
            display_text("Game Over!", big_font, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            display_text("Press R to Restart", font, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)

        pygame.display.update()


if __name__ == "__main__":
    main()
