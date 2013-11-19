"""
    Factor a number

    Wj.
"""

# Simple factoring
def factor(n, noduplicates = False):
    intn = int(n)
    factors = {}
    lastfactor = n
    i = 0

    # 1 is a special case
    if n == 1:
        return {1: 1}

    while 1:
        i += 1

        # avoid duplicates like {1: 3, 3: 1}
        if noduplicates and lastfactor <= i:
            break

        # stop when i is bigger than n
        if i > n:
            break

        if n % i == 0:
            factors[i] = n / i
            lastfactor = n / i

    return factors

if __name__ == "__main__":
    import sys

    print "Enter an integer:"
    number = sys.stdin.readline()
    print "Factors: " + str(factor(int(number), True))

