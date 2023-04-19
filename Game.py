import pyglet.clock
from AI import *
from Utilities import *
from Interfaces import *
from pyglet.window import *
from Settings import *
from Display import *


class Game:

    def __init__(self, window):
        """
        Init permet de crée et setup la var Game qui est basiquement le truc qui 
        relie tous le sytemes ensembre du coup si ça marche pas rien ne marchera 
        a la fin on passe la var GAME_RUNNING a True tant qu'elle est a fausse
        il n'y a ni update ni aucun autre truc a par cette fonction qui marche .
        """
        try:
            # ============== VARS =============================
            self.screen = window
            self.fps_display = pyglet.window.FPSDisplay(window=window)
            self.fps_display.label.color = (100, 255, 100, 100)
            self.fps_display.label.font_size = 15
            self.fps_display.label.x = -window.width // 2 + 20
            self.fps_display.label.y = window.height // 2 - 20
            self.fps_display.label.batch = self.screen.guiBatch
            self.spawnLabel = pyglet.text.Label("",
                                                font_name='Times New Roman',
                                                font_size=20,
                                                color=(0, 0, 0, 255),
                                                x=-window.width // 2 + 20, y=window.height // 2 - 50,
                                                anchor_x='left', anchor_y='center')

            self.descriptionPanel = DescriptionPanel((window.width // 3, -window.height // 15 + 100),
                                                     window.worldCamera.sizeMultiplier,self.screen.guiBatch)
            self.descLabel = pyglet.text.Label("",
                                               font_name='Times New Roman',
                                               font_size=15,
                                               color=(255, 255, 255, 255),
                                               x=self.descriptionPanel.x, y=self.descriptionPanel.y,
                                               anchor_x='center', anchor_y='center',
                                               multiline=True,
                                               width=300,
                                               batch=self.screen.guiBatch)
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
            # self.interfaces["descriptionPanel"] = self.descriptionPanel
            self.PopulateSpawnableDict()
            self.sprites = self.PreLoadSprites()
            self.mouse_pos = 0, 0
            # =================================================
            # C'est bon on a fini le setup la game loop peut commencer :D
            self.UpdateFantomeSprite()
            window.set_caption("HumanSI")

            self.GAME_RUNNING = True
            debugSuccessMsg("l'init c'est bien déroulé ! \n lancement de HumanSI...")

        except Exception as e:
            debugFailMsg("/!\ FAIL DE L'INIT DANS Game.py \n HumanSI ne peut pas démarer !")
            debugFailMsg(e.with_traceback())

    def PreLoadSprites(self):
        """
        fonct pour renplir un dict d'image
        vue que les img sont déjà charger dans la mémoire
        ça optimise les perf vue que y'a pas besoin de les
        recharger a chaque fois.
        """
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
        if clickedSprite is None:
            self.selectedTarget = None
            self.descriptionPanel.HidePanel()
            self.descLabel.text = ""
            return
        self.selectedTarget = self.visibleSprite[clickedSprite]
        self.descriptionPanel.ShowPanel(self.visibleSprite[clickedSprite])
        self.descLabel.text = self.descriptionPanel.GetInfos()

    def UpdateFantomeSprite(self):
        names = []
        [names.extend([v]) for v in self.spawnAbleUnit.keys()]

        if "none" in names[self.spriteIndex]:
            if self.currentFantomeSprite is not None:
                self.currentFantomeSprite.Hide()
            return

        preset = LoadPreset(Directories.PresetDir + "Presets.csv", names[self.spriteIndex])
        if self.currentFantomeSprite is None:
            self.currentFantomeSprite = FantomeSprite(preset, self.GetMouseOffset(), self.screen.worldBatch)

        self.currentFantomeSprite.UpdateSprite(preset)

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

        if "CityHall" in names[self.spriteIndex]:
            self.SpawnCivilisation(names[self.spriteIndex])
            return

        self.newUnit = Unit(preset, None, self.GetMouseOffset(), self.screen.worldBatch)

        return self.newUnit

    def ToolAction(self, preset):

        if preset["name"] == "oppenheimer":
            closestObject = game.GetClosestObjectToLocation(self.GetMouseOffset(), 45)
            if closestObject != None:
                self.visibleSprite[closestObject].Destroy()

        if preset["name"] == "badaboom":
            closestObject = game.GetClosestObjectToLocation(self.GetMouseOffset(), 45)
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

        self.newUnit = Unit(popPreset, civilisation, pos, self.screen.worldBatch)
        return self.newUnit

    def SpawnCivilisation(self, civilisationName):

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
            maxDistance (float): la distance max entre les deux objets
            exeption (string): bas c'est une exeption....
        Returns:
            string: le nom de l'objet le plus proche du point
        """
        temp = self.visibleSprite.copy()
        result = {}

        for object in temp:
            if object == exeption:
                continue
            distance = GetDistanceFromVector(location, temp[object].GetLocation())
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
            if object == exeption or temp[object].GetCivilisation() == unit.GetCivilisation() or temp[
                object].category == "none":
                continue
            distance = GetDistanceFromVector(unit.GetLocation(), temp[object].GetLocation())
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

    def GetMouseOffset(self):
        offsetPos_x = self.screen.worldCamera.offset_x - self.screen.width + self.mouse_pos[0] * 2
        offsetPos_y = self.screen.worldCamera.offset_y - self.screen.height + self.mouse_pos[1] * 2

        return offsetPos_x, offsetPos_y

    def SuperUpdate(self):
        pass
        l = []
        [l.extend([v]) for v in game.spawnAbleUnit.keys()]
        if len(l) > 0:
            self.spawnLabel.text = "Spawn : " + str(l[self.spriteIndex])

        if self.currentFantomeSprite is not None:
            self.currentFantomeSprite.x, self.currentFantomeSprite.y = self.GetMouseOffset()
            self.currentFantomeSprite.Update()


game = None


def StartGame(window):
    global game
    game = Game(window)
    return game
