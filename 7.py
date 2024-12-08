# imports
import numpy as np
from utils import *

print(__file__)

# command line call : python main.py <input_file>
import sys
if len(sys.argv)>1:
    input_file = sys.argv[1]
else:
    input_file = "test_input.txt"

##################################################

# data = open(input_file).read().strip().split('\n')

# C = ['A','K','Q','J','T'] + [str(x) for x in range(9,1,-1)]
# 
# cards = [line.split()[0] for line in data]
# bids = [int(line.split()[1]) for line in data]
# 
# def ctype(card, pt2=False):
# 
#     if pt2 and 'J' in card:
#         # print(card)
#         un = list(np.unique([x for x in card]))
# 
#         if len(un)==1 or len(un)==2:
#             return 7 # definitely 5 of a kind
#         
#         un.remove('J')
# 
#         new_cards = []
#         for new in un:
#             new_cards.append(card.replace('J',new))
# 
#         # This is in case you might want to replace one J with a character,
#         # and another J with a different character
#         # This turned out not to be necessary
#         # iJ = [i for i in range(5) if card[i]=='J']
#         # new_cards = [card]
# 
#         # for i in iJ:
#         #     n=len(new_cards)
#         #     for j in range(len(new_cards)):
#         #             nc = new_cards[j]
#         #             for c in un:
#         #                 new_cards.append(nc[:i]+c+nc[i+1:])
# 
#         # new_cards = [nc for nc in new_cards if 'J' not in nc]
# 
#         scores=[]
#         for nc in new_cards:
#             scores.append(ctype(nc))
#         return max(scores)
#     
#     chars = [x for x in card]
#     if len(set(chars))==1:
#         return 7 # five of a kind
# 
#     elif len(set(chars))==2:
#         s = set(chars).pop()
#         num = len(list(findall(s,card)))
#         if num in (4,1):
#             return 6 # four of a kind
#         else:
#             return 5 # full house
#         
#     elif len(set(chars))==3:
#         counts=[]
#         S = set(chars)
#         for _ in range(3):
#             s = S.pop()
#             counts.append(len(list(findall(s,card))))
#         # print(counts)
#         if tuple(counts) in permutations([3,1,1]):
#             return 4 # three of a kind
#         elif tuple(counts) in permutations([2,2,1]):
#             return 3 # two pair
#         
#     elif len(set(chars))==5:
#         return 1 # high card
#     
#     else:
#         return 2 # one pair
# 
# 
# # Because I didnt know about python sorted(list, key=...)
# def bubble_sort(pt2=False):
#     
#     CC = C
#     if pt2:
#         CC.remove('J')
#         CC.append('J')
# 
#     idx = [i for i in range(len(cards))]
#     n = len(idx)
# 
#     for i in range(n):
#         for j in range(0,n-i-1):
#             c1,c2 = cards[idx[j]], cards[idx[j+1]]
#             ct1,ct2 = ctype(c1,pt2),ctype(c2,pt2)
#             if ct2>ct1:
#                 idx[j],idx[j+1]=idx[j+1],idx[j]
#             elif ct1==ct2:
#                 for k in range(5):
#                     if CC.index(c2[k])>CC.index(c1[k]):
#                         break
#                     elif CC.index(c2[k])<CC.index(c1[k]):
#                         idx[j],idx[j+1]=idx[j+1],idx[j]
#                         break
#     idx = idx[::-1]
#     return idx
# 
# # Part 1
# ans = 0
# idx = bubble_sort()
# for j,i in enumerate(idx):
#     # print(i+1,cards[i],bids[i])
#     ans += (j+1)*bids[i]
# print("Part 1: ",ans)
# 
# # Part 2
# ans = 0
# idx = bubble_sort(pt2=True)
# for j,i in enumerate(idx):
#     # print(i+1,cards[i],bids[i])
#     ans += (j+1)*bids[i]
# print("Part 2: ",ans)


# Unhappy with my initial solution
# This is where I learn about .sort and .count

data = open(input_file).read().strip().split('\n')
hands_bids = [line.split() for line in data]

def strength(hand, pt2):

    lettermap = {'T':'A', 'J':'B', 'Q':'C', 'K':'D', 'A':'E'}

    # For sorting hands of same type
    # .get: check for c in lettermap, otherwise return c (for the digits)
    hand_lettermapped = ''.join([lettermap.get(c,c) for c in hand])

    if pt2:
        lettermap['J'] = '0'
        hand_lettermapped = ''.join([lettermap.get(c,c) for c in hand])

        if 'J' in hand:
            if hand.count('J') in (4,5):
                # Definitely a five-of a kind
                return (7,hand_lettermapped)
            
            # Otherwise, replace J's (now 0's) with the hand in the highest number
            counts_notJ = {c:hand.count(c) for c in hand if c!='J'}
            char = max(counts_notJ, key=counts_notJ.get)

            # Get only the strength part
            st = strength(hand.replace('J',char), pt2=False)[0]

            return (st,hand_lettermapped)


    counts = [hand.count(c) for c in hand]
    if 5 in counts:
        # five of a kind
        return (7,hand_lettermapped)
    elif 4 in counts:
        # four of a kind
        return (6,hand_lettermapped)
    elif 3 in counts:
        if 2 in counts:
            # full house
            return (5,hand_lettermapped)
        else:
            # three of a kind
            return (4,hand_lettermapped)
        
    if 2 in counts:
        if counts.count(2)==4:
            # two pair
            return (3,hand_lettermapped)
        else:
            # one pair
            return (2,hand_lettermapped)
    
    # high hand
    return (1,hand_lettermapped)


for i,pt2 in enumerate((False,True)):
    CB = sorted(hands_bids, key=lambda cb: strength(cb[0], pt2))
    # print(CB)
    ans = 0
    for j,(hand,bid) in enumerate(CB):
        # print(j+1,hand,bid,strength(hand,pt2=pt2))
        ans += (j+1)*int(bid)
    print(f"Part {i+1}: {ans}")
