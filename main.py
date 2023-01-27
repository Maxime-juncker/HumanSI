# Je vais partir du principe que ceux qui lise ce code ne save rien des modules 
# que j'utilise, vue que je suis un chic type je vais mettre les liens vers 
# la documentation que j'utilise (ou au moins un truc en rapport genre stackOverflow)

# ༼ つ ◕_◕ ༽つ

#slt

import AI #Un sripte custome (ont peut faire ça si vous saviez po ╰(*°▽°*)╯
import turtle
import os


CURR_DIR = os.path.dirname(os.path.realpath(__file__))
print(CURR_DIR)

screen = turtle.Screen()


ressourceImage = CURR_DIR + "/R.gif"
image = CURR_DIR + "/S_Test.gif"

screen.addshape(ressourceImage)
screen.addshape(image)

screen.setup(1.0, 1.0)
screen.bgcolor("#7b7b7f")



test = AI.AEntity()





def MoveActor(actorToMove:AI.AEntity(), actorState:AI.ActorState=AI.ActorState["Idle"]):

    if (not actorToMove.isMoving and actorState == AI.ActorState["Idle"]):
        newCoord = actorToMove.FindRandomPointAtDistance(50)
        actorToMove.MoveTo(newCoord)


screen.listen()

while True:
    MoveActor(test)



    screen.update()


