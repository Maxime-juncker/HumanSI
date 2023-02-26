from turtle import *
#from main import * 
from random import *
perlinNoiseValue = random()

def turtelColor(value) :
    pixelType = None
    if value == 0 :
        pixelType = 'DeepWater'
    elif value>0 and value<1 :
        pixelType = 'Water'
    elif value>1 and value<2 :
        pixelType = 'Bitche'
    elif value>2 and value<3 :
        pixelType = 'Medaw'