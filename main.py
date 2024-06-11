from __future__ import annotations
from exceptions import DATFileNotProvidedException, UnableToConvertDATFileToArray

import numpy
import re
import os
import argparse
import simulation_model

def main():
    # Load data from .dat file
    global SIM

    try:
        data : numpy.ndarray[numpy.ndarray] = numpy.loadtxt(FILENAME, dtype=float, usecols=(i for i in range(0,10)))
        SIM = simulation_model.Simulation(data)
    except Exception as exception:
        raise UnableToConvertDATFileToArray(f'Unable to load the dat file into array.\n{exception}')


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
