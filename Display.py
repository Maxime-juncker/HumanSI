import math
from random import randint
import pyglet
from pyglet.gl import *
from Settings import *
import Game


class Camera:
    """
    y'a deux camera celle ci n'est pas centrer et quand on zoom ça decale tout du coup utiliser la version center juste
    en bas
    """

    def __init__(self, window: pyglet.window.Window, scroll_speed=1, min_zoom=.5, max_zoom=4):
        assert min_zoom <= max_zoom
        self._window = window
        self.scroll_speed = scroll_speed
        self.max_zoom = max_zoom
        self.min_zoom = min_zoom
        self.offset_x = 0
        self.offset_y = 0
        self._zoom = min_zoom

        self.sizeMultiplier = math.sqrt(window.width ** 2 + window.height ** 2) / 2200

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

    def SetPosition(self,value):
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


class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set la taille
        if not FULLSCREEN:
            self.set_size(WIDTH, HEIGHT)
        # Background
        glClearColor(255, 255, 255, 1.0)  # red, green, blue, and alpha(transparency)

        self.worldCamera = CenteredCamera(self, scroll_speed=5, min_zoom=.5, max_zoom=6)
        self.game: Game.Game = None
        self.worldBatch = pyglet.graphics.Batch()
        self.guiCamera = CenteredCamera(self)
        self.guiBatch = pyglet.graphics.Batch()
        self.updateFonct = []
        self.terrain:pyglet.sprite.Sprite = None



    def on_close(self):
        pyglet.app.exit()

    def AddTerrain(self,terrainImg):
        self.terrain = pyglet.sprite.Sprite(terrainImg,-self.width,-self.height)
        self.terrain.scale = self.terrain.scale * 5

    def Update(self, dt):
        self.OnDraw(dt)

        if self.game is not None and self.game.selectedTarget is not None:
            self.worldCamera.position = self.game.selectedTarget.GetLocation()[0] + 70, self.game.selectedTarget.GetLocation()[1]
            if self.worldCamera.zoom < self.worldCamera.max_zoom:
                self.worldCamera.zoom += .2

        for i in range(len(self.updateFonct)):
            self.updateFonct[i](dt)

    def AddToUpdate(self, f):
        self.updateFonct.append(f)

    def OnDraw(self, dt):
        self.clear()


        with self.worldCamera:
            self.terrain.draw()
            self.worldBatch.draw()
        # quand on draw avec le gui les element ne bouge pas avec l'offset de la cam
        with self.guiCamera:
            self.guiBatch.draw()


screen = None



def CreateWindow(updateMain, startGame,terrainImg=""):
    global screen
    global game
    screen = MyWindow(WIDTH, HEIGHT, "HumanSI", fullscreen=FULLSCREEN)
    screen.AddToUpdate(updateMain)
    if terrainImg != "":
        screen.AddTerrain(terrainImg)
    game = startGame(screen)
    pyglet.clock.schedule_interval(screen.Update, 1 / 120)
    return screen, game


def StartWindow():
    pyglet.app.run()
