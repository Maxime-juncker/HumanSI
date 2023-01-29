from turtle import *


ChunkPos = { #pas enlever
             #pas enlever
}            #pas enlever

ChunkCoinFinal = {

}

class ChunkDeBase() :
    currentChunk = str(len(ChunkPos))
    ChunkPos["Chunk " + currentChunk] = []
    coord = (0,0)
    for i in range(6) :
        color('black')
        begin_fill()
        forward(50)
        left(60)
        ChunkPos["Chunk " + currentChunk].append(pos())
    setpos(int(20),int(80))
    print(ChunkPos)
    print(ChunkPos['Chunk 0'])
    setpos(ChunkPos['Chunk 0'][0])
    forward(100)
    #ChunkCoinFinal["Chunk"] = ChunkPos : test un peux rater
    end_fill()
    done()

print(ChunkPos)
""""
class GenerationMap() :
    #color('red')
    coord = ChunkPos['Chunk 0']
    begin_fill()
    setpos(int(10),int(50))
    forward(100)
    end_fill
    print("ok ok")


#GenerationMap
"""