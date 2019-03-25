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

# Indicator Command Class - Active
# Management
COMMAND_CLASS_INDICATOR = 0x87


# noinspection PyAbstractClass
class Indicator(CommandClassBase):
    """
    Indicator Command Class

    symbol: `COMMAND_CLASS_INDICATOR`
    """

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_INDICATOR]

    __indicator_doc = """
        Indicator (`property`)

        :param value: ?
        :type value: int
        :return: ? or None if command failed
        :rtype: int, None
    """

    def __indicator_get(self):
        key = ('Indicator', COMMAND_CLASS_INDICATOR)
        try:
            return self[key].data
        except KeyError:
            return None

    def __indicator_set(self, value):
        key = ('Indicator', COMMAND_CLASS_INDICATOR)
        try:
            self[key].data = value
        except KeyError:
            pass

    indicator = property(
        __indicator_get,
        __indicator_set,
        doc=__indicator_doc
    )
