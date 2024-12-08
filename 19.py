import sys
import numpy as np
import copy
from utils import *
print(__file__)
input_file = sys.argv[1] if len(sys.argv)>1 else "test_input.txt"

data = open(input_file).read().strip().split('\n')
R,C = len(data),len(data[0])
ans = res = 0
##################################################
work,parts = open(input_file).read().strip().split('\n\n')
work = work.split('\n')
parts = parts.split('\n')

names = [w.split('{')[0] for w in work]
i0 = names.index('in') # the starting workflow

def valid_part(x,m,a,s):
    i=i0
    while True:
        checks = work[i].split('{')[1][:-1].split(',')
        for k,chk in enumerate(checks):
            if k==len(checks)-1:
                condition,go = 'True',chk
            else:
                condition,go = chk.split(':')
                
            if eval(condition):
                if go=='A':
                    return True
                elif go=='R':
                    return False
                else:
                    i = names.index(go) # which workflow to go next
                break
    return False

ans=0
for part in parts:
    part=part[1:-1].split(',')
    (x,m,a,s) = [int(part[i].split('=')[1]) for i in range(4)]
    if valid_part(x,m,a,s):
        ans += x+m+a+s
print("Part 1", ans)



######## Part 2
# Need to do some range splitting

# a silly function to invert 0 and 1 (0->1, 1->0)
switch = lambda x: int(abs(2**x-2))

accepted_ranges = []

def cut_range(i, range_dict):
    checks = work[i].split('{')[1][:-1].split(',')
    for k,chk in enumerate(checks):

        if k==len(checks)-1:
            if chk=='A': # we are done, this is a valid range
                accepted_ranges.append(range_dict)

            elif chk=='R':
                return # nothing to do

            else: # we pass this range to another workflow
                i = names.index(chk)
                cut_range(i, range_dict)

        else:
            condition, go = chk.split(':')
            letter = [let for let in 'xmas' if let in condition][0]
            sign,num = condition[1], int(condition[2:])
            # print(letter,sign,num)
            # which boundary we are considering
            b = 0 if sign=='>' else 1

            # Cut up according to true case
            # We'll either send this back recursively to a new workflow, or accept directly
            accept_dict = copy.deepcopy(range_dict)
            accept_dict[letter][b] = num+1 if sign=='>' else num-1

            if go=='A':
                # Accept the true case as a valid range
                accepted_ranges.append(accept_dict)

            elif go=='R':
                pass

            else:
                # Send to new workflow
                i = names.index(go)
                cut_range(i, accept_dict)

            # put the false case back into the loop to check the next evaluation in this workflow
            range_dict[letter][switch(b)] = num # note the false case is always <= or >=, so we take num not num+-1

cut_range(i0, {'x':[1,4000],'m':[1,4000],'a':[1,4000],'s':[1,4000]})
ans=0
for r in accepted_ranges:
    # print(r)
    # add the hypervolume to the answer
    # This assumes all of the 4d regions do not intersect anywhere, which is true 
    ans += mul([lims[1]-lims[0]+1 for lims in r.values()]) 
print("Part 2: ", ans)


