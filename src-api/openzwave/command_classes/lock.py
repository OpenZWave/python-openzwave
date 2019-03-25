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

# Lock Command Class - Depreciated
# Application
COMMAND_CLASS_LOCK = 0x76


# noinspection PyAbstractClass
class Lock(CommandClassBase):
    """
    Lock Command Class

    symbol: `COMMAND_CLASS_LOCK`
    """

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_LOCK]

    __lock_locked_doc = """
        Lock Locked (`property`)

        :param value: state `True`/`False`
        :type value: bool
        :return: `True`/`False` or None if command failed
        :rtype: bool, None
    """

    def __lock_locked_get(self):
        key = ('Locked', COMMAND_CLASS_LOCK)
        try:
            return self[key].data
        except KeyError:
            return None

    def __lock_locked_set(self, value):
        key = ('Locked', COMMAND_CLASS_LOCK)
        try:
            self[key].data = value
        except KeyError:
            pass

    lock_locked = property(
        __lock_locked_get,
        __lock_locked_set,
        doc=__lock_locked_doc
    )
