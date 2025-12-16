#!/usr/bin/env python3

merit_map = {'A': 20,
             'B': 17.5,
             'C': 15,
             'D': 12.5,
             'E': 0,
             }

merit = 0

with open('/home/niklas/bbb.csv') as f:
    for line in f:
        subject, grade = line.split()

        if grade in 'ABCDE':
            print(subject, grade)
            merit += merit_map[grade]

print('Merit = ', merit)



