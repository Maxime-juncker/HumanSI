import random

import pyglet.clock
from AI import *
from Utilities import *
from Interfaces import *
from pyglet.window import *
from Settings import *
from Display import *
import TestPerlinNoise
from geneObject import coordRandInList


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
            self.screen: MyWindow = window
            self.screen.game = self
            self.fps_display = pyglet.window.FPSDisplay(window=window)
            self.fps_display.label.color = (100, 255, 100, 100)
            self.fps_display.label.font_size = 32
            self.fps_display.label.x = -window.width + 20
            self.fps_display.label.y = window.height - 50
            self.fps_display.label.batch = self.screen.guiBatch
            self.spawnLabel = pyglet.text.Label("",
                                                font_name='Times New Roman',
                                                font_size=32,
                                                color=(0, 0, 0, 255),
                                                x=-window.width + 20, y=window.height // 2 - 50,
                                                anchor_x='left', anchor_y='center',
                                                batch=self.screen.guiBatch)
            self.categoryLabel = pyglet.text.Label("categorie : tool",
                                                   font_name='Times New Roman',
                                                   font_size=20,
                                                   color=(0, 0, 0, 255),
                                                   x=-window.width + 20, y=window.height // 2 - 100,
                                                   anchor_x='left', anchor_y='center',
                                                   batch=self.screen.guiBatch)

            self.toolTipLabel = pyglet.text.Label("A / E pour changer d'objet, click gauche pour placer",
                                                  font_name='Times New Roman',
                                                  font_size=18,
                                                  color=(0, 0, 0, 200),
                                                  x=window.width - 20, y=-window.height + 50,
                                                  anchor_x='right', anchor_y='center',
                                                  batch=self.screen.guiBatch)
            self.descriptionPanel = DescriptionPanel(pos=(window.width // 1.7, -window.height // 15 + 100),
                                                     scale=window.worldCamera.sizeMultiplier,
                                                     batch=self.screen.guiBatch)
            self.descLabel = pyglet.text.Label("",
                                               font_name='Times New Roman',
                                               font_size=25,
                                               color=(255, 255, 255, 255),
                                               x=self.descriptionPanel.x - 30, y=self.descriptionPanel.y,
                                               anchor_x='center', anchor_y='center',
                                               multiline=True,
                                               width=300,
                                               batch=self.screen.guiBatch)

            self.slowUpdateTimer = None
            self.newUnit = None
            self.selectedTarget = None
            self.currentFantomeSprite = None
            self.civilisationSpawned = {}
            self.visibleSprite = {}
            self.activeDisplayText = {}
            self.activeSprite = []
            self.interfaces = {}
            self.categoryButtons = {}
            self.currentCategory = "tool"

            self.biomes = {}

            self.spriteIndex = 0
            self.activeImageIndex = 0
            self.spawnAbleUnit = LoadPreset(Directories.PresetDir + "Presets.csv")
            # self.interfaces["descriptionPanel"] = self.descriptionPanel
            self.PopulateSpawnableDict()
            self.SetupCategoriesButton(("Other", "Pop", "Civilisation", "Tools"))
            self.sprites = self.PreLoadSprites()
            self.mouse_pos = 0, 0
            # =================================================
            # C'est bon on a fini le setup la game loop peut commencer :D
            self.UpdateFantomeSprite()
            window.set_caption("HumanSI")

            self.GAME_RUNNING = True
            debugSuccessMsg("l'init c'est bien déroulé ! \n lancement de HumanSI...")
            debugInfoMsg("ci jamais la fenetre ne prend pas tous l'écran il faut \n modifier les paramètres WIDTH et HEIGHT dans Settings.py et mettre la résolution de votre écran")

        except Exception as e:
            debugFailMsg("/!\ FAIL DE L'INIT DANS Game.py \n HumanSI ne peut pas démarer !")
            debugFailMsg(e.with_traceback())

    def CreateProps(self):
        coords = coordRandInList(MAX_RESSOURCES_SPAWN_ON_START, self.screen.terrain.width, self.screen.terrain.height)
        for i in coords:
            if CheckCoordInBiome(i) > .2:
                self.SpawnUnit(LoadPreset(Directories.PresetDir + "Presets.csv", "RandomAssets"), i, None)

        if GAME_DEBUG:
            debugSuccessMsg("Placement des pros bons")

        """coords = coordRandInList(MAX_CIVILISATION_ON_START, self.screen.terrain.width, self.screen.terrain.height)
        for i in coords:
            if CheckCoordInBiome(i) < .1:
                civilisation = ("YellowCityHall", "RedCityHall", "PurpleCityHall", "BlueCityHall", "GreenCityHall",
                                "WhiteCityHall", "BlackCityHall", "DefaultCityHall")
                r = random.randint(0, 7)
                self.SpawnCivilisation(civilisation[r], i)
        """
    def LoadBiomeDict(self, csvFile):
        content = csv.DictReader(open(csvFile))
        for line in content:
            for element in line:
                self.biomes[element] = line[element]

    def toggle_button_handler(self, button: ToggleButton):
        if GAME_DEBUG:
            debugWarningMsg("switch to:" + button.category)
        self.currentCategory = button.category
        self.categoryLabel.text = "categorie : " + button.category
        self.spriteIndex = 0
        self.PopulateSpawnableDict()
        self.UpdateFantomeSprite()

    def SetupCategoriesButton(self, listCategories: list):
        for i in range(len(listCategories)):
            pos = (-self.screen.width + 50, i * 100)
            self.categoryButtons[listCategories[i]] = ToggleButton(self.toggle_button_handler, listCategories[i], pos,
                                                                   1, self.screen.guiBatch)

    def ToggleButtonAction(self):
        result = []
        for button in self.categoryButtons:
            result.append(self.categoryButtons[button].CheckIfClicked(self.GetMouseOffset()))

        if True in result:
            return True
        else:
            return False

    def DisableAllButtons(self, buttonToggle):
        if GAME_DEBUG:
            debugWarningMsg("Bouton pressé: " + str(buttonToggle))

        for button in self.categoryButtons:
            if self.categoryButtons[button] != buttonToggle:
                self.categoryButtons[button].Disable()

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
            if ligne["spritesPath"] != "none":
                temp = LoadSpritesFromFolder(ligne["spritesPath"])
                if len(temp) == 1:
                    result[ligne["name"]] = (pyglet.image.load(
                        Directories.SpritesDir + ligne["spritesPath"] + "/" + temp[0]),)
                    continue

                sprites = []
                for i in range(len(temp)):
                    sprites.append(pyglet.image.load(Directories.SpritesDir + ligne["spritesPath"] + "/" + temp[i]))
                result[ligne["name"]] = sprites

        return result

    def LoadAnimationFrames(self, preset):
        file = open(Directories.PresetDir + "Presets.csv", "r")

        if preset["name"] != "none":
            temp = LoadSpritesFromFolder(preset["spritesPath"])
            frames = []
            for i in range(len(temp)):
                frames.append(pyglet.resource.image(Directories.SpritesDir + preset["spritesPath"] + "/" + temp[i]))

        return frames

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
        self.activeImageIndex = randint(0, len(self.sprites[preset["name"]]) - 1)
        if self.currentFantomeSprite is None:
            self.currentFantomeSprite = FantomeSprite(preset, self.GetMouseOffset(), self.screen.worldBatch)

        self.currentFantomeSprite.UpdateSprite(preset)

    def CreatePopupMsg(self, info, priority):
        DispalyText(info, priority, -self.screen.width + 20, -self.screen.height + 30,
                    self.screen.guiBatch)

    def SpawnUnitBaseByIndex(self):
        '''
        on recup les different sprites en fonction de l'index
        et on le passe en parametre au truc que on vas spawn
        '''

        names = []
        [names.extend([v]) for v in self.spawnAbleUnit.keys()]

        preset = LoadPreset(Directories.PresetDir + "Presets.csv", names[self.spriteIndex])
        if "tool" in preset["category"]:
            self.ToolAction(preset)
            return

        self.SpawnUnit(LoadPreset(Directories.PresetDir + "Presets.csv", "spawnEffect"), self.GetMouseOffset(), None)

        if "none" in preset["category"]:
            return

        if CheckCoordInBiome(self.GetMouseOffset()) < .1:
            pyglet.media.StaticSource(pyglet.media.load('Assets/SFX/CantBuild.wav')).play()
            DispalyText("impossible de créer un objet ici !", 2, -self.screen.width + 20, -self.screen.height + 30,
                        self.screen.guiBatch)
            return

        pyglet.media.StaticSource(pyglet.media.load('Assets/SFX/Place_build.wav')).play()
        if "CityHall" in names[self.spriteIndex]:
            self.SpawnCivilisation(names[self.spriteIndex], self.GetMouseOffset())
            return

        self.newUnit = Unit(preset, None, self.GetMouseOffset(), self.screen.worldBatch)
        DispalyText("Spawned : " + self.newUnit.name, 0, -self.screen.width + 20, -self.screen.height + 30,
                    self.screen.guiBatch)

        return self.newUnit

    def ToolAction(self, preset):

        if preset["name"] == "exterminator":
            closestObject = self.GetClosestObjectToLocation(self.GetMouseOffset(), 45)

            if closestObject != None:
                self.visibleSprite[closestObject].Destroy()
                pyglet.media.StaticSource(pyglet.media.load('Assets/SFX/DeleteTool.wav')).play()

        if preset["name"] == "ouch":
            closestObject = self.GetClosestObjectToLocation(self.GetMouseOffset(), 45)
            if closestObject != None:
                self.visibleSprite[closestObject].Damage(int(preset["damage"]))
                pyglet.media.StaticSource(pyglet.media.load('Assets/SFX/DamageTool.wav')).play()

        if preset["name"] == "inspecter":
            offsetPos = self.GetMouseOffset()
            closestObject = self.GetClosestObjectToLocation(offsetPos, 90)
            # L'update du panneau de desc peut supporter les valuer None c'est pas un probleme
            if GAME_DEBUG:
                debugSuccessMsg(closestObject)
            self.UpdateDescPanel(closestObject)

    def SpawnUnit(self, popPreset, pos, civilisation):
        self.newUnit = Unit(popPreset, civilisation, pos, self.screen.worldBatch)
        return self.newUnit

    def SpawnCivilisation(self, civilisationName, pos):
        if len(self.civilisationSpawned) >= MAX_CIVILISATION:
            msg = "Limite de civilisation atteinte, pour en recréé utiliser l'exterminator et detruiser l'un des hotel de ville"
            DispalyText(msg, 2, -self.screen.width + 20, -self.screen.height + 30, self.screen.guiBatch)
            return

        tempPreset = LoadPreset(Directories.PresetDir + "Presets.csv", civilisationName)
        preset = LoadPreset(Directories.PresetDir + "Civilisation.csv", tempPreset["civilisation"])
        newCivilisation = Civilisation(preset, pos)

    def GetRandomSprite(self, sprites):
        return sprites[random.randint(0, len(sprites) - 1)]

    def PopulateSpawnableDict(self):
        temp = LoadPreset(Directories.PresetDir + "Presets.csv")
        self.spawnAbleUnit.clear()
        for element in temp:
            if int(temp[element]["isSpawnable"]) == 1 and temp[element]["category"] == self.currentCategory or \
                    temp[element]["category"] == "none":
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
            if object == exeption or self.visibleSprite[object].category == "VFX":
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
