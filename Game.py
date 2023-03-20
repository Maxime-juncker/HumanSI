import pygame
import AI
from AI import *
from Utilities import *

spriteResources = {
    "BasicHuman": ("Assets/Pop1c.png", "Assets/Pop1c.png"),

    "Chief_Devan": ("Assets/Pop1c.png", "Assets/Pop1c.png"),
    "Chief_Yohann": ("Assets/caillou1.png", "Assets/caillou1.png"),
    "Chief_Alexandre": ("Assets/fer.png", "Assets/fer.png"),
    "Chief_Nathan": ("Assets/or.png", "Assets/or.png"),
    "Chief_Maxime": ("Assets/Arbre1.png", "Assets/Arbre1.png"),

    "Chief_Romain": ("Assets/Arbre1.png", "Assets/Arbre1.png"),
    "Chief_Antonin": ("Assets/Arbre1.png", "Assets/Arbre1.png"),

    "Rock": ("Assets/caillou1.png", "Assets/fer.png", "Assets/or.png"),
    "Tree": ("Assets/Arbre1.png", "Assets/Arbre2.png"),
    "YellowCityHall": ("Assets/download.jpg", "Assets/download.jpg"),

}


class Game:

    def __init__(self):
        # Creation de la fenetre de l'app

        self.newUnit = None
        self.visibleSprite = {}
        self.civilisationSpawned = {}
        self.spriteIndex = 0

        pygame.init()

        pygame.display.set_caption("HumainSI")
        self.display = pygame.display.set_mode((1000, 1000))

        SetupRichPresence()

        self.GAME_RUNNING = True

    def SpawnUnitBaseByIndex(self):
        '''
        on recup les different sprites en fonction de l'index
        et on le passe en parametre au truc que on vas spawn
        '''

        sprites = []
        names = []

        [sprites.extend([v]) for v in spriteResources.values()]
        [names.extend([v]) for v in spriteResources.keys()]

        preset = LoadPreset(Directories.PresetDir + "Presets.csv", names[self.spriteIndex])

        pos = pygame.mouse.get_pos()
        newUnit = Unit(self.display, self.GetRandomSprite(sprites[self.spriteIndex]), preset,pos)
        self.visibleSprite[newUnit.name] = newUnit

    def SpawnUnit(self, popPreset):
        pos = pygame.mouse.get_pos()

        newUnit = Unit(self.display, self.GetRandomSprite(spriteResources[popPreset["name"]]), popPreset,pos)
        self.visibleSprite[newUnit.name] = newUnit

    def SpawnCivilisation(self):
        popPreset = LoadPreset(Directories.PresetDir + "Presets.csv", "Chief_Devan")
        preset = LoadPreset(Directories.PresetDir + "Civilisation.csv", popPreset["civilisation"])
        newCivilisation = Civilisation(preset, popPreset)

        self.civilisationSpawned[newCivilisation.name] = newCivilisation

    def GetRandomSprite(self, sprites: tuple):
        return sprites[random.randint(0, len(sprites) - 1)]

    def Update(self):
        '''
        fonct appeler toutes les frames

        PS : on fait une copie de la liste que on vas update
             sinon si on spawn un truc et que la longueur de la
             liste change ça nique tout :D

        '''

        sprites = self.visibleSprite
        for sprite in sprites:
            sprites[sprite].Update()


    def SuperUpdate(self):
        '''
        fonct appeler toutes les frames
        Est appeler AVANT Update, ça peut permetre
        de prioriser certaine update
        '''

        civilisations = self.civilisationSpawned
        for civilisation in civilisations:
            civilisations[civilisation].Update()


        l = []
        [l.extend([v]) for v in spriteResources.keys()]

        # on met aussi un petit text (debug)
        font = pygame.font.SysFont("Arial", 27)
        letter = font.render("Spawn : " + str(l[self.spriteIndex]), 0, (0, 0, 0))
        self.display.blit(letter, (50, 50))


game = Game()
