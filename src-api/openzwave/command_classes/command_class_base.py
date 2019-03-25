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

    @property
    def values(self):
        raise NotImplementedError

    @property
    def network(self):
        raise NotImplementedError

    @property
    def id(self):
        raise NotImplementedError

    @property
    def home_id(self):
        raise NotImplementedError

    def has_command_class(self, class_id):
        """
        Check that this node use this commandClass.

        :param class_id: the COMMAND_CLASS to check
        :type class_id: int
        :rtype: bool

        """
        return self == class_id

    @property
    def command_classes(self):
        """
        The commandClasses of the node.

        :rtype: set()

        """
        return self._cls_ids[:]

    @property
    def command_classes_as_string(self):
        """
        Return the command classes of the node as string.

        :rtype: set()

        """
        commands = self.command_classes
        command_str = set()
        for cls in commands:
            command_str.add(self.network.manager.COMMAND_CLASS_DESC[cls])
        return ', '.join(c for c in command_str)

    def get_command_class_as_string(self, class_id):
        """
        Return the command class representation as string.

        :param class_id: the COMMAND_CLASS to get string representation
        :type class_id: hexadecimal code
        :rtype: str

        """
        return self.network.manager.COMMAND_CLASS_DESC[class_id]

    def get_command_class_genres(self):
        """
        Return the list of genres of command classes

        :rtype: set()

        """

        res = set()
        for value in self.values:
            res.add(value.genre)

        return res

    def get_values_by_command_classes(
        self,
        genre='All',
        type='All',
        readonly='All',
        writeonly='All'
    ):
        """
        Retrieve values in a dict() of dicts(). The dict is indexed on the
        COMMAND_CLASS.

        This allows to browse values grouped by the COMMAND_CLASS.You can
        optionally filter for a command class, a genre and/or a type. You can
        also filter readonly and writeonly params.

        This method always filter the values.
        If you want to get all the nodes values, use the property
        self.values instead.

        :param genre: the genre of value
        :type genre: 'All' or PyGenres
        :param type: the type of value
        :type type: 'All' or PyValueTypes
        :param readonly: Is this value readonly
        :type readonly: 'All' or True or False
        :param writeonly: Is this value writeonly
        :type writeonly: 'All' or True or False
        :rtype: dict(command_class : dict(valueids))

        """
        values = dict()
        for value_id, value in self.values.items():

            if (
                genre in ('All', value.genre) and
                type in ('All', value.type) and
                readonly in ('All', value.is_read_only) and
                writeonly in ('All', value.is_write_only)
            ):
                if value.command_class not in values:
                    values[value.command_class] = dict()

                values[value.command_class][value_id] = value

        return values

    def get_values_for_command_class(self, class_id):
        """
        Retrieve the set of values for a command class.
        Deprecated
        For backward compatibility only.
        Use get_values instead

        :param class_id: the COMMAND_CLASS to get values
        :type class_id: hexadecimal code or string
        :type writeonly: 'All' or True or False
        :rtype: set() of classId

        """
        # print class_id

        res = []

        for value in self.values.values():
            if value.command_class == class_id:
                res += [value]

        return res


# noinspection PyAbstractClass
class EmptyCommandClass(CommandClassBase):
    pass


