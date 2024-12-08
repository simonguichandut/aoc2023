# imports
import numpy as np
from utils import *

# debug
#dbg = True
dbg = False

def main(input_file):
    data = open(input_file).read().strip().split('\n')
    # print(data)
    tot = 0
    ncards=[1 for _ in range(len(data))]
    for i,line in enumerate(data):
        ll = line.split(":")[1]
        win,my = ll.split('|')
        win = win.strip().split(' ')
        my = my.strip().split(' ')

        # print(win,my)
        win = list(filter(None,win))
        my = list(filter(None,my))
        # print(win,my)
        # print(win)
        # print(my)
        # print('\n')
        good = []
        for m in my:
            if m in win:
                if m not in good:
                    good.append(m)

        if len(good)>=1:
            # print(len(good),'good cards')
            tot+=2**(len(good)-1)

            for j in range(len(good)):
                ii = i+j+1
                ncards[ii] += ncards[i]
            # print(ncards)

    # 33105

    print("Part 1: ",tot)
    print("Part 2: ",sum(ncards))


# command line call : python main.py <input_file>
import sys
if __name__ == "__main__":
    if len(sys.argv)==2:
        input_file = sys.argv[1]
    else:
        input_file = "test_input.txt"
    main(input_file)
