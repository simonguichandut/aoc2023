# imports
import numpy as np
from utils import *

# print(__file__)

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
grid = [['\\' if x=='\\' else x for x in line] for line in data]

# Ray direction
# north west south east: 1,2,3,4
#   1
# 2   4
#   3

objects = {
    '|':{1:[1],2:[1,3],3:[3],4:[1,3]},
    '-':{1:[2,4],2:[2],3:[2,4],4:[4]},
    '/':{1:[4],2:[3],3:[2],4:[1]},
    "\\":{1:[2],2:[1],3:[4],4:[3]}
}

def drdc(d):
    if   d==1: dr,dc = -1,0
    elif d==2: dr,dc = 0,-1
    elif d==3: dr,dc = 1,0
    elif d==4: dr,dc = 0,1
    else: assert False, d
    return dr,dc

def get_num(r0,c0,d0):

    queue = [(r0,c0,d0)] #(row,col,direction)
    visited = {}

    while queue:
        r,c,d = queue.pop(0)
        dr,dc = drdc(d)

        if 0<=r+dr<R and 0<=c+dc<C:
            # go there
            r += dr
            c += dc
            if (r,c) not in visited:
                visited[(r,c)] = []
            ob = grid[r][c]

            if ob=='.': # keep going same direction, from new current position
                if d not in visited[(r,c)]:
                    queue.append((r,c,d))
                    visited[(r,c)].append(d)

            else:
                for d in objects[ob][d]:
                    if d not in visited[(r,c)]:
                        queue.append((r,c,d))
                        visited[(r,c)].append(d)

    return len(visited)

print("Part 1: ", get_num(0,-1,4))

ans = 0
for r in range(R):
    ans = max(ans, get_num(r,-1,4))
    ans = max(ans, get_num(r,C,2))
for c in range(C):
    ans = max(ans, get_num(-1,c,3))
    ans = max(ans, get_num(R,c,1))
print("Part 2: ", ans)

## Printing the path
# path=[]
# for r in range(R):
#     path.append('')
#     for c in range(C):
#         if (r,c) in visited:
#             if grid[r][c] in '/\|-':
#                 path[-1]+=grid[r][c]
#             else:
#                 path[-1]+='#'
#         else:
#             path[-1]+='.'
# path='\n'.join(path)
# print(path)