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
            game.KillAllActors()
            game.slowUpdateTimer.cancel()

        if event.type == pygame.MOUSEBUTTONDOWN:

            '''
            0 - left click
            1 - middle click
            2 - right click
            '''

            mouseButton = pygame.mouse.get_pressed()

            if mouseButton[0]:
                game.SpawnUnitBaseByIndex()
            if mouseButton[1]:
                game.KillAllActors()

            if mouseButton[2]:
                # get a list of all sprites that are under the mouse cursor
                offsetPos = game.cameraGroup.offset - game.cameraGroup.internalOffset + pygame.mouse.get_pos()
                clicked_sprites = [s for s in game.cameraGroup if s.rect.collidepoint(offsetPos)]

                game.CreateDescPanel()
                if len(clicked_sprites) > 0:
                    game.selectedTarget = clicked_sprites[0]

        """if event.type == pygame.MOUSEWHEEL:

            if 1 < game.cameraGroup.zoomScale + event.y * 0.3 < 3.5:
                game.cameraGroup.zoomScale += event.y * 0.3"""

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_a:
                if game.spriteIndex + 1 > len(game.spawnAbleUnit) - 1:
                    game.spriteIndex = 0
                else:
                    game.spriteIndex += 1

            elif event.key == pygame.K_e:
                if game.spriteIndex - 1 < 0:
                    game.spriteIndex = len(game.spawnAbleUnit) - 1
                else:
                    game.spriteIndex -= 1

    game.SuperUpdate()
    game.Tick()
