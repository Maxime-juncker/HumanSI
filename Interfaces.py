import pyglet
from Utilities import *
import AI


class Panel(AI.BasicObject):

    def __init__(self, imageName, pos, scale, batch):
        super().__init__()

        self.x, self.y = pos[0], pos[1]
        img = pyglet.image.load(Directories.SpritesDir + "Interfaces/" + imageName)
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2
        self.image = pyglet.sprite.Sprite(img, x=self.x, y=self.y, batch=batch)
        self.image.update(self.x, self.y, scale=self.image.scale * scale)

        self.HidePanel()  # on cache instant le pannel si jamais faut pas override la funct

    def ShowPanel(self):
        pass

    def HidePanel(self):
        pass

    def Update(self):
        pass


class DescriptionPanel(Panel):
    def __init__(self, imageName="descriptionPanel.png", pos=(0,0), scale=1, batch=None):
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


class SpawnButton():
    def __init__(self,batch,pos):
        depressed = pyglet.resource.image('Assets/Graphics/Interfaces/Buttons/depressed.png')
        pressed = pyglet.resource.image('Assets/Graphics/Interfaces/Buttons/pressed.png')
        hover = pyglet.resource.image('Assets/Graphics/Interfaces/Buttons/hover.png')



