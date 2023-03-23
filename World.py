import pygame
import random

# --- constants --- (UPPER_CASE_NAMES)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FPS = 25

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# --- main ---

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()

surface = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

# --- objects ---

bg_image = pygame.image.load('Assets/download.jpg').convert()
bg_rect = bg_image.get_rect(center=screen_rect.center)

player_image = pygame.image.load("Assets/Props/fer.png").convert()
player_rect = player_image.get_rect(center=screen_rect.center)

# --- mainloop ---

clock = pygame.time.Clock()

follow_player = False
zoom = False

# number = 0  # to generate images for animated `gif`
# `ffmpeg -i image-%03d.jpg -vf scale=250:200 video.gif`

running = True
while running:

    # --- events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_SPACE:
                follow_player = not follow_player

            elif event.key == pygame.K_RETURN:
                zoom = not zoom

    # --- changes/moves/updates ---

    move_x = random.randint(-5, 5)
    move_y = random.randint(-5, 5)
    player_rect.move_ip(move_x, move_y)

    # --- draw on surface ---

    surface.fill(BLACK)
    surface.blit(bg_image, bg_rect)
    surface.blit(player_image, player_rect)

    # --- modify surface ---

    surface_mod = surface.copy()
    surface_mod_rect = surface_mod.get_rect()

    if zoom:
        scale = 2
        surface_mod = pygame.transform.rotozoom(surface_mod, 0, scale)
        surface_mod_rect = surface_mod.get_rect()
    else:
        scale = 1

    if follow_player:
        surface_mod_rect.x = (screen_rect.centerx - player_rect.centerx * scale)
        surface_mod_rect.y = (screen_rect.centery - player_rect.centery * scale)
    else:
        surface_mod_rect.center = screen_rect.center