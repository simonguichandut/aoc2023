# imports
import numpy as np

# debug
#dbg = True
dbg = False

alphabet = 'abcdefghijklmnopqrstuvwxyz'
symbols = "*-=@%/#+&$"

def symbols_around(arr,i,j1,j2):
    surr = []
    # left
    surr.append(arr[i][j1-1])
    # right
    surr.append(arr[i][j2+1])
    for jj in range(j1-1,j2+2):
        # up
        surr.append(arr[i-1][jj])
        # down
        surr.append(arr[i+1][jj])
    if [x for x in surr if x in symbols]:
        return True
    return False

def gears_around(arr,i,j1,j2):
    gears=[]
    # left
    if arr[i][j1-1]=='*':
        gears.append([i,j1-1])
    # right
    if arr[i][j2+1]=='*':
        gears.append([i,j2+1])
    for jj in range(j1-1,j2+2):
        # up
        if arr[i-1][jj]=='*':
            gears.append([i-1,jj])
        # down
        if arr[i+1][jj]=='*':
            print(i+1,jj)
            gears.append([i+1,jj])

    return gears


def main(input_file):
    data = open(input_file).read().strip().split('\n')
    arr = []
    for line in data:
        l = ['.'] + [c for c in line] + ['.']
        arr.append(l)

    arr.insert(0,['.' for _ in range(len(line)+2)])
    arr.append(['.' for _ in range(len(line)+2)])
    # print(arr)

    all_numbs = []
    all_gears = {'00':[]}

    for i in range(1,len(arr)-1):
        j=1
        while j<len(arr[0])-1:
            c=arr[i][j]
            if c.isdigit():
                numb = c
                j1=j2=j
                while True:
                    j+=1
                    c = arr[i][j]
                    if c.isdigit():
                        numb+=c
                    else:
                        j2=j-1
                        j+=1
                        break
                if symbols_around(arr,i,j1,j2):
                    all_numbs.append(eval(numb))

                gears = gears_around(arr,i,j1,j2)
                if len(gears)>0:
                    for g in gears:
                        gstring = str(g[0])+str(g[1])
                        if gstring not in all_gears.keys():
                            all_gears[gstring] = [eval(numb)]
                        else:
                            all_gears[gstring].append(eval(numb))

            else:
                j+=1

                    
    print(all_numbs)
    print(all_gears)
    # for g in list(all_gears.values()):
    gear_ratios = [g[0]*g[1] for g in list(all_gears.values()) if len(g)==2]

    print("Part 1: ",sum(all_numbs))
    print("Part 2: ",sum(gear_ratios))

# wrong
# 321454
# 525685

# command line call : python main.py <input_file>
import sys
if __name__ == "__main__":
    if len(sys.argv)==2:
        input_file = sys.argv[1]
    else:
        input_file = "test_input.txt"
    main(input_file)
