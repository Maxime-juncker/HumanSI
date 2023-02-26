import AI
import turtle

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




class UWorld():

    screen:turtle.Screen()

    def __init__(self):
        pass
    
    def Setup(self, screen):
        self.screen = screen

    actorCurentlyInWorld = {}
    actorCurrentlyMoving = 0

    def KillAllActor(self):

        nbOffTurtle=self.screen.turtles()

        for turtle in self.screen.turtles():
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


    def Spawn_Unit(self,x,y):

        newActor = AI.AEntity()
        newActor.actorTurtle.speed(999)
        newActor.actorTurtle.setpos(x,y)
        newActor.actorName = "AEntity " + str( len(self.actorCurentlyInWorld) + 1)
        self.actorCurentlyInWorld[newActor.actorName] = newActor

currentWorld:UWorld

def SetupNewWorld():
    global currentWorld
    currentWorld = UWorld()






