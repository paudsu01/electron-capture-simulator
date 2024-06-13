import vpython

PAUSED = True
SIM_RATE = 30
SIMULATION_ENDED = False
SIMULATION_STARTED = False

GRAPH = vpython.graph(title='Electron Energy graph', xtitle='Time', ytitle='Energy', align='right', width=500, fast=False)

# Create a gvbars object to align GRAPH on top right
bar = vpython.gvbars()
bar.plot(0, 0)

CANVAS = vpython.canvas(visible=True)
CANVAS.select()

PROJECTILE = vpython.sphere(radius=1.5, color=vpython.color.red, make_trail=True)
NUCLEUS = vpython.sphere(radius=1.5,
                         color=vpython.color.green,
                         make_trail=True,
                         opacity=0.5)
ELECTRON = vpython.sphere(radius=1,
                          color=vpython.color.yellow,
                          make_trail=True)
bar.delete()
