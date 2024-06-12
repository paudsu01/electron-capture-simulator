from __future__ import annotations

import numpy as np


class Simulation(object):

    def __init__(self, data : np.ndarray) -> None:

        self.__data = data
        self.__projectile = SimulationObject(self, 0)
        self.__target_nucleus = SimulationObject(self, 3)
        self.__electron = SimulationObject(self, 6)
        self.__time = 0

    @property
    def projectile(self) -> SimulationObject:
        return self.__projectile

    @property
    def target_nucleus(self) -> SimulationObject:
        return self.__target_nucleus

    @property
    def electron(self) -> SimulationObject:
        return self.__electron

    @property
    def data(self) -> SimulationObject:
        return self.__data

    @property
    def time(self) -> SimulationObject:
        return self.__time

    @time.setter
    def time(self, value : int) -> None:
        self.__time = value

class SimulationObject:

    def __init__(self, simulation : Simulation, offset : int) -> None:

        self.__simulation = simulation
        self._offset = offset

    @property
    def x(self) -> float:
        return self.__simulation.data[self.__simulation.time][0+self._offset]

    @property
    def y(self) -> float:
        return self.__simulation.data[self.__simulation.time][1+self._offset]

    @property
    def z(self) -> float:
        return self.__simulation.data[self.__simulation.time][2+self._offset]

