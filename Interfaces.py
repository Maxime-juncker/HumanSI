from Utilities import *
import pygame
import AI
import ptext

class Panel(pygame.sprite.Sprite, AI.BasicObject):

    def __init__(self, size, pos):
        super().__init__()
            
        self.image = pygame.image.load(Directories.SpritesDir +"Interfaces/descriptionPanel.png").convert_alpha()
        self.rect = self.image.get_rect()
        # create a 2x bigger image than self.image
        self.image = pygame.transform.scale(self.image, (size*self.image.get_size()[0] \
                                                            , size*self.image.get_size()[1]))
        self.pos = pos
        
        
        self.HidePanel() # on cache instant le pannel si jamais faut pas override la funct
        
    def ShowPanel(self):
        pass
    
    def HidePanel(self):
        pass
    
    def Update(self):
        pass
        
        
class DescriptionPanel(Panel):
    def __init__(self, size, pos):
        super().__init__(size, pos)
        self.statsToShow = None
        
    def ShowPanel(self, object):
        #print(object)
        self.statsToShow = object.GetPreset()
        self.image.set_alpha(255)
        
    
    def HidePanel(self):
        self.image.set_alpha(0)
        self.statsToShow = None
        
        
    def Update(self):
        if self.statsToShow is None: # si le panel est cacher c'est con de l'update pour rien
            return None
        
        text = []
        for info in self.statsToShow:
            text.append("{} : {}".format(info, self.statsToShow[info]))
            
        return text

        