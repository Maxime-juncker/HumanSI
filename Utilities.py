import math
import random
import csv
import os

import Game
from Settings import UTILITIES_DEBUG


class Directories:
    PresetDir = "Assets/Presets/"
    SpritesDir = "Assets/Graphics/"


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


def debugSuccessMsg(info):
    print(bcolors.OKCYAN + "Success : " + bcolors.OKGREEN + str(info) + bcolors.ENDC)


def debugFailMsg(info):
    print(bcolors.FAIL + str(info) + bcolors.ENDC)


def debugWarningMsg(info):
    print(bcolors.WARNING + "Warning : " + bcolors.BOLD + str(info) + bcolors.ENDC)


def SeekNewPos(currentPos, distance):
    randomX = random.randint(currentPos[0] - distance, currentPos[0] + distance)
    randomY = random.randint(currentPos[1] - distance, currentPos[1] + distance)

    if CheckCoordInBiome((randomX, randomY)) < .1:
        return currentPos

    """while CheckPosition(randomX, randomY)[2] > 100: # prb de perf donc désactivé
        return currentPos[0], currentPos[1]"""

    return randomX, randomY


def CheckCoordInBiome(coord):
    try:
        return float(Game.game.biomes[str(coord)])
    except:  # y'a moyen que y'a probleme si jamais on click en dehors de l'ecran
        return -9999

def LoadPreset(presetPath, name=""):
    file = open(presetPath, "r")
    content = csv.DictReader(file, delimiter=",")

    result = {}
    if name == "":
        for ligne in content:
            result[ligne["name"]] = ligne
        return result

    else:
        for ligne in content:
            if ligne["name"] == name:
                return ligne

    # Si on arrive ici ça veut dire que on a pas trouver de result :
    print(bcolors.FAIL + "Preset non trouver, essaye de vertifier l'orthographe" + bcolors.ENDC)
    return presetPath, name


def LoadSpritesFromFolder(folderPath):
    return os.listdir(Directories.SpritesDir + folderPath)


def Clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)


def LoadSpriteFromSpriteSheet(sheet="spriteSheet/PopSpriteSheet.png", x=0, y=0):
    pass

    """
    De base j'ai essayer de faire une sprite sheet pour les perf mais j'ai pas l'impression que ça ai changé grand chose...
    en plus on utilise plus pygame donc bon...
    par contre l'idée de faire une sprite sheet est a garder on utilisera ça plus tard a la place.
    ça sera plus sexy que 10 000 png.
    """
    """x_coord = 12 * x  # This would be the third column.
    y_coord = 16 * y
    width = 12
    height = 16

    sheet = pygame.image.load(Directories.SpritesDir + sheet).convert_alpha()
    return sheet.subsurface((x_coord, y_coord, width, height))"""


def GetDistanceFromVector(vect1: tuple = (0, 0), vect2: tuple = (0, 0)):
    return math.sqrt((vect1[0] - vect2[0]) ** 2 + (vect1[1] - vect2[1]) ** 2)
