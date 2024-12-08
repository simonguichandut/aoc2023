# imports

import numpy as np
from utils import *

print(__file__)

# command line call : python main.py <input_file>
import sys
if len(sys.argv)>1:
    input_file = sys.argv[1]
else:
    input_file = "test_input.txt"

##################################################

data = open(input_file).read().strip().split('\n')
nr,nc = len(data), len(data[0])

# Locations of galaxies
locs = []
for r,line in enumerate(data):
    for c,ch in enumerate(data[r]):
        if ch=='#':
            locs.append((r,c))

# Cartesian coordinate of each point, considering expansion
def get_xy(expansion):

    x = np.array([i*np.ones(nr) for i in range(nc)]).T
    y = np.array([i*np.ones(nc) for i in range(nr)])


    for r,row in enumerate(data):
        if '#' not in row:
            # print(r)
            y[r+1:,:]+=expansion

    for c in range(len(data[0])):
        col = [data[r][c] for r in range(nr)]
        if '#' not in col:
            x[:,c+1:]+=expansion
    
    return x,y

def calc_sum(expansion):
    x,y = get_xy(expansion)
    S=0
    for i,loc1 in enumerate(locs):
        for _,loc2 in enumerate(locs[i+1:]):
            x1,y1 = x[loc1[0],loc1[1]], y[loc1[0],loc1[1]]
            x2,y2 = x[loc2[0],loc2[1]], y[loc2[0],loc2[1]]
            S+=abs(x2-x1)+abs(y2-y1)

    return int(S)

print("Part 1: ", calc_sum(expansion=1))
if "test" in input_file:
    print("Test cases for part 2:")
    # Not sure why the -1 has to be there but it does to get the right answer
    print("Expansion 10: ", calc_sum(expansion=10-1))
    print("Expansion 100: ", calc_sum(expansion=100-1))
else:
    print("Part 2: ", calc_sum(expansion=1_000_000-1)) 