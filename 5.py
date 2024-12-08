# imports
import numpy as np
from utils import *

# debug
dbg = True
# dbg = False

# print("5")
def update_map(m, ll):
    pass

def main(input_file):
    data = open(input_file).read().strip().split('\n')
    # print(data)

    seeds = data[0].split()[1:]
    seeds = [int(s) for s in seeds]
    # print(seeds)
    Maps = []

    reading_map = False
    for line in data[1:]:
        if "map:" in line:
            reading_map = True # on the next iteration

        elif line=='':
            reading_map = False
            Maps.append([])
        
        else:
            assert reading_map  
            Maps[-1].append([eval(x) for x in line.split()])

    # print(Maps)

    def go_seed(seed):
        curr = seed  
        for mm in Maps:
            for m in mm:
                if curr in range(m[1],m[1]+m[2]):
                    # print(m)
                    # i = list(range(m[1],m[1]+m[2])).index(curr)
                    i = curr-m[1]
                    curr = m[0]+i
                    break
        return curr

    locations = []
    for seed in seeds:
        locations.append(go_seed(seed))
    print("Part 1: ", min(locations))

    # Part 2
    a = seeds[::2]
    b = seeds[1::2]



    # Go upwards instead, and start at 0, since theres a location range starting at 0
    def go_reverse(loc):
        curr = loc 
        for mm in Maps[::-1]:
            for m in mm:
                if curr in range(m[0],m[0]+m[2]):
                    # print(m)
                    # i = list(range(m[1],m[1]+m[2])).index(curr)
                    i = curr-m[0]
                    curr = m[1]+i
                    break
        seed = curr
        for i in range(len(a)):
            if seed>=a[i] and seed<a[i]+b[i]:
                return True
            
        return False

    loc=0
    while True:
        if loc%100_000==0: print(loc)
        if go_reverse(loc):
            print(loc)
            break
        loc+=1


    # final_rg_starts = [m[0] for m in Maps[-1]]
    # x_sorted = sorted(final_rg_starts)

    # # m_check = Maps[-1][final_rg_starts.index(min(final_rg_starts))]

    # m_check = Maps[-1][final_rg_starts.index(x_sorted[0])]
    # # m_check = Maps[-1][final_rg_starts.index(x_sorted[1])]
    # print(m_check)

    # keep_going = True

    # for final_location in range(m_check[0],m_check[0]+m_check[2]):

    #     if not keep_going: break

    # for final_location in [12634632,]:

    #     curr = m_check[1] + final_location - m_check[0]
    #     # print(final_location, curr)

    # # # For the test problem
    # # for final_location in range(0,47):

    #     curr = final_location
    #     for mm in Maps[:-1][::-1]:
    #         # print(mm)
    #         for m in mm:
    #             if curr>=m[0] and curr<=m[0]+m[2]-1:
    #                 curr = m[1]+curr-m[0]
    #                 break
    #         # print(curr)

    #     for j in range(len(a)):
    #         if curr>=a[j] and curr<=a[j]+b[j]-1:
    #             print(final_location, 'for seed', curr)
    #             keep_going = False
    #             break
        
    #     # print('\n')
    # if keep_going: print("Not found :'(")
    

    # Minimum of final destinations???
    # for m in Maps[-1]:
    # print(min([m[0] for m in Maps[-1] if m[0]>0]))
    # thats not it



    # My first working solution here
    # Semi brute force
    # Start with the commented part A to find the most likely range

    ### A
    # min_locations = []
    # for i in range(len(a)):
    #     for seed in list(range(a[i],a[i]+b[i],1000)):
    #         # print(seed)
    #         locations.append(go_seed(seed))
    #     min_locations.append(min(locations))
    # # print(min_locations)
    # i_best = min_locations.index(min(min_locations))
    # print("Best range is", a[i_best], b[i_best])

    # best_sofar = min(min_locations)
    # print(best_sofar)

    # best_seed = 0
    # for s in range(a[i_best],a[i_best]+b[i_best],10):
    #     loc = go_seed(s)
    #     if loc<best_sofar:
    #         best_sofar = loc
    #         best_seed = s
    # print(best_sofar, "for seed ", best_seed)

    # This returns  12634716 for seed  692213738
    # Search Around that

    ### B
    # best_sofar = 12634716
    # for s in range(692213738-100,692213738+100):
    #     loc = go_seed(s)
    #     if loc<best_sofar:
    #         best_sofar = loc
    #         best_seed = s
    # print(best_sofar, "for seed ", best_seed)
    # print("Part 2: ", best_sofar)














    # best_sofar = min(min_locations)
    # dx = 10000
    # while True:
    #     dx = int(dx/10)
    #     if dx<1: break
    #     print(dx, best_sofar)
    #     locations = []
    #     for seed in list(range(a[i_best],a[i_best]+b[i_best],dx)):
    #         # print(seed)
    #         locations.append(go_seed(seed))
        
    #     if min(locations)>=best_sofar:
    #         print("Part 2: ", best_sofar)
    #         break

    #     best_sofar = min(locations)

    #     if dx==1: break

        # 12634716
        # 12634636
        # 3763465
        # 12634632

    # Brute force approach

    # all_seeds = []
    # min_location = 10000000000000000000000
    # for i in range(len(a)):
    #     # print(a[i],b[i])
    #     print(i)
    #     for s in range(a[i],a[i]+b[i]):
    #         prog = (s-a[i])/b[i]
    #         if prog>0.01 and int(prog*10)%10==0:
    #             print(prog)
    #             print(min_location)
    #         all_seeds.append(s)
    #         loc = go_seed(s)
    #         if loc<min_location:
    #             min_location = loc

    # print("Part 2: ", min_location)

    # Way too slow!



# command line call : python main.py <input_file>
import sys
if __name__ == "__main__":
    if len(sys.argv)>1:
        input_file = sys.argv[1]
    else:
        input_file = "test_input.txt"
    main(input_file)
