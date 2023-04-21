from pyglet import *
from pyglet.window import *
from Game import *
import pyglet
from Utilities import *
from Settings import *
from Display import *

if MAIN_DEBUG:
    debugWarningMsg("Version de pyglet: " + str(pyglet.__version__))

"""@game.window.event
def on_draw():
    if not game.GAME_RUNNING:
        return

    game.window.clear()
    with game.worldCamera:
        game.batch.draw()
    # quand on draw avec la gui les element ne bouge pas avec l'offset de la cam
    with game.GuiCamera:
        game.spawnLabel.draw()
        game.fps_display.draw()
        game.descriptionPanel.image.draw()
        if game.descLabel.text != "":
            game.descLabel.draw()"""

keyPress = {
    "Forward": False,
    "Backward": False,
    "Left": False,
    "Right": False
}


def update(dt):
    if game is not None and not game.GAME_RUNNING:
        return

    if keyPress["Forward"]:
        screen.worldCamera.move(0, 2)
    if keyPress["Backward"]:
        screen.worldCamera.move(0, -2)
    if keyPress["Left"]:
        screen.worldCamera.move(-2, 0)
    if keyPress["Right"]:
        screen.worldCamera.move(2, 0)

    if game is not None:
        game.SuperUpdate()

game:Game.Game = None
screen:MyWindow = None
screen, game = CreateWindow(update, StartGame)


@screen.event
def on_key_press(symbol, modifiers):
    if MAIN_DEBUG:
        debugSuccessMsg(str(symbol) + " | " + str(modifiers))

    # =========== Mouvement ==================
    if game.selectedTarget is None:
        if symbol == pyglet.window.key.Z or symbol == pyglet.window.key.UP:
            keyPress["Forward"] = True
        if symbol == pyglet.window.key.Q or symbol == pyglet.window.key.LEFT:
            keyPress["Left"] = True
        if symbol == pyglet.window.key.S or symbol == pyglet.window.key.DOWN:
            keyPress["Backward"] = True
        if symbol == pyglet.window.key.D or symbol == pyglet.window.key.RIGHT:
            keyPress["Right"] = True
    # =========== Description Panel ==========
    if symbol == pyglet.window.key.F:
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
        game.UpdateFantomeSprite()


@screen.event
def on_mouse_motion(x, y, dx, dy):
    game.mouse_pos = x, y


@screen.event
def on_key_release(symbol, modifiers):
    if MAIN_DEBUG:
        debugSuccessMsg(str(symbol) + " | " + str(modifiers))

    if symbol == pyglet.window.key.Z or symbol == pyglet.window.key.UP:
        keyPress["Forward"] = False
    if symbol == pyglet.window.key.Q or symbol == pyglet.window.key.LEFT:
        keyPress["Left"] = False
    if symbol == pyglet.window.key.S or symbol == pyglet.window.key.DOWN:
        keyPress["Backward"] = False
    if symbol == pyglet.window.key.D or symbol == pyglet.window.key.RIGHT:
        keyPress["Right"] = False


@screen.event
def on_mouse_press(x, y, button, modifiers):
    if MAIN_DEBUG:
        debugWarningMsg(str(button) + " | " + str(modifiers))

    if button == 1:  # clic gauche
        game.SpawnUnitBaseByIndex()
        game.ToggleButtonAction()
        #game.togglebutton.CheckIfClicked(game.GetMouseOffset())
    if button == 2:  # Clic molette
        pass
    if button == 4:  # clic droit
        pass


@screen.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    screen.worldCamera.zoom += scroll_y


StartWindow()
