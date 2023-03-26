from enum import Enum
import random
import Game
from Utilities import *
from Game import *
import threading


class UnitState(Enum):
    NONE = -1
    IDLE = 0
    MOVING = 1


class BasicObject:
    name = ""
    id = 0

    def Update(self):
        pass


class Unit(pygame.sprite.Sprite, BasicObject):

    def __init__(self, _display, sprite, preset, pos, group):

        super().__init__(group)

        self.unitPreset = preset
        self.image = pygame.image.load(Directories.SpritesDir + preset["spritesPath"] + "/" + sprite)
        self.rect = self.image.get_rect()
        self.speed = int(self.unitPreset["speed"])
        self.moveTimer = int(self.unitPreset["moveTimer"])
        self.maxMoveTimer = int(self.unitPreset["moveTimer"])
        self.display = _display
        self.id = str(random.randint(0, 99999))
        self.name = self.unitPreset["name"] + str(self.id)
        self.lifeSpawn = int(self.unitPreset["lifeSpan"])

        self.rect.bottomright = pos

        Game.game.visibleSprite[self.name] = self

        self.currentDestination = SeekNewPos(self.rect, 30)
        self.state = UnitState.IDLE

        debugSuccessMsg("Unit Spawned --> " + self.name)

    def Update(self):
        self.StateMachine()
        self.UpdateLifeSpan()

    def UpdateLifeSpan(self):
        if self.lifeSpawn < 0:  # Si le lifeSpan < 0 s'a veut dire que l'unit est imortelle
            return

        self.lifeSpawn -= 1
        if self.lifeSpawn > 0:
            return
        elif self.lifeSpawn == 0:
            self.kill()

    def StateMachine(self):
        if self.state == UnitState.MOVING:
            self.MoveTo(self.currentDestination)
        if self.state == UnitState.IDLE:
            self.currentDestination = SeekNewPos(self.rect, 200)
            self.SetNewState(UnitState.MOVING)

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

        if not self.state == UnitState.MOVING:
            return

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


class Civilisation(BasicObject):

    def __init__(self, preset, popPreset):

        super().__init__()

        self.civilisationPreset = preset

        self.populationPreset = LoadPreset(Directories.PresetDir + "Presets.csv", preset["popName"])
        self.housePreset = LoadPreset(Directories.PresetDir + "Presets.csv", preset["houseName"])
        cityHallPreset = LoadPreset(Directories.PresetDir + "Presets.csv", self.civilisationPreset["cityHallName"])

        offsetPos = Game.game.cameraGroup.offset - Game.game.cameraGroup.internalOffset + pygame.mouse.get_pos()
        self.cityHallPos = offsetPos
        self.cityHall = Game.game.SpawnUnit(cityHallPreset, self.cityHallPos)

        self.id = random.randint(0, 9999)
        self.name = self.civilisationPreset["name"] + str(self.id)

        self.spawnRate = int(self.civilisationPreset["fertility"])
        self.houseSpawnRate = int(self.civilisationPreset["spawnRate"])

        self.religion = self.civilisationPreset["religion"]
        self.aggressivity = self.civilisationPreset["aggressivity"]
        self.inWar = False
        self.currentPopulation = 0

        self.timerActive = False

        self.currentZoneSize = 100
        debugSuccessMsg("Civilisation Spawned --> " + self.name)

        self.PopTimer = threading.Timer(self.spawnRate, self.SpawnNewPopulation)
        self.PopTimer.start()

        self.houseTimer = threading.Timer(self.houseSpawnRate, self.SpawnNewHouse)
        self.houseTimer.start()
    def Update(self):
        if not Game.game.GAME_RUNNING:
            self.cityHall.kill()

    def SpawnCityHall(self):
        Game.game.SpawnUnit()

    def SpawnNewPopulation(self):
        if not Game.game.GAME_RUNNING:
            return

        Game.game.SpawnUnit(self.populationPreset, SeekNewPos(self.cityHallPos, self.currentZoneSize))
        self.currentPopulation += 1

        if self.currentPopulation % 5 == 0:
            self.SpawnNewHouse()

        self.PopTimer = threading.Timer(self.spawnRate, self.SpawnNewPopulation)
        self.PopTimer.start()


    def SpawnNewHouse(self):
        self.houseTimer.cancel()

        if not Game.game.GAME_RUNNING:
            return

        self.currentZoneSize += 20
        Game.game.SpawnUnit(self.housePreset, SeekNewPos(self.cityHallPos, self.currentZoneSize))


