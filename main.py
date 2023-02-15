# Je vais partir du principe que ceux qui lise ce code ne save rien des modules
# que j'utilise, vue que je suis un chic type je vais mettre les liens versgi
# la documentation que j'utilise (ou au moins un truc en rapport genre stackOverflow)

# ༼ つ ◕_◕ ༽つ



import AI #Un sripte custome (ont peut faire ça si vous saviez po ╰(*°▽°*)╯
import turtle
import os
import random
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


    def CheckIfActorExist(self, actorName:str=""):
        

        if (actorName == ""):
            print(bcolors.FAIL + "ActorName est empty peut être qu'il n'est pas renseigner a l'appelle de GetActorByName" + bcolors.ENDC)
            return 

        
        
        for actor in self.actorCurentlyInWorld:

            if self.actorCurentlyInWorld[actor].actorName == actorName:
                return actor


        print(bcolors.FAIL + "L'acteur n'est pas présent dans : " + bcolors.WARNING + "self.actorCurentlyInWorld" + bcolors.ENDC)




    def Spawn_Unit(self):
        newActor = AI.AEntity()
        newActor.actorName = "AEntity " + str( len(self.actorCurentlyInWorld) + 1)
        self.actorCurentlyInWorld[newActor.actorName] = newActor;





World = UWorld()




screen.setup(1.0, 1.0)
screen.bgcolor("#7b7b7f")






def MoveActor(actorToMove:AI.AEntity()):


    newCoord = actorToMove.FindRandomPointAtDistance(100)
    actorToMove.MoveTo(newCoord)



World.KillAllActor()

screen.listen()





screen.onkey(World.Spawn_Unit, 'space')
screen.onkey(World.KillAllActor, 'a')

World.Spawn_Unit()
World.Spawn_Unit()





while True:

    '''
    lorsque game_on passe a false, ça veut dire que la fenetre vas ce fermer dans 1000ms
    il faut detruire tous les acteurs, faire les truc de sauvegarde + exit ka boucle infini

    (sinon y'a des erreur mais ça impacte pas le jeux c'est juste pas jolie =D )
    '''

    if not game_on : 
        World.KillAllActor()

        #Parameters.Save() <- Pas encore fait
        break


    for element in World.actorCurentlyInWorld:
        MoveActor(World.actorCurentlyInWorld[element])


    screen.update()








