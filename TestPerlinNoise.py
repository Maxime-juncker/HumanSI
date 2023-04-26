import random

import pyglet.sprite
from PIL import Image
from perlin_noise import PerlinNoise
from Utilities import *
from Settings import *
from pygame.locals import *

noise1 = PerlinNoise(octaves=3)
noise2 = PerlinNoise(octaves=6)
noise3 = PerlinNoise(octaves=3)
noise4 = PerlinNoise(octaves=5)


biomes = {}

def AddBiomeToDict(value, coord):
    for i in range(5):

        biomes[(coord[0]*6-i, coord[1]*6+i)] = round(value,1)  # Up left
        biomes[(coord[0]*6-i, coord[1]*6)] = round(value,1)  # Middle left
        biomes[(coord[0]*6-i, coord[1]*6-i)] = round(value,1)  # Down left

        biomes[(coord[0]*6, coord[1]*6+i)] = round(value,1)  # Up
        biomes[(coord[0]*6, coord[1]*6)] = round(value,1)  # Middle
        biomes[(coord[0]*6, coord[1]*6-i)] = round(value,1)  # Down

        biomes[(coord[0]*6+i, coord[1]*6+i)] = round(value,1)  # Up right
        biomes[(coord[0]*6+i, coord[1]*6)] = round(value,1)  # Middle right
        biomes[(coord[0]*6+i, coord[1]*6-i)] = round(value,1)  # Down right


def SaveBiomeToCSV(name):
    with open("Assets/Presets/MapBiomes/" + name + ".csv", 'w') as csvfile:
        w = csv.DictWriter(csvfile, biomes.keys())
        w.writeheader()
        w.writerow(biomes)


def GenerateWorld(heightMap: Image):
    """
    fonct pour générer un terrain en utilisant la librairy perlin_noise (pip install perlin_noise) et genere
    un terrain en fonction de la resolution et du taux de chaos (dans Setting.py). On ajoute aussi chaque coord
    dans un dict de biome pour le retrouver plus tard (y'a une autre technique plus facile mais elle est pas
    opti et on vas checker assez souvent le biome donc bon...)
    Args:
        heightMap (Image): image contenant la couleur d'un pixel en fonction de ça hauteur (noiseVal=
    Returns:
        Image pyglet: l'image du terrain pixelisé'
    """
    global biomes
    im = Image.new('RGB', (WIDTH_RESOLUTION, HEIGHT_RESOLUTION))
    width, height = im.size
    pix = im.load()
    for x in range(0, width):
        for y in range(0, height):
            noiseVal = noise3([x / im.width, y / im.height])  # basic noise
            noiseVal += noise2([x / im.width, y / im.height])
            noiseVal += 0.3  # c'est une valeur arbitraire pour juste qu'il y ai un peu moins d'eau
            noiseVal += Clamp(random.random() * CHAOS_FORCE, -.5, .5)

            AddBiomeToDict(noiseVal, (x,y))  # avant de continuer on ajoute le pixel a la liste de biome

            noiseVal = Clamp(WIDTH_RESOLUTION * noiseVal, 0, WIDTH_RESOLUTION - 1)

            # val = PlaceBiome(x, y, noise_val, biomes)
            val = heightMap.getpixel((noiseVal, 0))
            im.putpixel((x, y), val)
        debugWarningMsg("Generation : " + str(round(x / im.width * 100, 1)) + "%")

    name = "terrain" + str(len(LoadSpritesFromFolder("Misc/GeneratedMap")))
    path = "Assets/Graphics/Misc/GeneratedMap/" + name + ".png"



    """path ="Assets/Graphics/Misc/GeneratedMap/"+"terrain"+str(len(LoadSpritesFromFolder("Misc/GeneratedMap")))+"("
           + str(WIDTH_RESOLUTION) + "/" + str(HEIGHT_RESOLUTION) + ")" + ".png"""

    terrain = PixelImg(im)
    size = terrain.size
    terrain = terrain.resize(size=(size[0] * 5, size[1] * 5))
    terrain.save(path)

    debugWarningMsg("Enregistrement des biomes en csv (cette étape peut prendre plusieurs secondes)")
    SaveBiomeToCSV(name)
    debugSuccessMsg("La génération de la carte [" + name + "] c'est bien dérouler !")

    return pyglet.image.load(path), "Assets/Presets/MapBiomes/" + name + ".csv"


def PixelImg(im):
    orgSize = im.size
    pixelateLevel = 2  # plus c'est petit plus la pixelisation sera minime

    # scale it down
    im = im.resize(
        size=(orgSize[0] // pixelateLevel, orgSize[1] // pixelateLevel),
        resample=0)
    # and scale it up to get pixelate effect
    im = im.resize(orgSize, resample=0)
    return im
