# imports

# debug
#dbg = True
dbg = False

def main(input_file):
    data = open(input_file).read().strip().split('\n')

    possible = []
    for i,line in enumerate(data):
        sets = line.split(":")[1].strip().split(";")
        poss = True
        for s in sets:
            items = s.split(',')
            for item in items:
                num, color = item.split()
                if (color=="red" and eval(num)>12) or (color=="green" and eval(num)>13) or (color=="blue" and eval(num)>14):
                    poss=False
                    break
        if poss:
            possible.append(i+1)
                    
    # print(possible)
    print("Part 1: ", sum(possible))

    tot = 0
    for i,line in enumerate(data):
        mins = [0,0,0] # red green blue
        sets = line.split(":")[1].strip().split(";")

        for s in sets:
            items = s.split(',')
            for item in items:
                num, color = item.split()
                num=eval(num)
                if (color=="red" and num>mins[0]):
                    mins[0] = num
                if (color=="green" and num>mins[1]):
                    mins[1] = num 
                if (color=="blue" and num>mins[2]):
                    mins[2] = num

        power = mins[0]*mins[1]*mins[2]
        # print(power)
        tot+=power

    print("Part 2: ",tot)

# command line call : python main.py <input_file>
import sys
if __name__ == "__main__":
    if len(sys.argv)==2:
        input_file = sys.argv[1]
    else:
        input_file = "test_input.txt"
    main(input_file)
