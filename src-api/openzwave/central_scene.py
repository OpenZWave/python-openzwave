# -*- coding: utf-8 -*-
"""
.. module:: openzwave.central_scene

This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave API

.. moduleauthor: Kevin Schlosser (@kdschlosser)

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

from .object import ZWaveNodeInterface


class ZWaveNodeCentralScene(ZWaveNodeInterface):

    @property
    def scenes(self):
        """
        Gets Scenes associated with this node.

        COMMAND_CLASS_CENTRAL_SCENE

        :return: list of class:`openzwave.value.ZWaveValue` instances
        :rtype: list
        """
        if 0x5B not in self._value_index_mapping:
            return []

        res = []

        start = self._value_index_mapping[0x5B].indexes.start
        end = self._value_index_mapping[0x5B].indexes.end + 1

        for i in range(start, end):
            if self._value_index_mapping[0x5B][i] is not None:
                res += [self._value_index_mapping[0x5B][i]]

        return res
