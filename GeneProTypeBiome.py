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
class BiomeDead() :

    type = "Sol"
    hauteur = -1
    SpawnRessource = False
    SpawnPasiveLife = False
    SpawnAgressiveLife = False
    SpawnWater = False

class BiomeLife() :
    type = "Sol"
    hauteur = 3
    SpawnRessource = True
    SpawnPasiveLife = True
    SpawnAgressiveLife = True
    SpawnWater = True

#Les infos pour que tout soit au meme endroit
class InfoBiomePlaine(BiomeLife) :
    def __init__(self):
        super().__init__()

        self.hauteur = 2

class InfoBiomeForest(BiomeLife) :
    pass
    

class InfoBiomeMontagne(BiomeLife) :
    def __init__(self):
        super().__init__()
        
        self.hauteur = 5
    

class InforBiomeHauteMontagne(BiomeLife) :
    def __init__(self):
        super().__init__()
        self.hauteur = 8
        self.SpawnAgressiveLife = False
        self.SpawnWater = False

class InfoBiomePlage(BiomeLife) :
    def __init__(self):
        super().__init__()
        self.hauteur = 1
        self.SpawnAgressiveLife = False
        self.SpawnWater = False

class InfoBiomeDesert(BiomeLife) :
    def __init__(self):
        super().__init__()
        self.hauteur = 2
        self.SpawnRessource = False
        self.SpawnPasiveLife = False
        self.SpawnWater = False

class InfoBiomeSea(BiomeLife) :
    def __init__(self):
        super().__init__()
        self.hauteur = 0
        self.SpawnAgressiveLife = False
        self.SpawnWater = False

class InfoBiomeDeepSea(BiomeLife) :
    def __init__(self):
        super().__init__()
        self.hauteur = -1
        self.SpawnRessource = False
        self.SpawnPasiveLife = False
        self.SpawnAgressiveLife = False
        self.SpawnWater = False


#la génération "materielle" des biomes


class GeneBiomePlaine(InfoBiomePlaine) :
    None