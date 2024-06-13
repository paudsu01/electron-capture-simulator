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

def add_delete_curves(event: vpython.vpython.checkbox):

    if event.checked:
        plot_graph()
    else:
        PROJECTILE_ENERGY_GRAPH.data = []
        TARGET_ENERGY_GRAPH.data = []

def setup_user_input():

    global pause_button
    global speed_slider
    global stop_button
    global graph_checkbox

    # Run/Pause button
    pause_button = vpython.button(bind=utils.run_pause_program,
                                  text='Run',
                                  background=vpython.color.green)
    config.CANVAS.append_to_caption("\t\t")

    # Camera focus options
    config.CANVAS.append_to_caption("Focus camera on: ")
    vpython.menu(bind=utils.change_camera_focus,
                 choices=['Nucleus', 'Projectile', 'Electron'],
                 index=0)
    config.CANVAS.append_to_caption("\t\t")

    # Pan mode enable button
    utils.setup_camera_pan_button()
    config.CANVAS.append_to_caption("\n\n")

    # Screenshot button
    vpython.button(text='Screenshot',
                   bind=utils.screenshot,
                   background=vpython.color.blue)
    config.CANVAS.append_to_caption("\t\t")

    # Stop button
    stop_button = vpython.button(text='Stop simulation',
                   bind=utils.stop_simulation,
                   background=vpython.color.red)
    config.CANVAS.append_to_caption("\t\t")

    # Enable graph checkbox
    if config.GRAPH_ENABLED:
        graph_checkbox = vpython.checkbox(text='Plot graph',
                    bind=add_delete_curves,
                    background=vpython.color.orange)

    config.CANVAS.append_to_caption("\n\n")

    # Speed slider
    config.CANVAS.append_to_caption("Change the simulation speed:")
    speed_slider = vpython.slider(bind=utils.change_simulation_rate,
                                  value=config.SIM_RATE,
                                  min=1,
                                  max=150)
    utils.setup_w_text_speed(speed_slider.value)
    config.CANVAS.append_to_caption("\n")

    # Help and Tips message
    config.CANVAS.append_to_caption(
        '\n\n\n\t<b>HELP/TIPS</b>:\n\nResize canvas by placing mouse at the egde of the canvas\n\n\t<b>Touchpad</b>:\nZoom in/out : Place two fingers on touchpad and move up/down\nRotate "camera" to view scene : Place two fingers on touchpad and press and move \nPan camera : Shift + press touchpad and move (Simulation needs to be paused !!)'
    )
    config.CANVAS.append_to_caption(
        '\n\n\t<b>Mouse</b>:\nRight button drag or Ctrl-drag to rotate "camera" to view scene.\nTo zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.\nOn a two-button mouse, middle is left + right.\nShift-drag to pan left/right and up/down.\nTouch screen: pinch/extend to zoom, swipe or two-finger rotate\n'
    )


def restart_simulation(event : vpython.vpython.button) -> None:

    # Allow the start_simulation function to be executed
    config.SIMULATION_ENDED = False
    config.SIMULATION_STARTED = False

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
    config.CANVAS.camera.follow(utils.latest_object_followed)

    if config.GRAPH_ENABLED:

        # Remove points from graph
        PROJECTILE_ENERGY_GRAPH.data = []
        TARGET_ENERGY_GRAPH.data = []
        graph_checkbox.disabled =  False

def end_simulation():

    speed_slider.disabled = True
    stop_button.disabled = True
    config.SIMULATION_ENDED = True

    config.PAUSED = False
    utils.run_pause_program(pause_button)
    pause_button.disabled = True

    vpython.button(bind=restart_simulation, text='Restart simulation', background=vpython.color.magenta, pos=config.CANVAS.title_anchor)
    config.CANVAS.append_to_title('\n\n')

def plot_graph():

    PROJECTILE_ENERGY_GRAPH.plot(SIM.actual_time, SIM.electron.energy_wrt_projectile)
    TARGET_ENERGY_GRAPH.plot(SIM.actual_time, SIM.electron.energy_wrt_target)

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
    config.CANVAS.title = f'\t\tSimulation Time elapsed: <b>{SIM.actual_time:.4f}</b>'
 

def start_simulation():

    # Setup the objects in canvas in their required coordinates
    change_coordinates_and_update_time()

    if config.GRAPH_ENABLED:
        if graph_checkbox.checked : plot_graph()

    while SIM.time < len(SIM.data):

        if config.SIMULATION_STARTED and config.GRAPH_ENABLED:
            graph_checkbox.disabled = True

        if config.SIMULATION_ENDED:
            break

        vpython.rate(config.SIM_RATE)

        if not config.PAUSED:

           config.SIMULATION_STARTED = True

           change_coordinates_and_update_time()
           if config.GRAPH_ENABLED and int(SIM.time) % 100 == 0 and graph_checkbox.checked : plot_graph()

           SIM.time += 1

    end_simulation()


if __name__ == '__main__':

    pattern = re.compile(r'.*\.dat')
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('coordinatesfileName.dat')

    # Make the energyfileName.dat positional argument optional
    # Only plot the graph is the argument is provided

    argument_parser.add_argument('energyfileName.dat', nargs='?')

    argument_parser.add_argument('-f', '--fast', help='Use fast mode for graphing instead of the default slow mode (Also needs the energyfileName.dat positional argument provided)', action='store_true')

    args = argument_parser.parse_args()
    COORDINATES_FILE_NAME = vars(args)['coordinatesfileName.dat']
    ENERGY_FILE_NAME = vars(args)['energyfileName.dat']

    if (pattern.match(COORDINATES_FILE_NAME) and ENERGY_FILE_NAME is None) or (pattern.match(COORDINATES_FILE_NAME) and pattern.match(ENERGY_FILE_NAME)):

        enable_graph = False if ENERGY_FILE_NAME is None else True


        # Load data from .dat file
        try:
            coordinates_data: numpy.ndarray[numpy.ndarray] = numpy.loadtxt(
                COORDINATES_FILE_NAME, dtype=float, usecols=(i for i in range(0, 10)))

            if enable_graph:

                energy_data: numpy.ndarray[numpy.ndarray] = numpy.loadtxt(
                    ENERGY_FILE_NAME, dtype=float, usecols=(i for i in range(0, 2)))

                if len(coordinates_data) != len(energy_data):
                    raise DATFilesHaveVaryingLengths(f'Both {COORDINATES_FILE_NAME} and {ENERGY_FILE_NAME} need to have the same number of lines')
            else:
                energy_data = numpy.array([])

            ### Init ###

            # Only load if no error with files
            import config
            config.setup_graph_and_canvas(args.fast, enable_graph)
            config.GRAPH_ENABLED = enable_graph

            import utils

            SIM = simulation_model.Simulation(coordinates_data, energy_data)

            if config.GRAPH_ENABLED:
                PROJECTILE_ENERGY_GRAPH = vpython.gdots(color=vpython.color.red, radius=1.5, graph=config.GRAPH)
                TARGET_ENERGY_GRAPH = vpython.gdots(color=vpython.color.blue, radius=1.5, graph=config.GRAPH)

            # Setup user input and options
            setup_user_input()
            config.CANVAS.camera.follow(config.NUCLEUS)

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
