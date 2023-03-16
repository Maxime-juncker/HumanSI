import random

import pygame
import Game

pygame.init()
font = pygame.font.Font(None, 30)


def debug(info, y=10, x=10):

    """
    fonction pour print une info sur l'ecran (c'est quand même plus pratique qui print .__.)
    info : n'importe quoi
    x / y = les postion a partir du coin haut gauche ou le msg vas pop
            (perso je trouve que 10 et 10 c'est pas mal)
    """

def SeekNewPos(currentPos, distance):
    randomX = random.randint(currentPos[0] - distance, currentPos[0] + distance)
    randomY = random.randint(currentPos[1] - distance, currentPos[1] + distance)

    return (randomX, randomY)

