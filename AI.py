import pygame
import random
import sys
from pygame.locals import *

FPS = pygame.time.Clock()
FPS.tick(60)

# les couleurs de BASEEEEEE
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH=400

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,600))
DISPLAYSURF.fill(WHITE)


# /!\  SPRITE PATH ATTENTION SI UN TRUC NE S'AFFICHE PAS C'EST probablement a cause de ça 
AI_PATH="TKT"



class AI_ACTOR(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("TKT.png")
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),0) 

    def draw(self, surface):
        surface.blit(self.image, self.rect) 


A1=AI_ACTOR()

while True:     
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
   # A1.move()
     
    DISPLAYSURF.fill(WHITE)
    A1.draw(DISPLAYSURF)
         
    pygame.display.update()
    
