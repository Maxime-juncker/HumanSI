import pygame
import AI
from AI import *
from Utilities import *


spriteResources = {
    "BasicHuman": ("Assets/Pop1c.png","Assets/Pop1c.png"),
    "Rock": ("Assets/caillou1.png","Assets/fer.png", "Assets/or.png"),
    "Tree": ("Assets/Arbre1.png", "Assets/Arbre2.png"),
}


class Game:

    def __init__(self):
        # Creation de la fenetre de l'app

        self.newUnit = None
        self.visibleSprite = {}
        self.spriteIndex = 0

        pygame.init()

        pygame.display.set_caption("HumainSI")
        self.display = pygame.display.set_mode((1000, 1000))

        SetupRichPresence()



        self.GAME_RUNNING = True

    def SpawnUnit(self):
        '''
        on recup les different sprites en fonction de l'index
        et on le passe en parametre au truc que on vas spawn
        '''

        sprites = []
        names = []

        [sprites.extend([v]) for v in spriteResources.values()]
        [names.extend([v]) for v in spriteResources.keys()]

        print(names[self.spriteIndex])
        preset = LoadPreset(Directories.PresetDir + "Presets.csv", names[self.spriteIndex])

        newUnit = Unit(self.display, self.GetRandomSprite(sprites[self.spriteIndex]), preset)
        self.visibleSprite[newUnit.name] = newUnit

    def GetRandomSprite(self, sprites: tuple):
        return sprites[random.randint(0, len(sprites)-1)]

    def Update(self):
        '''
        fonct appeler toutes les frames
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

        l = []
        [l.extend([v]) for v in spriteResources.keys()]

        myfont = pygame.font.SysFont("Arial", 27)

        letter = myfont.render("Spawn : " + str(l[self.spriteIndex]), 0, (0, 0, 0))
        self.display.blit(letter, (50, 50))


game = Game()
