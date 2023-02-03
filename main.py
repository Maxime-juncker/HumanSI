# Je vais partir du principe que ceux qui lise ce code ne save rien des modules
# que j'utilise, vue que je suis un chic type je vais mettre les liens versgi
# la documentation que j'utilise (ou au moins un truc en rapport genre stackOverflow)

# ༼ つ ◕_◕ ༽つ



import AI #Un sripte custome (ont peut faire ça si vous saviez po ╰(*°▽°*)╯
import turtle
import os
#import proceduraleGeneration

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



CURR_DIR = os.path.dirname(os.path.realpath(__file__))


game_on = True


screen = turtle.Screen()


def on_quit():
    global game_on
    game_on = False

    screen._root.after(1000, screen._root.destroy)

screen._root.protocol("WM_DELETE_WINDOW", on_quit)


ressourceImage = CURR_DIR + "/R.gif"
image = CURR_DIR + "/S_Test.gif"

screen.addshape(ressourceImage)
screen.addshape(image)

SpriteLibrary = {

    "Humain" : image,
    "Tree" : ressourceImage
    
}


class UWorld():
    def __init__(self):
        pass

    actorCurentlyInWorld = {}

    def KillAllActor(self):

        nbOffTurtle=screen.turtles()

        for turtle in screen.turtles():
            turtle.hideturtle()
            turtle.clear()

        print(bcolors.WARNING + str(len(nbOffTurtle)) + " turtle were killed !" + bcolors.ENDC)
        


World = UWorld()




screen.setup(1.0, 1.0)
screen.bgcolor("#7b7b7f")


test = AI.AEntity()





def MoveActor(actorToMove:AI.AEntity(), actorState:AI.ActorState=AI.ActorState["Idle"]):

    if (not actorToMove.isMoving and actorState == AI.ActorState["Idle"]):
        newCoord = actorToMove.FindRandomPointAtDistance(100)
        actorToMove.MoveTo(newCoord)

World.KillAllActor()

screen.listen()





#AI.World.KillActor(test.actor)



unit=[]

def Spawn_Unit():
    unit.append(AI.AEntity())
    print(unit)

screen.onkey(Spawn_Unit, 'space')
screen.onkey(World.KillAllActor, 'a')


while True:

    if not game_on :
        break

    MoveActor(test)

    for element in unit:
        MoveActor(element)


    screen.update()








