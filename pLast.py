import random
import numpy as np
import time
import sys
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.pyplot import plot, ion, show
from mpl_toolkits.mplot3d import axes3d
import argparse


random.seed(time.clock())
#CONSTANTS VALUES
W=0.5
C1=0.8
C2=0.9

RANGE=10
VELMAX=1
PARTICLESN=10

ERROR=1e-6

GRAPHRES=30
##Endof CONSTANT VALUES

#global values
BENCHMARKMODE=0
MEASUREMOD=100 #how many tests we are going to make before measuring time
LOOPS=1

ANIMATIONTIME=0.1
#end of global values

def printf(format, *args):
    sys.stdout.write(format % args)

def f(x,y):
    #return x**2+y**2 #sphere function
    #return 0.26*(x*x+y*y)-0.48*x*y #Matyas function
    #return pow((x+2*y-7),2)+pow((x*2+y-5),2) #Booth function
    #return pow((pow(x,2)+y-11),2)+pow((x+pow(y,2)-7),2) #Himmelblau's function
    #return ( (1+pow(x+y+1,2)) * (19-14*x+3**x-14*y+6*x*y+3**y) )*( (30+pow(2*x-3*y,2))*(18-32*x+12**x+48*y-36*x*y+27**y) )
    #return (100*np.sqrt(np.abs(y-(0.01*pow(x,2)))))+(0.01*np.abs(x+10))#Bukin function N.6
    #return -x**2-y**2-((np.abs(x)+np.abs(y))*(np.abs(x)+np.abs(y))) #sphere function
    #return 0.5+( (pow(x*x-y*y,2)-0.5)/pow((1+0.001*(x*x+y*y)),2) )
    #return ((10 * 2 + (x * x - 10 * np.cos(2 * math.pi * x)) + (y * y - 10 * np.cos(2 * math.pi * y)))) #Rastrigin fitness_function
    #return  ((pow(1.5 - x + x * y, 2) + pow(2.25 - x + x * y * y, 2) +pow(2.625 - x + x * y * y * y, 2)) )#Beale's function
    return -20 * np.exp(-0.2 * np.sqrt(0.5 * (x * x + y * y))) + np.exp(0.5 * (np.cos(2 * math.pi * x) + np.cos(2 * math.pi * y))) - 20 #Ackley's fitness_function


def rand():
    return random.random()*2*RANGE-RANGE

class Best:
    x=0
    y=0
    fitness=0
    delta=0

    def __init__(self):
        self.x=rand()
        self.y=rand()
        self.fitness=f(self.x,self.y)
        self.delta=1000

    def printInfo(self):
        printf("x:%.2f y:%.2f gbFitness:%.2f delta:%f BEST!\n",self.x,self.y,self.fitness,self.delta)

Best=Best()

class Particle:
    x=0
    y=0
    xvel=0
    yvel=0
    fitness=f(x,y)
    bestFitness=f(x,y)
    bestX=x
    bestY=y

    def __init__(self):
        self.x=random.random()*2*RANGE-RANGE
        self.y=random.random()*2*RANGE-RANGE
        self.xvel=(random.random()*VELMAX)%(RANGE-self.x)
        self.yvel=(random.random()*VELMAX)%(RANGE-self.y)
        self.fitness=f(self.x,self.y)
        self.bestFitness=self.fitness
        self.bestX=self.x
        self.bestY=self.y

    def printInfo(self):
        printf("x:%.2f y:%.2f xv:%.2f yv:%.2f fit:%.2f pbfit:%.2f\n",self.x,self.y,self.xvel,self.yvel,self.fitness,self.bestFitness)

    def updateFitness(self):
        self.fitness=f(self.x,self.y)
        if(self.fitness<self.bestFitness):
            self.bestFitness=self.fitness
            self.bestX=self.x
            self.bestY=self.y
        if(self.fitness<Best.fitness):
            Best.delta=abs(Best.fitness-self.fitness)
            Best.fitness=self.fitness
            Best.x=self.x
            Best.y=self.y

    def updatePosition(self):
        self.xvel=W*self.xvel+(C1*random.random()*(self.bestX-self.x))+(C2*random.random()*(Best.x-self.x))
        self.yvel=W*self.yvel+(C1*random.random()*(self.bestX-self.x))+(C2*random.random()*(Best.y-self.y))
        self.x+=self.xvel
        self.y+=self.yvel


#initializing for every simulation
p=[]
#init particles
for i in range(PARTICLESN):
    p.append(Particle())
#ENDOF initializing for every simulation

if not(BENCHMARKMODE):
    #initializing for every simulation
    p=[]
    #init particles
    for i in range(PARTICLESN):
        p.append(Particle())
    #ENDOF initializing for every simulation

    print("Drawing everything!")
    #will print function and every point

    #create canvas
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    # Grab some test data.
    x = np.linspace(-RANGE, RANGE, GRAPHRES)
    y = np.linspace(-RANGE, RANGE, GRAPHRES)

    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)
    #interactive mode on
    plt.ion()

    j=0
    split=time.time()
    while (Best.delta>ERROR and j<100):
        ax.plot_surface(X, Y, Z,cmap=cm.hsv,lw=3,linewidth=1,alpha=0.5,rstride=1, cstride=1, )
        #ax.plot_wireframe(X, Y, Z, rstride=3, cstride=3)

        for i in range(PARTICLESN):
            p[i].updateFitness()
            p[i].updatePosition()
    #        p[i].printInfo()
            p[i].printInfo()
            ax.scatter3D(p[i].x, p[i].y,f(p[i].x,p[i].y),lw='1',color='r' )
        plt.show()
        raw_input()
        ax.clear()
        j+=1;

    print("at iteration ",j," time:",time.time()-split)
    Best.printInfo()

else:
    print("Gotta go fast!")
    split=time.time()
    for a in range(10000):
        #initializing for every simulation
        p=[]
        #init particles
        for i in range(PARTICLESN):
            p.append(Particle())
        #ENDOF initializing for every simulation

        j=0

        while (Best.delta>ERROR and j<1):
            for i in range(PARTICLESN):
                p[i].updateFitness()
                p[i].updatePosition()
            j+=1

        #print("at iteration ",i," time:",time.time()-split)
        Best.printInfo()
        #printf("%f\n",Best.fitness)
    print(time.time()-split)
