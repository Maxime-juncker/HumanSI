from perlin_noise import PerlinNoise
from Utilities import *
from pygame.locals import *

noise1 = PerlinNoise(octaves=3)
noise2 = PerlinNoise(octaves=10)
noise3 = PerlinNoise(octaves=3)
noise4 = PerlinNoise(octaves=5)

BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGTHGREEN = (102, 255, 102)
GREEN = (0,255,0)
DEEPGREEN = (0, 153, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
DARKGREY = (180, 180, 180)
DEFAULTCOLOR = (0, 0, 0)


biomes = {
    "ocean" : (-.75, BLUE),
    "plage" : (-.50, YELLOW),
    "plaine" : (-.25, LIGTHGREEN),
    "forest" : (0, GREEN),
    "deepForest" : (.25, DEEPGREEN),
    "stonyMontagne" :  (.50, DARKGREY),
    "montagne" : (.75,GREY ),
    "hightMontagne" : (1, WHITE),
}

import pygame

# ============ SETUP PYGAME =====================

pygame.init() #Important pour pygame
display = pygame.display.set_mode((200, 200)) #taille de la fenetre pygame
GAME_RUNNING = True
genFinished = False

def CheckForBiomeAt(value):

    for biome in biomes:
        if biomes[biome][0] >= value:
            return(biome)
        
    debugFailMsg("failed to find a biome !")

print(CheckForBiomeAt(.3))
    

def PlaceBiome(x, y, valuePerlinNoise, Biomeliste, ) :
    ScanVal = -1
    for biome in Biomeliste :
        if Biomeliste[biome][0]>1 :
            return debugFailMsg("depassement de la valeur de 1 dans : PlaceBiome")
        elif valuePerlinNoise>=Biomeliste[biome][0] and valuePerlinNoise<=Biomeliste[biome][0]+.25 :
            return Biomeliste[CheckForBiomeAt(valuePerlinNoise)][1]
            

# Boucle update
while GAME_RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_RUNNING = False
            pygame.quit()
    display.fill(WHITE)

    rect = pygame.Rect(display.get_rect())

    try:

        if not genFinished:

            try:
                for x in range(rect.width):
                    for y in range(rect.height):
                        noise_val = noise3([x / rect.width, y / rect.height])  # basic noise
                        noise_val += noise4([x / rect.width, y / rect.height])  # basic noise
                        pygame.event.wait()
                        for event in pygame.event.get():
                            if event.type == MOUSEBUTTONUP:
                                None
                        """
                        Display.set_at = funct de pygame pour poser un pixel sur une surface elle prend
                        2 params:
                            - une position (Vecteur 2d)
                            - une couleur sous le format RGB

                        """
                        print(noise_val)
                        try :
                            display.set_at((rect.left + x, rect.top + y), (PlaceBiome(rect.left + x, rect.top + y, noise_val, biomes)))
                            #Clamp(noise_val * 255, 0, 255), Clamp(noise_val * 204, 0, 0), Clamp(noise_val * 255, 0, 255)))
                            pygame.display.flip()
                        except :
                            pass
                        print("Generation : " + str(round(x / rect.width * 100, 1)) + "%")
                        
                debugSuccessMsg("Generation successful \(￣︶￣*\))")
                genFinished = True
            except:
                debugFailMsg("Generation failed |!|")
                genFinished = True
    except:
        print("probleme")

pygame.display.flip()

pygame.quit()
exit()


