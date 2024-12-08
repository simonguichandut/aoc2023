import sys
import numpy as np
from utils import *
import copy
from collections import defaultdict
print(__file__)
input_file = sys.argv[1] if len(sys.argv)>1 else "test_input.txt"

data = open(input_file).read().strip().split('\n')
R,C = len(data),len(data[0])
ans = res = 0
##################################################

def get_graph():
    graph = defaultdict(list)
    for line in  data:
        src,dests = line.split(': ')
        for dest in dests.split():
            graph[src].append(dest)
            graph[dest].append(src) # it's a two-way graph
    return graph

graph = get_graph()
nodes = set(graph.keys())
N = len(nodes)
# print(N)

sys.setrecursionlimit(int(N*5))

def traverse(graph, root, node=None, visited=None, path=None, cycles=None):
    if node is None: 
        node = root
    if visited is None:
        visited = set()
    if path is None:
        path = []
    if cycles is None:
        # cycles = set()
        cycles = []

    visited.add(node)
    path.append(node)
    # print(node)
    for new_node in graph[node]:
        if new_node==root and len(path)>2:
            # cycles.add(tuple(path))
            cycles.append(path)
        elif new_node not in path:
            traverse(graph, root, new_node, visited, path, cycles)

    return cycles
    
def groups_from_breaks(breaks):
    g = copy.deepcopy(graph)
    for (src,dest) in breaks:
        assert dest in g[src]
        g[src].remove(dest)
        g[dest].remove(src)

    cycles1 = traverse(g, breaks[0][0])
    ngroup1 = max(len(c) for c in cycles1)

    cycles2 = traverse(g, breaks[0][1])
    ngroup2 = max(len(c) for c in cycles2)

    return ngroup1,ngroup2

# n1,n2 = groups_from_breaks((('hfx','pzl'),('bvb','cmg'),('nvd','jqt')))
# print(n1,n2)

def brute_force():
    prune = set()
    for i,n1 in enumerate(nodes):
        if i%10 == 0:
            print(f"{i/N*100:.2f}% through", end='\r')

        for n2 in graph[n1]:

            for n3 in nodes-{n1,n2}:
                for n4 in graph[n3] - {n1,n2}:

                    if n3+n4 not in prune and n4+n3 not in prune:

                        for n5 in nodes-{n1,n2,n3,n4}:
                            for n6 in graph[n5] - {n1,n2,n3,n4}:

                                if n5+n6 not in prune and n6+n5 not in prune: 

                                    breaks = ((n1,n2),(n3,n4),(n5,n6)) 
                                    ng1,ng2 = groups_from_breaks(breaks)
                                    if ng1+ng2==N:
                                        print("\nPart 1: ", ng1*ng2)
                                        return                    
            # prune.add(n1+n2)
                                    
# brute_force() # This does work for the test input

# Karger's algorithm
# https://en.wikipedia.org/wiki/Karger%27s_algorithm#The_global_minimum_cut_problem
# Idea is to randomly select an edge an collapse the two end vertices into a single one
# keep doing that until there are only 2 vertices. The number of edges between the two is the minimum cut
# Not guarenteed to find the true minimum cut, but likely. This is a monte carlo algorithm
# In the present case, we can stop once the cut is 3, we know that is the answer
# Found this implementation in python in the case where the graph is represented by an adjacency list
# https://gist.github.com/zaksamalik/457adbf0d60c1d4486484c1fac0a95f5
# I've changed it a bit
# Combining nodes abc and def is creating a new node "abcdef" (can just string add)
# End up with two nodes "abcdefghi..." and "lmnopqrst..."
# The size of each group is the length of the string divided by 3!

import random
def karger():
    while True:
        g = get_graph() # reset the graph

        while len(g)>2:

            # Randomly select an edge (its two nodes)
            n1 = random.choice(list(g))
            n2 = random.choice(g[n1])

            # send all destination nodes of n1 and n2 into the combined node (called n1+n2)
            n1_dests = [n for n in g[n1] if n != n2]
            n2_dests = [n for n in g[n2] if n != n1]
            g[n1+n2] = n1_dests+n2_dests

            # delete n1 and n2
            g.pop(n1)
            g.pop(n2)

            # send all that pointed to n1 and n2 to n1+n2
            for n3 in n1_dests+n2_dests:
                g[n3] = [n1+n2 if n in (n1,n2) else n for n in g[n3]]

        n1,n2 = g.keys()
        if len(g[n1]) == len(g[n2]) == 3:
            print("Answer :", int(len(n1)/3 * len(n2)/3))
            return

karger()