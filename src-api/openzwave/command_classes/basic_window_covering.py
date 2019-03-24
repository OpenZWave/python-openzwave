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
import threading
from .command_class_base import CommandClassBase

# Basic Window Covering Command Class - Obsolete
# Application
COMMAND_CLASS_BASIC_WINDOW_COVERING = 0x50


# noinspection PyAbstractClass
class BasicWindowCovering(CommandClassBase):
    """
    Basic Window Covering Command Class

    symbol: `COMMAND_CLASS_BASIC_WINDOW_COVERING`
    """

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_BASIC_WINDOW_COVERING]

        self.__thread = None
        self.__event = threading.Event()

    def window_covering_open(self):
        """
        Window Covering Open

        Opens the window covering.

        :return: if command successfully sent `True`/`False`
        :rtype: bool
        """
        key = ('Open', COMMAND_CLASS_BASIC_WINDOW_COVERING)
        try:
            self[key].data = True
            return True
        except AttributeError:
            return False

    def window_covering_close(self):
        """
        Window Covering Close

        Closes the window covering.

        :return: if command successfully sent `True`/`False`
        :rtype: bool
        """
        key = ('Close', COMMAND_CLASS_BASIC_WINDOW_COVERING)
        try:
            self[key].data = True
            return True
        except AttributeError:
            return False
