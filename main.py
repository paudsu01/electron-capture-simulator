from __future__ import annotations

import argparse
import os
import re

import numpy
import vpython

import simulation_model
from exceptions import (DATFileNotProvidedException,
                        UnableToConvertDATFileToArray,
                        DATFilesHaveVaryingLengths)


def setup_user_input():

    global pause_button
    global speed_slider
    global stop_button

    # Run/Pause button
    pause_button = vpython.button(bind=utils.run_pause_program,
                                  text='Run',
                                  background=vpython.color.green)
    vpython.scene.append_to_caption("\t\t")

    # Camera focus options
    vpython.scene.append_to_caption("Focus camera on: ")
    vpython.menu(bind=utils.change_camera_focus,
                 choices=['Nucleus', 'Projectile', 'Electron'],
                 index=0)
    vpython.scene.append_to_caption("\t\t")

    # Pan mode enable button
    utils.setup_camera_pan_button()
    vpython.scene.append_to_caption("\n\n")

    # Screenshot button
    vpython.button(text='Screenshot',
                   bind=utils.screenshot,
                   background=vpython.color.blue)
    vpython.scene.append_to_caption("\t\t")

    # Stop button
    stop_button = vpython.button(text='Stop simulation',
                   bind=utils.stop_simulation,
                   background=vpython.color.red)
    vpython.scene.append_to_caption("\n\n")

    # Speed slider
    vpython.scene.append_to_caption("Change the simulation speed:")
    speed_slider = vpython.slider(bind=utils.change_simulation_rate,
                                  value=config.SIM_RATE,
                                  min=1,
                                  max=150)
    utils.setup_w_text_speed(speed_slider.value)
    vpython.scene.append_to_caption("\n")

    # Help and Tips message
    vpython.scene.append_to_caption(
        '\n\n\n\t<b>HELP/TIPS</b>:\n\nResize canvas by placing mouse at the egde of the canvas\n\n\t<b>Touchpad</b>:\nZoom in/out : Place two fingers on touchpad and move up/down\nRotate "camera" to view scene : Place two fingers on touchpad and press and move \nPan camera : Shift + press touchpad and move (Simulation needs to be paused !!)'
    )
    vpython.scene.append_to_caption(
        '\n\n\t<b>Mouse</b>:\nRight button drag or Ctrl-drag to rotate "camera" to view scene.\nTo zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.\nOn a two-button mouse, middle is left + right.\nShift-drag to pan left/right and up/down.\nTouch screen: pinch/extend to zoom, swipe or two-finger rotate\n'
    )


def restart_simulation(event : vpython.vpython.button) -> None:

    # Allow the start_simulation function to be executed
    config.SIMULATION_ENDED = False

    # Delete restart button
    event.delete()

    # Reset simulation time to 0
    SIM.time = 0

    # Enable buttons and slider
    speed_slider.disabled = False
    pause_button.disabled = False
    stop_button.disabled = False

    # Pause the simulation at the beginning
    config.PAUSED = False
    utils.run_pause_program(pause_button)

    # Remove trails created from previous sim run
    config.PROJECTILE.clear_trail()
    config.NUCLEUS.clear_trail()
    config.ELECTRON.clear_trail()

    # Set camers to latest object followed in case pan mode enabled
    vpython.scene.camera.follow(utils.latest_object_followed)


def end_simulation():

    speed_slider.disabled = True
    stop_button.disabled = True
    config.SIMULATION_ENDED = True

    config.PAUSED = False
    utils.run_pause_program(pause_button)
    pause_button.disabled = True

    vpython.button(bind=restart_simulation, text='Restart simulation', background=vpython.color.magenta, pos=vpython.scene.title_anchor)
    vpython.scene.append_to_title('\n\n')

def change_coordinates_and_update_time() -> None:

    config.PROJECTILE.pos = vpython.vector(SIM.projectile.x,
                                           SIM.projectile.y,
                                           SIM.projectile.z)
    config.ELECTRON.pos = vpython.vector(SIM.electron.x,
                                         SIM.electron.y,
                                         SIM.electron.z)
    config.NUCLEUS.pos = vpython.vector(SIM.target_nucleus.x,
                                        SIM.target_nucleus.y,
                                        SIM.target_nucleus.z)
    vpython.scene.title = f'\t\tSimulation Time elapsed: <b>{SIM.actual_time:.4f}</b>'
 

def start_simulation():

    # Setup the objects in canvas in their required coordinates
    change_coordinates_and_update_time()

    while SIM.time < len(SIM.data):

        if config.SIMULATION_ENDED:
            break

        vpython.rate(config.SIM_RATE)

        if not config.PAUSED:

           change_coordinates_and_update_time()
           SIM.time += 1

    end_simulation()


if __name__ == '__main__':

    pattern = re.compile(r'.*\.dat')
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('coordinatesfileName.dat')
    argument_parser.add_argument('energyfileName.dat')

    args = argument_parser.parse_args()

    if pattern.match(vars(args)['coordinatesfileName.dat']) and pattern.match(vars(args)['energyfileName.dat']):

        COORDINATES_FILE_NAME = vars(args)['coordinatesfileName.dat']
        ENERGY_FILE_NAME = vars(args)['energyfileName.dat']


        # Load data from .dat file
        try:
            coordinates_data: numpy.ndarray[numpy.ndarray] = numpy.loadtxt(
                COORDINATES_FILE_NAME, dtype=float, usecols=(i for i in range(0, 10)))

            energy_data: numpy.ndarray[numpy.ndarray] = numpy.loadtxt(
                ENERGY_FILE_NAME, dtype=float, usecols=(i for i in range(0, 2)))

            if len(coordinates_data) != len(energy_data):
                raise DATFilesHaveVaryingLengths(f'Both {COORDINATES_FILE_NAME} and {ENERGY_FILE_NAME} need to have the same number of lines')

            ### Init ###

            # Only load if no error with files
            import config
            import utils

            SIM = simulation_model.Simulation(coordinates_data, energy_data)

            # Setup user input and options
            setup_user_input()
            vpython.scene.camera.follow(config.NUCLEUS)

            # Main while loop
            while True:

                vpython.rate(config.SIM_RATE)
                if not config.SIMULATION_ENDED:
                    start_simulation()

        except Exception as exception:
            raise UnableToConvertDATFileToArray(
                f'Unable to load the dat file into array.\n{exception}')

    else:
        raise DATFileNotProvidedException(
            f".dat file required.\nUsage: python {os.path.relpath(__file__)} coordinatesfileName.dat energyfileName.dat"
        )
