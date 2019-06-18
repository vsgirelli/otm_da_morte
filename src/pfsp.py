import sys

if len(sys.argv) < 2:
    print("Usage: python3 pfsp.py inputFile")
    sys.exit(1)

def read_values(filename):
    with open('../inputs/' + filename) as f:
        return [int(elem) for elem in f.read().split()]

def read_input():
    inputFile = iter(read_values(sys.argv[1]))
    # number of jobs and machines
    nbtasks = int(next(inputFile))
    nbmachines = int(next(inputFile))

    # i-th job's processing time at j-th machine
    processingTime = []

    for i in range(nbtasks):
        temp = []
        for j in range(nbmachines):
            time = int(next(inputFile))
            time = int(next(inputFile))
            temp.append(time)
        processingTime.append(temp)

    print(nbtasks)
    print(nbmachines)
    print(processingTime)


read_input()
