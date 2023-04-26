from random import *
from Settings import *


def coordRandInList():
    # comme parametre on met les coordoner des extremiter de la map et le nombre de coordonnée renvoyer
    listCoord = []
    for i in range(MAX_RESSOURCES_SPAWN_ON_START):
        x = randint(0, WIDTH_RESOLUTION + 1)  # met en argument des nombres aléatoires
        y = randint(0, HEIGHT_RESOLUTION + 1)
        try:
            listCoord.index((x, y))  # verifie qu'il n'y a pas  2 fois les meme coords
            pass
        except:
            listCoord.append((x, y))
    return listCoord


print(coordRandInList())
