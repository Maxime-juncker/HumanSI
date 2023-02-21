# Je vais partir du principe que ceux qui lise ce code ne save rien des modules
# que j'utilise, vue que je suis un chic type je vais mettre les liens versgi
# la documentation que j'utilise (ou au moins un truc en rapport genre stackOverflow)

# ༼ つ ◕_◕ ༽つ



import AI #Un sripte custome (ont peut faire ça si vous saviez po ╰(*°▽°*)╯
import turtle
import os
import random
import time
#import proceduraleGeneration

fps = 200
time_delta = 1./fps


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

    isCreatingActor = False
    wanToCreateActor=False


    def __init__(self):
        pass

    actorCurentlyInWorld = {}

    def KillAllActor(self):

        nbOffTurtle=screen.turtles()

        for turtle in screen.turtles():
            turtle.hideturtle()
            turtle.clear()

        print(bcolors.WARNING + str(len(nbOffTurtle)) + " turtle were killed !" + bcolors.ENDC)


    def CheckIfActorExist(self, actorName:str=""):
        

        if (actorName == ""):
            print(bcolors.FAIL + "ActorName est empty peut être qu'il n'est pas renseigner a l'appelle de GetActorByName" + bcolors.ENDC)
            return 

        
        
        for actor in self.actorCurentlyInWorld:

            if self.actorCurentlyInWorld[actor].actorName == actorName:
                return actor


        print(bcolors.FAIL + "L'acteur n'est pas présent dans : " + bcolors.WARNING + "self.actorCurentlyInWorld" + bcolors.ENDC)


    def TryToCreateActor(self,x,y):
        self.wanToCreateActor = True
        self.Spawn_Unit(x,y)

    def Spawn_Unit(self,x,y):
        self.wanToCreateActor = False
        self.isCreatingActor = True



        newActor = AI.AEntity()
        newActor.actorTurtle.speed(999)
        newActor.actorTurtle.setpos(x,y)
        newActor.actorName = "AEntity " + str( len(self.actorCurentlyInWorld) + 1)
        self.actorCurentlyInWorld[newActor.actorName] = newActor


        self.isCreatingActor = False






World = UWorld()




screen.setup(1.0, 1.0)
screen.bgcolor("#7b7b7f")






def MoveActor(actorToMove:AI.AEntity()):


    newCoord = actorToMove.FindRandomPointAtDistance(100)
    actorToMove.MoveTo(newCoord)



World.KillAllActor()

screen.listen()




screen.onclick(World.TryToCreateActor)
screen.onkey(World.KillAllActor, 'a')




canCreateActor=False
while True:

    '''
    lorsque game_on passe a false, ça veut dire que la fenetre vas ce fermer dans 1000ms
    il faut detruire tous les acteurs, faire les truc de sauvegarde + exit ka boucle infini

    (sinon y'a des erreur mais ça impacte pas le jeux c'est juste pas jolie =D )
    '''

    time.sleep(time_delta) # Permet de limiter le nb te time que la loop run avec les Fps 


    if not game_on : 
        World.KillAllActor()
        #Parameters.Save() <- Pas encore fait
        break

    actorInScene = World.actorCurentlyInWorld.copy()

    for element in actorInScene:
        MoveActor(World.actorCurentlyInWorld[element])


    screen.update()










