import AI 
import pygame
import random
import sys
from pygame.locals import *

FPS = pygame.time.Clock()
FPS.tick(30)


# les couleurs de BASEEEEEE
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH=1920
SCREEN_HIGHT=1080

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HIGHT))
DISPLAYSURF.fill(WHITE)

AI.SCREEN_HIGHT = SCREEN_HIGHT
AI.SCREEN_WIDTH = SCREEN_WIDTH


A1 = AI.AI_ACTOR()
A2 = AI.AI_ACTOR()
A3 = AI.AI_ACTOR()
A4 = AI.AI_ACTOR()


goal1 = A2.FindRandomPointAtDistance(50)
goal2 = A3.FindRandomPointAtDistance(50)
goal3 = A4.FindRandomPointAtDistance(50)


while True:     
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    A1.update()

    if A2.suceed == False:
        A2.suceed = A2.move(goal1, A2.suceed)
    else:
        goal1 = A2.FindRandomPointAtDistance(200)
        A2.suceed = False

        
    if A3.suceed == False:
        A3.suceed = A3.move(goal2, A3.suceed)
    else:
        goal2 = A3.FindRandomPointAtDistance(200)
        A3.suceed = False

        
    if A4.suceed == False:
        A4.suceed = A4.move(goal3, A4.suceed)
    else:
        goal3 = A4.FindRandomPointAtDistance(200)
        A4.suceed = False

        

     
    DISPLAYSURF.fill(WHITE)
    
    A1.draw(DISPLAYSURF)
    A2.draw(DISPLAYSURF)
    A3.draw(DISPLAYSURF)
    A4.draw(DISPLAYSURF)
    pygame.display.update()
    

