#!/usr/bin/env python3
import __main__


def get_args():
    import sys, os, argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description='Parse arguments from cmdline')
    parser.usage = f'{Path(__main__.__file__).name} Do like this'
    parser.add_argument('-i', '--integer', type=int, dest='integer', default=0, help='integer value')
    parser.add_argument('-f', '--float', type=float, dest='float', default=0, help='float value')

    opts, args = parser.parse_known_args()

    return opts, args


if __name__ == '__main__':
    opts, args = get_args()
    print(opts.integer)
    print(opts.float)
    print(args)


