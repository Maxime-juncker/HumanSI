# Je vais partir du principe que ceux qui lise ce code ne save rien des modules 
# que j'utilise, vue que je suis un chic type je vais mettre les liens vers 
# la documentation que j'utilise (ou au moins un truc en rapport genre stackOverflow)

# ༼ つ ◕_◕ ༽つ


import random
import math
import turtle

image = "C:/Users/Amaro01/Documents/GitHub/HumanSI/S_Test.gif"
ressourceImage = "C:/Users/Amaro01/Documents/GitHub/HumanSI/R.gif"

ActorState = {

    "None" : 0,
    "Idle" : 1,
    
}

ActorImage = {
    
    "Humain" : image,
    "Tree" : ressourceImage
}

class Object():

    def __init__(self):
        pass

    objectComponents = {}

    def DoesComponentExist(self, componentName:str):
        return componentName in self.objectComponents





class CActor(Object): 

    actor = turtle.Turtle()

        

    def __init__(self, spriteName:str="square"):
        super().__init__()
    
        self.actor.shape(spriteName)
        self.actor.setheading(90)
        self.actor.penup()
        self.objectComponents["CActor"] = self
        



class CEntity(CActor):

    speed = 1
    isMoving = False

    def __init__(self):
        super().__init__()

        self.actor.speed(self.speed)


        self.objectComponents["CEntity"] = self


    
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



class CRessource(CActor):



    def __init__(self):
        super().__init__()
        self.objectComponents["CRessource"] = self
        


