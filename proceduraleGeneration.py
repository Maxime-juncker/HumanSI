from turtle import *
#from main import * 
from random import *
from tkinter import *
import random as rand


root = Tk()
dimX=1000
dimY=500
canvas = Canvas(root, bg="blue", height= dimY, width= dimX)
canvas.pack()

Carte = {'xy': [200, 100],'cLevel': 0,'nodes': [],'seed': 10,'Choice': [-100, 200]}

class node : 
    def commencement (self, xy):
        self.el = 0
        self.xy = xy
        self.temp = 0
        self.neighbors = []
        self.active = True
    def couleur_pixel(self):
        if self.el <= (-25):
            couleur = 'bleu fonce'                              #océan
        elif self.el <= Carte['cLevel']:
            couleur = 'bleue'                                   #mer
        elif self.el <= 25 and self.temp <= 0 :
            couleur = 'gris fonce'                              #Haute montagne
        elif self.el <= 25 and self.temp <= 5 :
            couleur = 'gris '                                   #montagne
        elif self.el <= 25 and self.temp <= 10 :
            couleur = 'vert'                                    #prairie
        elif self.el <= 25 and self.temp <= 50 : 
            couleur = 'vert fonce'                              #forêt
        elif self.el <= 25 and self.temp <= 100:
            couleur = 'jaune'                                   #plage
        else : 
            couleur = 'marron'                                  #marais
        a = self.xy[0] * 5
        b = self.xy[1] * 5
        c = a + 5 
        d = b + 5
        canvas.create_rectangle(a,b,c,d, fill = couleur, outline = couleur)

def generationNode() :
    for i in range(Carte['xy'][0]):
        for j in range(Carte['xy'][1]):
            Carte['nodes'].append(node([i,j]))
print('Génération du monde')
generationNode()

def PlusProcheVoisins():
    temp = []
    for i in Carte['nodes']:
        temp.append(i)
    for j in Carte['nodes']:
        temp.pop(0)
        for k in temp :
            if j != k :
                if j.xy[0] == k.xy[0]:
                    if k.xy[1] == j.xy[1] + 1 :
                        j.neighbors.append(k)
                elif j.xy[1] == k.xy[1] : 
                    if k.xy[0] == j.xy[0] + 1 :
                        j.neighbors.append(k)
                if len(j.neighbors) >= 2:
                    break
print('Generations des PlusProcheVoisins')
PlusProcheVoisins()

def SetActive():
    for i in Carte['nodes'] :
        i.active = True

def CartePlusBelle():
        for j in Carte['nodes']:
            j.active = False
        for k in j.neighbors:
            if k.active == True:
                if j.el != k.el:
                    if rand.randrange(0, 100) < 5:
                        a = (j.el + k.el)/2
                        j.el = a
                        k.el = a
                    elif rand.randrange(0, 100) < 5:
                        a = (j.temp + k.temp)/2
                        j.temp = a
                        k.temp = a

def TerrainPlusHaut():
    for i in Carte['nodes']:
        if i.el > 0:
            if rand.randrange(0, 100) < 1:
                i.el += 100

def MerPlusBasse():
    for i in Carte['nodes']:
        if i.el <= 0:
            if rand.randrange(0, 100) < 1:
                i.el -= 100

def RaiseTemp():
    for i in Carte['nodes']:
        if i.el > 0:
            if rand.randrange(0, 100) < 1:
                i.temp += 10

def process():
    SetActive()
    CartePlusBelle()

def process1():
    SetActive()
    MerPlusBasse()
    canvas.delete('all')

def process2():
    SetActive()
    TerrainPlusHaut()
  
def process3():
    SetActive()
    RaiseTemp()

print('0')
for i in range(100):
    process()
    process3()
print('1')
for i in range(15):
    process1()
    process2()
print('2')
for i in range(100):
    process()

canvas.delete('all')
for i in Carte['nodes']:
    i.render()
canvas.update()

mainloop()

