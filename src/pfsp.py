#!/usr/bin/python3
import sys
import random
import numpy as np
import pprint as p

# number of jobs and machines
nbtasks = 0
nbmachines = 0
# i-th job's processing time at j-th machine
processingTimes = []
seed = 0

# For the SA, we need to keep track of the current and the old best solutions.
# They'll only represent the order in which the tasks should be executed.
# Ex: oldbest = [9, 3, 4, 1, 6, 2, 7, 0, 8, 5]
# is how the old best solution sheduled the tasks.
# When calculating the makespan, we're going to verify the execution times
# stored in processingTimes.
oldbest = []
newbest = []

def readValues(filename):
    with open(filename) as f:
        return [int(elem) for elem in f.read().split()]

def readInput():
    inputFile = iter(readValues(sys.argv[1]))
    nbtasks = int(next(inputFile))
    nbmachines = int(next(inputFile))
    seed = sys.argv[2]

    for i in range(nbtasks):
        temp = []
        for j in range(nbmachines):
            # this line is only to skip the machine's indicators in the inputFile
            time = int(next(inputFile))
            # the only thing we're interested about is the execution time
            time = int(next(inputFile))
            temp.append(time)
        processingTimes.append(temp)

    #print(nbtasks)
    #print(nbmachines)
    #print(processingTimes)
    #print(seed)

    return nbtasks, nbmachines, processingTimes, seed

# The initial random solution
def randomNeighboor(nbtasks, seed):
    random.seed(seed)
    sol = random.sample(range(0, nbtasks), nbtasks)
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

# Generates a better solution given a current solution.
# We will, in each iteration, change the order in which the tasks will be executed
# based on the tasks' mean execution time.
# Therefore, in the first iteration, the task with the smaller mean execution time
# will be swaped with the first task to be executed in the given solution.
# In the second iteration, the second smaller mean execution time will be swaped
# with the second task to be executed in the given solution, and so on.
def newNeighboor(sol, processingTimes, iteration):
    print("Initial random solution")
    p.pprint(sol)
    # just generating a numpy array with the processingTimes
    means = np.array(processingTimes)
    # taking the mean execution time for each task
    means = np.mean(means, axis = 1)

    print("Means:")
    p.pprint(means)

    indexes = np.argsort(means)
    print("indexes sorted")
    p.pprint(indexes)

    # swaps the iteration'th element of the solution with the
    # iteration'th smaller mean execution time
    sol[iteration], sol[indexes[iteration]] = sol[indexes[iteration]], sol[iteration]
    print("new swaped solution")
    p.pprint(sol)
    return sol

# EXECUTION
if len(sys.argv) < 3:
    p.pprint("Usage: python3 pfsp.py inputFile seed")
    sys.exit(1)

# reads the input and initializes the variables
nbtasks, nbmachines, processingTimes, seed = readInput()

#p.pprint(processingTimes)
# first random solution
solution = randomNeighboor(nbtasks, seed)
# calculating the makespan
makespan = calcMakespan(solution, processingTimes, nbtasks, nbmachines)
#p.pprint(makespan)
# generating a better solution
for iteration in range(0,(nbtasks//2)):
    solution = newNeighboor(solution, processingTimes, iteration)
    makespan = calcMakespan(solution, processingTimes, nbtasks, nbmachines)
    print("Makespan:")
    print(makespan)
