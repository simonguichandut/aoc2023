# imports
import numpy as np

# debug
dbg = True
# dbg = False

"""
This is an absolutely terrible solution!!
"""

numbers=['one','two','three','four','five','six','seven','eight','nine']

def main(input_file):
    data = open(input_file).read().strip().split('\n')
    
    # tot = 0
    # for line in data:
    #     # print(line)
    #     # chars = [eval(c) for c in line]
    #     num = ''
    #     for c in line:
    #         if c.isdigit():
    #             if len(num)==0:
    #                 num = c + 'x'
    #             else:
    #                 num=num[0]+c
    #         # if len(num)==2:break
    #     if num[1]=='x':
    #         num=num[0]*2
    #     num = eval(num)
    #     print(line,num)
    #     tot += num
    #     # print(chars)
    # print("Part 1: ",tot)

    tot=0
    for line in data:
        
        # line =line.replace('one','1')
        # line =line.replace('two', '2')
        # line =line.replace('three','3' )
        # line =line.replace('four','4' )
        # line =line.replace('five','5' )
        # line =line.replace('six' ,'6' )
        # line =line.replace('seven','7' )
        # line =line.replace('eight','8' )
        # line =line.replace('nine','9' )
        # print(line)

        # cont=True
        # line2=line
        # while cont:
        #     # print(line2)
        #     for i,c in enumerate(line2):
        #         # print(c)
        #         if i==len(line2)-1:
        #             cont=False
        #             break
        #         for k,numb in enumerate(numbers):
        #             if line2[i:i+len(numb)]==numb:
        #                 line2=line2.replace(numb,str(k+1))
        #                 # print(line2)
        #                 break

        line2=""
        for i,c in enumerate(line):
            if c.isdigit():
                line2+=c
            for k,numb in enumerate(numbers):
                if line[i:i+len(numb)] == numb:
                    line2 += str(k+1)

        # break
        num = ''
        for c in line2:
            if c.isdigit():
                if len(num)==0:
                    num = c + 'x'
                else:
                    num=num[0]+c
            # if len(num)==2:break
        if num[1]=='x':
            num=num[0]*2
        num = eval(num)
        print(line,line2,num)
        tot += num

    print("Part 2: ",tot)


# command line call : python main.py <input_file>
import sys
if __name__ == "__main__":
    if len(sys.argv)==2:
        input_file = sys.argv[1]
    else:
        input_file = "test_input.txt"
    main(input_file)
