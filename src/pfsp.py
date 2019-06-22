#!/usr/bin/python3
import random as rand
import numpy as np
import pprint as p
import sys, getopt
from time import gmtime, strftime
from queue import Queue,PriorityQueue
import time
import math
import glob
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import hashlib

# Here we're going to test different cooling functions
# Some of the cooling functions are from:
# http://www.btluke.com/simanf1.html
def cool0(i,N,initTemp,finalTemp):
    return (initTemp-i*((initTemp-finalTemp)/N))

def cool1(i,N,initTemp,finalTemp):
    return (initTemp*((finalTemp/initTemp)**(i/N)))

def cool2(i,N,initTemp,finalTemp):
    A=(initTemp-finalTemp)*(N+1)/(N)+N/2
    B=10#initTemp-A
    return A/(i+1)+B

def cool3(i,N,initTemp,finalTemp):
    A=math.log(initTemp,N)
    return initTemp-i**A

def cool4(i,N,initTemp,finalTemp):
    exxx = ((25/N)*(i-N/2))
    exx = math.exp(exxx)
    return (initTemp-finalTemp)/(1+exx)+finalTemp

def cool5(i,N,initTemp,finalTemp):
    return .5*(initTemp-finalTemp)*(1+math.cos(i*math.pi/N))+finalTemp

def cool6(i,N,initTemp,finalTemp):
    return 0.5*(initTemp-finalTemp)*(1-math.tanh(10*i/N-5))+finalTemp

def cool7(i,N,initTemp,finalTemp):
    return (initTemp-finalTemp)/math.cosh(10*i/N)+finalTemp

def cool8(i,N,initTemp,finalTemp):
    A = (1/N)*math.log(initTemp/finalTemp)
    return initTemp*(math.e**(-A*i))

def cool9(i,N,initTemp,finalTemp):
    A = (1/(N**2))*math.log(initTemp/finalTemp)
    return initTemp*(math.e**(-A*(i**2)))

def calcTemp(i,N,initTemp,finalTemp,tipo):
    if(tipo==0):
        return cool0(i,N,initTemp,finalTemp)
    elif(tipo==1):
        return cool1(i,N,initTemp,finalTemp)
    elif(tipo==2):
        return cool2(i,N,initTemp,finalTemp)
    elif(tipo==3):
        return cool3(i,N,initTemp,finalTemp)
    elif(tipo==4):
        return cool4(i,N,initTemp,finalTemp)
    elif(tipo==5):
        return cool5(i,N,initTemp,finalTemp)
    elif(tipo==6):
        return cool6(i,N,initTemp,finalTemp)
    elif(tipo==7):
        return cool7(i,N,initTemp,finalTemp)
    elif(tipo==8):
        return cool8(i,N,initTemp,finalTemp)
    elif(tipo==9):
        return cool9(i,N,initTemp,finalTemp)
    else:
        return cool0(i,N,initTemp,finalTemp)

# Generates a better solution given a current solution.
# We will, in each iteration, change the order in which the tasks will be executed
# based on the tasks' mean execution time.
# Therefore, in the first iteration, the task with the smaller mean execution time
# will be swaped with the first task to be executed in the given solution.
# In the second iteration, the second smaller mean execution time will be swaped
# with the second task to be executed in the given solution, and so on.
def newNeighboorMeans(sol, processingTimes, iteration):
    # just generating a numpy array with the processingTimes
    means = np.array(processingTimes)
    # taking the mean execution time for each task
    means = np.mean(means, axis = 1)

    # ordering the means array and saving the indexes ordered to swap
    indexes = np.argsort(means)

    # swaps the iteration'th element of the solution with the
    # iteration'th smaller mean execution time
    sol[iteration], sol[indexes[iteration]] = sol[indexes[iteration]], sol[iteration]
    return sol

# Just randomicaly swaps two tasks.
# This is not the smartest approach, but with it we can increase the number of iterations,
# since the newNeighboorMeans is limited by the number of tasks.
# Another approach is to swap more than only two elements if the number of tasks is big enough:
# If the number of tasks is bigger than x, then swap two more elements.
def newNeighboorRandTasks(sol):
    idx = range(len(sol))

    # TODO
    for swaps in range(10):
        i1, i2 = rand.sample(idx, 2)
        sol[i1], sol[i2] = sol[i2], sol[i1]
    return sol

