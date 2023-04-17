import pyglet.clock

from AI import *
from Utilities import *
from Interfaces import *
from pyglet.window import *
from Settings import *

'''
TRUC IMPORTANT. 
pygame fonctionne en dessinant les truc qui sont contenu dans une liste 
(ici CameraGroup) sauf que la liste est h24 en bordel du coup j'override 
la class de pygame pour ajouter des fonctionalité c'est CameraGroup qui vas donc
etre la liste des sprites a l'ecran 
SI VOUS AJOUTEZ DES SPRITE AJOUTER LES A CAMERAGROUP
'''


class Camera:
    """
    y'a deux camera celle ci n'est pas centrer et quand on zoom ça decale tout du coup utiliser la version center juste
    en bas
    """

    def __init__(self, window: pyglet.window.Window, scroll_speed=1, min_zoom=1, max_zoom=4):
        assert min_zoom <= max_zoom
        self._window = window
        self.scroll_speed = scroll_speed
        self.max_zoom = max_zoom
        self.min_zoom = min_zoom
        self.offset_x = 0
        self.offset_y = 0
        self._zoom = min_zoom

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        """ on change le zoom tout en le clamp (j'ai le seum j'ai fait une jolie fonct dans Utilities mais elle sert a rien...)"""
        self._zoom = max(min(value, self.max_zoom), self.min_zoom)

    @property
    def position(self):
        return self.offset_x, self.offset_y

    @position.setter
    def position(self, value):
        self.offset_x, self.offset_y = value

    def move(self, axis_x, axis_y):
        """
        fonct pour bouger la cam avec les axes et en fonction
        du zoom
        """
        self.offset_x += self.scroll_speed * axis_x
        self.offset_y += self.scroll_speed * axis_y

    def begin(self):
        view_matrix = self._window.view.translate((-self.offset_x * self._zoom, -self.offset_y * self._zoom, 0))
        view_matrix = view_matrix.scale((self._zoom, self._zoom, 1))
        self._window.view = view_matrix

    def end(self):
        # ici faut tous inversé PS : c'est trop chiant a expliquer ici venez me demander en direct.
        view_matrix = self._window.view.scale((1 / self._zoom, 1 / self._zoom, 1))
        view_matrix = view_matrix.translate((self.offset_x * self._zoom, self.offset_y * self._zoom, 0))

        self._window.view = view_matrix

    def __enter__(self):
        self.begin()

    def __exit__(self, exception_type, exception_value, traceback):
        self.end()


class CenteredCamera(Camera):
    """comme avant mais mieux :p"""

    def begin(self):
        x = -self._window.width // 2 / self._zoom + self.offset_x
        y = -self._window.height // 2 / self._zoom + self.offset_y

        view_matrix = self._window.view.translate((-x * self._zoom, -y * self._zoom, 0))
        view_matrix = view_matrix.scale((self._zoom, self._zoom, 1))
        self._window.view = view_matrix

    def end(self):
        x = -self._window.width // 2 / self._zoom + self.offset_x
        y = -self._window.height // 2 / self._zoom + self.offset_y

        view_matrix = self._window.view.scale((1 / self._zoom, 1 / self._zoom, 1))
        view_matrix = view_matrix.translate((x * self._zoom, y * self._zoom, 0))
        self._window.view = view_matrix


