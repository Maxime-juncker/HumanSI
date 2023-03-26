import pygame
import AI
from AI import *
from Utilities import *

'''
TRUC IMPORTANT. 
pygame fonctionne en dessinant les truc qui sont contenu dans une liste 
(ici CameraGroup) sauf que la liste est h24 en bordel du coup j'override 
la class de pygame pour ajouter des fonctionalité c'est CameraGroup qui vas donc
etre la liste des sprites a l'ecran 
SI VOUS AJOUTEZ DES SPRITE AJOUTER LES A CAMERAGROUP
'''


class CameraGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()

        self.offset = pygame.math.Vector2(0, 0)
        self.half_w = self.displaySurface.get_size()[0] // 2
        self.half_h = self.displaySurface.get_size()[1] // 2

        self.groundSurface = pygame.image.load("Assets/Graphics/ground.png").convert_alpha()
        self.groundRect = self.groundSurface.get_rect(topleft=(0, 0))

        # Box setup
        self.cameraBorder = {"left": 200, "right": 200, "top": 100, "bottom": 100}
        l = self.cameraBorder["left"]
        t = self.cameraBorder["top"]
        w = self.displaySurface.get_size()[0] - (self.cameraBorder["left"] + self.cameraBorder["right"])
        h = self.displaySurface.get_size()[1] - (self.cameraBorder["top"] + self.cameraBorder["bottom"])
        self.cameraRect = pygame.Rect(l, t, w, h)

        # Camera Speed
        self.keyboardSpeed = 20

        # zoom (honetement j'ai aucune idée de pk ça marche mais tkt...)
        self.zoomScale = 1
        self.internalSurfaceSize = (self.displaySurface.get_size()[0], self.displaySurface.get_size()[1])
        self.internalSurface = pygame.Surface(self.internalSurfaceSize, pygame.SRCALPHA)
        self.internalRect = self.internalSurface.get_rect(center=(self.half_w, self.half_h))
        self.internalSurfaceSizeVector = pygame.math.Vector2(self.internalSurfaceSize)
        self.internalOffset = pygame.math.Vector2()
        self.internalOffset_x = self.internalSurfaceSize[0] // 2 - self.half_w
        self.internalOffset_y = self.internalSurfaceSize[1] // 2 - self.half_h

    def CustomDraw(self):
        if not game.GAME_RUNNING:
            return
        # self.centerCameraOnTarget()
        # self.boxTargetCamera()

        if game.selectedTarget is not None:
            self.centerCameraOnTarget(game.selectedTarget)
        self.keyboardControl()

        self.internalSurface.fill('#71ddee')

        # Terrain
        groundOffset = self.groundRect.topleft - self.offset + self.internalOffset
        self.internalSurface.blit(self.groundSurface, groundOffset)

        # Elements actifs
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offestPos = sprite.rect.center - self.offset + self.internalOffset
            self.internalSurface.blit(sprite.image, offestPos)

        scaledSurf = pygame.transform.scale(self.internalSurface, self.internalSurfaceSizeVector * self.zoomScale)
        scaledRect = scaledSurf.get_rect(center=(self.half_w, self.half_h))
        self.displaySurface.blit(scaledSurf, scaledRect)

    def keyboardControl(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.cameraRect.x -= self.keyboardSpeed
            game.selectedTarget = None
        if keys[pygame.K_d]:
            self.cameraRect.x += self.keyboardSpeed
            game.selectedTarget = None

        if keys[pygame.K_z]:
            self.cameraRect.y -= self.keyboardSpeed
            game.selectedTarget = None

        if keys[pygame.K_s]:
            self.cameraRect.y += self.keyboardSpeed
            game.selectedTarget = None

        self.offset.x = self.cameraRect.left - self.cameraBorder['left']
        self.offset.y = self.cameraRect.top - self.cameraBorder['top']

    def centerCameraOnTarget(self, target):
        self.offset.x = game.newUnit.rect.centerx - self.half_w
        self.offset.y = game.newUnit.rect.centery - self.half_h


class Game:

    def __init__(self):
        # Creation de la fenetre de l'app

        self.newUnit = None
        self.selectedTarget = None
        self.visibleSprite = {}
        self.civilisationSpawned = {}
        self.spriteIndex = 0
        self.spawnAbleUnit = LoadPreset(Directories.PresetDir + "Presets.csv")

        # ============ SETUP PYGAME =====================

        pygame.init()
        pygame.display.set_caption("Chargement...")

        self.display = pygame.display.set_mode((1920, 1080))
        self.cameraGroup = CameraGroup()

        self.clock = pygame.time.Clock()

        # =================================================
        # C'est bon on a fini le setup la game loop peut commencer :D
        pygame.display.set_caption("HumainSI")

        self.GAME_RUNNING = True

    def SpawnUnitBaseByIndex(self):
        '''
        on recup les different sprites en fonction de l'index
        et on le passe en parametre au truc que on vas spawn
        '''

        names = []
        [names.extend([v]) for v in self.spawnAbleUnit.keys()]

        preset = LoadPreset(Directories.PresetDir + "Presets.csv", names[self.spriteIndex])
        sprites = LoadSpritesFromFolder(preset["spritesPath"])

        offsetPos = self.cameraGroup.offset - self.cameraGroup.internalOffset + pygame.mouse.get_pos()
        print(offsetPos)

        pixelColor = pygame.Surface.get_at(self.display,(0,0))
        if pixelColor[0] == 113 and pixelColor[1] == 221 and pixelColor[2] == 238:
            print("HEYAAA")



        self.newUnit = Unit(self.display, self.GetRandomSprite(sprites), preset, offsetPos,
                            self.cameraGroup)
        self.visibleSprite[self.newUnit.name] = self.newUnit

    def SpawnUnit(self, popPreset, pos):
        print(pos)

        pixelColor = self.cameraGroup.internalSurface.get_at((round(pos[0], round(pos[1]))))
        if pixelColor[0] == 113 and pixelColor[1] == 221 and pixelColor[2] == 238:
            debugFailMsg("unable to spanw on water !")
            return


        sprites = LoadSpritesFromFolder(popPreset["spritesPath"])

        self.newUnit = Unit(self.display, self.GetRandomSprite(sprites), popPreset, pos,
                            self.cameraGroup)
        self.visibleSprite[self.newUnit.name] = self.newUnit

    def SpawnCivilisation(self):
        popPreset = LoadPreset(Directories.PresetDir + "Presets.csv", "Chief_Yohann")
        preset = LoadPreset(Directories.PresetDir + "Civilisation.csv", popPreset["civilisation"])
        newCivilisation = Civilisation(preset, popPreset)

        self.civilisationSpawned[newCivilisation.name] = newCivilisation

    def GetRandomSprite(self, sprites):
        print(sprites)
        return sprites[random.randint(0, len(sprites) - 1)]

    def Update(self):
        '''
        fonct appeler toutes les frames

        PS : on fait une copie de la liste que on vas update
             sinon si on spawn un truc et que la longueur de la
             liste change ça nique tout :D

        '''

        civilisations = self.civilisationSpawned
        for civilisation in civilisations:
            civilisations[civilisation].Update()

        sprites = self.visibleSprite
        for sprite in sprites:
            sprites[sprite].Update()

    def SuperUpdate(self):
        '''
        fonct appeler toutes les frames
        Est appeler AVANT Update, ça peut permetre
        de prioriser certaine update

        du coup pour l'instant c'est surtout les update de pygame
        que je met là vue que ça a l'air plutot important :D
        '''

        self.cameraGroup.update()
        self.cameraGroup.CustomDraw()

        # on met aussi un petit text (debug)
        l = []
        [l.extend([v]) for v in game.spawnAbleUnit.keys()]
        font = pygame.font.SysFont("Arial", 27)
        letter = font.render("Spawn : " + str(l[self.spriteIndex]), 0, (0, 0, 0))
        self.display.blit(letter, (50, 50))

        self.fps_counter()

        pygame.display.update()
        self.clock.tick(60)

    def fps_counter(self):
        font = pygame.font.SysFont("Arial", 27)

        fps = str(int(self.clock.get_fps()))
        fps_t = font.render(fps, 1, pygame.Color("RED"))
        self.display.blit(fps_t, (0, 0))


game = Game()
