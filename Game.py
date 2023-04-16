
import threading
import AI
from AI import *
from Utilities import *
from Interfaces import *
from pyglet import *
from pyglet.window import *


'''
TRUC IMPORTANT. 
pygame fonctionne en dessinant les truc qui sont contenu dans une liste 
(ici CameraGroup) sauf que la liste est h24 en bordel du coup j'override 
la class de pygame pour ajouter des fonctionalité c'est CameraGroup qui vas donc
etre la liste des sprites a l'ecran 
SI VOUS AJOUTEZ DES SPRITE AJOUTER LES A CAMERAGROUP
'''


class Game:

    def __init__(self):
        """
        Init permet de crée et setup la var Game qui est basiquement le truc qui 
        relie tous le sytemes ensembre du coup si ça marche pas rien ne marchera 
        a la fin on passe la var GAME_RUNNING a True tant qu'elle est a fausse
        il n'y a ni update ni aucun autre truc a par cette fonction qui marche .
        """
        try:

            # ============== VARS =============================
            self.batch = pyglet.graphics.Batch()

            self.descPanelLocation = (self.display.get_rect().right - 560, 0)
            self.slowUpdateTimer = None
            self.newUnit = None
            self.selectedTarget = None
            self.currentFantomeSprite = None
            self.civilisationSpawned = {}
            self.normalUpdateDict = {}
            self.slowUpdateDict = {}
            self.visibleSprite = {}
            self.activeSprite = []
            self.interfaces = {}
            self.spriteIndex = 0
            self.spawnAbleUnit = LoadPreset(Directories.PresetDir + "Presets.csv")
            self.descriptionPanel = DescriptionPanel(self.cameraGroup.spriteSizeMultiplier, self.descPanelLocation)
            self.interfaces["descriptionPanel"] = self.descriptionPanel
            self.PopulateSpawnableDict()
            self.sprites = self.PreLoadSprites()
            self.mouse_pos = 0,0
            # =================================================

            # C'est bon on a fini le setup la game loop peut commencer :D
            pygame.display.set_caption("HumainSI")

            # self.SlowUpdate()
            self.UpdateFantomeSprite()

            self.GAME_RUNNING = True
            debugSuccessMsg("l'init c'est bien déroulé ! \n lancement de HumanSI...")
        except Exception as e:
            debugFailMsg("/!\ FAIL DE L'INIT DANS Game.py \n HumanSI ne peut pas démarer !")
            debugFailMsg(e)

    def PreLoadSprites(self):
        file = open(Directories.PresetDir + "Presets.csv", "r")
        content = csv.DictReader(file, delimiter=",")

        result = {}
        for ligne in content:
            if ligne["name"] != "none":
                temp = LoadSpritesFromFolder(ligne["spritesPath"])
                result[ligne["name"]] = pyglet.image.load(Directories.SpritesDir + ligne["spritesPath"] + "/" + temp[
                    random.randrange(0, len(temp))])
        return result

    def UpdateDescPanel(self, clickedSprite):
        if clickedSprite == None:
            self.selectedTarget = None
            self.descriptionPanel.HidePanel()
            return
        self.selectedTarget = self.visibleSprite[clickedSprite]
        self.descriptionPanel.ShowPanel(self.visibleSprite[clickedSprite])

    def UpdateFantomeSprite(self):

        if self.currentFantomeSprite is not None:
            self.currentFantomeSprite.Destroy()

        names = []
        [names.extend([v]) for v in self.spawnAbleUnit.keys()]

        if "none" in names[self.spriteIndex]:
            return
        preset = LoadPreset(Directories.PresetDir + "Presets.csv", names[self.spriteIndex])
        sprites = LoadSpritesFromFolder(preset["spritesPath"])

        offsetPos = self.cameraGroup.offset - self.cameraGroup.internalOffset + pygame.mouse.get_pos()
        self.currentFantomeSprite = FantomeSprite(sprites, preset, self.cameraGroup.spriteSizeMultiplier, \
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

        if "tool" in preset["category"]:
            self.ToolAction(preset)
            return

        sprites = LoadSpritesFromFolder(preset["spritesPath"])
        if "CityHall" in names[self.spriteIndex]:
            self.SpawnCivilisation(names[self.spriteIndex])
            return

        offsetPos = self.cameraGroup.offset - self.cameraGroup.internalOffset + pygame.mouse.get_pos()
        self.newUnit = Unit(self.display, sprites, preset, None, self.cameraGroup.spriteSizeMultiplier, \
                            offsetPos, self.cameraGroup)

        return self.newUnit

    def ToolAction(self, preset):
        if preset["name"] == "oppenheimer":
            offsetPos = self.cameraGroup.offset - self.cameraGroup.internalOffset + pygame.mouse.get_pos()
            closestObject = game.GetClosestObjectToLocation(offsetPos, 45)
            if closestObject != None:
                self.visibleSprite[closestObject].Destroy()

        if preset["name"] == "badaboom":
            offsetPos = self.cameraGroup.offset - self.cameraGroup.internalOffset + pygame.mouse.get_pos()
            closestObject = game.GetClosestObjectToLocation(offsetPos, 45)
            if closestObject != None:
                self.visibleSprite[closestObject].Damage(int(preset["damage"]))

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
        newCivilisation = Civilisation(preset)

    def GetRandomSprite(self, sprites):
        return sprites[random.randint(0, len(sprites) - 1)]

    def PopulateSpawnableDict(self):
        temp = LoadPreset(Directories.PresetDir + "Presets.csv")
        self.spawnAbleUnit.clear()
        for element in temp:
            if int(temp[element]["isSpawnable"]) == 1:
                self.spawnAbleUnit[element] = LoadPreset(Directories.PresetDir + "Presets.csv", element)

    def KillAllActors(self):

        for object in self.visibleSprite.copy():
            self.visibleSprite[object].Destroy()
        self.slowUpdateDict.clear()
        self.normalUpdateDict.clear()
        self.visibleSprite.clear()

    def GetClosestObjectToLocation(self, location: tuple, maxDistance, exeption=""):
        """
        fonct pour get l'object le plus proche d'un point 
        c'est surtout utiliser pour quand le user click sur un object 
        et veut ses stats
        Args:
            location (tuple): coordoner d'un point
        Returns:
            string: le nom de l'objet le plus proche du point
        """
        temp = self.visibleSprite.copy()
        result = {}

        for object in temp:
            if object == exeption:
                continue
            distance = location.distance_to(temp[object].GetLocation())
            if distance <= maxDistance:
                result[object] = distance
        if len(result) == 0:
            return None
        result = {key: val for key, val in sorted(result.items(), key=lambda ele: ele[1])}
        return list(result.keys())[0]

    def GetClosestObjectToOtherObject(self, unit, maxDistance, exeption=""):
        """
        fonct pour get l'object le plus proche d'un point 
        c'est surtout utiliser pour quand le user click sur un object 
        et veut ses stats
        Args:
            location (tuple): coordoner d'un point
        Returns:
            string: le nom de l'objet le plus proche du point
        """
        temp = self.visibleSprite.copy()
        result = {}

        for object in temp:
            if object == exeption or temp[object].GetCivilisation() == unit.GetCivilisation():
                continue
            distance = unit.GetLocation().distance_to(temp[object].GetLocation())
            if distance <= maxDistance:
                result[object] = distance
        if len(result) == 0:
            return None

        for ele in result:
            if "CityHall" in ele:
                return ele
        result = {key: val for key, val in sorted(result.items(), key=lambda ele: ele[1])}
        return list(result.keys())[0]

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
            # self.currentFantomeSprite.Update()


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
                self.display.blit(stats, (self.descPanelLocation[0] + 200, self.descPanelLocation[1] + 190 + 20 * i))

        pygame.display.flip()
        self.clock.tick(30)

    def debugUI(self):

        font = pygame.font.SysFont("Arial", 27)

        temp = self.visibleSprite.copy()
        units = str(len(temp))

        fps = str(int(self.clock.get_fps()))
        debug_t = font.render("FPS : " + fps + " | " + "units : " + units, 1, pygame.Color("RED"))
        self.display.blit(debug_t, (0, 0))


game = Game()
