import random

import Game
import pygame
from Utilities import *


class UnitState:
    NONE = -1
    IDLE = 0
    MOVING = 1
    IN_WAR = 2


class BasicObject:
    name = ""
    id = 0

    def Tick(self):
        pass
    
    def GetSprite(self):
        return None
    
    def GetInfos(self):
        return None
    
    def GetLocation(self):
        return (0,0)
    
    def Destroy(self):
        del self
    


class Unit(pygame.sprite.Sprite, BasicObject):

    def __init__(self, _display, spriteSheet, preset, civilisation, size, pos, group):

        super().__init__(group)
        

        self.unitPreset = preset

        # Animations
        self.sprites = spriteSheet
        self.currentSprite = 0.0
        scale = Clamp(size * random.random() + 0.4, 0.75, 1.1)
        self.image = pygame.image.load(Directories.SpritesDir + preset["spritesPath"] + "/" + spriteSheet[random.randrange(0, len(spriteSheet))])
        self.image = pygame.transform.scale(self.image, (scale*self.image.get_size()[0] \
                                                        , scale*self.image.get_size()[1]))

        self.animTimer = 5

        self.rect = self.image.get_rect()
        self.speed = int(self.unitPreset["speed"])
        self.moveTimer = int(self.unitPreset["moveTimer"])
        self.maxMoveTimer = int(self.unitPreset["moveTimer"])
        self.display = _display
        self.id = str(random.randint(0, 99999))
        self.name = self.unitPreset["name"] + str(self.id)
        self.lifeSpawn = int(self.unitPreset["lifeSpan"])
        self.health = int(self.unitPreset["health"])
        self.currentTarget = None

        self.image = pygame.transform.rotate(self.image, random.randint(-6,6))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.bottomright = pos
        self.civilisation = civilisation

        Game.game.visibleSprite[self.name] = self

        self.currentDestination = SeekNewPos(self.rect, 30)
        self.state = UnitState.IDLE

        # debugSuccessMsg("Unit Spawned --> " + self.name)

    def Tick(self):
        self.StateMachine()
        self.UpdateLifeSpan()

        # self.DoAnimation()

    def GetSprite(self):
        return self.image

    def GetInfos(self):
        result = {}
        result["id"] = self.name
        result["pv"] = self.health
        result["vitesse"] = self.unitPreset["speed"]
        result["atk"] = self.unitPreset["attack"]
        result["vitesse atk"] = self.unitPreset["attackSpeed"]
        result["civilisation"] = self.unitPreset["civilisation"]
        result["coût objet"] = self.unitPreset["unitCost"]
        result["chemin des sprites"] = self.unitPreset["spritesPath"]
        result["est spawnable"] = self.unitPreset["isSpawnable"]
        result["updateWeight"] = self.unitPreset["updateWeight"]
        if self.currentTarget != None:
            result["target"] = self.currentTarget.name
        return result
    
    def GetLocation(self):
        return pygame.Vector2(self.rect.bottomright)

    def Destroy(self):
        Game.game.visibleSprite.pop(self.name)
        Game.game.cameraGroup.remove(self)
        self.kill()
        return super().Destroy()
    
    def DoAnimation(self):
        self.currentSprite += 0.05

        if self.currentSprite >= len(self.sprites):
            self.currentSprite = 0
        self.image = pygame.image.load(
            Directories.SpritesDir + self.unitPreset["spritesPath"] + "/" + self.sprites[
                round(int(self.currentSprite))])

    def UpdateLifeSpan(self):
        if self.lifeSpawn < 0:  # Si le lifeSpan < 0 s'a veut dire que l'unit est imortelle
            return

        self.lifeSpawn -= 1
        if self.lifeSpawn > 0:
            return
        elif self.lifeSpawn == 0:
            self.civilisation.currentPopulation -= 1
            Game.game.visibleSprite.pop(self.name)
            Game.game.cameraGroup.remove(self)
            self.Destroy()


    def StateMachine(self):
        
        #si y'a le temps faut deplacer ça dans les civilisations pour que ça soit pas appeler chaques frames
        #==================A DEPLACER======================================================
        if self.civilisation is not None:
            if self.civilisation.inWar:
                self.SetNewState(UnitState.IN_WAR)
        #=================================================================================
        
        if self.state == UnitState.MOVING:
            self.MoveTo(self.currentDestination)
        if self.state == UnitState.IDLE:
            self.currentDestination = SeekNewPos(self.rect, 200)
            self.SetNewState(UnitState.MOVING)
        if self.state == UnitState.IN_WAR:
            self.AttackNearbyEnemies()
            self.MoveTo(self.currentDestination)
            
    def AttackNearbyEnemies(self):
        target = Game.game.GetClosestObjectToLocation(self.GetLocation(), 50, self.name)
        if target == None:
            self.currentTarget = self.civilisation.inWarAgainst.cityHall
        else:
            self.currentTarget = Game.game.visibleSprite[target]
        self.currentDestination = self.currentTarget.GetLocation()

    def SetNewState(self, newState: UnitState):
        '''
        Fonct pour changer le state
        renvois True si le state est changer
                False si le state reste le même
        '''

        if not newState == self.state:
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

        # self.image = pygame.transform.rotate(self.image, 90)


