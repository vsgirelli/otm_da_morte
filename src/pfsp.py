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
# These functions decide how the temperature will be decreased.
# As the temperature decreases, so decreases the chances of a worse solution to be accepted.
def cool0(ite,saIter,initTemp,finalTemp):
    return (initTemp-ite*((initTemp-finalTemp)/saIter))

def cool1(ite,saIter,initTemp,finalTemp):
    return (initTemp*((finalTemp/initTemp)**(ite/saIter)))

def cool2(ite,saIter,initTemp,finalTemp):
    A=(initTemp-finalTemp)*(saIter+1)/(saIter)+saIter/2
    B=10#initTemp-A
    return A/(ite+1)+B

def calcTemp(ite,saIter,initTemp,finalTemp,tipo):
    if(tipo==0):
        return cool0(ite,saIter,initTemp,finalTemp)
    elif(tipo==1):
        return cool1(ite,saIter,initTemp,finalTemp)
    elif(tipo==2):
        return cool2(ite,saIter,initTemp,finalTemp)
    else:
        return cool0(ite,saIter,initTemp,finalTemp)

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

# Just randomicaly swaps tasks.
# The number of swaps depends on the number of tasks.
# At each 100 tasks, increases the number of swaps.
# For ex: for 500 tasks will be performed 5 swaps per iteration.
def newNeighboorRandTasks(sol):
    idx = range(len(sol))

    for swaps in range((len(sol)//100) + 1):
        i1, i2 = rand.sample(idx, 2)
        sol[i1], sol[i2] = sol[i2], sol[i1]

    return sol

# Just randomicaly swaps tasks. Should be used with a great number of iterations (>1k).
# At each 1k iterations, increases the number of swaps.
# TODO try to increase the number of iterations
def newNeighboorRandIter(sol, iters):
    idx = range(len(sol))

    # when iters<1000, iters//1000 is equal to zero, and range(0) does not execute
    # but when it's bigger than 0, it makes more swaps
    for swaps in range((iters//1000) + 1):
        i1, i2 = rand.sample(idx, 2)
        sol[i1], sol[i2] = sol[i2], sol[i1]

    return sol

# Just randomicaly swaps tasks. Should be used with a great number of iterations (>1k).
# At each iteration, swaps a random number of tasks (smaller than the number of tasks).
def newNeighboorRandRand(sol, iters):
    idx = range(len(sol))

    for swaps in range(rand.randint(0, len(sol))):
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
    #seed = iseed

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
    bestSolValue = None

    # number of iterations for the SA
    # initially, for the neighboors being created accordingly with the mean execution times,
    # we're going to use the number of tasks as the maximum number of iterations
    # because it does not make sense to iterate more than this
    #saIter = nbtasks
    # For randomic generation of neighboors:
    # the inital value was 100, and then 5k. 50k is the best value we found.
    saIter = 50000
    # intial temperature
    initTemp = 100.0
    # this can't be zero because there are some divisions for tempFinal
    finalTemp = 1.0
    # repetitions needed
    rep = 10

    temp = initTemp

    # We tested different cooling methods, but using the 2 we got the best results.
    tipo = 2

    # Executing the 10 repetitions, one with a different seed ranging from 0 to 10
    for r, seed in zip(range(rep), range(rep)):
        # first random solution
        oldBest = randomNeighboor(nbtasks, seed)
        oldBestValue = calcMakespan(oldBest, processingTimes, nbtasks, nbmachines)
        # remember to update the best one so far
        bestSol = oldBest
        bestSolValue = oldBestValue

        print("Execucao: "+str(r) + " Seed: "+str(seed))
        startTime = time.time()

        ite = 0
        while ( ite < saIter):
            # decreases the temperature
            temp = calcTemp(ite,saIter,initTemp,finalTemp,tipo)-1
            if( temp < 0):
                temp = 0

            # creates a new neighboor and checks its makespan
            newBest = newNeighboorRandIter(oldBest, ite)
            newBestValue = calcMakespan(newBest, processingTimes, nbtasks, nbmachines)

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
                    # As the temperature decreases,
                    # the chances of a worse solution be accepted also decreases.
                    oldBest = newBest
                    oldBestValue = newBestValue

        print("Final solution and value:")
        p.pprint(bestSol)
        p.pprint(bestSolValue)
        endTime = time.time() - startTime
        print("Execution time: "+str(endTime) + "\n")
