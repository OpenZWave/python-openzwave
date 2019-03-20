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

# Manufacturer Specific Command Class - Active
# Management
# Nodes MUST reply to Manufacturer Specific Get Commands received non-securely
# if S0 is the highest granted key (CC:0072.01.00.41.004)
COMMAND_CLASS_MANUFACTURER_SPECIFIC = 0x72


# noinspection PyAbstractClass
class ManufacturerSpecific(CommandClassBase):
    """
    Manufacturer Specific Command Class

    symbol: `COMMAND_CLASS_MANUFACTURER_SPECIFIC`
    """

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_MANUFACTURER_SPECIFIC]
