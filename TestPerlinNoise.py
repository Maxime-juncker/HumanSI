from perlin_noise import PerlinNoise
from Utilities import *
from pygame.locals import *

noise1 = PerlinNoise(octaves=3)
noise2 = PerlinNoise(octaves=10)
noise3 = PerlinNoise(octaves=3)
noise4 = PerlinNoise(octaves=5)

WHITE = (255, 255, 255)
DARKWHITE = (225,225,225)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGTHGREEN = (102, 255, 102)
MIDGREEN = (60, 255, 60)
GREEN = (0,255,0)
DEEPGREEN = (0, 153, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)
DARKGREY = (180, 180, 180)
DEFAULTCOLOR = (0, 0, 0)
BLACK = (0, 0, 0)


biomes = {      #dico avec la liste des biomes et leurs characteristiques
    "ocean" : (-8/9, YELLOW, "ocean"),
    "plage" : (-6/9, BLUE, "plage"),
    "plaine" : (-4/9, LIGTHGREEN, "plaine"),
    "forest" : (-2/9, GREEN,"forest"),
    #"midForest" : (0, MIDGREEN, "midForest"),      #Si on met se biome le monde devient tres plat
    "deepForest" : (2/9, DEEPGREEN, "deepForest"),
    "stonyMontagne" :  (4/9, DARKGREY, "stonyMontagne"),
    "montagne" : (6/9, GREY, "montagne"),
    "hightMontagne" : (8/9, DARKWHITE, "hightMontagne"),
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
            print(biomes[biome][2])
            return(biome)
        
    debugFailMsg("failed to find a biome !")

print(CheckForBiomeAt(.3))
    

def PlaceBiome(x, y, valuePerlinNoise, Biomeliste, ) :
    
    for biome in Biomeliste :
        if Biomeliste[biome][0]>1 :
            return debugFailMsg("depassement de la valeur de 1 dans : PlaceBiome")
        elif valuePerlinNoise>=Biomeliste[biome][0] and valuePerlinNoise<=Biomeliste[biome][0]+.25 :
            return Biomeliste[CheckForBiomeAt(valuePerlinNoise)][1]


displaySurface = pygame.display.get_surface()
half_w = displaySurface.get_size()[0] // 2
half_h = displaySurface.get_size()[1] // 2
internalSurfaceSize = (displaySurface.get_size()[0], displaySurface.get_size()[1])
internalSurface = pygame.Surface(internalSurfaceSize, pygame.SRCALPHA)
internalRect = internalSurface.get_rect(center=(half_w, half_h))


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
                        print("ejfe")

                        noise_val = noise3([x / rect.width, y / rect.height])  # basic noise
                        noise_val += noise4([x / rect.width, y / rect.height])  # basic noise
                        Buffer = -.25 #Un buffer pour varier les valeur de perlin noise
                        """if noise_val + Buffer>=-1 and noise_val + Buffer<=1 :
                            noise_val += Buffer"""
                            
                        """pygame.event.wait()
                        for event in pygame.event.get():
                            if event.type == MOUSEBUTTONUP:
                                None
                        
                        Display.set_at = funct de pygame pour poser un pixel sur une surface elle prend
                        2 params:
                            - une position (Vecteur 2d)
                            - une couleur sous le format RGB

                        """
                        print(noise_val)
                        try :
                            internalSurface.set_at((rect.left + x, rect.top + y), (PlaceBiome(rect.left + x, rect.top + y, noise_val, biomes)))
                            displaySurface.blit(internalSurface, internalRect)
                            pygame.display.update()

                            #Clamp(noise_val * 255, 0, 255), Clamp(noise_val * 204, 0, 0), Clamp(noise_val * 255, 0, 255)))
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

    displaySurface.blit(internalSurface, internalRect)
    pygame.display.update()



