import random
import Game
import time
import threading
from Utilities import *
import pyglet
from pyglet import *
from pyglet.window import *

class UnitState:
    NONE = -1
    IDLE = 0
    MOVING = 1
    DED = 2


class BasicObject:
    name = ""
    id = 0
    category = None

    def Update(self,dt):
        pass

    def GetSprite(self):
        return None

    def GetInfos(self):
        return None

    def GetLocation(self):
        return (0, 0)

    def GetCivilisation(self):
        return None

    def Damage(self, amount):
        pass

    def Destroy(self):
        del self


class Unit():

    def __init__(self, preset, civilisation, size, pos, batch): # le batch doit etre different entre les buildings et les unit pour le truc de z clipping

        super().__init__()

        self.unitPreset = preset

        self.x = pos[0]
        self.y = pos[1]

        print(civilisation, size, pos, batch)
        print(preset)

        debugSuccessMsg(Game.game.sprites[preset["name"]])
        self.image = pyglet.sprite.Sprite(Game.game.sprites[preset["name"]], x=self.x, y=self.y, batch=batch)

        self.speed = int(self.unitPreset["speed"])
        self.moveTimer = int(self.unitPreset["moveTimer"])
        self.maxMoveTimer = int(self.unitPreset["moveTimer"])
        self.id = str(random.randint(0, 99999))
        self.name = self.unitPreset["name"] + str(self.id)
        self.lifeSpawn = int(self.unitPreset["lifeSpan"])
        self.health = int(self.unitPreset["health"])
        self.category = self.unitPreset["category"]
        self.currentTarget = None

        self.civilisation = civilisation

        self.canAttack = True

        Game.game.visibleSprite[self.name] = self

        self.currentDestination = SeekNewPos(self.GetLocation(), 30)
        self.state = UnitState.IDLE

        # debugSuccessMsg("Unit Spawned --> " + self.name)
        if float(self.unitPreset["updateWeight"]) > -1:
            clock.schedule_interval(self.Update, float(self.unitPreset["updateWeight"]))

    def Update(self,dt):
        self.StateMachine()
        self.UpdateLifeSpan()
        # self.DoAnimation()
        self.image.update(self.x,self.y)

    def GetSprite(self):
        return self.image

    def GetCivilisation(self):
        return self.civilisation

    def GetInfos(self):
        if "CityHall" in self.name:
            return self.civilisation.GetInfos()

        result = {}
        result["id"] = self.name
        result["pv"] = self.health
        result["vitesse"] = self.unitPreset["speed"]
        result["dégats"] = self.unitPreset["damage"]
        result["vitesse atk"] = self.unitPreset["attackSpeed"]
        if self.civilisation != None:
            result["civilisation"] = self.civilisation.name
        result["coût objet"] = self.unitPreset["unitCost"]
        result["est spawnable"] = self.unitPreset["isSpawnable"]
        result["updateWeight"] = self.unitPreset["updateWeight"]
        if self.currentTarget != None:
            result["target"] = self.currentTarget.name
        return result

    def GetLocation(self):
        return self.x, self.y

    # ============ A FAIRE =============================================================================================
    def Destroy(self):
        pass
        debugWarningMsg("Trouve un moyen pour enlever un sprite du batch (ligne 129 AI.py)")

        """self.SetNewState(UnitState.DED)
        
        if Game.game.selectedTarget == self:
            Game.game.UpdateDescPanel(None)
            
        if "building" in self.unitPreset["category"]:
            Game.game.SpawnUnit(LoadPreset(Directories.PresetDir + "Presets.csv", "Ruines"), self.rect.bottomright, None)
            
            
        if self.civilisation is not None:
            if self.unitPreset["category"] == "unit":
                self.civilisation.currentPopulation.pop(self.name)
            elif self.unitPreset["category"] == "building":
                self.civilisation.currentHousing.pop(self.name)
                
        if "CityHall" in self.name:
            self.civilisation.Destroy()
        
        Game.game.visibleSprite.pop(self.name)
        Game.game.cameraGroup.remove(self)
        self.kill()
        return super().Destroy()"""

    # ==================================================================================================================

    # ============ A FAIRE =============================================================================================

    def DoAnimation(self):
        pass
        """self.currentSprite += 0.05

        if self.currentSprite >= len(self.sprites):
            self.currentSprite = 0
        self.image = pygame.image.load(
            Directories.SpritesDir + self.unitPreset["spritesPath"] + "/" + self.sprites[
                round(int(self.currentSprite))])"""

    # ==================================================================================================================

    def UpdateLifeSpan(self):
        if self.lifeSpawn < 0:  # Si le lifeSpan < 0 s'a veut dire que l'unit est imortelle
            return

        self.lifeSpawn -= 1
        if self.lifeSpawn > 0:
            return
        elif self.lifeSpawn == 0:
            self.Destroy()

    def StateMachine(self):

        # si y'a le temps faut deplacer ça dans les civilisations pour que ça soit pas appeler chaques frames
        # ==================A DEPLACER======================================================
        if self.civilisation is not None:
            if self.civilisation.inWar:
                self.CheckForNearbyEnemies()
                self.AttackNearbyEnemies()
        # =================================================================================

        if self.state == UnitState.MOVING:
            self.MoveTo(self.currentDestination)
        if self.state == UnitState.IDLE:
            self.currentDestination = SeekNewPos((self.x, self.y), 200)
            self.SetNewState(UnitState.MOVING)

    def AttackNearbyEnemies(self):
        if self.currentTarget == None:
            return
        if self.currentTarget.category == "building":
            reach = 40
        else:
            reach = 25

        # ==========================A FAIRE ============================================================================
        if GetDistanceFromVector(self.GetLocation(), self.currentTarget.GetLocation()) < reach:
            self.currentTarget.Damage(int(self.unitPreset["damage"]))
            time.sleep(float(self.unitPreset["attackSpeed"]))
        self.canAttack = True
        # ==============================================================================================================

    def Damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.Destroy()

        if Game.game.selectedTarget == self:
            Game.game.UpdateDescPanel(self.name)

    def CheckForNearbyEnemies(self):
        target = Game.game.GetClosestObjectToOtherObject(self, 50, self.name)
        if target is None and self.civilisation.inWarAgainst is not None:
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

        self.x += self.speed * dir

    def MoveUp(self, dir):
        '''
        fonct pour move un sprite
        dir = la direction (ex : dir = -1 donc vers la right)
                           (     dir = 1 donc vers la gauche)
        '''

        self.y += self.speed * dir

    def MoveTo(self, coord):

        if abs(self.y - coord[1]) < 5 and abs(self.x - coord[0]) < 5:
            self.SetNewState(UnitState.IDLE)
            return

        self.moveTimer -= 1

        if self.moveTimer > 0:
            return
        else:
            self.moveTimer = self.maxMoveTimer

        if self.x <= coord[0]:
            self.MoveRight(1)
        elif self.x >= coord[0]:
            self.MoveRight(-1)
        if self.y <= coord[1]:
            self.MoveUp(1)
        elif self.y >= coord[1]:
            self.MoveUp(-1)

        # self.image = pygame.transform.rotate(self.image, 90)


