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
    "Z": False,
    "Q": False,
    "S": False,
    "D": False
}

def update(dt):
    if game is not None and not game.GAME_RUNNING:
        return

    if keyPress["Z"]:
        game.worldCamera.move(0, 2)
    if keyPress["S"]:
        game.worldCamera.move(0, -2)
    if keyPress["Q"]:
        game.worldCamera.move(-2, 0)
    if keyPress["D"]:
        game.worldCamera.move(2, 0)

    if game is not None:
        game.SuperUpdate()

temp, game = CreateWindow(update,StartGame)


@temp.event
def on_key_press(symbol, modifiers):
    if MAIN_DEBUG:
        debugSuccessMsg(str(symbol) + " | " + str(modifiers))

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


@temp.event
def on_mouse_motion(x, y, dx, dy):
    game.mouse_pos = x, y


@temp.event
def on_key_release(symbol, modifiers):
    if MAIN_DEBUG:
        debugSuccessMsg(str(symbol) + " | " + str(modifiers))

    if symbol == pyglet.window.key.Z:
        keyPress["Z"] = False
    if symbol == pyglet.window.key.Q:
        keyPress["Q"] = False
    if symbol == pyglet.window.key.S:
        keyPress["S"] = False
    if symbol == pyglet.window.key.D:
        keyPress["D"] = False


@temp.event
def on_mouse_press(x, y, button, modifiers):
    if MAIN_DEBUG:
        debugWarningMsg(str(button) + " | " + str(modifiers))

    if button == 1:  # clic gauche
        game.SpawnUnitBaseByIndex()
    if button == 2:  # Clic molette
        pass
    if button == 4:  # clic droit
        offsetPos = game.GetMouseOffset()
        closestObject = game.GetClosestObjectToLocation(offsetPos, 40)
        # L'update du panneau de desc peut supporter les valuer None c'est pas un probleme
        if MAIN_DEBUG:
            debugSuccessMsg(closestObject)
        game.UpdateDescPanel(closestObject)


@temp.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    game.worldCamera.zoom += scroll_y




StartWindow()