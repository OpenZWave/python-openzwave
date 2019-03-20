# -*- coding: utf-8 -*-
"""
This file is part of **python-openzwave**
project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave API

.. moduleauthor: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com>

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

# Thermostat Fan Mode Command Class - Active
# Application
COMMAND_CLASS_THERMOSTAT_FAN_MODE = 0x44


# noinspection PyAbstractClass
class ThermostatFanMode(CommandClassBase):
    FAN_MODES = [
        'Auto Low',
        'On Low',
        'Auto High',
        'On High',
        'Circulate',
     ]

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_THERMOSTAT_FAN_MODE]

    @property
    def fan_mode(self):
        try:
            return self[('Fan Mode', COMMAND_CLASS_THERMOSTAT_FAN_MODE)].data
        except KeyError:
            return None

    @fan_mode.setter
    def fan_mode(self, value):
        if isinstance(value, int):
            try:
                value = self.FAN_MODES[value]
            except IndexError:
                return

        if value in self.FAN_MODES:
            try:
                self[('Fan Mode', COMMAND_CLASS_THERMOSTAT_FAN_MODE)].data = (
                    value
                )
            except KeyError:
                pass
