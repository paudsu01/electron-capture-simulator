from __future__ import annotations

import argparse
import os
import re

import numpy
import vpython

import simulation_model
import config
import utils
from exceptions import (DATFileNotProvidedException,
                        UnableToConvertDATFileToArray)


def setup_user_input():

    vpython.button(bind=utils.run_pause_program, text='Pause', background=vpython.color.red)

def start_simulation():

    # Setup user input and options
    setup_user_input()

    vpython.scene.camera.follow(NUCLEUS)

    while SIM.time < len(SIM.data):

        vpython.rate(config.SIM_RATE)
        if not config.PAUSED:

            PROJECTILE.pos = vpython.vector(SIM.projectile.x, SIM.projectile.y, SIM.projectile.z)
            ELECTRON.pos = vpython.vector(SIM.electron.x, SIM.electron.y, SIM.electron.z)
            NUCLEUS.pos = vpython.vector(SIM.target_nucleus.x, SIM.target_nucleus.y, SIM.target_nucleus.z)

            SIM.time += 1

if __name__ == '__main__':

    pattern = re.compile(r'.*\.dat')
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('fileName.dat')
    args = argument_parser.parse_args()

    if pattern.match(vars(args)['fileName.dat']):
        FILENAME = vars(args)['fileName.dat']

        # Load data from .dat file
        try:
            data: numpy.ndarray[numpy.ndarray] = numpy.loadtxt(
                FILENAME, dtype=float, usecols=(i for i in range(0, 10)))


            ### Init ###

            SIM = simulation_model.Simulation(data)
            PROJECTILE = vpython.sphere(radius=2, color=vpython.color.red, make_trail=True)
            NUCLEUS = vpython.sphere(radius=2, color=vpython.color.green, make_trail = True, opacity=0.5)
            ELECTRON = vpython.sphere(radius=1, color=vpython.color.yellow, make_trail=True)

            start_simulation()

        except Exception as exception:
            raise UnableToConvertDATFileToArray(
                f'Unable to load the dat file into array.\n{exception}')

    else:
        raise DATFileNotProvidedException(
            f".dat file required.\nUsage: python {os.path.relpath(__file__)} fileName.dat"
        )
