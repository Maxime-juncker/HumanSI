from turtle import *


ChunkPos = { #pas enlever
             #pas enlever
}            #pas enlever

ChunkCoinFinal = {

}

ChunkCentre = {

}

NbrChunk = 0
NbrLigne = 0
speed(0)
title("salut a tous c'est Fanta")
class ChunkDeBase() :
    currentChunk = str(len(ChunkPos))
    ChunkPos[currentChunk] = []
    ChunkCentre[currentChunk] = []
    coord = (0,0)
    color('black')
    for i in range(6) :
        forward(25)
        for carre in range(4) :
            forward(50)
            left(90)
            ChunkPos[currentChunk].append(pos())
        penup()
        forward(25)
        left(90)
        forward(25)
        ChunkCentre[currentChunk].append(pos())
        backward(25)
        right(90)
        pendown()
        NbrChunk+=1
if NbrChunk >=100 :
    goto(ChunkPos['' + NbrLigne][1])
    NbrLigne+=1
        
    print(ChunkPos)
    
    """
    left(60)
    penup()
    forward(50)
    ChunkCentre[currentChunk].append(pos())
    right(60)
    forward(50)
    pendown()
    NbrChunk += 1
    """
    done()






"""
print(ChunkPos)

class GenerationMap() :
    #color('red')
    coord = ChunkPos['0'][1]
    setpos(int(10),int(50))
    forward(100)
    print("ok ok")


#GenerationMap
"""