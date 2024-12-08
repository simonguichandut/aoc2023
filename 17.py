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
grid = [[int(x) for x in line] for line in data]

from collections import defaultdict
# unvisited = defaultdict(lambda: float('inf'))

# Directions in the complex plane
#      ^
#     -j
# <-1    +1>
#     +j
#      v

# def neighbors(pos,d,n):
#     new_directions = {0-1j, 0+1j, -1+0j, 1+0j} - {-d}  # not possible to go back
#     if n>=3:
#         new_directions -= {d} # cant keep going straight
#     neighbors = []
#     for nd in new_directions:
#         np = pos+nd
#         if 0<=np.real<C and 0<=np.imag<R:
#             neighbors.append((np,nd,n+1 if nd==d else 1))
#     return neighbors

def neighbors1(pos,d,n):
    new_directions = {(-1,0),(1,0),(0,-1),(0,1)} - {(-d[0],-d[1])}  # not possible to go back
    if d==(0,0):
        new_directions = {(1,0),(0,1)} # starting state, can go right or down
    elif n>=3:
        new_directions -= {d} # cant keep going straight
    neighbors = []
    for nd in new_directions:
        np = (pos[0]+nd[0],pos[1]+nd[1])
        if 0<=np[0]<R and 0<=np[1]<C:
            neighbors.append((np, nd, n+1 if nd==d else 1))
    return neighbors

def neighbors2(pos,d,n):
    new_directions = {(-1,0),(1,0),(0,-1),(0,1)} - {(-d[0],-d[1])}  # not possible to go back
    if d==(0,0):
        new_directions = {(1,0),(0,1)} # starting state, can go right or down
    elif n<4:
        new_directions = {d} # have to keep going straight
    elif n>=10:
        new_directions -= {d} # cannot keep going straight

    neighbors = []
    for nd in new_directions:
        np = (pos[0]+nd[0], pos[1]+nd[1])
        if 0<=np[0]<R and 0<=np[1]<C:
            neighbors.append((np, nd, n+1 if nd==d else 1))
    return neighbors

# import matplotlib.pyplot as plt
# plt.figure()
# plt.gca().set_aspect('equal')
# y=np.arange(0,R)
# x=np.arange(0,C)
# xx,yy = np.meshgrid(x,y)
# Z=np.ones((C,R))
# plt.scatter(xx,yy,Z)
# plt.gca().invert_yaxis()
# plt.scatter(0,0,100)

import heapq
def djikstra(neighbors, start=(0,0), end=(R-1,C-1), pt2=False):

    visited = set()

    # Initial state    
    pos = start
    d = (0,0)
    n = 0
    distance = 0

    queue = [(distance,pos,d,n)]

    while queue:
        distance,pos,d,n = heapq.heappop(queue)
        # print(distance,pos,d,n)
       
        if pos==end:
            if not pt2:
                return distance
            else:
                if n>=4:
                    return distance

        
        if (pos,d,n) in visited:
            # print('seen')
            continue
        visited.add((pos,d,n))

        # plt.scatter(pos[1],[pos[0]],200,color='c')
        # plt.text(pos[1],pos[0],distance,ha='center',va='center',fontweight='bold')
        # plt.pause(0.1)
        
        for neigh in neighbors(pos,d,n):
            new_pos = neigh[0]
            new_distance = distance + grid[new_pos[0]][new_pos[1]]
            heapq.heappush(queue, (new_distance, new_pos, neigh[1], neigh[2]))

    return float('inf')


print("Part 1: ", djikstra(neighbors1))
print("Part 2: ", djikstra(neighbors2, pt2=True))
# plt.show()









