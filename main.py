from __future__ import annotations

import argparse
import os
import re

import numpy
import vpython

import simulation_model
from exceptions import (DATFileNotProvidedException,
                        UnableToConvertDATFileToArray)


def start_simulation():

    camera_focus_index = 0
    vpython.scene.camera.follow(ELECTRON)
    while SIM.time < len(SIM.data):
        vpython.rate(10)
        keys = vpython.keysdown()
        if 'c' in keys:
            camera_focus_index = (camera_focus_index + 1) % 3
            if camera_focus_index == 1:
                vpython.scene.camera.follow(PROJECTILE)
            elif camera_focus_index == 2:
                vpython.scene.camera.follow(ELECTRON)
            else:
                vpython.scene.camera.follow(NUCLEUS)

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
