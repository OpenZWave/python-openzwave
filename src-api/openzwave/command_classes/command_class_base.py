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


class CommandClassBase(object):

    def __init__(self):
        self._cls_ids = getattr(self, '_cls_ids', [])
        self.values = getattr(self, 'values', {})
        self._network = getattr(self, '_network', None)

    def get_values(self, *_, **__):
        raise NotImplementedError

    def __iter__(self):
        return iter(list(self.values.values()))

    def __getitem__(self, key):
        if isinstance(key, tuple):
            key, command_class = key
        else:
            command_class = None

        if isinstance(key, slice):
            value_indices = sorted(
                list(value.index for value in self),
                key=int
            )

            values = []
            while value_indices:
                index = value_indices.pop(0)
                for value in self:
                    if (
                        command_class is not None and
                        command_class != value.command_class
                    ):
                        continue

                    if value.index == index:
                        values += [value]

            return values[key]

        if key is None:
            return list(
                value for value in self
                if command_class is None or
                value.command_class == command_class
            )

        if isinstance(key, int):
            if key == -1:
                found_value = None

                for value in self:
                    if (
                        command_class is None or
                        value.command_class == command_class
                    ):
                        if (
                            found_value is None or
                            found_value.index > value.index
                        ):
                            found_value = value

                if found_value is not None:
                    return found_value

                raise IndexError('There are no values available')

            else:
                if key in self.values:
                    if (
                        command_class is None or
                        self.values[key].command_class == command_class
                    ):
                        return self.values[key]

                raise IndexError('There is no value id ' + str(key))
        else:
            found_value = None

            for value in self:
                if (
                    value.label != key or
                    (
                        command_class is not None and
                        value.command_class != command_class
                    )
                ):
                    continue

                if found_value is None or found_value.index > value.index:
                    found_value = value

            if found_value is not None:
                return found_value

            raise KeyError('No Value with the label ' + key)


# noinspection PyAbstractClass
class EmptyCommandClass(CommandClassBase):
    pass


