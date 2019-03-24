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
        """
        Stop dimmer ramp.

        This method stops any dimmers that are ramping using either
        :func:`switch_multilevel.SwitchMultilevel.switch_ramp_up`
        or
        :func:`switch_multilevel.SwitchMultilevel.switch_ramp_down`

        :return: None
        :rtype: None
        """
        if self.__thread is not None:
            self.__event.set()
            self.__thread.join()

    def switch_ramp_up(self, level, speed=0.17, step=1):
        """
        Ramp up a dimmer switch

        Allows you to control how fast a dimmer switch will increase it's
        brightness. This is a fickle process and it will require some fine
        tuning based on your network. There are quite a few factors that can
        cause an undesirable effect. One being far away the node is from
        the controller, another is how many nodes are on the network. There
        is no "one size fits all" solution. If you want to stop the ramping
        process you will use
        :func:`switch_multilevel.SwitchMultilevel.switch_stop_ramp`

        :param level: The level to stop at
        :type level: int
        :param speed: the duration of time between level changes
        :type speed: float
        :param step: how many levels to increase after each duration has passed
        :type step: int
        :return: None
        :rtype: None
        """
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
        """
        Ramp down a dimmer switch

        Allows you to control how fast a dimmer switch will decrease it's
        brightness. This is a fickle process and it will require some fine
        tuning based on your network. There are quite a few factors that can
        cause an undesirable effect. One being far away the node is from
        the controller, another is how many nodes are on the network. There
        is no "one size fits all" solution. If you want to stop the ramping
        process you will use
        :func:`switch_multilevel.SwitchMultilevel.switch_stop_ramp`

        :param level: The level to stop at
        :type level: int
        :param speed: the duration of time between level changes
        :type speed: float
        :param step: how many levels to decrease after each duration has passed
        :type step: int
        :return: None
        :rtype: None
        """
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

    __switch_secondary_step_doc = """
        Secondary Switch Step Size (`property`)
        
        Sets the number of "steps" or levels to change the secondary switch.
        
        This feature is only available for version 3 and higher dimmers
        
        :param value: the number of steps to take
        :type value: int
        :return: the number of steps taken
        :rtype: int
    """

    def __switch_secondary_step_get(self):

        key = ('Step Size', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    def __switch_secondary_step_set(self, value):
        key = ('Step Size', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            self[key].data = value
        except KeyError:
            pass

    switch_secondary_step = property(
        __switch_secondary_step_get,
        __switch_secondary_step_set,
        doc=__switch_secondary_step_doc
    )

    __switch_dimming_duration_doc = """
        Switch Dimming Duration (`property`)
        
        Sets the amount of time it takes to get to the target level.
        
        This feature is only available for version 3 and higher dimmers
        
        
        :param value: the duration to target level (ms)
        :type value: int
        :return: the duration to target level (ms)
        :rtype: int
    """

    def __switch_dimming_duration_get(self):
        key = ('Dimming Duration', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    def __switch_dimming_duration_set(self, value):
        key = ('Dimming Duration', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            self[key].data = value
        except KeyError:
            pass

    switch_dimming_duration = property(
        __switch_dimming_duration_get,
        __switch_dimming_duration_set,
        doc=__switch_dimming_duration_doc
    )

    __switch_level_doc = """
        Switch Light Level (`property`)

        Adjusts the level of a switch

        :param value: target level (%)
        :type value: int
        :return: current level (%)
        :rtype: int
    """

    def __switch_level_get(self):
        key = ('Level', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    def __switch_level_set(self, value):
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

    switch_level = property(
        __switch_level_get,
        __switch_level_set,
        doc=__switch_level_doc
    )

    __switch_ignore_start_level_doc = """
        Ignore Start Level (`property`)

        Ignores the starting level the switch has stored.

        :param value: ignore start level `True`/`False`
        :type value: bool
        :return: is ignoring start level `True`/`False`
        :rtype: bool
    """

    def __switch_ignore_start_level_get(self):
        key = ('Ignore Start Level', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    def __switch_ignore_start_level_set(self, value):
        key = ('Ignore Start Level', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            self[key].data = value
        except KeyError:
            pass

    switch_ignore_start_level = property(
        __switch_ignore_start_level_get,
        __switch_ignore_start_level_set,
        doc=__switch_ignore_start_level_doc
    )

    __switch_start_level_doc = """
        Switch Start Level (`property`)

        Changes the initial level of a level change

        :param value: start level (%)
        :type value: int
        :return: current start level (%)
        :rtype: int
    """

    def __switch_start_level_get(self):
        key = ('Start Level', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    def __switch_start_level_set(self, value):
        key = ('Start Level', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            self[key].data = value
        except KeyError:
            pass

    switch_start_level = property(
        __switch_start_level_get,
        __switch_start_level_set,
        doc=__switch_start_level_doc
    )

    def switch_secondary_increase_level(self):
        """
        Increase level for Secondary Switch Type

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        self.switch_stop_ramp()

        key = ('Inc', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            self[key].data = True
            return True
        except KeyError:
            return False

    def switch_secondary_decrease_level(self):
        """
        Decrease level for Secondary Switch Type

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        self.switch_stop_ramp()

        key = ('Dec', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            self[key].data = True
            return True
        except KeyError:
            return False

    def switch_bright(self):
        """
        Bright

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        self.switch_stop_ramp()

        key = ('Bright', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            self[key].data = True
            return True
        except KeyError:
            return False

    def switch_dim(self):
        """
        Dim

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        self.switch_stop_ramp()

        key = ('Dim', COMMAND_CLASS_SWITCH_MULTILEVEL)
        try:
            self[key].data = True
            return True
        except KeyError:
            return False

    def switch_on(self):
        """
        On

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        self.switch_stop_ramp()

        values = self._get_values('On')
        if len(values):
            values[0].data = True
            return True

        return False

    def switch_off(self):
        """
        Off

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        self.switch_stop_ramp()

        values = self._get_values('Off')
        if len(values):
            values[0].data = True
            return True

        return False

    def switch_up(self):
        """
        Direction Up

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        self.switch_stop_ramp()

        values = self._get_values('Up')
        if len(values):
            values[0].data = True
            return True

        return False

    def switch_down(self):
        """
        Direction Down

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        self.switch_stop_ramp()

        values = self._get_values('Down')
        if len(values):
            values[0].data = True
            return True

        return False

    def switch_open(self):
        """
        Open

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        self.switch_stop_ramp()

        values = self._get_values('Open')
        if len(values):
            values[0].data = True
            return True

        return False

    def switch_closed(self):
        """
        Close

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        self.switch_stop_ramp()

        values = self._get_values('Closed')
        if len(values):
            values[0].data = True
            return True

        return False

    def switch_clockwise(self):
        """
        Turn Clockwise

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        self.switch_stop_ramp()

        values = self._get_values('Clockwise')
        if len(values):
            values[0].data = True
            return True

        return False

    def switch_counter_clockwise(self):
        """
        Turn Counter-Clockwise

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        self.switch_stop_ramp()

        values = self._get_values('Counter-Clockwise')
        if len(values):
            values[0].data = True
            return True

        return False

    def switch_right(self):
        """
        Direction Right

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        self.switch_stop_ramp()

        values = self._get_values('Right')
        if len(values):
            values[0].data = True
            return True

        return False

    def switch_left(self):
        """
        Direction Left

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        self.switch_stop_ramp()

        values = self._get_values('Left')
        if len(values):
            values[0].data = True
            return True

        return False

    def switch_forward(self):
        """
        Direction Forward

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        self.switch_stop_ramp()

        values = self._get_values('Forward')
        if len(values):
            values[0].data = True
            return True

        return False

    def switch_reverse(self):
        """
        Direction Reverse

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        self.switch_stop_ramp()

        values = self._get_values('Reverse')
        if len(values):
            values[0].data = True
            return True

        return False

    def switch_push(self):
        """
        Push

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        self.switch_stop_ramp()

        values = self._get_values('Push')
        if len(values):
            values[0].data = True
            return True

        return False

    def switch_pull(self):
        """
        Pull

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        self.switch_stop_ramp()

        values = self._get_values('Pull')
        if len(values):
            values[0].data = True
            return True

        return False

    def switch_secondary_on(self):
        """
        Secondary On

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        values = self._get_values('On')
        if len(values) == 2:
            values[-1].data = True
            return True

        return False

    def switch_secondary_off(self):
        """
        Secondary Off

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        values = self._get_values('Off')
        if len(values) == 2:
            values[-1].data = True
            return True

        return False

    def switch_secondary_up(self):
        """
        Secondary Direction Up

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        values = self._get_values('Up')
        if len(values) == 2:
            values[-1].data = True
            return True

        return False

    def switch_secondary_down(self):
        """
        Secondary Direction Down

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        values = self._get_values('Down')
        if len(values) == 2:
            values[-1].data = True
            return True

        return False

    def switch_secondary_open(self):
        """
        Secondary Open

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        values = self._get_values('Open')
        if len(values) == 2:
            values[-1].data = True
            return True

        return False

    def switch_secondary_closed(self):
        """
        Secondary Close

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        values = self._get_values('Closed')
        if len(values) == 2:
            values[-1].data = True
            return True

        return False

    def switch_secondary_clockwise(self):
        """
        Secondary Turn Clockwise

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        values = self._get_values('Clockwise')
        if len(values) == 2:
            values[-1].data = True
            return True

        return False

    def switch_secondary_counter_clockwise(self):
        """
        Secondary Turn Counter-Clockwise

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        values = self._get_values('Counter-Clockwise')
        if len(values) == 2:
            values[-1].data = True
            return True

        return False

    def switch_secondary_right(self):
        """
        Secondary Direction Right

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        values = self._get_values('Right')
        if len(values) == 2:
            values[-1].data = True
            return True

        return False

    def switch_secondary_left(self):
        """
        Secondary Direction Left

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        values = self._get_values('Left')
        if len(values) == 2:
            values[-1].data = True
            return True

        return False

    def switch_secondary_forward(self):
        """
        Secondary Direction Forward

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        values = self._get_values('Forward')
        if len(values) == 2:
            values[-1].data = True
            return True

        return False

    def switch_secondary_reverse(self):
        """
        Secondary Direction Reverse

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        values = self._get_values('Reverse')
        if len(values) == 2:
            values[-1].data = True
            return True

        return False

    def switch_secondary_push(self):
        """
        Secondary Push

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        values = self._get_values('Push')
        if len(values) == 2:
            values[-1].data = True
            return True

        return False

    def switch_secondary_pull(self):
        """
        Secondary Pull

        :return: if the command was successful `True`/`False`
        :rtype: bool
        """
        values = self._get_values('Pull')
        if len(values) == 2:
            values[-1].data = True
            return True

        return False

    def _get_values(self, label):
        found = []
        for value in self:
            if value.command_class != COMMAND_CLASS_SWITCH_MULTILEVEL:
                continue
            if value.label == label:
                if found:
                    if found[-1].instance > value.instance:
                        found.insert(0, value)
                        continue
                found += [value]
        return found
    SUPPORTED_BUTTON_LABELS = [
        'Bright',
        'Dim',
        'On',
        'Off',
        'Up',
        'Down',
        'Open',
        'Close',
        'Clockwise',
        'Counter-Clockwise',
        'Right',
        'Left',
        'Forward',
        'Reverse',
        'Push',
        'Pull'
    ]

    for label in SUPPORTED_BUTTON_LABELS[:]:
        SUPPORTED_BUTTON_LABELS += ['Secondary ' + label]

    def supported_methods(self):
        res = []

        for label in self.SUPPORTED_BUTTON_LABELS:
            if 'Secondary' in label:
                break

            found = 0

            for value in self:
                if value.command_class != COMMAND_CLASS_SWITCH_MULTILEVEL:
                    continue
                if value.label == label:
                    found += 1

            if found:
                res += [[label, getattr(self, 'switch_' + label.lower())]]
            if found == 2:
                res += [
                    [
                        'Secondary ' + label,
                        getattr(self, 'switch_secondary_' + label.lower())
                    ]
                ]

        return res
