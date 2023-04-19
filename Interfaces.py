import pyglet
from Utilities import *
import AI


class Panel(AI.BasicObject):

    def __init__(self, pos,scale,batch):
        super().__init__()

        self.x, self.y = pos[0], pos[1]
        img = pyglet.image.load(Directories.SpritesDir + "Interfaces/descriptionPanel.png")
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2
        self.image = pyglet.sprite.Sprite(img, x=self.x, y=self.y,batch=batch)
        self.image.update(self.x,self.y,scale=self.image.scale*scale)


        self.HidePanel()  # on cache instant le pannel si jamais faut pas override la funct

    def ShowPanel(self):
        pass

    def HidePanel(self):
        pass

    def Update(self):
        pass


class DescriptionPanel(Panel):
    def __init__(self, pos, scale,batch):
        super().__init__(pos,scale,batch)
        self.statsToShow = None

    def ShowPanel(self, object):
        self.image.visible = True
        infos = object.GetInfos()
        result = ""
        for info in infos:
            result += info + " : " + str(infos[info]) + "                                        "
        self.statsToShow = result

    def GetInfos(self):
        if self.statsToShow is not None:
            return self.statsToShow

    def HidePanel(self):
        self.image.visible = False
        self.statsToShow = None

    def Update(self):
        if self.statsToShow is None:  # si le panel est cacher c'est con de l'update pour rien
            return None

        text = []
        for info in self.statsToShow:
            text.append("{} : {}".format(info, self.statsToShow[info]))

        return text
