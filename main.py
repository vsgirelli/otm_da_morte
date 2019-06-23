#!/usr/bin/python3
import random as rand
import sys
import pprint as p
sys.path.insert(0, 'src/')
import pfsp

def readValues(filename):
    with open(filename) as f:
        return [int(elem) for elem in f.read().split()]

def readInput():
    inputFile = iter(readValues(sys.argv[1]))
    nbtasks = int(next(inputFile))
    nbmachines = int(next(inputFile))
    seed = sys.argv[2]
    processingTimes = []

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


if len(sys.argv) < 3:
    p.pprint("Usage: python3 pfsp.py inputFile seed")
    sys.exit(1)
        
nbtasks, nbmachines, processingTimes, seed = readInput()
pfsp.main(nbtasks, nbmachines, processingTimes, seed)
