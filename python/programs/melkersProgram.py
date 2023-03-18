#!/usr/bin/env python3

name = 'Melker'
born = 2008

def ask():
    print()
    svar = input(f'Hej {name}, skriv ett årtal: ')
    try:
        return int(svar)
    except:
        return False

try:
    while True:
        now_year = ask()
        if not now_year:
            continue

        if now_year < 0:
            raise KeyboardInterrupt

        print(f'År {now_year} är jag {now_year - born} år')
        print(f'Då är pappa {now_year - 1973} år')

except KeyboardInterrupt as E:
    print()
    print('Slut')
