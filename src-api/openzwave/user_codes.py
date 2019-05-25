# -*- coding: utf-8 -*-
"""
.. module:: openzwave.user_codes

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


class ZWaveUserCodes(object):

    def __init__(self, indices):
        self._indices = indices

    def __setitem__(self, key, value):
        start = self._indices.indexes.start
        end = self._indices.indexes.end

        if isinstance(key, int):
            if start <= key <= end:
                if value not in self:
                    self._indices[key].data = value
            else:
                raise IndexError(str(key))

        else:
            for i in range(start, end + 1):
                if (
                    self._indices[i] is not None and
                    self._indices[i].label == key
                ):
                    self._indices[i].data = value
                    break
            else:
                i = start + len(self)

                if i > end:
                    raise KeyError('Maximum Codes reached.')

                self._indices[i].label = key
                self._indices[i].data = value

    def append(self, code):
        if code in self:
            return False

        start = self._indices.indexes.start

        try:
            self[start + len(self)] = code
            return True
        except IndexError:
            return False

    def remove(self, code):
        if code in self:
            self._indices.remove_code.data = code
            return True
        return False

    def __radd__(self, other):
        for code in other:
            if not self.append(code):
                break

    def __contains__(self, item):
        start = self._indices.indexes.start
        end = self._indices.indexes.end

        for i in range(start, end + 1):
            if (
                self._indices[i] is not None and
                item in (self._indices[i].data, self._indices[i].label)
            ):
                return True

        return False

    def extend(self, codes):
        for code in codes:
            if not self.append(code):
                return False
        return True

    def __len__(self):
        return self._indices.count.data

