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
    
    actorCurentlyInWorld = {}
    actorCurrentlyMoving = 0

    ressourceList = ["Unit", "Tree", "Rock", "None"]




    def __init__(self):
        pass
    
    def Setup(self, screen):
        self.screen = screen

    ressouceIndexCurrentlySelected = 0

    def KillAllActor(self):

        nbOffTurtle=self.screen.turtles()

        for turtle in self.screen.turtles():
            turtle.hideturtle()
            turtle.clear()

        print(bcolors.WARNING + str(len(nbOffTurtle)) + " turtle were killed !" + bcolors.ENDC)

    def SwitchRessource(self):

        if self.ressouceIndexCurrentlySelected > len( self.ressourceList):
            self.ressouceIndexCurrentlySelected = 0
        else:
            self.ressouceIndexCurrentlySelected += 1


    def CheckIfActorExist(self, actorName:str=""):
        
        if (actorName == ""):
            print(bcolors.FAIL + "ActorName est empty peut être qu'il n'est pas renseigner a l'appelle de GetActorByName" + bcolors.ENDC)
            return 

        for actor in self.actorCurentlyInWorld:

            if self.actorCurentlyInWorld[actor].actorName == actorName:
                return actor

        print(bcolors.FAIL + "L'acteur n'est pas présent dans : " + bcolors.WARNING + "self.actorCurentlyInWorld" + bcolors.ENDC)


    def SpawnBasedOnRessourceIndex(self, x, y):

        if self.ressourceList[self.ressouceIndexCurrentlySelected] == "Unit":
            self.SpawnUnit(x,y)
        else:
            self.SpawnRessource(x,y, self.ressourceList[self.ressouceIndexCurrentlySelected])

    def SpawnUnit(self,x,y):

        newActor = AI.AEntity()
        newActor.actorTurtle.speed(999)
        newActor.actorTurtle.setpos(x,y)
        newActor.actorName = "AEntity " + str( len(self.actorCurentlyInWorld) + 1)
        self.actorCurentlyInWorld[newActor.actorName] = newActor

    def SpawnRessource(self, x, y, ressourceName:str="None"):

        newRessource = AI.AActor("square", ressourceName)
        newRessource.actorTurtle.speed(999)
        newRessource.actorTurtle.setpos(x,y)
        newRessource.actorName = "ERessource " + str(len(self.actorCurentlyInWorld) + 1)


currentWorld:UWorld

def SetupNewWorld():
    global currentWorld
    currentWorld = UWorld()






