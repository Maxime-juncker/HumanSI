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

WHITE = (255, 255, 255, 255)
DARKWHITE = (225, 225, 225, 255)
BLUE = (0, 0, 255, 255)
YELLOW = (255, 255, 0, 255)
LIGTHGREEN = (0, 0, 0, 255)
MIDGREEN = (181, 186, 97, 255)
GREEN = (124, 141, 76, 255)
DEEPGREEN = (0, 153, 0, 255)
RED = (255, 0, 0, 255)
GREY = (128, 128, 128, 255)
DARKGREY = (180, 180, 180, 255)
DEFAULTCOLOR = (0, 0, 0, 255)
BLACK = (0, 0, 0, 255)

biomes = {  # dico avec la liste des biomes et leurs characteristiques
    "ocean": (-8 / 9, YELLOW, "ocean"),
    "plage": (-6 / 9, BLUE, "plage"),
    "plaine": (-4 / 9, LIGTHGREEN, "plaine"),
    "forest": (-2 / 9, GREEN, "forest"),
    "midForest": (0, MIDGREEN, "midForest"),  # Si on met se biome le monde devient tres plat
    "deepForest": (2 / 9, DEEPGREEN, "deepForest"),
    "stonyMontagne": (4 / 9, DARKGREY, "stonyMontagne"),
    "montagne": (6 / 9, GREY, "montagne"),
    "hightMontagne": (8 / 9, DARKWHITE, "hightMontagne"),
}


def CheckForBiomeAt(value):
    for biome in biomes:
        if biomes[biome][0] >= value:
            return (biome)


def PlaceBiome(x, y, valuePerlinNoise, Biomeliste):
    for biome in Biomeliste:
        if Biomeliste[biome][0] > 1:
            return debugFailMsg("depassement de la valeur de 1 dans : PlaceBiome")
        elif valuePerlinNoise >= Biomeliste[biome][0] and valuePerlinNoise <= Biomeliste[biome][0] + .25:
            return Biomeliste[CheckForBiomeAt(valuePerlinNoise)][1]


def GenerateWorld(heightMap: Image):
    global biomes
    im = Image.new('RGB', (WIDTH_RESOLUTION, HEIGHT_RESOLUTION))
    width, height = im.size
    colortuples = im.getcolors()
    mycolor1 = min(colortuples)[1]
    mycolor2 = max(colortuples)[1]
    pix = im.load()
    for x in range(0, width):
        for y in range(0, height):
            noiseVal = noise3([x / im.width, y / im.height])  # basic noise
            noiseVal += noise2([x / im.width, y / im.height])
            noiseVal += 0.3  # c'est une valeur arbitraire pour juste qu'il y ai un peu moins d'eau
            noiseVal += Clamp(random.random() * .01, -.5, .5)  # c'est une valeur arbitraire pour un peu de variation

            noiseVal = Clamp(WIDTH_RESOLUTION * noiseVal, 0, WIDTH_RESOLUTION - 1)

            # val = PlaceBiome(x, y, noise_val, biomes)
            val = heightMap.getpixel((noiseVal, 0))
            im.putpixel((x, y), val)
        debugWarningMsg("Generation : " + str(round(x / im.width * 100, 1)) + "%")

    path = "Assets/Graphics/Misc/GeneratedMap/" + "terrain" + str(
        len(LoadSpritesFromFolder("Misc/GeneratedMap"))) + ".png"

    """path ="Assets/Graphics/Misc/GeneratedMap/"+"terrain"+str(len(LoadSpritesFromFolder("Misc/GeneratedMap")))+"("
           + str(WIDTH_RESOLUTION) + "/" + str(HEIGHT_RESOLUTION) + ")" + ".png"""

    terrain = PixelImg(im)
    terrain.save(path)
    debugSuccessMsg("finished !")

    return pyglet.image.load(path)


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
