import sys
import numpy as np
from utils import *
print(__file__)
input_file = sys.argv[1] if len(sys.argv)>1 else "test_input.txt"

data = open(input_file).read().strip().split('\n')
R,C = len(data),len(data[0])
ans = res = 0
##################################################
stones = []
for line in data:
    p,v = line.split(' @ ')
    p = tuple([float(pi) for pi in p.split(', ')])
    v = tuple([float(vi) for vi in v.split(', ')])
    stones.append((p,v))

min_xy = 7 if 'test' in input_file else 200000000000000
max_xy = 27 if 'test' in input_file else 400000000000000

# y=ax+c and y=bx+d intersect at x,y = (d-c)/(a-b), a*(d-c)/(a-b)+c
def intersection(stone1,stone2):
    ((x1,y1,z1),(vx1,vy1,vz1)) = stone1
    ((x2,y2,z2),(vx2,vy2,vz2)) = stone2
    a,c = vy1/vx1, y1 - x1*vy1/vx1
    b,d = vy2/vx2, y2 - x2*vy2/vx2
    if a==b:
        return None
    x,y = (d-c)/(a-b), a*(d-c)/(a-b)+c
    t1 = (x-x1)/vx1
    t2 = (x-x2)/vx2
    return (x,y,t1,t2)

ans=0
for i,stone1 in enumerate(stones):
    for j,stone2 in enumerate(stones[i+1:]):
        pt = intersection(stone1,stone2)
        if pt is None:
            continue
        x,y,t1,t2 = pt
        if t1>=0 and t2>=0 and min_xy<=x<=max_xy and min_xy<=y<=max_xy:
            ans+=1
print("Part 1: ", ans)

# Part 2 by linear algebra. Using 3 stones, can get 6 linear equations for the 6 unknowns xs,ys,zs,vxs,vys,vzs
# It might be that some stones are traveling parallel resulting in a singular system. But we have many stones to pick from
import random
while True:
    stone1 = random.choice(stones)
    stone2 = random.choice(list(set(stones) - {stone1}))
    stone3 = random.choice(list(set(stones) - {stone1,stone2}))
    [(x1,y1,z1),(vx1,vy1,vz1)] = stone1
    [(x2,y2,z2),(vx2,vy2,vz2)] = stone2
    [(x3,y3,z3),(vx3,vy3,vz3)] = stone3
    
    A = np.array([[vy2-vy1,  vx1-vx2,    0,     y1-y2,  x2-x1,    0],
                  [vy3-vy1,  vx1-vx3,    0,     y1-y3,  x3-x1,    0],
                  [vz2-vz1,     0,    vx1-vx2,  z1-z2,    0,    x2-x1],
                  [vz3-vz1,     0,    vx1-vx3,  z1-z3,    0,    x3-x1],
                  [   0,     vz2-vz1, vy1-vy2,    0,    z1-z2,    y2-y1],
                  [   0,     vz3-vz1, vy1-vy3,    0,    z1-z3,    y3-y1]])
    
    if np.linalg.det(A)!=0:
        b = np.array([y1*vx1 - y2*vx2 + x2*vy2 - x1*vy1,
                    y1*vx1 - y3*vx3 + x3*vy3 - x1*vy1,
                    z1*vx1 - z2*vx2 + x2*vz2 - x1*vz1,
                    z1*vx1 - z3*vx3 + x3*vz3 - x1*vz1,
                    z1*vy1 - z2*vy2 + y2*vz2 - y1*vz1,
                    z1*vy1 - z3*vy3 + y3*vz3 - y1*vz1])

        (xs,ys,zs,vxs,vys,vzs) = np.linalg.solve(A,b)
        t1,t2,t3 = (xs-x1)/(vx1-vxs),(xs-x2)/(vx2-vxs),(xs-x3)/(vx3-vxs)

        if t1>0 and t2>0 and t3>0 and \
        xs.is_integer() and ys.is_integer() and zs.is_integer() and \
        vxs.is_integer() and vys.is_integer() and vzs.is_integer():
            print("Part 2: ", int(xs+ys+zs))
            break



