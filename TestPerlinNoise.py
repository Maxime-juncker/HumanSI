from perlin_noise import PerlinNoise
from Utilities import *

noise1 = PerlinNoise(octaves=3)
noise2 = PerlinNoise(octaves=10)

BLUE = (0, 0, 255)
WHITE = (0, 0, 0)

import pygame

# ============ SETUP PYGAME =====================

pygame.init()
display = pygame.display.set_mode((300, 300))
GAME_RUNNING = True
genFinished = False

# Boucle update
while GAME_RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_RUNNING = False
            pygame.quit()
    display.fill(WHITE)

    rect = pygame.Rect(display.get_rect())

    if not genFinished:

        try:
            for x in range(rect.width):
                for y in range(rect.height):
                    noise_val = noise1([x / rect.width, y / rect.height])  # basic noise


                    """
                    Display.set_at = funct de pygame pour poser un pixel sur une surface elle prend
                    2 params:
                        - une position (Vecteur 2d)
                        - une couleur sous le format RGB
                    """
                    display.set_at((rect.left + x, rect.top + y), (
                        Clamp(noise_val * 255, 0, 255), Clamp(noise_val * 255, 0, 255), Clamp(noise_val * 255, 0, 255)))

                    pygame.display.flip()
                    print("Generation : " + str(round(x / rect.width * 100, 1)) + "%")

            debugSuccessMsg("Generation successful \(￣︶￣*\))")
            genFinished = True
        except:
            debugFailMsg("Generation failed |!|")
            genFinished = True


pygame.display.flip()

pygame.quit()
exit()
