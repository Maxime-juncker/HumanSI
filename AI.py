# Je vais partir du principe que ceux qui lise ce code ne save rien des modules 
# que j'utilise, vue que je suis un chic type je vais mettre les liens vers 
# la documentation que j'utilise (ou au moins un truc en rapport genre stackOverflow)

# ༼ つ ◕_◕ ༽つ


import random
import math
import turtle
import Parameters
import os
import World



CURR_DIR = os.path.dirname(os.path.realpath(__file__))


if CURR_DIR == "":
    print(World.bcolors.FAIL + "FAIL : CURR_DIR est empty ce probleme ne doit pas etre mis de coter si le jeu crach c'est a cause DE CURR_DIR" + World.bcolors.ENDC)
else:
    print(World.bcolors.OKGREEN + "CURR_DIR a bine été assigné : " + CURR_DIR + World.bcolors.ENDC)





class Object(): #Toutes les classes doivent dériver de celle ci (ça permet de tout centraliser)

    def __init__(self):
        pass






#region Les Actors

class AActor(Object): 

    actorTurtle : turtle.Turtle()
    actorName : str


        
    actorComponents = {}

    def DoesComponentExist(self, componentName:str):
        return componentName in self.actorComponents


    def __init__(self, spriteName:str="square"):


        super().__init__()
        self.actorTurtle = turtle.Turtle()
    
        self.actorTurtle.shape(spriteName)
        self.actorTurtle.setheading(90)
        self.actorTurtle.penup()


class AEntity(AActor):

    speed = 999
    isMoving = False
    currentDestination:tuple
    movingToken = 0

    debugText = turtle.Turtle()


    #===========================================================================================
    middleOfAnAction = False

    Entityname = ""
    

    def __init__(self):
        super().__init__()

        self.movingToken = random.randint(0, 10)
        self.actorTurtle.speed(self.speed)

    def CanMove(self):
        return self.movingToken >= Parameters.MOVING_TOKEN_THRESHOLD




        
    
    def MoveTo(self, newPosition:tuple):

        #self.debugText.setpos(self.actorTurtle.pos())
        
        if (not self.isMoving):
            self.currentDestination = newPosition
    

        if (self.actorTurtle.pos()[0] < self.currentDestination[0]):
            middleOfAnAction = True
            self.isMoving = True
            self.actorTurtle.goto(self.actorTurtle.pos()[0] + 2, self.actorTurtle.pos()[1])

        if (self.actorTurtle.pos()[0] > self.currentDestination[0]):
            middleOfAnAction = True
            self.isMoving = True
            self.actorTurtle.goto(self.actorTurtle.pos()[0] - 2, self.actorTurtle.pos()[1])

        if (self.actorTurtle.pos()[1] < self.currentDestination[1]):
            middleOfAnAction = True
            self.isMoving = True
            self.actorTurtle.goto(self.actorTurtle.pos()[0], self.actorTurtle.pos()[1] + 2)

        if (self.actorTurtle.pos()[1] > self.currentDestination[1]):
            middleOfAnAction = True
            self.isMoving = True
            self.actorTurtle.goto(self.actorTurtle.pos()[0], self.actorTurtle.pos()[1] - 2)

        if abs(self.actorTurtle.pos()[0] - self.currentDestination[0]) < 10 and abs( self.actorTurtle.pos()[1] - self.currentDestination[1]) < 10:
            middleOfAnAction = False
            self.isMoving = False
            self.movingToken = 0

            World.currentWorld.actorCurrentlyMoving -= 1



        



    def FindRandomPointAtDistance(self, distance:float):

        pos = self.actorTurtle.pos()
        randomX = random.randint(pos[0] - distance, pos[0] + distance)
        randomY = random.randint(pos[1] - distance, pos[1] + distance)

        return (randomX, randomY)

#endregion
#region Les Component


class CComponent(Object):
    def __init__(self):
        super().__init__()


class CRessource(CComponent):

    

    def __init__(self):
        super().__init__()
        self.objectComponents["CRessource"] = self


class CDamageable(CComponent):

    maxHp = 100
    currentHp:maxHp

    def OnDamaged(self, amount:int):

        self.currentHp -= amount

        if (self.currentHp <= 0):
            self.OnDie()

    def OnDie(self):
        self.currentHp = 0





#endregion


