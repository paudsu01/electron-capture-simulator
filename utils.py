from __future__ import annotations

import random
import string

import vpython

import config

speed_wtext = None
camera_pan_button = None

name_to_object_dict = {
    'Nucleus': config.NUCLEUS,
    'Projectile': config.PROJECTILE,
    'Electron': config.ELECTRON
}
latest_object_followed = config.NUCLEUS


def enable_pan_mode(event: vpython.vpython.checkbox) -> None:

    if event.text == "Pan mode: disabled" or event.text == 'Enable Pan mode':
        config.CANVAS.camera.follow(None)
        camera_pan_button.text = "Pan mode: enabled"
    else:
        config.CANVAS.camera.follow(latest_object_followed)
        camera_pan_button.text = "Pan mode: disabled"


def change_camera_focus(event: vpython.vpython.menu) -> None:

    global latest_object_followed
    latest_object_followed = name_to_object_dict[event.selected]

    config.CANVAS.camera.follow(latest_object_followed)
    camera_pan_button.text = "Enable Pan mode"


def run_pause_program(event: vpython.vpython.button) -> None:

    config.PAUSED = False if config.PAUSED else True
    event.text = 'Run' if config.PAUSED else 'Pause'
    event.background = vpython.color.green if config.PAUSED else vpython.color.red
    if config.PAUSED:
        camera_pan_button.disabled = False
        camera_pan_button.text = "Enable Pan mode"
    else:
        camera_pan_button.disabled = True
        camera_pan_button.text = "Enable Pan mode"
        config.CANVAS.camera.follow(latest_object_followed)


def change_simulation_rate(event: vpython.vpython.slider) -> None:

    config.SIM_RATE = event.value
    setup_w_text_speed(event.value, False)


def setup_w_text_speed(value: int, firstTime: bool = True) -> None:

    global speed_wtext

    if firstTime:
        speed_wtext = vpython.wtext(text=value)
    else:
        speed_wtext.text = value


def setup_camera_pan_button() -> None:

    global camera_pan_button

    camera_pan_button = vpython.button(text='Enable Pan mode',
                                       bind=enable_pan_mode,
                                       background=vpython.color.cyan,
                                       disabled=not config.PAUSED)

def stop_simulation(event: vpython.vpython.button) -> None:

    config.SIMULATION_ENDED = True

def screenshot(evt: vpython.vpython.button) -> None:

    config.CANVAS.capture(random_text_generator())


def random_text_generator() -> str:

    length = random.randint(8, 15)
    options = string.ascii_letters + ''.join([str(i) for i in range(10)])
    return ''.join([random.choice(options) for i in range(length)])
