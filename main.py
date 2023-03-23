import sys
import pygame

import Game
from Utilities import *
from Game import *

# Boucle update
while game.GAME_RUNNING:

    # Si on ferme la fenetre
    for event in pygame.event.get():
        # l'événement de fermeture de la window
        if event.type == pygame.QUIT:
            game.GAME_RUNNING = False
            pygame.quit()
            debugFailMsg("Exiting...")

        if event.type == pygame.MOUSEBUTTONDOWN:

            '''
            0 - left click
            1 - middle click
            2 - right click
            '''

            mouseButton = pygame.mouse.get_pressed()

            if mouseButton[0]:
                game.SpawnUnitBaseByIndex()
            if mouseButton[2]:
                game.SpawnCivilisation()
        if event.type == pygame.MOUSEWHEEL:

            if 1 < game.cameraGroup.zoomScale + event.y * 0.3 < 3.5:
                game.cameraGroup.zoomScale += round(event.y * 0.3, 2)

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_a:
                if game.spriteIndex + 1 > len(spriteResources) - 1:
                    game.spriteIndex = 0
                else:
                    game.spriteIndex += 1

            elif event.key == pygame.K_e:
                if game.spriteIndex - 1 < 0:
                    game.spriteIndex = len(spriteResources) - 1
                else:
                    game.spriteIndex -= 1

    game.display.fill('#71ddee')

    game.SuperUpdate()
    game.Update()
