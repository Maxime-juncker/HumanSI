# Je vais partir du principe que ceux qui lise ce code ne save rien des modules
# que j'utilise, vue que je suis un chic type je vais mettre les liens versgi
# la documentation que j'utilise (ou au moins un truc en rapport genre stackOverflow)

# ༼ つ ◕_◕ ༽つ



import AI #Un sripte custome (ont peut faire ça si vous saviez po ╰(*°▽°*)╯
import turtle
import os
import World
import time
import Parameters
#import proceduraleGeneration

# \\ ======================================= VARS ======================================= //

game_on = False

fps = 200
time_delta = 1./fps

CURR_DIR = os.path.dirname(os.path.realpath(__file__))

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

# \\ ============================================================================== //

screen:turtle.Screen()


def Setup():
    """
    Setup des different parametre du mon (World, turtle etc...)
    si vous voulez mettre un truc qui se fait au début du script mettez le ici
    Merci :)

    a la fin ont lock la fonction
    (si jamais elle était appeler une deuxieme fois y'aurais 2 World 2 screen etc....)
    """

    global game_on

    if game_on:
        return

    global screen
    screen = turtle.Screen()

    # ====== Setup un new world ========
    World.SetupNewWorld()
    World.currentWorld.Setup(screen)
    # ==================================



    # ====== Setup le screen de turlte ========

    screen.setup(1.0, 1.0)
    screen.bgcolor("#7b7b7f")

    # =========================================


    #pour être prudent si jamais y'a un actor pour x raison ont le delete 
    World.currentWorld.KillAllActor()

    #ont lock la fonction pour ne pas pouvoir la ré-appeler par accident
    game_on = True



def on_quit():
    global game_on
    game_on = False

    screen._root.after(1000, screen._root.destroy)

    screen._root.protocol("WM_DELETE_WINDOW", on_quit)

def MoveActor(actorToMove:AI.AEntity()):


    newCoord = actorToMove.FindRandomPointAtDistance(100)
    actorToMove.MoveTo(newCoord)


Setup()


screen.listen()
screen.onclick(World.currentWorld.Spawn_Unit)
screen.onkey(World.currentWorld.KillAllActor, 'a')





while True:

    '''
    lorsque game_on passe a false, ça veut dire que la fenetre vas ce fermer dans 1000ms
    il faut detruire tous les acteurs, faire les truc de sauvegarde + exit ka boucle infini

    (sinon y'a des erreur mais ça impacte pas le jeux c'est juste pas jolie =D )
    '''

    time.sleep(time_delta) # Permet de limiter le nb te time que la loop run avec les Fps 


    if not game_on : 
        World.currentWorld.KillAllActor()
        #Parameters.Save() <- Pas encore fait
        break

    actorInScene = World.currentWorld.actorCurentlyInWorld.copy()

    print(World.currentWorld.actorCurrentlyMoving)

    for element in actorInScene:
        if actorInScene[element].CanMove() and World.currentWorld.actorCurrentlyMoving <= Parameters.MAX_ACTORS_MOVING or actorInScene[element].isMoving:
            
            if not actorInScene[element].isMoving:
                World.currentWorld.actorCurrentlyMoving += 1 
                
            MoveActor(actorInScene[element])

        else:
            actorInScene[element].movingToken += 1


    screen.update()
