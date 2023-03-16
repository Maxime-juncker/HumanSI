import pygame
import AI
from AI import *

spriteResources = {
    "basicHuman": "Assets/Pop1c.png",
    "Stone": "Asset/caillou1.png",
}


class Game:
    visibleSprite = {}

    def __init__(self):
        # Creation de la fenetre de l'app

        self.newUnit = None
        pygame.init()

        pygame.display.set_caption("HumainSI")
        self.display = pygame.display.set_mode((1920, 1080))

        self.background = pygame.image.load("Assets/download.jpg")

        self.GAME_RUNNING = True

    def SpawnUnit(self):
        newUnit = Test(self.display)


game = Game()