class Game:

    def __init__(self):
        """
        Init permet de crée et setup la var Game qui est basiquement le truc qui 
        relie tous le sytemes ensembre du coup si ça marche pas rien ne marchera 
        a la fin on passe la var GAME_RUNNING a True tant qu'elle est a fausse
        il n'y a ni update ni aucun autre truc a par cette fonction qui marche .
        """
        try:
            self.window = Window(WIDTH, HEIGHT, "HumanSI | Chargement...", fullscreen=FULLSCREEN)

            # ============== VARS =============================
            self.batch = pyglet.graphics.Batch()
            self.worldCamera = CenteredCamera(self.window, scroll_speed=5, min_zoom=.5, max_zoom=6)
            self.GuiCamera = CenteredCamera(self.window)

            self.fps_display = pyglet.window.FPSDisplay(window=self.window)
            self.fps_display.label.color = (100, 255, 100, 100)
            self.fps_display.label.font_size = 15
            self.fps_display.label.x = -self.window.width // 2 + 20
            self.fps_display.label.y = self.window.height // 2 - 20
            self.spawnLabel = pyglet.text.Label("",
                                                font_name='Times New Roman',
                                                font_size=20,
                                                x=-self.window.width // 2 + 20, y=self.window.height // 2 - 50,
                                                anchor_x='left', anchor_y='center')

            self.descriptionPanel = DescriptionPanel((self.window.width //3, -self.window.height // 15 + 100))
            self.descLabel = pyglet.text.Label("",
                                                font_name='Times New Roman',
                                                font_size=15,
                                                x=self.descriptionPanel.x, y=self.descriptionPanel.y,
                                                anchor_x='center', anchor_y='center',
                                                multiline=True,
                                                width=300)
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
            self.window.set_caption("HumanSI")

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
        pass

        if self.currentFantomeSprite is not None:
            self.currentFantomeSprite.Destroy()

        names = []
        [names.extend([v]) for v in self.spawnAbleUnit.keys()]

        if "none" in names[self.spriteIndex]:
            return
        preset = LoadPreset(Directories.PresetDir + "Presets.csv", names[self.spriteIndex])

        self.currentFantomeSprite = FantomeSprite(preset, self.worldCamera.zoom, \
                                                  self.GetMouseOffset(), self.batch)

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

        self.newUnit = Unit(preset, None, self.worldCamera.zoom, \
                            self.GetMouseOffset(), self.batch)

        return self.newUnit

    def ToolAction(self, preset):
        pass
        """if preset["name"] == "oppenheimer":
            offsetPos = self.cameraGroup.offset - self.cameraGroup.internalOffset + pygame.mouse.get_pos()
            closestObject = game.GetClosestObjectToLocation(offsetPos, 45)
            if closestObject != None:
                self.visibleSprite[closestObject].Destroy()

        if preset["name"] == "badaboom":
            offsetPos = self.cameraGroup.offset - self.cameraGroup.internalOffset + pygame.mouse.get_pos()
            closestObject = game.GetClosestObjectToLocation(offsetPos, 45)
            if closestObject != None:
                self.visibleSprite[closestObject].Damage(int(preset["damage"]))"""

    def SpawnUnit(self, popPreset, pos, civilisation):

        """try:
            (r, g, b, a) = self.cameraGroup.internalSurface.get_at((int(pos[0]), int(pos[1])))
            if r == 113 and g == 221 and b == 238:
                debugFailMsg("unable to spawn on water !")
                return
        except:
            print("probleme")"""

        self.newUnit = Unit(popPreset, civilisation, self.worldCamera.zoom, pos, self.batch)
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
            if object == exeption or temp[object].GetCivilisation() == unit.GetCivilisation():
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

    def SlowUpdate(self):
        sprites = self.slowUpdateDict.copy()
        for sprite in sprites:
            sprites[sprite].Tick()

        self.slowUpdateTimer = threading.Timer(1, self.SlowUpdate)
        self.slowUpdateTimer.start()

    def GetMouseOffset(self):
        offsetPos_x = self.worldCamera.offset_x - self.window.width + self.mouse_pos[0] * 2
        offsetPos_y = self.worldCamera.offset_y - self.window.height + self.mouse_pos[1] * 2

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
        '''
        fonct appeler toutes les frames
        Est appeler AVANT Update, ça peut permetre
        de prioriser certaine update

        du coup pour l'instant c'est surtout les update de pygame
        que je met là vue que ça a l'air plutot important :D
        '''

        """ if len(self.interfaces) > 0:
            self.descriptionPanel.rect.center = self.cameraGroup.offset + self.descriptionPanel.pos

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
        self.clock.tick(30)"""

    def debugUI(self):

        font = pygame.font.SysFont("Arial", 27)

        temp = self.visibleSprite.copy()
        units = str(len(temp))

        fps = str(int(self.clock.get_fps()))
        debug_t = font.render("FPS : " + fps + " | " + "units : " + units, 1, pygame.Color("RED"))
        self.display.blit(debug_t, (0, 0))


game = Game()
