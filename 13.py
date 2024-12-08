# imports
import numpy as np
from utils import *
from copy import copy,deepcopy

print(__file__)

# command line call : python main.py <input_file>
import sys
if len(sys.argv)>1:
    input_file = sys.argv[1]
else:
    input_file = "test_input.txt"

##################################################

# data = open(input_file).read().strip().split('\n')
data = open(input_file).read().strip().split('\n\n') # input data in blocks

def vertical_mirror(grid, ignore=None):
    loc = {i for i in range(len(grid[0]))}
    for row in grid:
        potential = set()
        for c in range(1,len(row)):
            l,r = row[max(0,c-len(row)+c):c],row[c:c+c][::-1]
            # assert (len(l)==len(r))
            if  l==r and c!=ignore:
                potential.add(c)
        loc = loc.intersection(potential)

    if len(loc)==1:
        return loc.pop()
    return 0

def get_transposed(grid):
    return [''.join([x for x in line]) for line in transposed(grid)]

def get_ans(pt2=False):
    ans=0

    for grid in data:
        grid = grid.split('\n')
        gridt = get_transposed(grid)
        # print('\n'.join(grid))
        # print('\n'.join(gridt))

        locs = (vertical_mirror(grid),vertical_mirror(gridt))

        if pt2:

            locs_swap = locs
            i,j=0,0
            while locs_swap==locs or locs_swap==(0,0):

                if j==len(grid[0]):
                    i+=1
                    j=0
                if i==len(grid): 
                    print('\n'.join(grid))
                    assert False

                grid2=copy(grid)
                gridt2=copy(gridt)

                if grid[i][j]=='#':
                    grid2[i] = grid2[i][:j]+'.'+grid2[i][j+1:]
                else:
                    grid2[i] = grid2[i][:j]+'#'+grid2[i][j+1:]

                gridt2=get_transposed(grid2)
                locs_swap = (vertical_mirror(grid2, ignore=locs[0]),
                             vertical_mirror(gridt2, ignore=locs[1]))

                del grid2,gridt2
                j+=1

            # Get the one that has changed
            locs_swap = (locs_swap[0] if locs[0]!=locs_swap[0] else 0,
                        locs_swap[1] if locs[1]!=locs_swap[1] else 0)
            # print(locs,' -> ',locs_swap,'; swap at (i,j)=',i,j)
            locs = locs_swap

        ans += locs[0] + 100*locs[1]
    return ans

print("Part 1: ",get_ans())
print("Part 2: ",get_ans(pt2=True))
