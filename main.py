from pyglet import *
from pyglet.window import *
from Game import *
import pyglet
from Utilities import *



mouse_pos = 0, 0

main_batch = pyglet.graphics.Batch()

temp=[]


keyPress = {
    "Z": False,
    "Q": False,
    "S": False,
    "D": False
}


@game.window.event
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
            game.descLabel.draw()


def draw_square(x, y, size, color=(255, 255, 255, 0), batch=game.batch):
    # Créer l'image
    ball_image = pyglet.image.load(Directories.SpritesDir + "Civilisations/Yellow/BuildingsYellow/HDV/HdvD1.png")
    ball = pyglet.sprite.Sprite(ball_image, x=x, y=y, batch=batch)
    temp.append(ball)


@game.window.event
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


@game.window.event
def on_mouse_motion(x, y, dx, dy):
    game.mouse_pos = x, y

@game.window.event
def on_key_release(symbol, modifiers):
    if symbol == pyglet.window.key.Z:
        keyPress["Z"] = False
    if symbol == pyglet.window.key.Q:
        keyPress["Q"] = False
    if symbol == pyglet.window.key.S:
        keyPress["S"] = False
    if symbol == pyglet.window.key.D:
        keyPress["D"] = False


@game.window.event
def on_mouse_press(x, y, button, modifiers):
    print(button)
    if button == 1:  # clic gauche
        game.SpawnUnitBaseByIndex()
        print("{0} pressed at: {1},{2}.".format(button, x, y))
    if button == 2:  # Clic molette
        pass
    if button == 4:  # clic droit
        offsetPos = game.GetMouseOffset()
        closestObject = game.GetClosestObjectToLocation(offsetPos, 40)
        # L'update du panneau de desc peut supporter les valuer None c'est pas un probleme
        print(closestObject)
        game.UpdateDescPanel(closestObject)


@game.window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    game.worldCamera.zoom += scroll_y


def update(dt):
    if not game.GAME_RUNNING:
        return

    if keyPress["Z"]:
        game.worldCamera.move(0, 2)
    if keyPress["S"]:
        game.worldCamera.move(0, -2)
    if keyPress["Q"]:
        game.worldCamera.move(-2, 0)
    if keyPress["D"]:
        game.worldCamera.move(2, 0)

    #print(f"{dt} seconds since last callback")

    for i in range(len(temp)):
        temp[i].x += dt * 10

    game.SuperUpdate()


"""for i in range(300):

    draw_square(i*20, 5+i, 10,main_batch)
print(temp)"""
clock.schedule_interval(update, 1/40)
print(pyglet.__version__)

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