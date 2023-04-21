import pyglet
from Utilities import *
import AI
import Game


class Panel(AI.BasicObject):

    def __init__(self, imageName, pos, scale, batch):
        super().__init__()

        self.x, self.y = pos[0], pos[1]
        img = pyglet.image.load(Directories.SpritesDir + "Interfaces/" + imageName)
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2
        self.image = pyglet.sprite.Sprite(img, x=self.x, y=self.y, batch=batch)
        self.image.update(self.x, self.y, scale=self.image.scale * scale * 2)

        self.HidePanel()  # on cache instant le pannel si jamais faut pas override la funct

    def ShowPanel(self):
        pass

    def HidePanel(self):
        pass

    def Update(self):
        pass


class DescriptionPanel(Panel):
    def __init__(self, imageName="descriptionPanel.png", pos=(0, 0), scale=1, batch=None):
        super().__init__(imageName, pos, scale, batch)
        self.statsToShow = None

    def ShowPanel(self, object):
        pyglet.media.StaticSource(pyglet.media.load('Assets/SFX/OpenDescPanel.wav')).play()
        self.image.visible = True
        infos = object.GetInfos()
        result = ""
        for info in infos:
            result += info + " : " + str(infos[info]) + "                                        "

        result += "  |                                                           " \
                  "  |                                                            " \
                  "F pour quitter"
        self.statsToShow = result

    def GetInfos(self):
        if self.statsToShow is not None:
            return self.statsToShow

    def HidePanel(self):
        pyglet.media.StaticSource(pyglet.media.load('Assets/SFX/CloseDescPanel.wav')).play()

        self.image.visible = False
        self.statsToShow = None

    def Update(self):
        if self.statsToShow is None:  # si le panel est cacher c'est con de l'update pour rien
            return None

        text = []
        for info in self.statsToShow:
            text.append("{} : {}".format(info, self.statsToShow[info]))

        return text


class ToggleButton():
    def __init__(self, eventHandler, category, pos, scale, batch):

        self.eventHandler = eventHandler
        self.category = LoadPreset(Directories.PresetDir + "Presets.csv", category)["category"]

        self.depressed = pyglet.image.load('Assets/Graphics/Interfaces/Buttons/depressed.png')
        self.depressed.anchor_x = self.depressed.width // 2
        self.depressed.anchor_y = self.depressed.height // 2

        self.pressed = pyglet.image.load('Assets/Graphics/Interfaces/Buttons/pressed.png')
        self.x, self.y = pos[0], pos[1]
        self.pressed.anchor_x = self.pressed.width // 2
        self.pressed.anchor_y = self.pressed.height // 2

        self.hover = pyglet.image.load('Assets/Graphics/Interfaces/Buttons/hover.png')
        self.x, self.y = pos[0], pos[1]
        self.hover.anchor_x = self.hover.width // 2
        self.hover.anchor_y = self.hover.height // 2

        self.image = pyglet.sprite.Sprite(self.depressed, x=self.x, y=self.y, batch=batch)
        self.image.update(self.x, self.y, scale=self.image.scale * scale)

        self.iconImg = pyglet.image.load("Assets/Graphics/Misc/Categories/" + category + ".png")
        self.icon = pyglet.sprite.Sprite(self.iconImg, x=self.x, y=self.y, batch=batch)
        self.icon.update(self.x, self.y, scale=self.image.scale * scale)

        self.isToggle = False

    def CheckIfClicked(self, mousePos):
        if GetDistanceFromVector(
                (self.x + Game.game.screen.worldCamera.offset_x, self.y + Game.game.screen.worldCamera.offset_y),
                mousePos) <= 50:
            self.isToggle = not self.isToggle
            if self.isToggle:
                self.Enable()
            else:
                self.Disable()
            self.eventHandler(self)

        return self.isToggle

    def Disable(self):
        self.image = pyglet.sprite.Sprite(self.depressed, x=self.x, y=self.y, batch=self.image.batch)
        self.image.update(self.x, self.y, scale=self.image.scale)
        self.icon = pyglet.sprite.Sprite(self.iconImg, x=self.x, y=self.y, batch=self.icon.batch)
        self.icon.update(self.x, self.y, scale=self.image.scale)

    def Enable(self):
        self.image = pyglet.sprite.Sprite(self.pressed, x=self.x, y=self.y, batch=self.image.batch)
        self.image.update(self.x, self.y, scale=self.image.scale)
        self.icon = pyglet.sprite.Sprite(self.iconImg, x=self.x, y=self.y, batch=self.icon.batch)
        self.icon.update(self.x, self.y, scale=self.image.scale)
        Game.game.DisableAllButtons(self)