# Just randomicaly swaps two tasks. Should be used with a great number of iterations (>1k).
# Another approach is to swap more than only two elements as the number of iterations grows:
# At each 1k iterations, increases the number of swaps.
def newNeighboorRandIter(sol, iters):
    idx = range(len(sol))

    # when iters<1000, iters//1000 is equal to zero, and range(0) does not execute
    # but when it's bigger than 0, it makes more swaps
    for swaps in range((iters//1000) + 1):
        i1, i2 = rand.sample(idx, 2)
        sol[i1], sol[i2] = sol[i2], sol[i1]

    return sol

# The initial random solution
def randomNeighboor(nbtasks, seed):
    rand.seed(seed)
    sol = rand.sample(range(0, nbtasks), nbtasks)
    return sol

# Calculates the makespan given a solution
# (an order in which the tasks should be executed).
# For each task (except first), the total time passed on a given machine is:
# The maximum time passed until it finishes processing on the previous machine
# or the time passed for predecessor job to finish on the current machine
# Time passed for a job to finish on a machine is:
# the total time passed so far (the sommatory of the executions)
# + time it takes to finish the current task on the machine
def calcMakespan(sol, processingTimes, nbtasks, nbmachines):
    # list for the time passed until the finishing of the job
    cost = [0] * nbtasks
    # for each machine, total time passed will be updated
    for machine in range(0, nbmachines):
        for task in range(0, nbtasks):
            # cumulative time passed so far until the task starts to process
            costSoFar = cost[task]
            # except the first task
            if task > 0:
                costSoFar = max(cost[task - 1], cost[task])

            cost[task] = costSoFar + processingTimes[sol[task]][machine]
    return cost[nbtasks - 1]


# SA
def main(tasks, machines, times, iseed):
    # number of jobs and machines
    nbtasks = tasks
    nbmachines = machines
    # i-th job's processing time at j-th machine
    processingTimes = times
    seed = iseed

    # For the SA, we need to keep track of the current and the old best solutions.
    # They'll only represent the order in which the tasks should be executed.
    # Ex: oldBest = [9, 3, 4, 1, 6, 2, 7, 0, 8, 5]
    # is how the old best solution sheduled the tasks.
    oldBest = []
    oldBestValue = None
    newBest = []
    newBestValue = None
    # However, the bestSol is used to save the best solution of all
    bestSol = []

    # number of iterations for the SA
    # initially, for the neighboors being created accordingly with the mean execution times,
    # we're going to use the number of tasks as the maximum number of iterations
    # because it does not make sense to iterate more than this
    #saIter = nbtasks
    # For randomic generation of neighboors:
    saIter = 5000
    # intial temperature TODO discover better inital values
    initTemp = 100.0
    # this can't be zero because there are some divisions for tempFinal
    finalTemp = 1.0
    # repetitions needed
    rep = 10

    temp = initTemp
    # this is used to save results and make the plots, not important right now
    list_pontos = np.zeros((rep,saIter))
    list_temp = np.zeros((saIter))
    list_tempos = np.zeros((rep))

    # we can test different decreasing methods TODO
    tipo = 1
    for r in range(rep):
        # first random solution
        oldBest = randomNeighboor(nbtasks, seed)
        oldBestValue = calcMakespan(oldBest, processingTimes, nbtasks, nbmachines)
        #print("oldBest and value")
        #p.pprint(oldBest)
        #p.pprint(oldBestValue)
        # remember to update the best one so far
        bestSol = oldBest
        bestSolValue = oldBestValue

        # this is used to save results and make the plots, not important right now
        print("Execucao:"+str(r) + " Funcao:"+str(tipo))
        start_time = time.time()

        ite = 0
        while ( ite < saIter):
            # decreases the temperature TODO this needs to be checked
            temp = calcTemp(ite,saIter,initTemp,finalTemp,tipo)-1
            if( temp < 0):
                temp = 0

            # this is used to save results and make the plots, not important right now
            #list_pontos[r][ite]= (ncla-ponto)/ncla
            #list_temp[ite]=(temp/initTemp)

            # creates a new neighboor and checks its makespan
            #newBest = newNeighboorMeans(oldBest, processingTimes, ite)
            newBest = newNeighboorRand(oldBest)
            newBestValue = calcMakespan(newBest, processingTimes, nbtasks, nbmachines)
            #print("newBest and value")
            #p.pprint(newBest)
            #p.pprint(newBestValue)

            # checks if it is the best solution so far
            if (bestSolValue >= newBestValue):
                bestSol = newBest
                bestSolValue = newBestValue

            delta = newBestValue - oldBestValue
            ite+=1
            # if delta <= 0, the new solution has a better makespan that the previous one
            # therefore, the oldBest must be updated
            if( delta <= 0):
                oldBest = newBest
                oldBestValue = newBestValue
            # if the solution has not a better makespan
            else:
                # then, to accept a worse solution, the following condition must be satisfied:
                if(temp > 0 and math.exp(-delta/temp) > rand.uniform(0, 1)):
                    # A worse solution is only accepted given the above probability.
                    # I don't know how to explaing it mathematicaly, but there's a lot about it in my labbook.
                    oldBest = newBest
                    oldBestValue = newBestValue

        # this is used to save results and make the plots, not important right now
        list_tempos[r]=(time.time() - start_time)

    print("final solution and value:")
    p.pprint(bestSol)
    p.pprint(bestSolValue)
    # this is used to save results and make the plots, not important right now
    real_final = list_pontos.mean(axis=0)
    listamenos = list_pontos.max(axis=1)
