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

    def switch_stop_ramp(self):
        if self.__thread is not None:
            self.__event.set()
            self.__thread.join()

    def switch_ramp_up(self, level, speed=0.17, step=1):
        self.switch_stop_ramp()

        try:
            value = self[('Level', COMMAND_CLASS_SWITCH_MULTILEVEL)]
        except KeyError:
            return

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

    def switch_ramp_down(self, level, speed=0.17, step=1):
        self.switch_stop_ramp()

        try:
            value = self[('Level', COMMAND_CLASS_SWITCH_MULTILEVEL)]
        except KeyError:
            return

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
    def switch_step_size(self):
        key = ('Step Size', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    @switch_step_size.setter
    def switch_step_size(self, value):
        key = ('Step Size', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            self[key].data = value
        except KeyError:
            pass

    @property
    def switch_dimming_duration(self):
        key = ('Dimming Duration', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    @switch_dimming_duration.setter
    def switch_dimming_duration(self, value):
        key = ('Dimming Duration', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            self[key].data = value
        except KeyError:
            pass

    @property
    def switch_light_level(self):
        key = ('Level', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    @switch_light_level.setter
    def switch_light_level(self, value):
        if 99 < value < 255:
            value = 99
        elif value < 0:
            value = 0

        self.switch_stop_ramp()

        key = ('Level', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            self[key].data = value
        except KeyError:
            pass

    @property
    def switch_ignore_start_level(self):
        key = ('Ignore Start Level', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    @switch_ignore_start_level.setter
    def switch_ignore_start_level(self, value):
        key = ('Ignore Start Level', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            self[key].data = value
        except KeyError:
            pass

    @property
    def switch_start_level(self):
        key = ('Start Level', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    @switch_start_level.setter
    def switch_start_level(self, value):
        key = ('Start Level', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            self[key].data = value
        except KeyError:
            pass

    def switch_increase_level(self):
        self.switch_stop_ramp()

        key = ('Inc', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            self[key].data = True
            return True
        except KeyError:
            return False

    def switch_decrease_level(self):
        self.switch_stop_ramp()

        key = ('Dec', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            self[key].data = True
            return True
        except KeyError:
            return False

    def switch_on_bright(self):
        self.switch_stop_ramp()

        key = ('Bright', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            self[key].data = True
            return True
        except KeyError:
            return False

    def switch_on_dim(self):
        self.switch_stop_ramp()

        key = ('Dim', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            self[key].data = True
            return True
        except KeyError:
            return False

