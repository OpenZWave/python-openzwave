# -*- coding: utf-8 -*-
"""
This file is part of **python-openzwave**
project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :synopsis: openzwave API

.. moduleauthor: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com> &
 kdschlosser aka Kevin Schlosser

License : GPL(v3)

**python-openzwave** is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

**python-openzwave** is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with python-openzwave. If not, see http://www.gnu.org/licenses.

"""

from .command_class_base import CommandClassBase

# Multilevel Sensor Command Class - Active
# Application
COMMAND_CLASS_SENSOR_MULTILEVEL = 0x31


# noinspection PyAbstractClass
class SensorMultilevel(CommandClassBase):

    SENSOR_TYPES = [
        None,
        'Temperature',
        'General',
        'Luminance',
        'Power',
        'Relative Humidity',
        'Velocity',
        'Direction',
        'Atmospheric Pressure',
        'Barometric Pressure',
        'Solar Radiation',
        'Dew Point',
        'Rain Rate',
        'Tide Level',
        'Weight',
        'Voltage',
        'Current',
        'CO2 Level',
        'Air Flow',
        'Tank Capacity',
        'Distance',
        'Angle Position',
        'Rotation',
        'Water Temperature',
        'Soil Temperature',
        'Seismic Intensity',
        'Seismic Magnitude',
        'Ultraviolet',
        'Electrical Resistivity',
        'Electrical Conductivity',
        'Loudness',
        'Moisture'
    ]

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SENSOR_MULTILEVEL]

    class Sensor(object):

        def __init__(self, value):
            self.__value = value

        @property
        def type(self):
            return self.__value.label

        @property
        def reading(self):
            return self.__value.data, self.__value.units

    @property
    def multilevel_sensors(self):
        res = []
        for value in self[(None, COMMAND_CLASS_SENSOR_MULTILEVEL)]:
            if value.label in self.SENSOR_TYPES:
                res += [self.Sensor(value)]

        return res
