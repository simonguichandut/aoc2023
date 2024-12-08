import sys
import numpy as np
from utils import *
print(__file__)
input_file = sys.argv[1] if len(sys.argv)>1 else "test_input.txt"

data = open(input_file).read().strip().split('\n')
R,C = len(data),len(data[0])
ans = res = 0
##################################################

# for line in  data:
#     print(line)

# print("Part 1: ",)
# print("Part 2: ",)



