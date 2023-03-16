import sys
import pygame
import Settings
from Settings import *
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


def Update():
    sprites = game.visibleSprite
    for sprite in sprites:
        sprites[sprite].Update()


# Boucle update
while game.GAME_RUNNING:

    game.display.fill('white')
    Update()

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
        if mouseButton[0]: # mouseButton[0] = souris gauche
            game.SpawnUnit()

