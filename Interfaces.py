from Utilities import *
import pygame
import AI

class DescriptionPanel(pygame.sprite.Sprite, AI.BasicObject):
    def __init__(self, size, pos):

        super().__init__()
        
        self.image = pygame.image.load(Directories.SpritesDir +"Interfaces/descriptionPanel.png").convert_alpha()
        self.rect = self.image.get_rect()
        # create a 2x bigger image than self.image
        self.image = pygame.transform.scale(self.image, (size*self.image.get_size()[0] \
                                                        , size*self.image.get_size()[1]))
        self.pos = pos

        # debugSuccessMsg("Unit Spawned --> " + self.name)