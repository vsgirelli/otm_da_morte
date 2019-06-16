import sys, getopt

seed = ''
inst = ''
try:
    opts, args = getopt.getopt(sys.argv, "f:s", ["seed=","file="])
except getopt.GetoptError:
    print("psfp.py -s <seed> -f <instance_file>")
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-s', "--seed"):
        seed = arg
    elif opt in ('-f', "--file"):
        inst = arg
print(seed)
print(inst)
