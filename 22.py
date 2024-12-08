import sys
import os
import pickle
import numpy as np
from utils import *
print(__file__)
input_file = sys.argv[1] if len(sys.argv)>1 else "test_input.txt"

data = open(input_file).read().strip().split('\n')
R,C = len(data),len(data[0])
ans = res = 0
##################################################
bricks = []
bricks2 = []
for line in data:
    p1,p2 = line.split('~')
    brick = [[int(x) for x in p1.split(',')], [int(x) for x in p2.split(',')]]
    brick = sorted(brick, key=lambda x: x[2]) # sort by z coordinate
    # print(brick)
    bricks.append(brick)

    # bricks 2 contains all the coordinates of that brick
    bricks2.append([])
    b = brick
    xcoords,ycoords,zcoords = [], [], []
    diff = [j for j in range(3) if b[0][j]!=b[1][j]]
    if len(diff)==0:
        # means we have a single cube
        bricks2[-1] = [(b[0][0],b[0][1],b[0][2])]
        
    else:
        idir = diff[0]
        length = b[1][idir] - b[0][idir]
        sign = int(length/abs(length)) # returns 1 or -1
        for c in range(b[0][idir], b[0][idir]+length+sign, sign):
            xcoords.append(b[0][0])
            ycoords.append(b[0][1])
            zcoords.append(b[0][2])
            
            # Change the one that has changed
            if idir==0:   xcoords[-1]=c
            elif idir==1: ycoords[-1]=c
            elif idir==2: zcoords[-1]=c

        # print(xcoords,ycoords,zcoords)
        for x,y,z in zip(xcoords,ycoords,zcoords):
            bricks2[-1].append((x,y,z))

# bricks = sorted(bricks, key=lambda brick: brick[0][2])
bricks = bricks2
bricks = sorted(bricks, key=lambda x: x[0][2])
N = len(bricks)

# Fall down
def fall(bricks, return_possible=False, return_fall_count=False):

    fell = set()

    while True:
        moved = False

        # all_coords = {c for brick in bricks2 for c in brick}

        for i,brick in enumerate(bricks):

            # check if a brick can go down one
            new_coords = [(x,y,z-1) for x,y,z in brick]

            possible = True
            for new in new_coords:
                if new[2]<0:
                    possible=False
                    break
                for j,other_brick in enumerate(bricks):
                    if i!=j and new in other_brick:
                        possible=False
                        break

            # if so change its z position       
            if possible:
                if return_possible:
                    return True
                
                bricks[i] = new_coords
                moved = True
                fell.add(i)
                # print(i, "moved")

        if not moved:
            break

    if return_possible:
        return False
    if return_fall_count:
        return len(fell)
    return bricks
    
# First fall
if 'test' in input_file:
    bricks = fall(bricks)

else:
    pickle_file = "bricks.pickle"
    if not os.path.exists(pickle_file):
        bricks = fall(bricks)
        pickle.dump(bricks, open(pickle_file, 'wb'))
        print("Saved to pickle")
        assert False
    else:
        bricks = pickle.load(open(pickle_file, 'rb'))
        print("Loaded pickled bricks")

# Loop takes 30 minutes on real input!!
ans1 = ans2 = 0
for i in range(N):
    # print(i, end='\r')
    bricks_disintegrated = [b for j,b in enumerate(bricks) if j!=i]
    # if not fall(bricks_disintegrated, return_possible=True):
    #     ans+=1
    #     if 'test' in input_file:
    #         print(f"Brick {LETTERS[i].upper()} can be disintegrated")
    count = fall(bricks_disintegrated, return_fall_count=True)
    if count==0:
        ans1 += 1
        print(f"Brick {i} can be disintegrated")
    else:
        ans2 += count
        print(f"Disintegrating brick {i} causes {count} other bricks to fall")


print("Part 1: ", ans1)
print("Part 2: ", ans2)



