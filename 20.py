import sys
import numpy as np
from utils import *
print(__file__)
input_file = sys.argv[1] if len(sys.argv)>1 else "test_input.txt"

data = open(input_file).read().strip().split('\n')
##################################################

class Pulse:
    def __init__(self, src, kind, dest):
        self.src = src
        self.kind = kind
        self.dest = dest

    def __repr__(self):
        return self.src + ' -' + self.kind + '-> ' + self.dest

class Module:
    def __init__(self,name, type, destinations):
        self.name = name
        self.type = type
        self.destinations = destinations

        if type=='%':
            self.state = 0 # off at init
        elif type=='&':
            self.memory = {}

    def __repr__(self):
        return self.name + '->' + ','.join([d for d in self.destinations])
        
    def process(self, pulse):
        assert pulse.dest == self.name, pulse.dest

        if self.type == 'broadcaster':
            new_kind = pulse.kind

        elif self.type == '%':
            if pulse.kind == 'high': 
                return [] # ignore received high pulses
            else:
                new_kind = 'high' if self.state==0 else 'low'
                self.state = int(abs(2**self.state-2)) # function to switch 0<->1

        elif self.type == '&':
            self.memory[pulse.src] = pulse.kind
            new_kind = 'low' if all(mem=='high' for mem in self.memory.values()) else 'high'

        else:
            assert False, self.kind

        new_pulses = []
        for dest in self.destinations:
            new_pulses.append(Pulse(self.name, new_kind, dest))

        return new_pulses

def create_modules():
    modules = {}
    for line in data:
        name, dests = line.split(' -> ')
        dests = dests.split(', ')
        if '%' in name or '&' in name:
            type, name = name[0], name[1:]

        elif name == 'broadcaster':
            type = name

        modules[name] = Module(name, type, dests)

    # Set up the memory of the source modules for each conjunction modules
    for src_mod in modules:
        for dest_mod in modules[src_mod].destinations:
            if dest_mod in modules and modules[dest_mod].type == '&':
                modules[dest_mod].memory[src_mod] = 'low'

    return modules

def push_button(Nlow=0, Nhigh=0):
    Nlow += 1
    pulses = modules['broadcaster'].process(Pulse('button','low','broadcaster'))
    while pulses:
        pulse = pulses.pop(0) # take first out
        # print(pulse)
        if pulse.kind == 'low': Nlow+=1
        elif pulse.kind == 'high': Nhigh+=1

        if pulse.dest in modules:
            pulses += modules[pulse.dest].process(pulse)
    return Nlow,Nhigh

modules = create_modules()
# Nlow = Nhigh = 0
# for _ in range(1000):
#     Nlow,Nhigh = push_button(Nlow,Nhigh)
# print("Part 1: ", Nlow*Nhigh)


def viz(modules):
    import graphviz
    g = graphviz.Digraph('G', filename='day20.gv')
    for m1 in modules.values():
        A = m1.name
          
        for dest in m1.destinations:
            B = dest

            conjunction = False
            if dest in modules:
                if modules[dest].type == '&':
                    conjunction=True
            
            print(A,B)
            g.edge(A,B, color='red' if conjunction else 'black')
    g.view()

# viz(create_modules())
# We see that only &ll feeds into rx. It needs to be on to send a low pulse
# So ll needs to remember a high pulse from its 4 sources: &kv,&vm,&kl,&vb
# The next pulse ll receives from *any* of those 4, it will send a low pulse to rx and that is the end condition
# Those nodes all come from individual parts of the graph, so we can look at them individually

nodes = ['vm','kv','kl','vb']
blocks = ['fn','tp','zz','lp'] # the 4 destinations of broadcaster which lead to the 4 independent blocks
N_high_to_ll = []

for i in range(4):
    modules = create_modules()
    modules['broadcaster'].destinations = [blocks[i]]
    Npress = 0

    done = False
    while not done:
        pulses = modules['broadcaster'].process(Pulse('button','low','broadcaster'))
        Npress += 1

        while pulses:
            pulse = pulses.pop(0)
            # if 'll' in pulse.dest:
            #     print(Npress, pulse)

            if 'll' in pulse.dest and pulse.kind == 'high':
                print(Npress, pulse)
                N_high_to_ll.append(Npress)
                done = True
                break

            if pulse.dest in modules:
                pulses += modules[pulse.dest].process(pulse)

# Answer is lcm of all the stored numbers (i thought maybe +1 but no..)
from math import lcm
print("Part 2: ", lcm(*N_high_to_ll))






