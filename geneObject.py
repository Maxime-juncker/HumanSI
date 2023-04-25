from random import*
def coordRandInList(coordX, coordY, nbrCoord) :     #comme parametre on met les coordoner des extremiter de la map et le nombre de coordonnée renvoyer
    listCoord = []
    for i in range(nbrCoord) :
        x = randint(0, coordX+1)    #met en argument des nombres aléatoires
        y = randint(0, coordY+1)
        try :
            listCoord.index((x, y))     #verifie qu'il n'y a pas  2 fois les meme coords
            pass
        except :
            listCoord.append((x, y))  
    return(listCoord)

print(coordRandInList(3000,2000, 200))