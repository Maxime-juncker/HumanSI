import proceduraleGeneration
import main
import random
"""
Liste des biome : ( h = hauteur)
Plaine h=2
Foret h=3
Montagne h=5
Haute-Montagne h=8
Plage h=1
Desert h=2
mer h=0
mer profonde h=-1
"""
#Class de base pour tout centraliser
class Biome() :

    type = "Sol"


#Les infos pour que tout soit au meme endroit
class InfoBiomePlaine(Biome) :

    hauteur = 2
    SpawnRessource = True
    SpawnPasiveLife = True
    SpawnAgressiveLife = False
    SpawnWater = True

class InfoBiomeForest(Biome) :

    hauteur = 3
    SpawnRessource = True
    SpawnPasiveLife = True
    SpawnAgressiveLife = True
    SpawnWater = True

class InfoBiomeMontagne(Biome) :

    hauteur = 5
    SpawnRessource = True
    SpawnPasiveLife = True
    SpawnAgressiveLife = True
    SpawnWater = True

class InforBiomeHauteMontagne(Biome) :

    hauteur = 8
    SpawnRessource = True
    SpawnPasiveLife = True
    SpawnAgressiveLife = False
    SpawnWater = False

class InfoBiomePlage(Biome) :

    hauteur = 1
    SpawnRessource = True
    SpawnPasiveLife = True
    SpawnAgressiveLife = False
    SpawnWater = False

class InfoBiomeDesert(Biome) :

    hauteur = 2
    SpawnRessource = False
    SpawnPasiveLife = False
    SpawnAgressiveLife = True
    SpawnWater = False

class InfoBiomeSea(Biome) :

    hauteur = 0
    SpawnRessource = True
    SpawnPasiveLife = True
    SpawnAgressiveLife = False
    SpawnWater = False

class InfoBiomeDeepSea(Biome) :

    hauteur = -1
    SpawnRessource = False
    SpawnPasiveLife = False
    SpawnAgressiveLife = False
    SpawnWater = False


#la génération "materielle" des biomes


class GeneBiomePlaine(InfoBiomePlaine) :
    None