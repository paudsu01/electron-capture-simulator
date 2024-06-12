from __future__ import annotations

import config
import vpython

def run_pause_program(event : vpython.vpython.button) -> None:

    config.PAUSED = False if config.PAUSED else True
    event.text = 'Run' if event.text == 'Pause' else 'Pause'
    event.background = vpython.color.green if event.background == vpython.color.red else vpython.color.red
