import pygame

pygame.init()
font = pygame.font.Font(None, 30)


def debug(info, y=10, x=10):

    """
    fonction pour print une info sur l'ecran (c'est quand même plus pratique qui print .__.)
    info : n'importe quoi
    x / y = les postion a partir du coin haut gauche ou le msg vas pop
            (perso je trouve que 10 et 10 c'est pas mal)
    """

    print(str(info))
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(display_surface, "Black", debug_rect)
    display_surface.blit(debug_surf, debug_rect)
