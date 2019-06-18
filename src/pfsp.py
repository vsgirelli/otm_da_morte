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
    problem.append(nbtasks)
    problem.append(nbmachines)

    for i in range(nbtasks):
        temp = []
        for j in range(nbmachines):
            # this line is only to skip the machine's indicators in the inputFile
            time = int(next(inputFile))
            # the only thing we're interested about is the execution time
            time = int(next(inputFile))
            temp.append(time)
        processingTimes.append(temp)
    problem.append(processingTimes)

    print(nbtasks)
    print(nbmachines)
    print(processingTimes)

    return problem

# the initial random solution
def random_neighboor(n):
    #sol = list(range(0,nbtasks)) # list of integers from 0 to nbtasks-1
    #random.shuffle(sol)
    sol = random.sample(range(0, n), n)
    return sol



# EXECUTION
if len(sys.argv) < 2:
    print("Usage: python3 pfsp.py inputFile")
    sys.exit(1)

problem = read_input(nbtasks, nbmachines, processingTimes)
nbtasks = problem[0]
nbmachines = problem[1]
processingTimes = problem[2]

solution = random_neighboor(nbtasks)
print(solution)
