# Je vais partir du principe que ceux qui lise ce code ne save rien des modules
# que j'utilise, vue que je suis un chic type je vais mettre les liens versgi
# la documentation que j'utilise (ou au moins un truc en rapport genre stackOverflow)

# ༼ つ ◕_◕ ༽つ


import sys
import os
import Settings
import pygame
from Settings import *
from debug import debug


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


# \\ ============================================================================== //


class Game:
    def __init__(self):

        # Pygame setup :
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('white')
            pygame.display.update()
            self.clock.tick(FPS)


game = Game()
game.run()
