from __future__ import annotations

import config
import vpython
import string
import random

speed_wtext = None
name_to_object_dict = {'Nucleus': config.NUCLEUS, 'Projectile': config.PROJECTILE, 'Electron': config.ELECTRON}

def change_camera_focus(event: vpython.vpython.menu) -> None:
    vpython.scene.camera.follow(name_to_object_dict[event.selected])

def run_pause_program(event : vpython.vpython.button) -> None:

    config.PAUSED = False if config.PAUSED else True
    event.text = 'Run' if event.text == 'Pause' else 'Pause'
    event.background = vpython.color.green if event.background == vpython.color.red else vpython.color.red

def change_simulation_rate(event :vpython.vpython.slider) -> None:

    config.SIM_RATE = event.value
    setup_w_text_speed(event.value, False)

def setup_w_text_speed(value : int, firstTime : bool = True) -> None:

    global speed_wtext

    if firstTime:
        speed_wtext = vpython.wtext(text=value)
    else:
        speed_wtext.text = value

def screenshot(evt: vpython.vpython.button) -> None:
    vpython.scene.capture(random_text_generator())

def random_text_generator() -> str:

    length = random.randint(8,15)
    options = string.ascii_letters + ''.join([str(i) for i in range(10)])
    return ''.join([random.choice(options) for i in range(length)])