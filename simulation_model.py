from __future__ import annotations

import numpy as np


class Simulation(object):

    def __init__(self, coordinate_data : np.ndarray, energy_data : np.ndarray) -> None:

        self.__coordinate_data = coordinate_data
        self.__energy_data = energy_data
        self.__projectile = SimulationObject(self, 0)
        self.__target_nucleus = SimulationObject(self, 3)
        self.__electron = ElectronObject(self, 6)
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
    def data(self) -> np.ndarray:
        return self.__coordinate_data

    @property
    def energy_data(self) -> np.ndarray:
        return self.__energy_data

    @property
    def time(self) -> int:
        return self.__time

    @time.setter
    def time(self, value : int) -> None:
        self.__time = value

    @property
    def actual_time(self) -> float:
        return self.data[self.time][9]


class SimulationObject:

    def __init__(self, simulation : Simulation, offset : int) -> None:

        self._simulation = simulation
        self._offset = offset

    @property
    def x(self) -> float:
        return self._simulation.data[self._simulation.time][0+self._offset]

    @property
    def y(self) -> float:
        return self._simulation.data[self._simulation.time][1+self._offset]

    @property
    def z(self) -> float:
        return self._simulation.data[self._simulation.time][2+self._offset]


class ElectronObject(SimulationObject):

    @property
    def energy_wrt_projectile(self):
        return self._simulation.energy_data[self._simulation.time][0]

    @property
    def energy_wrt_target(self):
        return self._simulation.energy_data[self._simulation.time][1]

