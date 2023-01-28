# Je vais partir du principe que ceux qui lise ce code ne save rien des modules 
# que j'utilise, vue que je suis un chic type je vais mettre les liens vers 
# la documentation que j'utilise (ou au moins un truc en rapport genre stackOverflow)

# ༼ つ ◕_◕ ༽つ


import random
import math
import turtle

import os

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
print(CURR_DIR)


ActorState = {

    "None" : 0,
    "Idle" : 1,
    
}






class Object(): #Toutes les classes doivent dériver de celle ci (ça permet de tout centraliser)

    def __init__(self):
        pass





#region Les Actors

class AActor(Object): 

    actor : turtle.Turtle()

        
    actorComponents = {}

    def DoesComponentExist(self, componentName:str):
        return componentName in self.actorComponents


    def __init__(self, spriteName:str="square"):
        super().__init__()
        self.actor = turtle.Turtle()
    
        self.actor.shape(spriteName)
        self.actor.setheading(90)
        self.actor.penup()


class AEntity(AActor):

    speed = 2
    isMoving = False

    Entityname = ""

    def __init__(self):
        super().__init__()

        self.actor.speed(self.speed)


    
    def MoveTo(self, newPosition:tuple):


        while (self.actor.pos()[0] < newPosition[0]):
            self.isMoving = True
            self.actor.goto(self.actor.pos()[0] + self.speed, self.actor.pos()[1])

        while (self.actor.pos()[0] > newPosition[0]):
            self.isMoving = True
            self.actor.goto(self.actor.pos()[0] - self.speed, self.actor.pos()[1])

        while (self.actor.pos()[1] < newPosition[1]):
            self.isMoving = True
            self.actor.goto(self.actor.pos()[0], self.actor.pos()[1] + self.speed)

        while (self.actor.pos()[1] > newPosition[1]):
            self.isMoving = True
            self.actor.goto(self.actor.pos()[0], self.actor.pos()[1] - self.speed)

        self.isMoving = False
        



    def FindRandomPointAtDistance(self, distance:float):

        pos = self.actor.pos()
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