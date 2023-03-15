import random
import pygame
import Game

class BasicObject():
    name = ""


class Test(pygame.sprite.Sprite, BasicObject):

    def Update(self):
        self.display.blit(self.image, self.rect)

    def __init__(self, _display):
        super().__init__()
        self.image = pygame.image.load("Assets/Pop1c.png")
        self.rect = self.image.get_rect()
        self.speed = 1
        self.moveTimer = 100
        self.display = _display
        self.name = str(random.randint(0, 1000))

        self.rect = pygame.mouse.get_pos()

        Game.game.visibleSprite[self.name] = self

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

        self.moveTimer -= 1

        if self.moveTimer > 0:
            return
        else:
            self.moveTimer = 10

        if abs(self.rect.y - coord[1]) < 5 and abs(self.rect.x - coord[0]) < 5:
            return

        if self.rect.x <= coord[0]:
            self.MoveRight(1)
        elif self.rect.x >= coord[0]:
            self.MoveRight(-1)
        if self.rect.y <= coord[1]:
            self.MoveUp(1)
        elif self.rect.y >= coord[1]:
            self.MoveUp(-1)
