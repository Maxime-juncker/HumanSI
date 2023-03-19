import sys
import pygame
from Utilities import *
from Game import *




# Boucle update
while game.GAME_RUNNING:

    game.display.fill('white')

    game.SuperUpdate()
    game.Update()

    # Update le screen
    pygame.display.flip()

    # Si on ferme la fenetre
    for event in pygame.event.get():
        # l'événement de fermeture de la window
        if event.type == pygame.QUIT:
            game.GAME_RUNNING = False
            pygame.quit()
            print(bcolors.FAIL + "Exiting..." + bcolors.ENDC)

        # on ecoute les input du clavier
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseButton = pygame.mouse.get_pressed()

            if mouseButton[0]:  # mouseButton[0] = souris gauche
                game.SpawnUnit()
        if event.type == pygame.MOUSEWHEEL:

            if game.spriteIndex == len(spriteResources)-1:
                game.spriteIndex = 0
            else:
                game.spriteIndex += 1



