# Je vais partir du principe que ceux qui lise ce code ne save rien des modules 
# que j'utilise, vue que je suis un chic type je vais mettre les liens vers 
# la documentation que j'utilise (ou au moins un truc en rapport genre stackOverflow)

# ༼ つ ◕_◕ ༽つ


import random
import math
import turtle

image = "C:/Users/Amaro01/Documents/GitHub/HumanSI/S_Test.gif"



class AI_ACTOR(): 

    speed = 20
    suceed=False
    actor = turtle.Turtle()

    def GetActor(self):
        return self.actor

        

    def __init__(self):
        super().__init__()
    
        self.actor.shape(image)
        self.actor.setheading(90)
        self.actor.speed(self.speed)
        

    def MoveTo(self, newPosition:tuple):

        while (self.actor.pos()[0] < newPosition[0]):
            self.actor.goto(self.actor.pos()[0] + self.speed, self.actor.pos()[1])

        while (self.actor.pos()[0] > newPosition[0]):
            self.actor.goto(self.actor.pos()[0] - self.speed, self.actor.pos()[1])

        while (self.actor.pos()[1] < newPosition[1]):
            self.actor.goto(self.actor.pos()[0], self.actor.pos()[1] + self.speed)

        while (self.actor.pos()[1] > newPosition[1]):
            self.actor.goto(self.actor.pos()[0], self.actor.pos()[1] - self.speed)

    def FindRandomPointAtDistance(self, distance:float):

        pos = self.actor.pos()

        randomX = random.randint(pos[0] - distance, pos[0] + distance)
        randomY = random.randint(pos[1] - distance, pos[1] + distance)

        return (randomX, randomY)
