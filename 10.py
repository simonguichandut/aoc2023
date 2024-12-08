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

##################################################

grid = open(input_file).read().strip().split('\n')

# Better solution (for part 1) after having seen others
# This is to make sure I undertand how to code BFS

# find starting position
for j,line in enumerate(grid):
    if 'S' in line:
        i = line.index('S')
        start = (i,j)
        break

visited = [start]
queue = [start]

while queue:
    i,j = queue.pop(0)
    ch = grid[j][i]

    # Try going up
    ib,jb = i,j-1
    if jb>=0 and ch in 'S|JL' and grid[jb][ib] in '|7F' and (ib,jb) not in visited:
        queue.append((ib,jb))
        visited.append((ib,jb))

    # down
    ib,jb = i,j+1
    if jb<=len(grid)-1 and ch in 'S|F7' and grid[jb][ib] in '|JL' and (ib,jb) not in visited:
        queue.append((ib,jb))
        visited.append((ib,jb))

    # left
    ib,jb = i-1,j
    if ib>=0 and ch in 'S-7J' and grid[jb][ib] in '-FL' and (ib,jb) not in visited:
        queue.append((ib,jb))
        visited.append((ib,jb))

    # right
    ib,jb = i+1,j
    if ib<=len(grid[0])-1 and ch in 'S-FL' and grid[jb][ib] in '-J7' and (ib,jb) not in visited:
        queue.append((ib,jb))
        visited.append((ib,jb))

print("Part 1: ", int(len(visited)/2))

"""
def possible_movement(A,B,lA_overwrite=None): # origin, destination, (i,j) coords

    # check if destination is inside grid
    if B[0]<0 or B[0]>=len(grid[0]):
        return False
    if B[1]<0 or B[1]>=len(grid):
        return False

    # letters
    lA,lB = grid[A[1]][A[0]],grid[B[1]][B[0]]

    if lA_overwrite is not None:
        lA = lA_overwrite

    if lA=='S':
        return possible_movement(A,B,'-') or \
                possible_movement(A,B,'|') or \
                possible_movement(A,B,'7') or \
                possible_movement(A,B,'J') or \
                possible_movement(A,B,'F') or \
                possible_movement(A,B,'L')

    if lA=='-':
        # if B[1]!=A[1]: return False
        if B[0]==A[0]+1: # right
            if lB in ('-','J','7'): return True
        elif B[0]==A[0]-1: # left
            if lB in ('-','L','F'): return True
    elif lA=='|':
        # if B[0]!=A[0]: return False
        if B[1]==A[1]-1: # up
            if lB in ('|','F','7'): return True
        elif B[1]==A[1]+1: # down
            if lB in ('|','L','J'): return True

    elif lA=='L':
        if B[0]==A[0]+1 and lB in ('-','J','7'): return True # right
        elif B[1]==A[1]-1 and lB in ('|','F','7'): return True # up
    
    elif lA=='J':
        if B[0]==A[0]-1 and lB in ('-','F','L'): return True # left
        elif B[1]==A[1]-1 and lB in ('|','F','7'): return True # up

    elif lA=='F':
        if B[0]==A[0]+1 and lB in ('-','7','J'): return True # right
        elif B[1]==A[1]+1 and lB in ('|','J','L'): return True # down

    elif lA=='7':
        if B[0]==A[0]-1 and lB in ('-','L','F'): return True # left
        elif B[1]==A[1]+1 and lB in ('|','J','L'): return True # down

    return False

# find starting position
for j,line in enumerate(grid):
    if 'S' in line:
        i = line.index('S')
        start = (i,j)
        break

visited = {}
queue = [(start,0)]
paths = ['S']
longest_path = 'S'

while len(queue)>0:
    # print(queue)
    pos, d = queue.pop(0)
    path = paths.pop(0)
    if len(path)>len(longest_path): longest_path=path

    if pos in visited:
        continue
    visited[pos]=d


    i,j = pos
    for mv in [(0,1),(0,-1),(1,0),(-1,0)]:
        ib,jb = i+mv[0],j+mv[1]
        if possible_movement((i,j),(ib,jb)):
            queue.append(((ib,jb),d+1))
            paths.append(path+grid[jb][ib])


# print(max(paths,key=len))
print("Part 1: ",max(visited.values()))
# print(longest_path)
# print(visited)

"""

# Part 2: area that is bounded by the path
# Will rely on the fact that having started BFS at S, we must
# have *only* visited things that are in the path
# That is to say that the visited dict only contains the actual path

# Now the trick (thanks reddit), is from geometry
# The loop is just a twisted un-knot. A cell is bounded by the loop if
# the number of path walls it sees to its left is odd. Otherwise, it's not bounded
# We must consider only *north* facing walls (|,J,L, but not -,F,7)
# One subtle point is that S is a 7 in the test input, and a J in the real input (just by visual inspection)

Spipe = '7' if "test" in input_file else "J"
# print("S is assumed to be a ",Spipe," pipe")

