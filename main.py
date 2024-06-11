from __future__ import annotations
from exceptions import DATFileNotProvidedException

import vpython
import numpy
import sys
import re
import os
import argparse

def main():
    DATA = numpy.loadtxt(FILENAME, dtype=int)
    print(DATA)
    # Open the file
    # Validate it has nine columns

if __name__ == '__main__':
    # Validate sys.argv ends in '.dat'
    pattern = re.compile(r'.*\.dat')
    argument_parser = argparse.ArgumentParser(add_help=False)
    argument_parser.add_argument('--help', '-h', action='store_true')
    args = argument_parser.parse_args()

    if args.help:
        print(f'A .dat file is required to run this file.\nUsage: python {os.path.relpath(__file__)} fileName.dat')

    else:
        if len(sys.argv) > 1 and pattern.match(sys.argv[1]):
            FILENAME = sys.argv[1]
            main()
        else:
            raise DATFileNotProvidedException(f".dat file required.\nUsage: python {os.path.relpath(__file__)} fileName.dat")
