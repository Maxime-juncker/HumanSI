import pyglet

from Utilities import *
import pygame
import AI
import ptext


class Panel(pygame.sprite.Sprite, AI.BasicObject):

    def __init__(self, pos):
        super().__init__()

        self.x, self.y = pos[0], pos[1]
        img = pyglet.image.load(Directories.SpritesDir + "Interfaces/descriptionPanel.png")
        self.image = pyglet.sprite.Sprite(img, x=self.x, y=self.y)
        self.image.update(self.x,self.y,scale_x=self.image.scale_x*0.8,scale_y=self.image.scale_y*0.8)

        self.HidePanel()  # on cache instant le pannel si jamais faut pas override la funct

    def ShowPanel(self):
        pass

    def HidePanel(self):
        pass

    def Update(self):
        pass


class DescriptionPanel(Panel):
    def __init__(self, pos):
        super().__init__(pos)
        self.statsToShow = None

    def ShowPanel(self, object):
        self.image.visible = True
        infos = object.GetInfos()
        result = ""
        for info in infos:
            space = 300 - len(info+" : " + str(infos[info]))
            print(space)
            result += info+" : " + str(infos[info]) + " " * space


        print(result)
        self.statsToShow = result

    def GetInfos(self):
        if self.statsToShow is not None:
            return self.statsToShow


        #self.image.set_alpha(255)

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
