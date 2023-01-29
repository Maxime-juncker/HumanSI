from turtle import *


chunkPos = { #pas enlever
             #pas enlever
}            #pas enlever
ChunkCoinFinal = {

}
class ChunkDeBase() :
    currentChunk = str(len(chunkPos))
    chunkPos["Chunk " + currentChunk] = []
    coord = (0,0)
    for i in range(6) :
        color('black')
        begin_fill()
        forward(50)
        left(60)
        chunkPos["Chunk " + currentChunk].append(pos())
    setpos(int(20),int(80))
    print(chunkPos)
    #ChunkCoinFinal["Chunk"] = chunkPos test un peux rater
    end_fill()
    done()

print(chunkPos)

def GenerationMap() :
    #color('red')
    begin_fill()
    setpos(int(chunkPos['Chunk 0'](1)))
    end_fill
    print("ok ok")
GenerationMap