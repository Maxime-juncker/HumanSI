import random

import Game
import pygame
from Utilities import *

currentResources = {
    "wood": 0,
    "stone": 0,
}


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


class Unit(pygame.sprite.Sprite, BasicObject):

    def __init__(self, _display, spriteSheet, preset, civilisation, pos, group):

        super().__init__(group)

        self.unitPreset = preset

        # Animations
        self.sprites = spriteSheet
        self.currentSprite = 0.0
        self.image = pygame.image.load(Directories.SpritesDir + preset["spritesPath"] + "/" + spriteSheet[0])
        self.animTimer = 5

        self.rect = self.image.get_rect()
        self.speed = int(self.unitPreset["speed"])
        self.moveTimer = int(self.unitPreset["moveTimer"])
        self.maxMoveTimer = int(self.unitPreset["moveTimer"])
        self.display = _display
        self.id = str(random.randint(0, 99999))
        self.name = self.unitPreset["name"] + str(self.id)
        self.lifeSpawn = int(self.unitPreset["lifeSpan"])

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
            Game.game.visibleSprite.pop(self.name)
            self.kill()

    def StateMachine(self):

        if self.civilisation is not None:
            if self.civilisation.inWar:
                self.SetNewState(UnitState.IN_WAR)

        if self.state == UnitState.MOVING:
            self.MoveTo(self.currentDestination)
        if self.state == UnitState.IDLE:
            self.currentDestination = SeekNewPos(self.rect, 200)
            self.SetNewState(UnitState.MOVING)
        if self.state == UnitState.IN_WAR:
            self.currentDestination = self.civilisation.inWarAgainst.cityHallPos
            self.MoveTo(self.currentDestination)

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

        print(preset["popName"])

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
        self.spawnRate = int(self.civilisationPreset["fertility"])
        self.houseSpawnRate = int(self.civilisationPreset["spawnRate"])
        self.religion = self.civilisationPreset["religion"]
        self.aggressivity = self.civilisationPreset["aggressivity"]

        self.inWar = False
        self.inWarAgainst = None
        self.currentPopulation = 0
        self.currentZoneSize = 100
        self.wonderAlreadyExist = False

        Game.game.visibleSprite[self.name] = self
        Game.game.civilisationSpawned[self.name] = self

        debugSuccessMsg("Civilisation Spawned --> " + self.name)

    def Tick(self):
        self.SpawnNewPopulation()
        self.DeclareWarOnCivilisation()

    def SpawnNewPopulation(self):
        Game.game.SpawnUnit(self.populationPreset, self.cityHallPos, self)
        self.currentPopulation += 1

        if self.currentPopulation % 5 == 0:
            self.SpawnNewHouse()

        if self.currentPopulation % 50 == 0:
            self.SpawnWonder()

    def SpawnNewHouse(self):
        Game.game.SpawnUnit(self.housePreset, SeekNewPos(self.cityHallPos, self.currentZoneSize), self)
        self.currentZoneSize += 20

    def SpawnWonder(self):
        if self.wonderAlreadyExist or self.wonderPreset is None:
            return

        self.currentZoneSize += 100
        self.spawnRate * 0.1
        self.wonderAlreadyExist = True

        Game.game.SpawnUnit(self.wonderPreset, SeekNewPos(self.cityHallPos, self.currentZoneSize), self)

    def DeclareWarOnCivilisation(self):
        if self.inWar:
            return

        if len(self.CheckNeighnorsCivilisation()) >= 1:
            # on prend une cible au pif dans les voisins
            temp = random.choice(list(self.CheckNeighnorsCivilisation()))
            target = Game.game.civilisationSpawned[temp]

            if self.CanDeclareWar(target):
                self.inWar = True
                self.inWarAgainst = target
                debugFailMsg(self.name + "declare la guerre a " + target.name)

    def CanDeclareWar(self, civilisation):
        if self.civilisationPreset["aggressivity"] == 0:
            return False

        if self.civilisationPreset["religion"] != civilisation.civilisationPreset["religion"] and \
                int(self.civilisationPreset["aggressivity"]) >= 25:
            return True
        return True

        # return random.randint(0, self.civilisationPreset["aggressivity"]) > 80

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

            if distance <= int(self.civilisationPreset["aggroDistance"]):
                result[civilisation] = distance
        result = {key: val for key, val in sorted(result.items(), key=lambda ele: ele[0])}
        return result
