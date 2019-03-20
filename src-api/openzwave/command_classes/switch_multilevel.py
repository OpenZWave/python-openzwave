# -*- coding: utf-8 -*-
"""
This file is part of **python-openzwave**
project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave API

.. moduleauthor: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com>

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
import time
from .command_class_base import CommandClassBase

# Multilevel Switch Command Class - Active
# Application
COMMAND_CLASS_SWITCH_MULTILEVEL = 0x26


# noinspection PyAbstractClass
class SwitchMultilevel(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SWITCH_MULTILEVEL]

        self.__event = threading.Event()
        self.__thread = None

    def stop_ramp(self):
        if self.__thread is not None:
            self.__event.set()
            self.__thread.join()

    def ramp_up(self, level, speed=0.17, step=1):
        try:
            value = self[('Level', COMMAND_CLASS_SWITCH_MULTILEVEL)]
        except KeyError:
            return

        self.stop_ramp()

        def do(val, stp, spd, lvl):
            self.__event.clear()

            while not self.__event.isSet():

                new_level = val.data + stp
                start = time.time()

                val.data = new_level
                self.__event.wait(spd)

                if val.data >= lvl:
                    break

                stop = time.time()
                finish = (stop - start) * 1000
                if finish < spd * 1000:
                    self.__event.wait(((spd * 1000) - finish) / 1000)

            self.__thread = None

        self.__thread = t = threading.Thread(
            target=do,
            args=(value, step, speed, level)
        )

        t.daemon = True
        t.start()

    def ramp_down(self, level, speed=0.17, step=1):
        try:
            value = self[('Level', COMMAND_CLASS_SWITCH_MULTILEVEL)]
        except KeyError:
            return

        self.stop_ramp()

        def do(val, stp, spd, lvl):
            self.__event.clear()

            while not self.__event.isSet():

                new_level = val.data - stp
                start = time.time()

                val.data = new_level
                self.__event.wait(spd)

                if val.data <= lvl:
                    break

                stop = time.time()

                finish = (stop - start) * 1000
                if finish < spd * 1000:
                    self.__event.wait(((spd * 1000) - finish) / 1000)

            self.__thread = None

        self.__thread = t = threading.Thread(
            target=do,
            args=(value, step, speed, level)
        )
        t.daemon = True
        t.start()

    @property
    def level(self):
        try:
            return self[('Level', COMMAND_CLASS_SWITCH_MULTILEVEL)].data
        except KeyError:
            return None

    @level.setter
    def level(self, value):
        if 99 < value < 255:
            value = 99
        elif value < 0:
            value = 0

        self.stop_ramp()

        try:
            self[('Level', COMMAND_CLASS_SWITCH_MULTILEVEL)].data = value
        except KeyError:
            pass

