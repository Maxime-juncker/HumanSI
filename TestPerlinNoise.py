import random

import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import time

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

def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)

# Boucle update
while GAME_RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_RUNNING = False
            pygame.quit()
    display.fill(WHITE)

    rect = pygame.Rect(display.get_rect())


    if not genFinished :
        for x in range(rect.width):
            print("Generation : " + str(round(x / rect.width * 100, 1)) + "%")
            for y in range(rect.height):
                noise_val = noise1([x / rect.width, y / rect.height])  # basic noise

                # on ajoute different type de noise pour ajouter un peu de varieter
                noise_val += 0.5 * noise2([x / rect.width, y / rect.height])
                display.set_at((rect.left + x, rect.top + y), (clamp(noise_val * 255, 0, 255), clamp(noise_val * 255, 0, 255), clamp(noise_val * 255, 0, 255)))

        genFinished = True

    pygame.display.flip()

pygame.quit()
exit()