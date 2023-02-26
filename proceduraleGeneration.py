from turtle import *
#from main import * 
from random import *
perlinNoiseValue = random()

def turtelColor(value) :
    pixelType = None
    if value == 0 :
        pixelType = 'DeepWater'
    elif value>0 and value<=0.1 :
        pixelType = 'Water'
    elif value>0.1 and value<=0.2 :
        pixelType = 'Bitche'
    elif value>0.2 and value<=0.5 :
        pixelType = 'Meadow'
    elif value>0.5 and value<=0.7 :
        pixelType = 'Forest'
    elif value>0.7 and value<=0.8 :
        pixelType = 'Hill'
    elif value>0.8 and value<=0.9 :
        pixelType = 'Mountain'
    elif value>0.9 and value<=1 :
        pixelType = 'HightMontain' 
    return(pixelType)


print(perlinNoiseValue)
print(turtelColor(perlinNoiseValue))
