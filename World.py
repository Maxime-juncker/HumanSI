import AI
import turtle
import random

class bcolors: # /!\ les couleurs ne marche que sur sur certains IDE (ex : edupython n'affiche pas les couleurs)
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
    ressouceIndexCurrentlySelected = 0

    actorsList = [
        ["Unit", ("Assets/Pop1a.gif", "Assets/Pop1b.gif", "Assets/Pop1c.gif")],
        ["House", ("square", "square")],
        ["Tree", ("Assets/Arbre1.gif", "Assets/Arbre2.gif")],
        ["Rock", ("Assets/caillou1.gif", "Assets/fer.gif", "Assets/or.gif")],
        ["None", ("square", "square")]]


    unitList = {

            "ClassicHumain" : ("Assets/Pop1a.gif", "Assets/Pop1b.gif", "Assets/Pop1c.gif")
        }



    debuText = turtle.Turtle()


    def __init__(self):
        pass
    
    def Setup(self, screen):
        self.screen = screen
        self.KillAllActor()
        self.RegisterAllSprite()
        self.debuText.hideturtle()
        self.debuText.clear()
        self.debuText.write("Spawn Selected : " + str(self.actorsList[self.ressouceIndexCurrentlySelected]), font=("Raleway", 20, "normal"), align="center")
        


    def KillAllActor(self):
        
        nbOffTurtle=self.screen.turtles()

        for turtle in self.screen.turtles():
            turtle.hideturtle()
            turtle.clear()

        print(bcolors.WARNING + str(len(nbOffTurtle)) + " turtle were killed !" + bcolors.ENDC)

    def SwitchRessource(self):

        if self.ressouceIndexCurrentlySelected == len(self.actorsList) -1:
            self.ressouceIndexCurrentlySelected = 0
        else:
            self.ressouceIndexCurrentlySelected += 1
        self.debuText.hideturtle()
        self.debuText.clear()
        self.debuText.write("Spawn Selected : " + str(self.actorsList[self.ressouceIndexCurrentlySelected]), font=("Raleway", 20, "normal"), align="center")


    def CheckIfActorExist(self, actorName:str=""):
        
        if (actorName == ""):
            print(bcolors.FAIL + "ActorName est empty peut être qu'il n'est pas renseigner a l'appelle de GetActorByName" + bcolors.ENDC)
            return 

        for actor in self.actorCurentlyInWorld:

            if self.actorCurentlyInWorld[actor].actorName == actorName:
                return actor

        print(bcolors.FAIL + "L'acteur n'est pas présent dans : " + bcolors.WARNING + "self.actorCurentlyInWorld" + bcolors.ENDC)


    def SpawnBasedOnRessourceIndex(self, x, y):

        if self.actorsList[self.ressouceIndexCurrentlySelected][0] == "Unit":
            self.SpawnUnit(x,y)
        else:
            self.SpawnRessource(x, y, self.actorsList[self.ressouceIndexCurrentlySelected][1], True)

    def SpawnUnit(self,x,y):


        newActor = AI.AEntity()
        newActor.Setup(self.actorsList[self.ressouceIndexCurrentlySelected][1])


        newActor.actorTurtle.speed(999)
        newActor.actorTurtle.setpos(x,y)
        newActor.actorName = "AEntity " + str(len(self.actorCurentlyInWorld) + 1)
        
        newActor.actorComponents["CHumain"] = AI.CHumainRace()
        newActor.actorComponents["CAnimator"] = AI.CAnimator()

        newActor.actorComponents["CAnimator"].Setup(newActor.actorTurtle, self.unitList["ClassicHumain"])
        print(newActor.actorTurtle)
        newActor.actorComponents["CHumain"].Setup(newActor.actorTurtle)
        self.actorCurentlyInWorld[newActor.actorName] = newActor

    def SpawnRessource(self, x, y, ressourceName:str="None", randomSprite:bool=True):

        print(self.actorsList[self.ressouceIndexCurrentlySelected][1])

        newRessource = AI.AActor()
        newRessource.Setup(self.actorsList[self.ressouceIndexCurrentlySelected][1])


        newRessource.actorTurtle.speed(999)
        newRessource.actorTurtle.setpos(x,y)
        newRessource.actorName = "ressourceName " + str(len(self.actorCurentlyInWorld) + 1)


    def RegisterAllSprite(self):
        self.screen.register_shape('Assets/Arbre1.gif')
        self.screen.register_shape('Assets/Arbre2.gif')
        self.screen.register_shape('Assets/caillou1.gif')
        self.screen.register_shape('Assets/Pop1a.gif')
        self.screen.register_shape('Assets/Pop1b.gif')
        self.screen.register_shape('Assets/Pop1c.gif')


        self.screen.register_shape('Assets/or.gif')
        self.screen.register_shape('Assets/fer.gif')
        


currentWorld:UWorld

def SetupNewWorld():
    global currentWorld
    currentWorld = UWorld()









