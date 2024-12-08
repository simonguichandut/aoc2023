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
# data = open(input_file).read().strip().split('\n\n') # input data in blocks
# print(data)

times = [int(x) for x in data[0].split(':')[1].split()]
dist = [int(x) for x in data[1].split(':')[1].split()]
# print(times,dist)

ans = 0
nwins = []
for i in range(len(times)):
    nwin=0
    t=times[i]
    for j in range(t):
        if j*(t-j)>dist[i]:
            nwin+=1
    nwins.append(nwin)

print("Part 1: ",mul(nwins))

t = eval(''.join([str(t) for t in times]))
d = eval(''.join([str(t) for t in dist]))
# print(t,d)

nwins = 0
for j in range(t):
    if j*(t-j)>d:
        nwins+=1

print("Part 2: ",nwins)