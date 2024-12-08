import sys
import numpy as np
from utils import *
print(__file__)
input_file = sys.argv[1] if len(sys.argv)>1 else "test_input.txt"

data = open(input_file).read().strip().split('\n')
R,C = len(data),len(data[0])
ans = res = 0
##################################################
grid = [[c for c in line] for line in data]

''' This works for part 1, but it probably shouldnt. Why BFS instead of DFS??
start = (0, grid[0].index('.'), 0,0,0) # last 2 is dr dc of last movement
end = (R-1, grid[-1].index('.'))
visited = [start]
queue = [start]
hikes = []
while queue:
    r0,c0,dr0,dc0,dist = queue.pop(0)
    ch = grid[r0][c0]

    # print(r0,c0,dr0,dc0,dist)
    if (r0,c0)==end:
        print(dist)
        hikes.append(dist)

    possible_directions = {(1,0),(-1,0),(0,1),(0,-1)}
    match ch:
        case '>':
            possible_directions = {(0,1)}
        case '<':
            possible_directions = {(0,-1)}
        case '^':
            possible_directions = {(-1,0)}
        case 'v':
            possible_directions = {(1,0)}

    possible_directions -= {(-dr0,-dc0)}

    for (dr,dc) in possible_directions:
        r,c = r0+dr,c0+dc
        if 0<=r<R and 0<=c<C and grid[r][c]!='#' and (r,c,dr,dc,dist+1) not in visited:
            queue.append((r,c,dr,dc,dist+1))
            visited.append((r,c,dr,dc,dist+1))

# print(visited)
# print(hikes)
print("Part 1: ", max(hikes))
'''

start = (0, grid[0].index('.'))
end = (R-1, grid[-1].index('.'))

sys.setrecursionlimit(10000)
def dfs(node=start, visited=set(), path=[], hikes=[0], pt2=False, print_max=False):
    r,c = node
    ch = grid[r][c]

    visited.add(node)
    path.append(node)

    if (r,c)==end:
        d=len(visited)-1
        if d>max(hikes) and print_max:
            print(d)
        hikes.append(d)

    else:
        possible_directions = {(1,0),(-1,0),(0,1),(0,-1)}

        # Slopes
        if not pt2:
            match ch:
                case '>':
                    possible_directions = {(0,1)}
                case '<':
                    possible_directions = {(0,-1)}
                case '^':
                    possible_directions = {(-1,0)}
                case 'v':
                    possible_directions = {(1,0)}

        for (dr,dc) in possible_directions:
            if 0<=r+dr<R and 0<=c+dc<C and grid[r+dr][c+dc]!='#' and (r+dr,c+dc) not in visited:
                dfs((r+dr,c+dc), visited, path, hikes, pt2, print_max)

    path.pop()
    visited.remove(node)

    return hikes

# print_max = 'test' not in input_file # this keeps track of our current progress
# print("Part 1: ", max(dfs(print_max=print_max)))
# print("Part 2: ", max(dfs(pt2=True, print_max=print_max)))  # Takes an 1.5 hr to get to the right answer (6590)

""" Unfinished implementation
# Get graph with only intersections, via BFS
graph = {start:{}}
r0,c0 = start
visited = [(start,r0,c0)] # restrict to points visited from the current node
queue = [(start,r0,c0,0,0,0)] # with root node, r,c,dr,dr,dist
while queue:
    root,r0,c0,dr0,dc0,dist = queue.pop(0)
    # print(root,r0,c0,dr0,dc0,dist)

    if (r0,c0)==end:
        graph[root][(r0,c0)] = dist
        # print("end: ",root,end,dist)
        break # can safely exit here because there's only one path to the end node

    neighbors = []
    possible_directions = {(1,0),(-1,0),(0,1),(0,-1)} - {(-dr0,-dc0)}
    for (dr,dc) in possible_directions:
        if 0<=r0+dr<R and 0<=c0+dc<C and grid[r0+dr][c0+dc]!='#' and (root,r0+dr,c0+dc) not in visited:
            neighbors.append((r0+dr, c0+dc, dr, dc))

    if len(neighbors)>1: 
        # We are at an intersection, save the distance from previous root, and start as a new root
        graph[root][(r0,c0)] = dist
        root = (r0,c0)
        graph[root] = {}
        dist = 1
    else:
        dist = dist+1

    for n in neighbors:
        r,c,dr,dc = n
        queue.append((root, r, c, dr, dc, dist))
        visited.append((root,r,c))

for key,val in graph.items():
    print(key,val)
"""
