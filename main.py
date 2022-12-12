import AI 
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

SCREEN_WIDTH=1000
SCREEN_HIGHT=1000

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HIGHT))
DISPLAYSURF.fill(WHITE)



A1 = AI.AI_ACTOR()
A2 = AI.AI_ACTOR()



while True:     
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    A1.update()
    A2.move()

     
    DISPLAYSURF.fill(WHITE)
    
    A1.draw(DISPLAYSURF)
    A2.draw(DISPLAYSURF)
    pygame.display.update()
    
