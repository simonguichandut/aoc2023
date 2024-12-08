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

data = open(input_file).read().strip().split('\n')
R,C = len(data),len(data[0])
ans = res = 0
##################################################
def get_answer(pt2):
    perim = 0
    vert = [[0,0],]
    pos = [0,0] # x,y
    for line in  data:
        d,n,hex = line.split()

        if pt2:
            hex = hex[2:-1]
            n = int(hex[:-1],16)
            d = hex[-1]

        if d in ('R','0'):
                pos[0]+=int(n)
        elif d in ('D','1'):
                pos[1]-=int(n)
        elif d in ('L','2'):
                pos[0]-=int(n)
        else:
                pos[1]+=int(n)

        vert.append(pos[:])
        perim+=int(n)
    
    shoelace = 0.5*sum((vert[i][1]+vert[i+1][1])*(vert[i][0]-vert[i+1][0]) for i in range(len(vert)-1))
    # need to account for the perimeter as well, though its not trivial
    # this worked on the test input, and magically on the real input as well!
    # It turns out this is called pick's theorem
    # https://en.wikipedia.org/wiki/Shoelace_formula
    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    return int(abs(shoelace) + perim/2 + 1)

# import matplotlib.pyplot as plt
# for i,c in enumerate(corners):
#     plt.scatter(c[0],c[1],10,color='k')
#     if i>=1:
#         plt.plot([corners[i-1][0],corners[i][0]],[corners[i-1][1],corners[i][1]],'k-')
# plt.show()

print("Part 1: ", get_answer(False)) 
print("Part 2: ", get_answer(True)) 