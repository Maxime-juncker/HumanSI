import pygame


class Test(pygame.sprite.Sprite):



    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Assets/Pop1c.png")
        self.rect = self.image.get_rect()
        self.speed = 1
        self.moveTimer = 30


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


class Game:

    def __init__(self):
        # Creation de la fenetre de l'app

        pygame.init()

        pygame.display.set_caption("HumainSI")
        self.display = pygame.display.set_mode((1080, 720))

        self.background = pygame.image.load("Assets/download.jpg")

        self.GAME_RUNNING = True
        self.test2 = Test()
        self.test = Test()