""" A brute forcing attempt which would probably work (it does on the test input) but takes too long
# Pt2
# Let's just assume that velocities will be reasonable (<50 in absolute magnitude)
# Then we can brute force check all 100*100*100 = 1e6 combinations
# The linear system of 5 equations, 5 variables, can be solved directly
# Let (xs,ys,zs) be the initial position of the hailstone,
# (vxs,vys,vzs) the initial velocity to brute force,
# (x1,y1,z1,vx1,vy1,vz1),(x2,y2,z2,vx2,vy2,vz2) the initial positions and velocities of stone 1 and 2 (we only need 2 stones)
# (t1s,t2s) the times at which the hailstone collides with stone 1 and stone 2
# xs + (vxs-vx1)t1s = x1
# ys + (vys-vy1)t1s = y1
# zs + (vzs-vz1)t1s = z1
# xs + (vxs-vx2)t2s = x1
# ys + (vys-vy2)t2s = y2
# Solve for the vector of 5 unknowns [xs,ys,zs,t1s,t2s]
# Solution is only valid if (xs,ys,zs) are integers and if t1s>=0, t2s>=0

# A speed up is wolfram to invert the matrix
# inv {[1,0,0,a,0],[0,1,0,b,0],[0,0,1,c,0],[1,0,0,0,d],[0,1,0,0,e]}
# = (bd-ae)^-1 * {[bd,-ad,0,-ae,ad],[be,-ae,0,-be,bd],[ce,-cd,1,-ce,cd],[-e,d,0,e,-d],[-b,a,0,b,-a]}

# There might be an infinite number of solutions for the 5-system
# So we'll do a final check for z: z2s + vzs*t2s = z2 + v2z*t2s

[(x1,y1,z1),(vx1,vy1,vz1)] = stones[0]
[(x2,y2,z2),(vx2,vy2,vz2)] = stones[1]
[(x3,y3,z3),(vx3,vy3,vz3)] = stones[4]

def solve(vxs,vys,vzs):
    a = vxs-vx1
    b = vys-vy1
    c = vzs-vz1
    d = vxs-vx2
    e = vys-vy2

    if (b*d-a*e)==0:
        return None
    
    Ainv = 1/(b*d-a*e) * np.array([
        [b*d,-a*d,0,-a*e,a*d],
        [b*e,-a*e,0,-b*e,b*d],
        [c*e,-c*d,b*d-a*e,-c*e,c*d],
        [-e,d,0,e,-d],
        [-b,a,0,b,-a]
    ])
    bvec = np.array([x1,y1,z1,x2,y2])
    xs,ys,zs,t1s,t2s = np.dot(Ainv, bvec.T)

    # assert xs + vxs*t1s == x1 + vx1*t1s, xs + vxs*t1s - x1 + vx1*t1s

    if xs.is_integer() and xs>=0 and ys.is_integer() and ys>=0 and zs.is_integer() and zs>=0 \
        and t1s>=0 and t2s>=0 \
        and zs + vzs*t2s == z2 + vz2*t2s:
        
            if vxs==vx3:
                if xs==x3: # traveling together in x, this can be valid
                    return (xs,ys,zs,t1s,t2s) 

            else:
                t3s = (x3-xs)/(vxs-vx3)
                if t3s>=0:
                    if ys + vys*t3s == y3 + vy3*t3s and zs + vzs*t3s == z3 + vz3*t3s:
                        return (xs,ys,zs,t1s,t2s)
    return None

max_v = 300
done = False

# for vxs in range(-max_v,max_v+1):
#     for vys in range(-max_v,max_v+1):
#         for vzs in range(-max_v,max_v+1):

# Instead of starting from the corner (-max_v,-max_v,-max_v), start from the center and alternate positive and negative
ix,iy,iz = True,True,True # increment or go to negative value
vxs = 0
for i in range(2*max_v+1):
    vxs,ix = abs(vxs)+1 if ix else -vxs, False if ix else True
    vys = 0

    if done: break

    for j in range(2*max_v+1):
        vys,iy = abs(vys)+1 if iy else -vys, False if iy else True
        vzs = 0

        if done: break

        for k in range(2*max_v+1):
            vzs,iz = abs(vzs)+1 if iz else -vzs, False if iz else True

            # print(vxs,vys,vzs)

            res = solve(vxs,vys,vzs)
            if res!=None:
                xs,ys,zs,t1s,t2s = res
                xs,ys,zs = int(xs),int(ys),int(zs)
                print("Solution found!!")
                print(f"{xs=} {ys=} {zs=}, {vxs=} {vys=} {vzs=}, {t1s=}, {t2s=}")
                print("Part 2: ",int(xs+ys+zs))
                done = True
                break
"""