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
steps = open(input_file).read().strip().split(',')

ans=0
for step in steps:
    curr=0
    for ch in step:
        curr = (curr + ord(ch))*17%256
    ans+=curr
print("Part 1: ",ans)

from collections import defaultdict
boxes = defaultdict(dict)
for step in steps:
    curr=0
    for i,ch in enumerate(step):
        if ch in '-=': break
        curr = (curr + ord(ch))*17%256
    box=int(curr)
    lenn = step[:i]
    if step[i]=='=':
        boxes[box][lenn] = int(step[i+1:])
    else:
        if lenn in boxes[box]:
            del boxes[box][lenn]

ans=0
for box,lens in boxes.items():
    for i,lenn in enumerate(lens):
        ans += (box+1) * (i+1) * boxes[box][lenn]
print("Part 2: ",ans)



