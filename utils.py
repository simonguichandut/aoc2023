# Utilities for advent of code

import re
import re
import math
import operator
from functools import reduce, total_ordering
from itertools import permutations

LETTERS = 'abcdefghijklmnopqrstuvwxyz'
DIGITS = '0123456789'
VOWELS = {'a', 'e', 'i', 'o', 'u'}
CONSONANTS = set(x for x in LETTERS if x not in VOWELS)
SYMBOLS = '*-=@%/#+&$'

# https://stackoverflow.com/a/34445090
def findall(p, s):
    '''Yields all the positions of
    the pattern p in the string s.'''
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)

# From https://github.com/iKevinY/advent/blob/main/2019/utils.py
def transposed(matrix):
    """Returns the transpose of the given matrix."""
    return [list(r) for r in zip(*matrix)]


def rotated(matrix):
    """Returns the given matrix rotated 90 degrees clockwise."""
    return [list(r) for r in zip(*matrix[::-1])]


def mul(lst):
    """Like sum(), but for multiplication."""
    return reduce(operator.mul, lst, 1)  # NOQA


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def all_unique(lst):
    return len(lst) == len(set(lst))

# https://stackoverflow.com/a/66081363
def closestSum(arr, k):
    #create a dp dictionary to grow. key is closest sum so far, value is the list of numbers that add up to key
    dp_dict = {0:[]}

    for num in arr:
        dict_copy = dict(dp_dict)
        # grow or update the dp dict with the closest sum so far
        for sum in dp_dict:
            if sum + num < k:
                dict_copy[sum+num] = dp_dict[sum]+[num]
        dp_dict = dict_copy

    #traceback - find the item in dp dict that is closest to k
    result = (k,[])
    for sum, number_list in dp_dict.items():
        distance = abs(k - sum)
        if distance < result[0]:
            result = (distance, number_list)
    return result[1]

# sample_list = [20, 15, 35, 50, 2, 300, 225]
# target_value = 200
# print(closestSum(sample_list, target_value))

# My own
def in_string(s, what='digits', return_indices=False, custom=None):
    """ Return list of items that appear in a list

        'what' argument is what you want to look for:
        - 'digits' : single digits
        - 'numbers' : whole numbers
        - 'letters' : single letters
        - 'custom' : either a single string or list of strings
                    ** to be provided with kwarg custom **
                    e.g. in_string('123hello456',what='custom',custom='hello')
                
        if return_indices=True, return list with index where each first
        character appears
        
    """
    items,indices = [],[]

    if what=='digits':
        for i,c in enumerate(s):
            if c.isdigit():
                items.append(c)
                indices.append(i)

    elif what=='numbers':
        i=0
        while i<len(s)-1:
            c = s[i]
            if c.isdigit():
                numb = c
                i0 = i
                while True:
                    i+=1
                    c = s[i]
                    if c.isdigit():
                        numb += c
                    else:
                        i+=1
                        break
                items.append(c)
                indices.append(i0)
            else:
                i+=1

    elif what=='letters':
        for i,c in enumerate(s):
            if c in LETTERS:
                items.append(c)
                indices.append(i)

    elif what=='custom':
        if custom is None:
            raise TypeError("Expecting a custom argument")
        elif type(custom) is str:
            custom = [custom,] # convert to a one item list

        for word in custom:
            ind = findall(word, s)
            for ii in ind:
                items.append(word)
                indices.append(ii)

    if return_indices:
        return items,indices
    else:
        return items
        
# Testing
if __name__ == '__main__':
    s = '123hello456hello7he8llo9_world$'
    print(s)
    print("Default call", in_string(s))
    print("Numbers", in_string(s, 'numbers'))
    print("Letters", in_string(s, 'letters'))
    print("hello", in_string(s, 'custom', return_indices=True, custom='hello'))
    print("hello and world", in_string(s, 'custom', return_indices=True, custom=['hello','world']))
