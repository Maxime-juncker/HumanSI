from turtle import *


ChunkPos = { #pas enlever
             #pas enlever
}            #pas enlever

ChunkCoinFinal = {

}

ChunkCentre = {

}

NbrChunk = 0
speed(0)
title("salut a tous c'est Fanta")
class ChunkDeBase() :
    currentChunk = str(len(ChunkPos))
    ChunkPos[currentChunk] = []
    ChunkCentre[currentChunk] = []
    coord = (0,0)
    color('black')
    for exagone in range(6) :
           forward(50)
           left(60)
           ChunkPos[currentChunk].append(pos())
    left(60)
    penup()
    forward(50)
    ChunkCentre[currentChunk].append(pos())
    right(60)
    forward(50)
    pendown()
    NbrChunk += 1
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