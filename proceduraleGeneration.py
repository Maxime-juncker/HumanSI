from turtle import *


ChunkPos = { #pas enlever
             #pas enlever
}            #pas enlever

ChunkCoinFinal = {

}

ChunkCentre = {

}

NbrChunk = 0

class ChunkDeBase() :
    currentChunk = str(len(ChunkPos))
    ChunkPos["Chunk " + currentChunk] = []
    ChunkCentre["Chunk " + currentChunk] = []
    coord = (0,0)
    for i in range(6) :
        color('black')
        forward(50)
        left(60)
        ChunkPos["Chunk " + currentChunk].append(pos())
    left(60)
    penup()
    forward(50)
    ChunkCentre["Chunk " + currentChunk].append(pos())
    setpos(ChunkPos['Chunk 0'][1])
    right(60)
    pendown()
    NbrChunk += 1


    done()
    

print(ChunkPos)

class GenerationMap() :
    #color('red')
    coord = ChunkPos['Chunk 0'][1]
    setpos(int(10),int(50))
    forward(100)
    print("ok ok")


#GenerationMap
