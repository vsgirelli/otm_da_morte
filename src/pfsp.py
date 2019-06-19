#!/usr/bin/python3
import sys
import random

# number of jobs and machines
nbtasks = 0
nbmachines = 0
# i-th job's processing time at j-th machine
processingTimes = []

# For the SA, we need to keep track of the current and the old best solutions.
# They'll only represent the order in which the tasks should be executed.
# Ex: oldbest = [9, 3, 4, 1, 6, 2, 7, 0, 8, 5]
# is how the old best solution sheduled the tasks.
# When calculating the makespan, we're going to verify the execution times
# stored in processingTimes.
oldbest = []
newbest = []

def read_values(filename):
    with open('../inputs/' + filename) as f:
        return [int(elem) for elem in f.read().split()]

def read_input(nbtasks, nbmachines, processingTimes):
    problem = []

    inputFile = iter(read_values(sys.argv[1]))
    nbtasks = int(next(inputFile))
    nbmachines = int(next(inputFile))

    for i in range(nbtasks):
        temp = []
        for j in range(nbmachines):
            # this line is only to skip the machine's indicators in the inputFile
            time = int(next(inputFile))
            # the only thing we're interested about is the execution time
            time = int(next(inputFile))
            temp.append(time)
        processingTimes.append(temp)

    print(nbtasks)
    print(nbmachines)
    print(processingTimes)

    return nbtasks, nbmachines, processingTimes

# the initial random solution
def random_neighboor(n):
    #sol = list(range(0,nbtasks)) # list of integers from 0 to nbtasks-1
    #random.shuffle(sol)
    sol = random.sample(range(0, n), n)
    return sol

# calculates the makespan
def makespan(sol, nbtasks, nbmachines, processingTimes):
    # list for the time passed until the finishing of the job
    cost = [0] * nbtasks
    # for each machine, update the time passed
    for m in range(0, nbmachines):
        for t in range(0, nbtasks):
            # time passed so far until the tast starts to run
            costSoFar = cost[t]

            # except for the first task
            if t > 0:
                costSoFar = max(cost[t - 1], cost[t])
            # adds to the cost of t the time it took so far plus the time to process t in m
            cost[t] = costSoFar + processingTimes[sol[t]][m]

    # returns the last cost calculated
    return cost[nbtasks - 1]


# EXECUTION
if len(sys.argv) < 2:
    print("Usage: python3 pfsp.py inputFile")
    sys.exit(1)

nbtasks, nbmachines, processingTimes = read_input(nbtasks, nbmachines, processingTimes)

solution = random_neighboor(nbtasks)
print(solution)

makespan = makespan(solution, nbtasks, nbmachines, processingTimes)
print(makespan)
