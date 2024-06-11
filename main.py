from __future__ import annotations
from exceptions import DATFileNotProvidedException, UnableToConvertDATFileToArray

import vpython
import numpy
import re
import os
import argparse

def main():
    # Load data from .dat file
    try:
        DATA : numpy.ndarray[numpy.ndarray] = numpy.loadtxt(FILENAME, dtype=float)
    except Exception as exception:
        raise UnableToConvertDATFileToArray(f'Unable to load the dat file into array.\n{exception}')

    # Validate it has nine columns

if __name__ == '__main__':

    pattern = re.compile(r'.*\.dat')
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('fileName.dat')
    args = argument_parser.parse_args()

    if pattern.match(vars(args)['fileName.dat']):
        FILENAME = vars(args)['fileName.dat']
        main()
    else:
        raise DATFileNotProvidedException(f".dat file required.\nUsage: python {os.path.relpath(__file__)} fileName.dat")
