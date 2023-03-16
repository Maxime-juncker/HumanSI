# A delete plus tard juste jsp pk mais pygame veut pas marcher donc je fais des test ici


import pygame
pygame.init()

#Creation de la fenetre de l'app
pygame.display.set_caption("HumainSI")
display = pygame.display.set_mode((1080, 720))

background = pygame.image.load("Assets/download.jpg")

GAME_RUNNING = True


class Test(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Assets/download.jpg")
        self.rect = self.image.get_rect()


class Game:
    def __init__(self):
        self.test = Test()

game = Game()

#Boucle d'update
while GAME_RUNNING:

    display.blit(game.test.image, game.test.rect)

    #Update le screen
    pygame.display.flip()

    #Si on ferme la fenetre
    for event in pygame.event.get():
        #l'événement de fermeture de la window
        if event.type == pygame.QUIT:
            GAME_RUNNING = False
            pygame.quit()
            print("Exiting...")

