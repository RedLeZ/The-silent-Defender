import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 400, 150
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sound Control")

# Colors
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load sound
pygame.mixer.music.load("GameFiles/assets/sounds/MenuMusic.mp3")

# Get sound volume range
MAX_VOLUME = pygame.mixer.music.get_volume()

# Set initial volume
current_volume = MAX_VOLUME / 2
pygame.mixer.music.set_volume(current_volume)

# Bar dimensions
BAR_WIDTH = 300
BAR_HEIGHT = 20
BAR_MARGIN = 20

# Button circle radius
BUTTON_RADIUS = 10

# Button circle position
button_x = BAR_MARGIN + current_volume * BAR_WIDTH
button_y = HEIGHT // 2

# Font
font = pygame.font.Font(None, 36)


# Function to draw the sound bar
def draw_sound_bar():
    pygame.draw.rect(
        screen, GRAY, (BAR_MARGIN, HEIGHT // 2 - BAR_HEIGHT // 2, BAR_WIDTH, BAR_HEIGHT)
    )
    fill_width = int(current_volume * BAR_WIDTH)
    pygame.draw.rect(
        screen,
        BLACK,
        (BAR_MARGIN, HEIGHT // 2 - BAR_HEIGHT // 2, fill_width, BAR_HEIGHT),
    )


# Function to draw the button circle
def draw_button_circle():
    pygame.draw.circle(screen, RED, (int(button_x), int(button_y)), BUTTON_RADIUS)


# Function to draw the volume percentage text
def draw_volume_text():
    volume_percentage = int(current_volume * 100)
    text_surface = font.render(f"Volume: {volume_percentage}%", True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT - 30)
    screen.blit(text_surface, text_rect)


# Main loop
running = True
dragging = False
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (
                BAR_MARGIN <= mouse_x <= BAR_MARGIN + BAR_WIDTH
                and abs(mouse_y - button_y) < BUTTON_RADIUS
            ):
                dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                button_x = max(BAR_MARGIN, min(BAR_MARGIN + BAR_WIDTH, mouse_x))
                current_volume = (button_x - BAR_MARGIN) / BAR_WIDTH
                pygame.mixer.music.set_volume(current_volume)

    # Fill the background
    screen.fill(WHITE)

    # Draw sound bar, button circle, and volume text
    draw_sound_bar()
    draw_button_circle()
    draw_volume_text()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
