import pygame
import threading
import AI
from AI import *
from Utilities import *
from Interfaces import *

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

        # self.groundSurface = pygame.image.load("Assets/Graphics/ground.png").convert_alpha()
        # self.groundRect = self.groundSurface.get_rect(topleft=(0, 0))

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
        
        #ça devrai a peu pres contrer les effets de quand on change de resolution
        #apres la tout de suite y'a plus mass temps du coup plus tard si quelqu'un
        #a le temps pour faire ça au propre ça serai sympas merci.
        self.spriteSizeMultiplier = self.internalSurfaceSizeVector.length() / 2500

    def CustomDraw(self):
        if not game.GAME_RUNNING:
            return
        # self.centerCameraOnTarget()
        # self.boxTargetCamera()

        if game.selectedTarget is not None:
            self.centerCameraOnTarget(game.selectedTarget)
        self.keyboardControl()

        self.internalSurface.fill('white')

        # Elements actifs
        try:

            sprites = sorted(self.sprites(), key=lambda sprite: sprite.rect.centery)
            for sprite in sprites:
                offestPos = sprite.rect.center - self.offset + self.internalOffset
                self.internalSurface.blit(sprite.image, offestPos)

                interfaces = sorted(list(game.interfaces.values()), key=lambda interface: interface.rect.centery)
                if len(interfaces) > 0:
                    for interface in interfaces:
                        offestPos = interface.rect.center - self.offset + self.internalOffset
                        self.internalSurface.blit(interface.image, offestPos)

            scaledSurf = pygame.transform.scale(self.internalSurface, self.internalSurfaceSizeVector * self.zoomScale)
            scaledRect = scaledSurf.get_rect(center=(self.half_w, self.half_h))
            self.displaySurface.blit(scaledSurf, scaledRect)
        except:

            debugFailMsg("fail to update")

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
        """
        Init permet de crée et setup la var Game qui est basiquement le truc qui 
        relie tous le sytemes ensembre du coup si ça marche pas rien ne marchera 
        a la fin on passe la var GAME_RUNNING a True tant qu'elle est a fausse
        il n'y a ni update ni aucun autre truc a par cette fonction qui marche .
        """
        
        # ============== VARS =============================
        self.descPanelLocation = (930, 0)
        self.slowUpdateTimer = None
        self.newUnit = None
        self.selectedTarget = None
        self.currentFantomeSprite = None
        self.civilisationSpawned = {}
        self.spriteIndex = 0
        self.spawnAbleUnit = LoadPreset(Directories.PresetDir + "Presets.csv")
        
        # =================================================
        # ============ SETUP LIST =====================
        self.normalUpdateDict = {}
        self.slowUpdateDict = {}
        self.visibleSprite = {}
        self.interfaces = {}
        self.PopulateSpawnableDict()

        # ============ SETUP PYGAME =====================

        pygame.init()
        pygame.display.set_caption("Chargement...")

        self.display = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        self.cameraGroup = CameraGroup()

        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.SysFont("Arial", 27)
        self.descFont = pygame.font.SysFont("Arial", 15)
        # =================================================
        
                
        # ============ HUD VARS =====================
        self.descriptionPanel = DescriptionPanel(self.cameraGroup.spriteSizeMultiplier, self.descPanelLocation)
        self.interfaces["descriptionPanel"] = self.descriptionPanel
        
        
        # C'est bon on a fini le setup la game loop peut commencer :D
        pygame.display.set_caption("HumainSI")

        self.SlowUpdate()
        self.UpdateFantomeSprite()

        self.GAME_RUNNING = True

    def UpdateDescPanel(self, clickedSprite):
        
        """
        en gros le but ici c'est de a partir du sprite qu'on a clicker il faut retrouver l'unit qui 
        le possede pour ça on use les id() pour associer un sprite avec une unit
        (en vrai maintenant que j'y pense y'a pas besoin de id(), mais balec ça fait plus stylé)
        :D
        """
        
        if clickedSprite is None:
            self.descriptionPanel.HidePanel()
            
        objects = self.visibleSprite.copy()
        for object in objects:
            if id(objects[object].GetSprite() == id(clickedSprite)): 
                print(objects[object].name)
                self.descriptionPanel.ShowPanel(objects[object])
                return
            
    def UpdateFantomeSprite(self):
        if self.currentFantomeSprite is not None:
            self.currentFantomeSprite.DestroySprite()
            
        names = []
        [names.extend([v]) for v in self.spawnAbleUnit.keys()]

        if "none" in names[self.spriteIndex]:
            return
        preset = LoadPreset(Directories.PresetDir + "Presets.csv", names[self.spriteIndex])
        sprites = LoadSpritesFromFolder(preset["spritesPath"])
        

        offsetPos = self.cameraGroup.offset - self.cameraGroup.internalOffset + pygame.mouse.get_pos()
        self.currentFantomeSprite = FantomeSprite(sprites, preset,self.cameraGroup.spriteSizeMultiplier,\
            offsetPos, self.cameraGroup)
        

    def SpawnUnitBaseByIndex(self):
        '''
        on recup les different sprites en fonction de l'index
        et on le passe en parametre au truc que on vas spawn
        '''

        names = []
        [names.extend([v]) for v in self.spawnAbleUnit.keys()]

        if "none" in names[self.spriteIndex]:
            return

        preset = LoadPreset(Directories.PresetDir + "Presets.csv", names[self.spriteIndex])
        sprites = LoadSpritesFromFolder(preset["spritesPath"])
        

        if "CityHall" in names[self.spriteIndex]:
            self.SpawnCivilisation(names[self.spriteIndex])
            return

        offsetPos = self.cameraGroup.offset - self.cameraGroup.internalOffset + pygame.mouse.get_pos()
        self.newUnit = Unit(self.display, sprites, preset, None,self.cameraGroup.spriteSizeMultiplier,\
            offsetPos, self.cameraGroup)

        if int(preset["updateWeight"]) == 0:
            self.normalUpdateDict[self.newUnit.name] = self.newUnit
        elif int(preset["updateWeight"]) == 1:
            self.slowUpdateDict[self.newUnit.name] = self.newUnit

            """if "Chief_" in names[self.spriteIndex]:
            self.SpawnCivilisation(names[self.spriteIndex])"""
            
        return self.newUnit

    def SpawnUnit(self, popPreset, pos, civilisation):

        """try:
            (r, g, b, a) = self.cameraGroup.internalSurface.get_at((int(pos[0]), int(pos[1])))
            if r == 113 and g == 221 and b == 238:
                debugFailMsg("unable to spawn on water !")
                return
        except:
            print("probleme")"""

        sprites = LoadSpritesFromFolder(popPreset["spritesPath"])

        self.newUnit = Unit(self.display, sprites, popPreset, civilisation, \
            self.cameraGroup.spriteSizeMultiplier, pos, self.cameraGroup)
        
        if int(popPreset["updateWeight"]) == 0:
            self.normalUpdateDict[self.newUnit.name] = self.newUnit
        elif int(popPreset["updateWeight"]) == 1:
            self.slowUpdateDict[self.newUnit.name] = self.newUnit
            
        return self.newUnit

    def SpawnCivilisation(self, civilisationName):

        offsetPos = self.cameraGroup.offset - self.cameraGroup.internalOffset + pygame.mouse.get_pos()

        """try:
            (r, g, b, a) = pygame.Surface.get_at(self.display, (int(offsetPos[0]), int(offsetPos[1])))
            if r == 113 and g == 221 and b == 238:
                debugFailMsg("unable to spawn on water !")
                return
        except:
            print("problème")"""

        tempPreset = LoadPreset(Directories.PresetDir + "Presets.csv", civilisationName)
        preset = LoadPreset(Directories.PresetDir + "Civilisation.csv", tempPreset["civilisation"])
        chiefPreset = LoadPreset(Directories.PresetDir + "Presets.csv", preset["chiefName"])
        newCivilisation = Civilisation(preset)

        self.SpawnUnit(chiefPreset, offsetPos, newCivilisation)

        if int(preset["updateWeight"]) == 0:
            self.normalUpdateDict[newCivilisation.name] = newCivilisation
        elif int(preset["updateWeight"]) == 1:
            self.slowUpdateDict[newCivilisation.name] = newCivilisation

    def GetRandomSprite(self, sprites):
        return sprites[random.randint(0, len(sprites) - 1)]

    def PopulateSpawnableDict(self):
        temp = LoadPreset(Directories.PresetDir + "Presets.csv")
        self.spawnAbleUnit.clear()
        for element in temp:
            if int(temp[element]["isSpawnable"]) == 1:
                self.spawnAbleUnit[element] = LoadPreset(Directories.PresetDir + "Presets.csv", element)

    def KillAllActors(self):
        for sprite in self.cameraGroup:
            sprite.kill()

        self.slowUpdateDict.clear()
        self.normalUpdateDict.clear()
        self.visibleSprite.clear()

    def Tick(self):
        '''
        fonct appeler toutes les frames

        PS : on fait une copie de la liste que on vas update
             sinon si on spawn un truc et que la longueur de la
             liste change ça nique tout :D

        '''

        """civilisations = self.civilisationSpawned
        for civilisation in civilisations:
            civilisations[civilisation].Update()"""

        sprites = self.normalUpdateDict.copy()
        for sprite in sprites:
            self.normalUpdateDict[sprite].Tick()

    def SlowUpdate(self):
        sprites = self.slowUpdateDict.copy()
        for sprite in sprites:
            sprites[sprite].Tick()

        self.slowUpdateTimer = threading.Timer(1, self.SlowUpdate)
        self.slowUpdateTimer.start()

    def SuperUpdate(self):
        '''
        fonct appeler toutes les frames
        Est appeler AVANT Update, ça peut permetre
        de prioriser certaine update

        du coup pour l'instant c'est surtout les update de pygame
        que je met là vue que ça a l'air plutot important :D
        '''
        
        if len(self.interfaces) > 0:
            self.descriptionPanel.rect.center = self.cameraGroup.offset + self.descriptionPanel.pos
            
        if self.currentFantomeSprite is not None:
            offsetPos = self.cameraGroup.offset - self.cameraGroup.internalOffset + pygame.mouse.get_pos()
            self.currentFantomeSprite.rect.bottomright = offsetPos
            self.currentFantomeSprite.Tick()

        self.cameraGroup.update()
        self.cameraGroup.CustomDraw()

        # on met aussi un petit text (debug)

        l = []
        [l.extend([v]) for v in game.spawnAbleUnit.keys()]
        if len(l) > 0:
            letter = self.font.render("Spawn : " + str(l[self.spriteIndex]), 0, (0, 0, 0))
            self.display.blit(letter, (50, 50))

        self.debugUI()
               
        
        if self.descriptionPanel.Update() is not None:
            text = self.descriptionPanel.Update()
            
            for i in range(len(text)):
                stats = self.descFont.render(text[i], 0, (255, 255, 255))    
                self.display.blit(stats, (self.descPanelLocation[0] + 200, \
                                          self.descPanelLocation[1] + 190 + 20*i))

        pygame.display.update()
        self.clock.tick(120)

    def debugUI(self):

        font = pygame.font.SysFont("Arial", 27)

        temp = self.visibleSprite.copy()
        units = str(len(temp))

        fps = str(int(self.clock.get_fps()))
        debug_t = font.render("FPS : " + fps + " | " + "units : " + units, 1, pygame.Color("RED"))
        self.display.blit(debug_t, (0, 0))


game = Game()
