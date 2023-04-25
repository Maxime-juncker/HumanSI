WIDTH = 1920
HEIGHT = 1080
FULLSCREEN = True

MUTATION_FORCE = .25
MAX_CIVILISATION = 4
MAX_POP_PER_CIVILISATION = 25

"""
LES SETTINGS SUIVANTS SONT POUR LA GEN PROC DU TERRAIN:

si USE_RANDOM_TERRAIN est a False, il n'y aura pas de génération procédural et l'un des terrain
déjà générer sera utiliser (a utiliser si vous voulez lancer rapidement HumanSI ou si la génération prend trop de temps)
plus les settings de résolution seront élever plus la generation prendra du temp
"""

USE_RANDOM_TERRAIN = True

WIDTH_RESOLUTION = 200
HEIGHT_RESOLUTION = 200

# c'est une valeur arbitraire pour un peu de variation quand on pixelise le terrain c'est un peu trop
# smooth et ça fais un randu bizzard, les valeurs qui marche le mieux sont entre .1 et .2 apres c'est
# trop chaotique et en deussous c'est trop lisse
CHAOS_FORCE = .015

"""
LES SETTINGS SUIVANTS SONT POUR LE DEBUG:

lorsque l'une des option est activer le script qui a le même nom vas output des tonnes de print
qui informe de tout ce qu'il est en train de faire pas un bonne idée d'activer toutes les options du coup...
"""

GAME_DEBUG = False
MAIN_DEBUG = False
AI_DEBUG = False
INTERFACES_DEBUG = False
UTILITIES_DEBUG = False


