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

data = open(input_file).read().strip().split('\n')

from functools import cache
@cache
def get_counts(row, nums, i=0, k=0, run=0):
    # i is the position in the row
    # k is the num we are interested in
    # run is the current run of #'s

    # If we are at the end of the row, check if we have a valid solution
    if i>len(row)-1: # means past the end of the row
        if k==len(nums) and run==0:
            # we have checked all nums and there is no room for more (last char is not #)
            # This is a valid case
            return 1
        elif k==len(nums)-1 and run==nums[k]:
            # we are checking the last num and the current run turns out to be the right length
            return 1
        else:
            return 0
        
    ## RECURSIVE PART
    # We traverse the row and increment i,k,run depending on what is going on
    count = 0 

    if row[i] in '.?':
        
        if run==0:
            # nothing to do, just go forward
            count += get_counts(row, nums, i+1, k, 0)

        elif k<=len(nums)-1 and run==nums[k]:
            # reached end of #'s and it was the correct length
            count += get_counts(row, nums, i+1, k+1, 0)

    if row[i] in '#?':
        # Try continuing the current run
        count += get_counts(row, nums, i+1, k, run+1)

    return count

# print(get_counts('???.###',[1,1,3]))
# print(get_counts('.??..??...?##.',[1,1,3]))
# print(get_counts('?###????????', [3,2,1]))

def get_answer(pt2=False):
    ans = 0
    for k,line in enumerate(data):
        row, nums = line.split()
        nums = [int(n) for n in nums.split(',')]

        if pt2:
            row = ((row+'?')*5)[:-1]
            nums*=5

        ans += get_counts(row,tuple(nums)) # tuple because lists are not hashable

    return ans

print("Part 1: ",get_answer())
print("Part 2: ",get_answer(pt2=True))




''' Initial brute force solve for part 1

def dmg_counts(row):
    counts = []
    n=0
    dmg=False
    for ch in row:
        if ch=='.':
            if dmg:
                counts.append(n)
                n=0 # reset counter
            dmg=False

        elif ch=='#':
            n+=1
            dmg=True

        else:
            assert False

    if dmg:
        counts.append(n)
    
    # print(counts)
    return counts

# dmg_counts("#.#.###")
# dmg_counts(".#...#....###.") 
# dmg_counts(".#.###.#.######")
# dmg_counts("####.#...#...")
# dmg_counts("#....######..#####.")
# dmg_counts(".###.##....#")

import itertools
def combs(n):
    yield from itertools.product(*(['#.'] * n))

# for x in combs(3):
#     print(x)

ans = 0
for k,line in enumerate(data):
    row, nums = line.split()
    nums = [int(n) for n in nums.split(',')]

    unknowns = [i for i in range(len(row)) if row[i]=='?']
    n = len(unknowns)

    for comb in combs(n):
        chars = [c for c in row]
        for i in range(n):
            chars[unknowns[i]] = comb[i]
        if dmg_counts(''.join(chars)) == nums:
            ans+=1

    print(f"{ans}, {k/len(data)*100:.2f}, %")

print("Part 1: ",ans)
'''