import vpython

PAUSED = True
SIM_RATE = 30
SIMULATION_ENDED = False
SIMULATION_STARTED = False
GRAPH_ENABLED = True

def setup_graph_and_canvas(fastGraph, enable_graph):

    global GRAPH
    global CANVAS
    global PROJECTILE
    global NUCLEUS
    global ELECTRON

    if enable_graph:
        GRAPH = vpython.graph(title='Electron Energy graph', xtitle='Time', ytitle='Energy', align='right', width=500, fast=fastGraph)

        # Create a gvbars object to align GRAPH on top right
        bar = vpython.gvbars()
        bar.plot(0, 0)
    
    CANVAS = vpython.canvas(visible=True)
    CANVAS.select()
    
    PROJECTILE = vpython.sphere(radius=0.5, color=vpython.color.red, make_trail=True, opacity=0.5)
    NUCLEUS = vpython.sphere(radius=0.5,
                             color=vpython.color.green,
                             make_trail=True,
                             opacity=0.5)
    ELECTRON = vpython.sphere(radius=0.15,
                              color=vpython.color.yellow,
                              make_trail=True)
    if enable_graph:
        bar.delete()
