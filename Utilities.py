import random
from pypresence import Presence
import csv


class Directories:
    PresetDir = "Assets/Presets/"


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


def SetupRichPresence():
    rpc = Presence(1087011571005390898)
    rpc.connect()
    rpc.update(details="une super simulation pas du tout inspiré d'un jeu", large_image="maxresdefault")


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

    return randomX, randomY


def LoadPreset(presetPath, name):
    file = open(presetPath, "r")
    content = csv.DictReader(file, delimiter=",")

    result = []
    for ligne in content:
        if ligne["name"] == name:
            return ligne

    # Si on arrive ici ça veut dire que on a pas trouver de result :
    print(bcolors.FAIL + "Preset non trouver, essaye de vertifier l'orthographe" + bcolors.ENDC)
    return presetPath, name
