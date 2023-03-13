# Je vais partir du principe que ceux qui lise ce code ne save rien des modules 
# que j'utilise, vue que je suis un chic type je vais mettre les liens vers 
# la documentation que j'utilise (ou au moins un truc en rapport genre stackOverflow)

# ༼ つ ◕_◕ ༽つ


import random
import math
import Settings
import World
import threading
import pygame
from pygame import *
from debug import debug
import os

CURR_DIR = os.path.dirname(os.path.realpath(__file__))


class Object(pygame.sprite.Sprite):  # Toutes les classes doivent dériver de celle ci (ça permet de tout centraliser)

    def __init__(self):
        super().__init__()


# region Les Actors

class AActor(Object):
    actorName: str

    actorComponents = {}

    def DoesComponentExist(self, componentName: str):
        return componentName in self.actorComponents

    def __init__(self, pos, group):
        super().__init__()
        print("s")
        self.image = pygame.image.load("Pop1c.png")
        self.rect = self.image.get_rect(topleft=pos)
        pygame.sprite.Sprite.__init__(group)




class AEntity(AActor):
    # NE MARCHE PLUS ATTENDER QUE JE LA REFACE

    Entityname = ""

    def update(self):
        for i in self.actorComponents:
            self.actorComponents[i].Update()

    def __init__(self, pos, groups):
        super().__init__(pos, groups)

    def MoveTo(self, newPosition: tuple):
        # A REFAIRE
        pass

    def FindRandomPointAtDistance(self, distance: float):
        pos = self.actorTurtle.pos()
        randomX = random.randint(pos[0] - distance, pos[0] + distance)
        randomY = random.randint(pos[1] - distance, pos[1] + distance)

        return (randomX, randomY)


class AResourceNode(AActor):
    def __init__(self):
        super().__init__()

    def Setup(self):
        # A REFAIRE
        pass


# endregion
# region Les Component


class CComponent(Object):
    def __init__(self):
        super().__init__()

    def Update(self):  # doit etre implementer dans tous les class enfants
        pass

    def Setup(self):
        pass


class CHumainRace(CComponent):
    InteractionType = {
        1: "Talk"
    }

    def Update(self):
        pass

    def __init__(self):
        super().__init__()

    def Setup(self):
        pass


class CAnimator(CComponent):
    def Setup(self):
        super().Setup()
        pass

    def Update(self):
        pass


class CRessource(CComponent):

    def __init__(self):
        super().__init__()

# endregion
