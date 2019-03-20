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

# Thermostat Mode Command Class - Active
# Application
COMMAND_CLASS_THERMOSTAT_MODE = 0x40


# noinspection PyAbstractClass
class ThermostatMode(CommandClassBase):
    MODES = [
        'Off',
        'Heat',
        'Cool',
        'Auto',
        'Aux Heat',
        'Resume',
        'Fan Only',
        'Furnace',
        'Dry Air',
        'Moist Air',
        'Auto Changeover',
        'Heat Econ',
        'Cool Econ',
        'Away',
    ]

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_THERMOSTAT_MODE]

    @property
    def operating_mode(self):
        try:
            return self[('Mode', COMMAND_CLASS_THERMOSTAT_MODE)].data
        except KeyError:
            return None

    @operating_mode.setter
    def operating_mode(self, value):
        if isinstance(value, int):
            try:
                value = self.MODES[value]
            except IndexError:
                return

        if value in self.MODES:
            try:
                self[('Mode', COMMAND_CLASS_THERMOSTAT_MODE)].data = (
                    value
                )
            except KeyError:
                pass

