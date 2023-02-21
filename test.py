"""
test = { 

}
test['sus'] = (10,20), (30,40), (50,60)
print(test['sus'][1])

sus = 0
print(''+ str(sus))
NbrChunk = 0
nombre = str(NbrChunk)
print(nombre)
"""

"""
from turtle import *

forward(50)
done()
""" 

import time
#import proceduraleGeneration

fps = 50
time_delta = 1./fps


while True:
    t0 = time.perf_counter()
    time.sleep(time_delta)
    t1 = time.perf_counter()
    print( str(1. / (t1 - t0)))