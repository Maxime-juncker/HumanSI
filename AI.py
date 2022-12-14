# Je vais partir du principe que ceux qui lise ce code ne save rien des modules 
# que j'utilise, vue que je suis un chic type je vais mettre les liens vers 
# la documentation que j'utilise (ou au moins un truc en rapport genre stackOverflow)

# ༼ つ ◕_◕ ༽つ


import pygame # https://www.pygame.org
import random
import sys
import math
from pygame.locals import *

FPS = pygame.time.Clock() # https://www.geeksforgeeks.org/pygame-time/ (pour tout ce qui touche au FPS)
FPS.tick(1)

# les couleurs de BASEEEEEE
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH=1920
SCREEN_HIGHT=1080


# /!\  SPRITE PATH ATTENTION SI UN TRUC NE S'AFFICHE PAS C'EST probablement a cause de ça 
AI_PATH="S_Test.png"



class AI_ACTOR(pygame.sprite.Sprite): #https://learnpython.com/blog/custom-class-python/

    speed = 1
    suceed=False

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("S_Test.png")
        self.rect = self.image.get_rect()
        self.rect.center=(SCREEN_WIDTH / 2, SCREEN_HIGHT/2)
        

    def update(self):
        
        #https://stackoverflow.com/questions/35136091/pygame-key-getting-pressed (pour les touches)
        #https://stackoverflow.com/questions/16183265/how-to-move-sprite-in-pygame (pour bouger un sprite)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -1)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,1)
         
        if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-1, 0)
        if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(1, 0)


    def move(self, goal:tuple, suceed:bool):
        

        if suceed == False:

            if abs(self.rect.x - goal[0]) < 15 and abs(self.rect.y - goal[1]) < 15:
                suceed = True 
                print("YEAHH")

            if self.rect.x < goal[0]:
                self.rect.move_ip(1, 0)
            else:
                self.rect.move_ip(-1, 0)

            if self.rect.y < goal[1]:
                self.rect.move_ip(0, 1)
            else:
                self.rect.move_ip(0, -1)

            #print ("goal : " + str(self.rect.x) + " " + str(self.rect.y) + " | Pos : " + str(goal[0]) + " " + str(goal[1]) 
            #+ str(abs(self.rect.x - goal[0])) + " " + str((self.rect.y - goal[1])))

            return suceed

        

    
    def FindRandomPointAtDistance(self, distance:float):
        randomX = random.randint(self.rect.x - distance, self.rect.x + distance)
        randomY = random.randint(self.rect.y - distance, self.rect.y + distance)

        return (randomX, randomY)
        
        
    #https://www.pygame.org/docs/ref/draw.html
    def draw(self, surface):
        surface.blit(self.image, self.rect) 