# print('\n'.join([''.join(['x' if (i,j) in visited else '.' for i in range(len(grid[0]))]) for j in range(len(grid))]))

map = []
area = 0

for j,line in enumerate(grid):
    map.append('')
    nwalls = 0 

    for i in range(len(line)):
        if (i,j) in visited:
            pipe = grid[j][i]
            map[-1]+=pipe

            if pipe=='S': pipe=Spipe

            if pipe in ('|','J','L'):
                nwalls+=1
                

        else:
            if nwalls%2 == 0:
                map[-1]+='.'
            else:
                map[-1]+='x'

map = '\n'.join([line for line in map])
# print(map)
print("Part 2: ", map.count('x'))
open("pipe_map.txt",'w').write(map)



"""
def possible_movement(A,B): # origin, destination, (i,j) coords

    # check if destination is inside grid
    if B[0]<0 or B[0]>=len(grid[0]):
        return False
    if B[1]<0 or B[1]>=len(grid):
        return False

    # letters
    lA,lB = grid[A[1]][A[0]],grid[B[1]][B[0]]

    # if lB=='S': 
    #     print('hello')

    if lA=='S' or lB=='S': return True

    if lB=='.': return False

    if lA=='-':
        if B[1]!=A[1]: return False
        if B[0]==A[0]+1: # right
            if lB in ('-','J','7'): return True
        elif B[0]==A[0]-1: # left
            if lB in ('-','L','F'): return True
    elif lA=='|':
        if B[0]!=A[0]: return False
        if B[1]==A[1]-1: # up
            if lB in ('-','J','7'): return True
        elif B[1]==A[1]+1: # down
            if lB in ('|','L','F'): return True

    elif lA=='L':
        if B[0]==A[0]+1 and lB in ('-','J','7'): return True
        elif B[1]==A[1]-1 and lB in ('|','F','7'): return True
    
    elif lA=='J':
        if B[0]==A[0]-1 and lB in ('-','F','L'): return True
        elif B[1]==A[1]-1 and lB in ('|','F','7'): return True

    elif lA=='F':
        if B[0]==A[0]+1 and lB in ('-','7','J'): return True
        elif B[1]==A[1]+1 and lB in ('|','J','L'): return True

    elif lA=='7':
        if B[0]==A[0]-1 and lB in ('-','L','F'): return True
        elif B[1]==A[1]+1 and lB in ('|','J','L'): return True

    return False


# find starting position
for j,line in enumerate(grid):
    if 'S' in line:
        i = line.index('S')
        break

# print(i,j)

# visited = [[(i,j)]]
# queue = [(i,j)]
# paths = ['S']

# start = True

# while True:
#     print(queue, paths)

#     i,j = queue.pop(0) # takes first element in the queue
#     path = paths.pop(0)
#     vis = visited.pop()
#     if not start and path[-1] == 'S':
#         break

#     for mv in ([(0,1),(0,-1),(1,0),(-1,0)]):
#         ib,jb = i+mv[0],j+mv[1]
#         if ib<0: 
#             continue
#         if (ib,jb) not in vis:
#             if start or possible_movement((i,j),(ib,jb)):
#                 #visited.append((ib,jb))
#                 visited.append(vis + [(ib,jb)])
#                 queue.append([ib,jb])
#                 paths.append(path + grid[jb][ib])

#     start = False

i0,j0 = i,j
good_paths = []
found = False
for fmv in ([(0,1),(0,-1),(1,0),(-1,0)]):
    if found: break

    ib,jb = i0+fmv[0],j0+fmv[1]
    # print(ib,jb)
    if ib<0:
        continue
    if possible_movement((i0,j0),(ib,jb)):
        #visited = [(i0,j0),(ib,jb)]
        visited = [(ib,jb)]
        queue = [(ib,jb)]
        paths = ['S'+grid[jb][ib]]
        # print(paths)

        start=True
        i,j = i0,j0

        while True:
            # print(queue, paths)
            if len(queue)==0: break

            i,j = queue.pop(0) # takes first element in the queue
            path = paths.pop(0)
            print(path)

            if not start and path[-1] == 'S':
                found=True
                good_paths.append(path)
                break

            if (i0,j0) in visited:
                assert False

            for mv in ([(0,1),(0,-1),(1,0),(-1,0)]):
                ib,jb = i+mv[0],j+mv[1]

                if ib<0: 
                    continue

                # if not start and grid[jb][ib]=='S':
                #     found=True
                #     good_paths.append(path)
                #     break
                
                if (ib,jb) not in visited:
                    if possible_movement((i,j),(ib,jb)):

                        if grid[jb][ib]=='S':
                            if not start:
                                # found=True
                                good_paths.append(path)
                                break

                        else:

                            visited.append((ib,jb))
                            # visited.append(vis + [(ib,jb)])
                            queue.append([ib,jb])
                            paths.append(path + grid[jb][ib])

            start = False

# print(path)
print(good_paths)
print("Part 1: ", int((len(max(good_paths,key=len))/2)))
"""