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

ans1 = 0
ans2=0
for line in data:
    nums = line.split()
    nums = [int(x) for x in nums]

    last = [nums[-1]]
    first = [nums[0]]

    while nums.count(0) != len(nums):
        nums = [nums[i+1]-nums[i] for i in range(len(nums)-1)]
        last.append(nums[-1])
        first.append(nums[0])
    ans1 += sum(last)

    x=0
    for f in first[:-1][::-1]:
        x = f-x
    ans2+=x

print("Part 1: ", ans1)
print("Part 2: ", ans2)