class Civilisation(BasicObject):

    def __init__(self, preset):
        super().__init__()

        self.civilisationPreset = preset

        self.populationPreset = LoadPreset(Directories.PresetDir + "Presets.csv", preset["popName"])
        self.housePreset = LoadPreset(Directories.PresetDir + "Presets.csv", preset["houseName"])
        cityHallPreset = LoadPreset(Directories.PresetDir + "Presets.csv", preset["cityHallName"])

        self.cityHallPos = Game.game.GetMouseOffset()
        debugWarningMsg("suppr ce msg si tout vas bien mais si le sprite \n"
                        "spawn pas au bon endroit c'est a cause de la ligne 298 dans AI.py :)")

        self.cityHall = Game.game.SpawnUnit(cityHallPreset, self.cityHallPos, self)
        self.wonderPreset = None

        if preset["wonderName"] != "none":
            self.wonderPreset = LoadPreset(Directories.PresetDir + "Presets.csv", self.civilisationPreset["wonderName"])

        self.id = random.randint(0, 9999)
        self.name = self.civilisationPreset["name"] + str(self.id)
        self.religion = self.civilisationPreset["religion"]
        self.aggressivity = int(self.civilisationPreset["aggressivity"])
        self.maxPop = int(self.civilisationPreset["maxBasePop"])
        self.category = "Civilisation"

        self.inWar = False
        self.inWarAgainst = None
        self.currentZoneSize = 100
        self.wonderAlreadyExist = False
        self.currentPopulation = {}
        self.currentHousing = {}
        self.ressources = 0
        self.chief = None
        self.isCivilisationAlived = True

        Game.game.civilisationSpawned[self.name] = self

        if float(self.civilisationPreset["updateWeight"]) > -1:
            clock.schedule_interval(self.Update, float(self.civilisationPreset["updateWeight"]))

        self.SpawnChief()
        self.currentHousing[self.cityHall.name] = self.cityHall
        debugSuccessMsg("Civilisation Spawned --> " + self.name)

    def Update(self, dt):
        debugSuccessMsg("updating")
        self.ressources += self.IncreaseRessources()
        self.SpawnNewPopulation()
        self.TryToDeclareWarOnCivilisation()

    def Destroy(self):
        if not self.isCivilisationAlived:
            return

        self.isCivilisationAlived = False
        for unit in self.currentPopulation.copy():
            self.currentPopulation[unit].Destroy()
        for building in self.currentHousing.copy():
            self.currentHousing[building].Destroy()

        for civilisation in Game.game.civilisationSpawned.copy():
            if Game.game.civilisationSpawned[civilisation].inWarAgainst == self:
                target = Game.game.civilisationSpawned[civilisation]
                target.MakePeace()
                for unit in target.currentPopulation:
                    target.currentPopulation[unit].currentTarget = None

        if self.inWar:
            self.MakePeace()
        Game.game.civilisationSpawned.pop(self.name)
        return super().Destroy()

    def IncreaseRessources(self):
        """
        Formule pour ajouter des ressources a la civilisation en fonction des bat, pop, et merveille
        chacun des preset peut etre modifier pour ajouter un multiplier + ou - grand
        (PS : vue que c'est des multiplicateur eviter de mettre des truc trop grand)
        
        Returns:
            int : les ressources suplémentaire
        """

        result = 1 + len(self.currentPopulation) + len(self.currentHousing)
        if self.wonderAlreadyExist:
            result += int(self.civilisationPreset["wonderRessourcesIncomes"])

        if Game.game.selectedTarget == self.cityHall:
            Game.game.UpdateDescPanel(self.cityHall.name)

        return result

    def GetSprite(self):
        return self.cityHall.image

    def GetCivilisation(self):
        return self

    def GetInfos(self):
        result = {}
        result["id"] = self.name
        result["health"] = self.cityHall.health
        result["religion"] = self.civilisationPreset["religion"]
        result["aggressiviter"] = self.civilisationPreset["aggressivity"]
        result["distance d'influance"] = self.currentZoneSize
        result["population"] = len(self.currentPopulation)
        result["max pop"] = self.maxPop
        result["maisons"] = len(self.currentHousing)
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
        return self.cityHallPos

    def SpawnChief(self):

        chiefPreset = LoadPreset(Directories.PresetDir + "Presets.csv", self.civilisationPreset["chiefName"])
        self.chief = Game.game.SpawnUnit(chiefPreset, self.cityHallPos, self)
        self.currentPopulation[self.chief.name] = self.chief

    def SpawnNewPopulation(self):
        """
        fonct pour générer une nouvelle pop / merveille / battiment en fonction des ressources de
        la civilisation (plus un truc est en haut plus il sera priorisé pour la construction)
        chaque unit a un prix qui peut etre mofif dans les presets 
        le nom c'est unitCost
        """

        if len(self.currentPopulation) < self.maxPop:
            if int(self.populationPreset["unitCost"]) <= self.ressources:
                unit = Game.game.SpawnUnit(self.populationPreset, self.cityHallPos, self)
                self.currentPopulation[unit.name] = unit
                self.ressources -= int(self.populationPreset["unitCost"])
                self.currentZoneSize += 5

        if self.wonderPreset is not None and int(self.wonderPreset["unitCost"]) <= self.ressources \
                and not self.wonderAlreadyExist:
            self.SpawnWonder()
        elif int(self.housePreset["unitCost"]) + len(self.currentPopulation) * 4 <= self.ressources:
            self.SpawnNewHouse()

        if Game.game.selectedTarget == self.cityHall:
            Game.game.UpdateDescPanel(self.cityHall.name)

    def Damage(self, amount):
        pass
        # self.cityHall.Damage(amount)

    def SpawnNewHouse(self):
        """
        fonct pour generer une nouvelle maison, elle augmente la zone d'influence
        et la pop max
        PS: le prix est + 4 * la pop sinon il constuise des tonne de maison et ça devient
        exponentielle
        """
        building = Game.game.SpawnUnit(self.housePreset, SeekNewPos(self.cityHallPos, self.currentZoneSize), self)
        self.ressources -= int(self.housePreset["unitCost"]) + len(self.currentPopulation) * 4
        self.currentZoneSize += 50
        self.currentHousing[building.name] = building
        self.maxPop += int(self.civilisationPreset["maxPopIncrease"])

    def SpawnWonder(self):
        if self.wonderAlreadyExist or self.wonderPreset is None:
            return
        self.ressources -= int(self.wonderPreset["unitCost"])
        self.currentZoneSize += 400
        self.wonderAlreadyExist = True

        Game.game.SpawnUnit(self.wonderPreset, SeekNewPos(self.cityHallPos, self.currentZoneSize), self)

    def TryToDeclareWarOnCivilisation(self):
        """
        fonct pour essayer de declarer la guerre au civilisation qui ce trouve dans
        la zone d'incluence de celle ci.
        """
        if self.inWar:
            return
        if len(self.CheckNeighnorsCivilisation()) > 0:
            # on prend une cible au pif dans les voisins
            temp = random.choice(list(self.CheckNeighnorsCivilisation()))
            target = Game.game.civilisationSpawned[temp]

            if self.CanDeclareWar(target):
                self.DeclareWar(target)

    def DeclareWar(self, target):
        self.inWar = True
        self.inWarAgainst = target
        debugFailMsg(self.name + "declare la guerre a " + target.name)

        if not target.inWar:  # si on fait pas ça, ça revien a aller frapper un enfant sans défence.
            target.DeclareWar(self)

        if Game.game.selectedTarget == self.cityHall:
            Game.game.UpdateDescPanel(self.cityHall.name)

    def MakePeace(self):
        self.inWar = False
        self.inWarAgainst = None

    def CanDeclareWar(self, civilisation):
        """
        La formule pour savoir si une civilisation declare la guerre a une autre
        Args:
            civilisation (civilisation): la civilisation target
        Returns:
            bool: oui ou non la civilisation entre en guerre
        """

        return True

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
            distance = GetDistanceFromVector(self.cityHallPos,Game.game.civilisationSpawned[civilisation].cityHallPos)

            if distance <=  1000000:#self.currentZoneSize:
                result[civilisation] = distance
        result = {key: val for key, val in sorted(result.items(), key=lambda ele: ele[0])}

        return result


