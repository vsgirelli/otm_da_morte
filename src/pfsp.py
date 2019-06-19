import sys
import random

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
    with open('../inputs/' + filename) as f:
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

    print(nbtasks)
    print(nbmachines)
    print(processingTimes)
    print(seed)

    return nbtasks, nbmachines, processingTimes, seed

# the initial random solution
def randomNeighboor(nbtasks, seed):
    #sol = list(range(0,nbtasks)) # list of integers from 0 to nbtasks-1
    #random.shuffle(sol)
    random.seed(seed)
    sol = random.sample(range(0, nbtasks), nbtasks)
    return sol


def makespan(sol, processingTimes, nbtasks, nbmachines):
    # list for the time passed until the finishing of the job
    cost = [0] * nbtasks
    # for each machine, total time passed will be updated
    for m in range(0, nbmachines):
        for t in range(nbtasks):
            # time passed so far until the task starts to process
            cost_so_far = cost[t]
            if t > 0:
                cost_so_far = max(cost[t - 1], cost[t])
            cost[t] = cost_so_far + processingTimes[sol[t]][m]
    return cost[nbtasks - 1]


# EXECUTION
if len(sys.argv) < 3:
    print("Usage: python3 pfsp.py inputFile seed")
    sys.exit(1)

nbtasks, nbmachines, processingTimes, seed = readInput()

solution = randomNeighboor(nbtasks, seed)
print(solution)
makespan = makespan(solution, processingTimes, nbtasks, nbmachines)
print(makespan)
