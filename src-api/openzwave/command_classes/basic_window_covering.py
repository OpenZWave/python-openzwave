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

    @property
    def is_window_covering_opening(self):
        key = ('Open', COMMAND_CLASS_BASIC_WINDOW_COVERING)
        try:
            return self[key].data is True
        except KeyError:
            return False

    @property
    def is_window_covering_closing(self):
        key = ('Close', COMMAND_CLASS_BASIC_WINDOW_COVERING)

        try:
            return self[key].data is False
        except KeyError:
            return False

    def open_window_covering(self, duration=0.0):
        key = ('Open', COMMAND_CLASS_BASIC_WINDOW_COVERING)

        self.stop_window_covering()

        if duration == 0:
            try:
                self[key].data = True
                return True
            except KeyError:
                return False
        else:
            def run(dur):
                try:
                    self[key].data = True
                    self.__event.wait(dur)
                except KeyError:
                    pass

                try:
                    self[key].data = False
                except KeyError:
                    pass

                self.__thread = None
                self.__event.clear()

            self.__thread = threading.Thread(
                target=run,
                args=(duration,)
            )
            self.__thread.daemon = True
            self.__thread.start()

            return True

    def stop_window_covering(self):
        if self.__thread is not None:
            self.__event.set()
            self.__thread.join()

        for key in ('Open', 'Close'):
            key = (key, COMMAND_CLASS_BASIC_WINDOW_COVERING)

            try:
                self[key].data = False
            except KeyError:
                pass

    def close_window_covering(self, duration=0.0):
        key = ('Close', COMMAND_CLASS_BASIC_WINDOW_COVERING)

        self.stop_window_covering()

        if duration == 0:
            try:
                self[key].data = True
                return True
            except KeyError:
                return False
        else:
            def run(dur):
                try:
                    self[key].data = True
                    self.__event.wait(dur)
                except KeyError:
                    pass

                try:
                    self[key].data = False
                except KeyError:
                    pass

                self.__thread = None
                self.__event.clear()

            self.__thread = threading.Thread(
                target=run,
                args=(duration,)
            )
            self.__thread.daemon = True
            self.__thread.start()

            return True
