# Je vais partir du principe que ceux qui lise ce code ne save rien des modules 
# que j'utilise, vue que je suis un chic type je vais mettre les liens vers 
# la documentation que j'utilise (ou au moins un truc en rapport genre stackOverflow)

# ༼ つ ◕_◕ ༽つ



import AI #Un sripte custome (ont peut faire ça si vous saviez po ╰(*°▽°*)╯
import turtle

screen = turtle.Screen()

image = "C:/Users/Amaro01/Documents/GitHub/HumanSI/S_Test.gif"

screen.addshape(image)
screen.setup(1.0, 1.0)
screen.bgcolor("#7b7b7f")



test = AI.AI_ACTOR()
test.speed = 1




def MoveActor(actorToMove:AI.AI_ACTOR(), actorState:AI.ActorState=AI.ActorState["Idle"]):

    if (not actorToMove.isMoving and actorState == AI.ActorState["Idle"]):
        newCoord = test.FindRandomPointAtDistance(50)
        actorToMove.MoveTo(newCoord)


screen.listen()

while True:
    MoveActor(test)



    screen.update()

screen.mainloop()


