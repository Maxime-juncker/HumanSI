import sys
import pygame
import Settings
from Settings import *
from debug import debug
from Game import *


class bcolors:  # /!\ les couleurs ne marche que sur sur certains IDE (ex : edupython n'affiche pas les couleurs)
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


game = Game()

# Boucle update
while game.GAME_RUNNING:

    game.display.fill('white')
    game.display.blit(game.test.image, game.test.rect)
    game.display.blit(game.test2.image, game.test2.rect)

    # Update le screen
    pygame.display.flip()

    game.test.MoveTo((500, 0))
    game.test2.MoveTo((0, 500))

    # Si on ferme la fenetre
    for event in pygame.event.get():
        # l'événement de fermeture de la window
        if event.type == pygame.QUIT:
            game.GAME_RUNNING = False
            pygame.quit()
            print(bcolors.FAIL + "Exiting..." + bcolors.ENDC)
