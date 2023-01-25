# Je vais partir du principe que ceux qui lise ce code ne save rien des modules 
# que j'utilise, vue que je suis un chic type je vais mettre les liens vers 
# la documentation que j'utilise (ou au moins un truc en rapport genre stackOverflow)

# ༼ つ ◕_◕ ༽つ


import random
import math



class AI_ACTOR(): 

    speed = 1
    suceed=False

    def __init__(self):
        super().__init__()

    def FindRandomPointAtDistance(self, distance:float):
        randomX = random.randint(self.rect.x - distance, self.rect.x + distance)
        randomY = random.randint(self.rect.y - distance, self.rect.y + distance)

        return (randomX, randomY)
