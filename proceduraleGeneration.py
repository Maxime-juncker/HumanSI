from turtle import *
LimiteChunk = {}

chunkPos = {
    
}

class ChunkDeBase() :
    currentChunk = str(len(chunkPos))
    chunkPos["Chunk " + currentChunk] = []


    for i in range(6) :
        color('black')
        begin_fill()
        forward(50)
        left(60)
        chunkPos["Chunk " + currentChunk].append(pos())

    print(chunkPos)
    end_fill()
    done()


 