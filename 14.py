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

grid = open(input_file).read().strip().split('\n')
R,C = len(grid),len(grid[0])

def rot_counterclock(matrix):
    # 90 degrees counter-clockwise
    return [''.join(r) for r in zip(*matrix)][::-1]

def rot_clock(matrix):
    # 90 degrees clockwise
    return [''.join(r) for r in zip(*matrix[::-1])]

def print_grid(g):
    print('\n'.join([line for line in g]))

def tilt_west(grid):
    new_grid = []
    for line in grid:
        new_line = ''
        isq = [-1]+[i for i in range(len(line)) if line[i]=='#']+[len(line)]

        for k in range(1,len(isq)):
            block=line[isq[k-1]+1:isq[k]]
            nO = block.count('O')
            new_line += 'O'*nO + '.'*(len(block)-nO)+'#'
        
        new_line = new_line[:-1]
        new_grid.append(new_line)
    return new_grid

# Some tests
# print_grid(rot_counterclock(grid))
# print('')
# print_grid(rot_clock(rot_counterclock(grid)))
# assert rot_counterclock(rot_counterclock(rot_counterclock(rot_counterclock(grid))))==grid

# Test example
# print_grid(rot_clock(tilt_west(rot_counterclock(grid))))

def get_load(grid):
    # Assuming a properly oriented grid, calculate north beam load
    ans = 0
    for line in rot_counterclock(grid):
        ans += sum([R-i for i in range(R) if line[i]=='O'])
    return ans

print("Part 1: ", get_load(rot_clock(tilt_west(rot_counterclock(grid)))))


def spin(grid):
    for _ in range(4):
        grid=tilt_west(grid)
        grid=rot_clock(grid)
    return grid

# Start with one overall rotation
grid0=rot_counterclock(grid)

# Figure out the cycling
grid=grid0
saved_grids=[grid]
start_cycle = False
i0,cycle=0,0
for i in range(1000000000):
    grid=spin(grid)
    if grid in saved_grids:
        if not start_cycle:
            i0 = i
            start_cycle=True
            saved_grids=[]
        else:
            cycle=i-i0
            break
    saved_grids.append(grid)

# print(i0,cycle)

grid=grid0
for _ in range(i0):
    grid=spin(grid)
for _ in range((1000000000-i0)%cycle):
    grid=spin(grid)

print("Part 2: ", get_load(rot_clock(grid)))




