"""def listCoord(limX, limY, path) :   #Je fait une boucle qui à une valeur x vas associer tout les valeurs y
    ListCoord = []
    for x in range(limX) :
        miniListCoord = [x]
        for y in range(limY) :
            miniListCoord.append(y)
            ListCoord.append(miniListCoord)
            miniListCoord = [x]
    return ListCoord
#print(listCoord(10, 10, 1))"""


from random import*
def coordRandInList(coordX, coordY, nbrCoord) :
    listCoord = []
    for i in range(nbrCoord) :
        listCoord.append((randint(0, coordX+1), randint(0, coordY+1)))
    return(listCoord)

print(coordRandInList(3000,2000, 100))