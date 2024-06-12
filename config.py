import vpython

PAUSED = False
SIM_RATE = 30

PROJECTILE = vpython.sphere(radius=2, color=vpython.color.red, make_trail=True)
NUCLEUS = vpython.sphere(radius=2,
                         color=vpython.color.green,
                         make_trail=True,
                         opacity=0.5)
ELECTRON = vpython.sphere(radius=1,
                          color=vpython.color.yellow,
                          make_trail=True)
