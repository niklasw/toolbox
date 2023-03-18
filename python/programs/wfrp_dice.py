#!/usr/bin/env python3

import random, sys

class DiceRoll:
    def __init__(self):
        self.history = []
        self.roll()

    def roll_one(self):
        self.d1 = random.randint(0,9)
        return self.d1

    def roll(self):
        self.d1,self.d2 = (self.roll_one(),self.roll_one())
        self.history.append((self.d1,self.d2))

    def dd10(self):
        d1 = 10 if self.d1 == 0 else self.d1
        d2 = 10 if self.d2 == 0 else self.d2
        return d1+d2

    def d100(self):
        if self.d1+self.d2 == 0:
            return 100
        else:
            return 10*self.d1+self.d2

    def check(self, n):
        v = 0
        for i in range(n):
            v += self.d100()
        return v/n

    def roll_max(self, name, add, n_rolls=3):
        value = 0
        for roll in range(n_rolls):
            self.roll()
            value = max(value, self.dd10())
        return value + add

class RPC:
    attr_names =      'WS  BS   S   T   I  Ag  Dex Int WP  Fel'.split()
    adds  =  {'halfling':[10, 30, 10, 20, 20, 20, 30, 20, 30, 30],
              'human':[20]*len(attr_names)}
    a = dict(zip())
    attr_defs = {'halfling':dict(zip(attr_names,adds['halfling'])),
                 'human':dict(zip(attr_names,adds['human']))}
    
    def __init__(self, name, specie, n_rolls=3):
        R = DiceRoll()
        self.defs = self.attr_defs[specie]
        roll = [R.roll_max(n,a, n_rolls=n_rolls) for n,a in self.defs.items()]
        self.attributes = dict(zip(self.attr_names, roll))

    def bonus(self,attribute):
        value = self.attributes[attribute]/10
        return int(value)

    def wounds(self):
        return self.bonus('S')+2*self.bonus('T')+self.bonus('WP')


def character():
    try:
        specie = sys.argv[1]
    except:
        specie = 'halfling'
    
    Leo = RPC('Leo Lostpocket', specie, n_rolls=3)
    
    print('\nAttributes')
    for key in Leo.attributes:
        print(f'{key}\t{Leo.attributes[key]}')
    
    print('\nWS bonus')
    print(Leo.bonus('WS'))
    
    print('\nBS bonus')
    print(Leo.bonus('BS'))
    
    print('\nStrength bonus')
    print(Leo.bonus('S'))
    
    print('\nWounds')
    print(Leo.wounds())

def roll():
    D = DiceRoll()
    print(D.d100())

if __name__ == '__main__':
    roll()



