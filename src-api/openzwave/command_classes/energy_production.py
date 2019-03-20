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

# Energy Production Command Class - Active
# Application
COMMAND_CLASS_ENERGY_PRODUCTION = 0x90


# noinspection PyAbstractClass
class EnergyProduction(CommandClassBase):
    """
    Energy Production Command Class

    symbol: `COMMAND_CLASS_ENERGY_PRODUCTION`
    """

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_ENERGY_PRODUCTION]

    @property
    def current_energy_production(self):
        key = ('Instant energy production', COMMAND_CLASS_ENERGY_PRODUCTION)
        try:
            return self[key].data
        except KeyError:
            return None

    @property
    def total_energy_production(self):
        key = ('Total energy production', COMMAND_CLASS_ENERGY_PRODUCTION)
        try:
            return self[key].data
        except KeyError:
            return None

    @property
    def energy_production_today(self):
        key = ('Energy production today', COMMAND_CLASS_ENERGY_PRODUCTION)
        try:
            return self[key].data
        except KeyError:
            return None

    @property
    def total_energy_production_time(self):
        key = ('Total production time', COMMAND_CLASS_ENERGY_PRODUCTION)
        try:
            return self[key].data
        except KeyError:
            return None
