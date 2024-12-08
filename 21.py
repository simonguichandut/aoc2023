import sys
import numpy
from utils import *
print(__file__)
input_file = sys.argv[1] if len(sys.argv)>1 else "test_input.txt"

data = open(input_file).read().strip().split('\n')
R,C = len(data),len(data[0])
ans = res = 0
##################################################
grid = [[s for s in line] for line in data]

def neighbors(r0,c0):
    neighbors = []
    for drdc in ((1,0),(-1,0),(0,1),(0,-1)):
        dr,dc = drdc
        r,c = r0+dr, c0+dc
        if 0<=r<R and 0<=c<C and grid[r][c] in '.S':
            neighbors.append((0,0,r,c))
    return neighbors

from functools import cache
@cache
def neighbors2(r0,c0):
    neighbors = []
    for drdc in ((1,0),(-1,0),(0,1),(0,-1)):
        dr,dc = drdc
        r,c = r0+dr, c0+dc

        # Apply periodic boundary conditions
        dRR,dCC = 0,0
        if r<0:
            r,dRR = R-1,-1
        elif r>=R:
            r,dRR = 0,+1
        elif c<0:
            c,dCC = C-1,-1
        elif c>=C:
            c,dCC = 0,+1

        if grid[r][c] in '.S':
            neighbors.append((dRR,dCC,r,c))

    return neighbors

for r in range(R):
    for c in range(C):
        if grid[r][c]=='S':
            start = (0,0,r,c)


def travel(n, pt2=False, prune_grids=True):

    points = [start]

    # Part 2 stuff
    finding_oscillation = True
    N_oscillation = (0,0)
    filled_grids = {}
    Nprev,Nprevprev = 0,0

    if isinstance(n, (list, numpy.ndarray)):
        checking_many = True
        nsteps = n[-1]+1
        N_tot_all = []
    else:
        checking_many = False
        nsteps = n

    for i in range(nsteps):
        new_points = []
        for p in points:
            RR,CC,r0,c0 = p
            if not pt2:
                new_points += neighbors(r0,c0)
            else:
                for np in neighbors2(r0,c0):
                    np_RR, np_CC = RR+np[0], CC+np[1]
                    if (np_RR,np_CC) not in filled_grids:
                        new_points.append((np_RR, np_CC, np[2], np[3]))

        points = list(set(new_points))

        if pt2 and prune_grids:
            if finding_oscillation:
                N = sum([1 for p in points if p[0]==0 and p[1]==0])
                if i>=2:
                    if N==Nprevprev:
                        N_oscillation = (Nprevprev,Nprev)
                        finding_oscillation = False
                        # print("Found oscillation!", N_oscillation)

                Nprevprev = Nprev
                Nprev = N
            
            # Find grids to prune out
            grids = {(0,0):0}
            for p in points:
                RR,CC,r0,c0 = p
                if (RR,CC) not in grids:
                    grids[(RR,CC)]=0
                grids[(RR,CC)] += 1

            # print(i, grids)

            for (RR,CC) in grids.keys():
                if grids[(RR,CC)] == N_oscillation[1]: # [0] does not give the right answer, [1] does :)
                    # print(i,"New filled grid at (RR,CC)=",(RR,CC), "; phase=",i%2)
                    filled_grids[(RR,CC)] = i%2 # track the phase

            points = [p for p in points if (p[0],p[1]) not in filled_grids]

        if checking_many and i+1 in n:
            Ntot = len(points)
            if prune_grids:
                for phase in filled_grids.values():
                    Ntot += N_oscillation[phase]
            # print(i+1, Ntot)
            N_tot_all.append(Ntot)

    if checking_many:
        return N_tot_all
    else:
        if pt2 and prune_grids:
            return len(points), N_oscillation, filled_grids
        if not pt2 or not prune_grids:
            return len(points)

print("Part 1:")
print("6 steps: ", travel(6))
print("64 steps: ", travel(64))


print("\nPart 2:")

# from scipy.optimize import curve_fit
# def quad()

''' Part 2 analysis
# Testing the pruning algorithm on test input
# nsteps = 5000 
# N, N_oscillation, filled_grids = travel(nsteps, True)
# # print(N, N_oscillation, filled_grids)
# ans = N
# for phase in filled_grids.values():
#     ans += N_oscillation[phase]
# print(ans)
# Actually works!!! But for just 5000 steps, takes 10 minutes. Not scalable at all

# Trend lines??
N_left, N_from_filled_grids, N_tot = [],[],[]
nsteps = numpy.arange(int((C-1)/2),300,10) # Start when first reach a new grid
# nsteps = numpy.arange(5, 300, C)
for nn in nsteps:
    print(nn)
    N, N_oscillation, filled_grids = travel(nn, True)
    N_left.append(N)

    nfg = 0
    for phase in filled_grids.values():
        nfg += N_oscillation[phase]
    N_from_filled_grids.append(nfg)

    N_tot.append(N+nfg)

import matplotlib.pyplot as plt
plt.figure()
plt.plot(nsteps, N_left)
plt.plot(nsteps, N_from_filled_grids)
plt.plot(nsteps, N_tot,'k.-')
# It looks like a perfect quadratic!!!!!!!!!!!!!
    
from scipy.optimize import curve_fit
def quad(nn,A,B):
    return A+B*nn**2
popt,pcov = curve_fit(quad, nsteps, N_tot)
print(f"Quadratic fit: {popt=}, {pcov=}")
prediction = quad(nsteps, *popt)
plt.plot(nsteps, prediction, 'r.-')

plt.figure()
plt.plot(nsteps, N_tot - quad(nsteps, *popt))

plt.show()

# Turns out it's not a perfect fit...

# BUT, the real input is nicer because the row and column of the starting square are
# fully cleared, so you can actually get a perfect quadratic fit.
'''


# nsteps = numpy.arange(int((C-1)/2), 600, C) # 
# nsteps = numpy.arange(100, 1000, 100)

# Insight from the number being asked
# 26501365 = 202300 * 131 + 65 !!
# 131 is the grid width/height. 65 is (C-1)/2, it's the number of steps to reach the end of the first grid
nsteps = numpy.arange(int((C-1)/2), 500, C)
grids_crossed = nsteps//C + 1 # plus 1 for the first grid which we start in the middle of. This is the parameter we fit on

N = travel(nsteps, pt2=True, prune_grids=True)
N2 = travel(nsteps, pt2=True, prune_grids=False)
# N and N2 are almost always the same, but not always, so sometimes the pruning introduces an error
N = N2
print(grids_crossed, N)

from scipy.optimize import curve_fit
def quad(x,A,B,C):
    return A+B*x*C*x**2
popt,_ = curve_fit(quad, grids_crossed, N)

nsteps = 26501365
print(f"{nsteps} steps (ans for part 2): {int(quad(nsteps//C + 1, *popt))}")



