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

data = open(input_file).read().strip().split('\n\n') # input data in blocks
instructions = data[0]

nodes = {}
for line in data[1].split('\n'):
    node,lr = line.split('=')
    node = node.strip()
    l,r = lr[2:5], lr[7:10]
    nodes[node] = (l,r)

def follow(initial):
    curr = initial
    for lr in instructions:
        i = 0 if lr=='L' else 1
        curr = nodes[curr][i]
        # print(curr)
    return curr

# follow(nodes,'AAA',instructions)

curr = 'AAA' # this only worked on the first test input
steps = 0
while curr!='ZZZ':
   curr = follow(curr)
   steps +=1
print("Part 1: ", steps*len(instructions))

# Part 2 simpler re-write
def one(initial):
    steps = 0
    curr = initial
    while curr[-1] != 'Z':
        curr = follow(curr)
        steps += 1
    return steps*len(instructions)

initials = [node for node in list(nodes.keys()) if node[-1]=='A']
from math import lcm
print("Part 2: ", lcm(*[one(ini) for ini in initials]))



# part 2
# def follow_many(nodes,initials):
#     currs = initials
#     for lr in instructions:
#         i = 0 if lr=='L' else 1
#         currs = [nodes[curr][i] for curr in currs]
#         # print(currs)
#     return currs

# currs = [el for el in list(nodes.keys()) if el[-1]=='A']
# print(currs,'\n')
# n0 = len(currs)
# # print(currs)
# # print(follow_many(currs))
# # print([el for el in currs if el[-1]=='Z'])
# steps = 0
# while len([el for el in currs if el[-1]=='Z']) != n0:
#     currs = follow_many(currs)
#     print(currs)
#     steps +=1
#     # break
# print(steps*len(instructions)) 

# This is taking too long, is it inherently cyclic though??
# Just keep going when we hit a Z but store the step
# initials = currs
# for ini in initials:
#     nz = [] # steps until Z
#     n = 0
#     curr = ini
#     while len(nz)<10:
#         curr = follow(curr)
#         n+=1
#         # print(curr)
#         if curr[-1] == 'Z':
#             nz.append(n*len(instructions))
#     print(ini, nz)
#     print(ini, [n/nz[0] for n in nz])

# All of them are cyclic!!
# So we want to find the first time all the cycle end
# in the same spot
# That's just the lowest common multiple of the cycle lengths

# steps = []
# for curr in currs:
#     n=0
#     while curr[-1]!='Z':
#         curr = follow(nodes,curr,instructions)
#         n+=1
#     steps.append(n*len(instructions))

# from math import lcm
# print(lcm(*tuple(steps)))