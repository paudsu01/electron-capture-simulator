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

    # Run/Pause button
    vpython.button(bind=utils.run_pause_program, text='Pause', background=vpython.color.red)
    vpython.scene.append_to_caption("\t\t")

    # Camera focus options
    vpython.scene.append_to_caption("Focus camera on: ")
    vpython.menu(bind=utils.change_camera_focus, choices=['Nucleus', 'Projectile', 'Electron'], index=0)
    vpython.scene.append_to_caption("\n")

    # Speed slider
    vpython.scene.append_to_caption("Change the simulation speed:")
    speed_slider = vpython.slider(bind=utils.change_simulation_rate, value=config.SIM_RATE, min=1, max=150)
    utils.setup_w_text_speed(speed_slider.value)
    vpython.scene.append_to_caption("\n")


def start_simulation():

    # Setup user input and options
    setup_user_input()

    vpython.scene.camera.follow(config.NUCLEUS)

    while SIM.time < len(SIM.data):

        vpython.rate(config.SIM_RATE)
        if not config.PAUSED:

            config.PROJECTILE.pos = vpython.vector(SIM.projectile.x, SIM.projectile.y, SIM.projectile.z)
            config.ELECTRON.pos = vpython.vector(SIM.electron.x, SIM.electron.y, SIM.electron.z)
            config.NUCLEUS.pos = vpython.vector(SIM.target_nucleus.x, SIM.target_nucleus.y, SIM.target_nucleus.z)

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
            start_simulation()

        except Exception as exception:
            raise UnableToConvertDATFileToArray(
                f'Unable to load the dat file into array.\n{exception}')

    else:
        raise DATFileNotProvidedException(
            f".dat file required.\nUsage: python {os.path.relpath(__file__)} fileName.dat"
        )