class FantomeSprite(BasicObject):

    def __init__(self, preset, size, pos, batch): # le batch doit etre gros pour qui passe devant tout

        super().__init__()

        self.preset = preset

        self.x = pos[0]
        self.y = pos[1]

        self.currentSprite = 0.0
        scale = Clamp(size * random.random() + 0.4, 0.75, 1.1)
        self.image = Game.game.sprites[preset["name"]]
        self.image.anchor_x = self.image.width // 2
        self.image.anchor_y = self.image.height // 2
        self.image = pyglet.sprite.Sprite(Game.game.sprites[preset["name"]], pos[0], pos[1], batch=batch)

        #self.image.color[3] = 150 # pas sur mais tkt
        self.isAddingAlpha = True  # True = ça monte False = ça déscend

        #threading.Thread(target=self.Update, daemon=True).start()

    def Destroy(self):
        #Game.game.cameraGroup.remove(self)
        #self.kill()
        debugWarningMsg("Trouve un moyen pour enlever un sprite du batch (ligne 565 AI.py)")

        return super().Destroy()

    def Update(self):
        self.image = pyglet.sprite.Sprite(Game.game.sprites[self.preset["name"]], self.x, self.y, batch=Game.game.batch)

        """while True:
            if self.isAddingAlpha:
                self.AddAlpha()
            else:
                self.SubstractAlpha()
            time.sleep(0.1)"""

    def AddAlpha(self):
        self.image.color[3] += 6
        if self.image.get_alpha() > 150:
            self.isAddingAlpha = False

    def SubstractAlpha(self):
        self.image.color[3] -= 6
        if self.image.get_alpha() < 30:
            self.isAddingAlpha = True
