import pygame
import random
import sys
import time
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
SCREEN_HIGHT=600

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HIGHT))
DISPLAYSURF.fill(WHITE)


# /!\  SPRITE PATH ATTENTION SI UN TRUC NE S'AFFICHE PAS C'EST probablement a cause de ça 
AI_PATH="S_Test.png"



class AI_ACTOR(pygame.sprite.Sprite):

    speed = 1

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("S_Test.png")
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),0)
        

    def update(self):
        

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -1)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,1)
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-1, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(1, 0)


    def move(self):
        self.rect.move_ip(0,10)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)


    def draw(self, surface):
        surface.blit(self.image, self.rect) 


def FindRandomPointAtDistance(distance:float):
    randomY = random.randrange(0, distance)
    randomX = random.randrange(0, distance)

    return (randomX, randomY)
    