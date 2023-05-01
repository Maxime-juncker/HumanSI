from random import *
from Settings import *


def coordRandInList(lenght, width, height):
    # comme parametre on met les coordoner des extremiter de la map et le nombre de coordonnée renvoyer
    listCoord = []
    for i in range(lenght):
        x = randint(0, width + 1)  # met en argument des nombres aléatoires
        y = randint(0, height + 1)
        try:
            listCoord.index((x, y))  # verifie qu'il n'y a pas  2 fois les meme coords
        except:
            listCoord.append((x, y))
    return listCoord

