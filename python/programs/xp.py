#!/usr/bin/env python3

import sys


debug=False
categories = ['chars','skills']
costs = {'chars'  : [25, 30, 40, 50, 70, 90],
         'skills' : [10, 15, 20, 30, 40, 60] }

levels    = [i for l in (5*[i] for i in range(6)) for i in l]
#           [0,0,,...,1,1,...,2,2,...]

print('levels:', levels)

def debug_print(s):
    if debug: print(s)

def read_args(argv, categories):
    global debug
    debug = '-g' in argv
    values = dict(zip(categories, ([] for i in range(len(categories)))))
    for cat in categories:
        if cat in argv:
            index = argv.index(cat)
            for i in range(index+1,len(argv)):
                try:
                    values[cat].append(int(argv[i]))
                except Exception as e:
                    debug_print(e)
                    break
    return values

def test_read_args():
    vals = read_args(['skills','0','1','2','3','chars','4','5','6'])
    vals['chars'].append(32)
    print(vals)

def advance(n, costs):
    cost = 0
    for i in range(n):
        level = levels[i]
        cost += costs[level]
    return cost

values = read_args(sys.argv[1:], categories)

total_spent = 0
for cat in categories:
    spent = 0
    for n in values[cat]:
        spent += advance(n, costs[cat])
    total_spent += spent
    print(f'XP spent on {cat} = {spent}')

print(f'XP spent total = {total_spent}')