class Civilisation(BasicObject):

    def __init__(self, preset):
        super().__init__()

        self.civilisationPreset = preset

        self.populationPreset = LoadPreset(Directories.PresetDir + "Presets.csv", preset["popName"])
        self.housePreset = LoadPreset(Directories.PresetDir + "Presets.csv", preset["houseName"])
        cityHallPreset = LoadPreset(Directories.PresetDir + "Presets.csv", preset["cityHallName"])

        offsetPos = Game.game.cameraGroup.offset - Game.game.cameraGroup.internalOffset + pygame.mouse.get_pos()
        self.cityHallPos = offsetPos
        self.cityHall = Game.game.SpawnUnit(cityHallPreset, self.cityHallPos, self)
        self.wonderPreset = None

        if preset["wonderName"] != "none":
            self.wonderPreset = LoadPreset(Directories.PresetDir + "Presets.csv", self.civilisationPreset["wonderName"])

        self.id = random.randint(0, 9999)
        self.name = self.civilisationPreset["name"] + str(self.id)
        self.religion = self.civilisationPreset["religion"]
        self.aggressivity = int(self.civilisationPreset["aggressivity"])
        self.maxPop = int(self.civilisationPreset["maxBasePop"])
        

        self.inWar = False
        self.inWarAgainst = None
        self.currentZoneSize = 100
        self.wonderAlreadyExist = False
        self.currentPopulation = 0
        self.currentHousing = 0
        self.ressources = 0
        
        Game.game.visibleSprite[self.name] = self
        Game.game.civilisationSpawned[self.name] = self

        debugSuccessMsg("Civilisation Spawned --> " + self.name)

    def Tick(self):
        
        self.ressources += self.IncreaseRessources()
    
        self.SpawnNewPopulation()
        self.DeclareWarOnCivilisation()
        
    def Destroy(self):
        return super().Destroy()
        
    def IncreaseRessources(self):
        """
        Formule pour ajouter des ressources a la civilisation en fonction des bat, pop, et merveille
        chacun des preset peut etre modifier pour ajouter un multiplier + ou - grand
        (PS : vue que c'est des multiplicateur eviter de mettre des truc trop grand)
        
        Returns:
            int : les ressources suplémentaire
        """
        result = 1 + self.currentPopulation + self.currentHousing * int(self.civilisationPreset["houseRessourcesMultiplier"])
        if self.wonderAlreadyExist:
            result += int(self.civilisationPreset["wonderRessourcesIncomes"])
            
        return result
        
    def GetSprite(self):
        return self.cityHall.image
    
    def GetInfos(self):
        result = {}
        result["nom"] = self.name
        result["religion"] = self.civilisationPreset["religion"]
        result["aggressiviter"] = self.civilisationPreset["aggressivity"]
        result["distance d'influance"] = self.currentZoneSize
        result["population"] = self.currentPopulation
        result["max pop"] = self.maxPop
        result["maisons"] = self.currentHousing
        result["ressources"] = self.ressources
        if self.wonderPreset != None:
            result["merveille"] = self.wonderPreset["name"]
            result["merveille construite ?"] = self.wonderAlreadyExist
            
        if self.inWar:
            result["en guerre contre"] = self.inWarAgainst.name
        else:
            result["civilisation"] = "en paix"
            
        result["chef"] = self.civilisationPreset["chiefName"]

        return result
    
    def GetLocation(self):
        return pygame.Vector2(self.cityHallPos)


    def SpawnNewPopulation(self):
        """
        fonct pour générer une nouvelle pop / merveille / battiment en fonction des ressources de
        la civilisation (plus un truc est en haut plus il sera priorisé pour la construction)
        chaque unit a un prix qui peut etre mofif dans les presets 
        le nom c'est unitCost
        """
        
        if self.currentPopulation < self.maxPop:    
            if int(self.populationPreset["unitCost"]) <= self.ressources:
                Game.game.SpawnUnit(self.populationPreset, self.cityHallPos, self)
                self.currentPopulation += 1
                self.ressources -= int(self.populationPreset["unitCost"])
            
        
        if self.wonderPreset is not None and int(self.wonderPreset["unitCost"]) <= self.ressources:
            self.SpawnWonder()
        elif int(self.housePreset["unitCost"]) <= self.ressources:
            self.SpawnNewHouse()
        

    def SpawnNewHouse(self):
        Game.game.SpawnUnit(self.housePreset, SeekNewPos(self.cityHallPos, self.currentZoneSize), self)
        self.ressources -= int(self.housePreset["unitCost"])
        self.currentZoneSize += 20
        self.currentHousing += 1
        self.maxPop += int(self.civilisationPreset["maxPopIncrease"])

    def SpawnWonder(self):
        if self.wonderAlreadyExist or self.wonderPreset is None:
            return
        self.ressources -= int(self.wonderPreset["unitCost"])
        self.currentZoneSize += 100
        self.spawnRate * 0.1
        self.wonderAlreadyExist = True

        Game.game.SpawnUnit(self.wonderPreset, SeekNewPos(self.cityHallPos, self.currentZoneSize), self)

    def DeclareWarOnCivilisation(self):
        if self.inWar:
            return
        if len(self.CheckNeighnorsCivilisation()) > 0:
            # on prend une cible au pif dans les voisins
            temp = random.choice(list(self.CheckNeighnorsCivilisation()))
            target = Game.game.civilisationSpawned[temp]

            if self.CanDeclareWar(target):
                self.inWar = True
                self.inWarAgainst = target
                debugFailMsg(self.name + "declare la guerre a " + target.name)

    def CanDeclareWar(self, civilisation):
        """
        La formule pour savoir si une civilisation declare la guerre a une autre
        Args:
            civilisation (civilisation): la civilisation target
        Returns:
            bool: oui ou non la civilisation entre en guerre
        """
        
        if int(self.civilisationPreset["aggressivity"]) == 0:
            return False
        if int(self.civilisationPreset["aggressivity"]) == 100:
            return True
        if self.civilisationPreset["religion"] != civilisation.civilisationPreset["religion"] and \
                int(self.civilisationPreset["aggressivity"]) >= 25:
            return True
        if random.randint(0, 100) <= int(self.civilisationPreset["aggressivity"]):
            return True
        return False
    
    def CheckNeighnorsCivilisation(self):

        """
        cette funct return la distance entre tous les voisins dans une liste triée
        """

        if len(Game.game.civilisationSpawned) == 1:
            return {}
        result = {}
        temp = Game.game.civilisationSpawned.copy()
        temp.pop(self.name)  # c'est un peu debile de calculer la distance avec soi même...

        for civilisation in temp:
            distance = self.cityHallPos.distance_to(Game.game.civilisationSpawned[civilisation].cityHallPos)

            if distance >= self.currentZoneSize:
                result[civilisation] = distance
        result = {key: val for key, val in sorted(result.items(), key=lambda ele: ele[0])}
        
        return result
    
class FantomeSprite(BasicObject, pygame.sprite.Sprite):

    def __init__(self, spriteSheet, preset, size, pos, group):

        super().__init__(group)
        
        self.image = pygame.image.load(Directories.SpritesDir + preset["spritesPath"] + "/" + spriteSheet[0])
        self.image = pygame.transform.scale(self.image, (size*self.image.get_size()[0] \
                                                        , size*self.image.get_size()[1]))

        self.rect = self.image.get_rect()
        self.rect.bottomright = pos
        self.image.set_alpha(150)
        self.isAddingAlpha = True # True = ça monte False = ça déscend

    def Destroy(self):
        Game.game.cameraGroup.remove(self)
        self.kill()
        return super().Destroy()
        
        
    def Tick(self):
        if self.isAddingAlpha:
            self.AddAlpha()
        else:
            self.SubstractAlpha()
    
    def AddAlpha(self):
        self.image.set_alpha(self.image.get_alpha()+1)
        if self.image.get_alpha() > 150:
            self.isAddingAlpha = False
            
    def SubstractAlpha(self):
        self.image.set_alpha(self.image.get_alpha()-1)
        if self.image.get_alpha() < 30:
            self.isAddingAlpha = True
            
        
        
    