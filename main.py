from pyglet import *
from pyglet.window import Window
#from Game import *
import pyglet

window = Window(500, 500)

batch = pyglet.graphics.Batch()

keyPress = {
    "Z": False,
    "Q": False,
    "S": False,
    "D": False
}


@window.event
def on_draw():
    window.clear()

    # Draw your world scene using the world camera
    with world_camera:
        draw_square(10, 10, 10)
        batch.draw()

    # Can also be written as:
    # camera.begin()
    # batch.draw()
    # camera.end()

    # Draw your GUI elements with the GUI camera.
    """with gui_camera:
        label.draw()"""


def draw_square(x, y, size, color=(255, 255, 255, 0)):
    # Créer l'image
    img = image.create(size, size, image.SolidColorImagePattern(color))
    img.blit(x, y)


@window.event
def on_key_press(symbol, modifiers):
    # =========== Mouvement ==================
    if symbol == pyglet.window.key.Z:
        keyPress["Z"] = True
    if symbol == pyglet.window.key.Q:
        keyPress["Q"] = True
    if symbol == pyglet.window.key.S:
        keyPress["S"] = True
    if symbol == pyglet.window.key.D:
        keyPress["D"] = True
    # =========== Description Panel ==========
    """if symbol == pyglet.window.key.ESCAPE:
        game.UpdateDescPanel(None)
        game.spriteIndex = 0
        game.UpdateFantomeSprite()
    # =========== Selection =================
    if symbol == pyglet.window.key.A:
        if game.spriteIndex + 1 > len(game.spawnAbleUnit) - 1:
            game.spriteIndex = 0
        else:
            game.spriteIndex += 1
        game.UpdateFantomeSprite()

    if symbol == pyglet.window.key.E:
        if game.spriteIndex - 1 < 0:
            game.spriteIndex = len(game.spawnAbleUnit) - 1
        else:
            game.spriteIndex -= 1
        game.UpdateFantomeSprite()"""


@window.event
def on_key_release(symbol, modifiers):
    if symbol == pyglet.window.key.Z:
        keyPress["Z"] = False
    if symbol == pyglet.window.key.Q:
        keyPress["Q"] = False
    if symbol == pyglet.window.key.S:
        keyPress["S"] = False
    if symbol == pyglet.window.key.D:
        keyPress["D"] = False


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == 1:  # clic gauche
        # game.SpawnUnitBaseByIndex()
        print("{0} pressed at: {1},{2}.".format(button, x, y))
    if button == 2:  # Clic molette
        world_camera.zoom += 1
    if button == 3:  # clic droit
        pass
        """offsetPos = game.cameraGroup.offset - game.cameraGroup.internalOffset + pygame.mouse.get_pos()
        closestObject = game.GetClosestObjectToLocation(offsetPos, 45)
        # L'update du panneau de desc peut supporter les valuer None c'est pas un probleme
        game.UpdateDescPanel(closestObject)"""


@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    world_camera.zoom += scroll_y


def update(dt):
    if keyPress["Z"]:
        world_camera.move(0, 1)
    if keyPress["S"]:
        world_camera.move(0, -1)
    if keyPress["Q"]:
        world_camera.move(-1, 0)
    if keyPress["D"]:
        world_camera.move(1, 0)

    #game.SuperUpdate()
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
        self._zoom = max(min(1, self.max_zoom), self.min_zoom)

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


world_camera = CenteredCamera(window, scroll_speed=5, min_zoom=1, max_zoom=4)
gui_camera = CenteredCamera(window)

clock.schedule_interval(update, 1/60)

app.run()



#==================#==================#==================#==================#==================#==================#=====

"""import sys

import Game
from Utilities import *
from Game import *

# Boucle update


while game.GAME_RUNNING:

    # Si on ferme la fenetre
    for event in pygame.event.get():
        # l'événement de fermeture de la window
        if event.type == pygame.QUIT:
            game.GAME_RUNNING = False
            debugFailMsg("Exiting...")
            game.KillAllActors()
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            '''
            0 - left click
            1 - middle click
            2 - right click
            '''

            mouseButton = pygame.mouse.get_pressed()

            if mouseButton[0]:
                game.SpawnUnitBaseByIndex()

            if mouseButton[2]:
                offsetPos = game.cameraGroup.offset - game.cameraGroup.internalOffset + pygame.mouse.get_pos()
                closestObject = game.GetClosestObjectToLocation(offsetPos, 45)
                # L'update du panneau de desc peut supporter les valuer None c'est pas un probleme
                game.UpdateDescPanel(closestObject)

        if event.type == pygame.MOUSEWHEEL:

            if 1 < game.cameraGroup.zoomScale + event.y * 0.3 < 3.5:
                game.cameraGroup.zoomScale += event.y * 0.3

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                game.UpdateDescPanel(None)
                game.spriteIndex = 0
                game.UpdateFantomeSprite()

            if event.key == pygame.K_a:
                if game.spriteIndex + 1 > len(game.spawnAbleUnit) - 1:
                    game.spriteIndex = 0
                else:
                    game.spriteIndex += 1
                game.UpdateFantomeSprite()

            elif event.key == pygame.K_e:
                if game.spriteIndex - 1 < 0:
                    game.spriteIndex = len(game.spawnAbleUnit) - 1
                else:
                    game.spriteIndex -= 1
                game.UpdateFantomeSprite()

    game.SuperUpdate()
    # game.Tick()


"""