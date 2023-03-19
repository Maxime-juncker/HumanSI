import random
import pygame
import Game
from enum import Enum
from Utilities import *




class UnitState(Enum):
    NONE = -1
    IDLE = 0
    MOVING = 1


class BasicObject():
    name = ""


class Unit(pygame.sprite.Sprite, BasicObject):

    def __init__(self, _display, sprite, preset=""):

        super().__init__()


        self.image = pygame.image.load(sprite)
        self.rect = self.image.get_rect()
        self.speed = int(preset["speed"])
        self.moveTimer = int(preset["moveTimer"])
        self.maxMoveTimer = int(preset["moveTimer"])
        self.display = _display
        self.name = preset["name"] + str(random.randint(0, 1000))

        Game.game.visibleSprite[self.name] = self

        self.rect.x = pygame.mouse.get_pos()[0]
        self.rect.y = pygame.mouse.get_pos()[1]

        self.currentDestination = SeekNewPos(self.rect, 100)
        self.state = UnitState.IDLE

    def Update(self):
        self.display.blit(self.image, self.rect)
        self.StateMachine()

    def StateMachine(self):
        if self.state == UnitState.MOVING:
            self.MoveTo(self.currentDestination)
        if self.state == UnitState.IDLE:
            self.currentDestination = SeekNewPos(self.rect, 100)
            self.SetNewState(UnitState.MOVING)

    def SetNewState(self, newState: UnitState):
        '''
        Fonct pour changer le state
        renvois True si le state est changer
                False si le state reste le même
        '''

        if (not newState == self.state):
            self.state = newState
            return False
        else:
            self.state = newState
            return True

    def MoveRight(self, dir):
        '''
        fonct pour move un sprite
        dir = la direction (ex : dir = 1 donc vers la right)
                           (     dir = -1 donc vers la gauche)
        '''

        self.rect.x += self.speed * dir

    def MoveUp(self, dir):
        '''
        fonct pour move un sprite
        dir = la direction (ex : dir = -1 donc vers la right)
                           (     dir = 1 donc vers la gauche)
        '''

        self.rect.y += self.speed * dir

    def MoveTo(self, coord):

        if not self.state == UnitState.MOVING:
            return

        if abs(self.rect.y - coord[1]) < 5 and abs(self.rect.x - coord[0]) < 5:
            self.SetNewState(UnitState.IDLE)
            return

        self.moveTimer -= 1

        if self.moveTimer > 0:
            return
        else:
            self.moveTimer = self.maxMoveTimer

        if self.rect.x <= coord[0]:
            self.MoveRight(1)
        elif self.rect.x >= coord[0]:
            self.MoveRight(-1)
        if self.rect.y <= coord[1]:
            self.MoveUp(1)
        elif self.rect.y >= coord[1]:
            self.MoveUp(-1)
