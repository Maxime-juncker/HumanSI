import random
from pypresence import Presence
import csv
import os

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


def SetupRichPresence():
    rpc = Presence(1087011571005390898)
    rpc.connect()
    rpc.update(details="une super simulation pas du tout inspiré d'un jeu", large_image="maxresdefault")


def debugSuccessMsg(info):
    print(bcolors.OKGREEN + "Success : " + bcolors.OKCYAN + str(info) + bcolors.ENDC)


def debugFailMsg(info):
    print(bcolors.FAIL + str(info) + bcolors.ENDC)


def debugWarningMsg(info):
    print(bcolors.WARNING + "Warning : " + bcolors.BOLD + str(info) + bcolors.ENDC)


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


def LoadSpritesFromFolder(folderPath):
    return os.listdir(Directories.SpritesDir + folderPath)

