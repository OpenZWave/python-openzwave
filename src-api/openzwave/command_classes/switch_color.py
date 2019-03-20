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

from .command_class_base import CommandClassBase

# Color Switch Command Class - Active
# Application
COMMAND_CLASS_SWITCH_COLOR = 0x33


# noinspection PyAbstractClass
class SwitchColor(CommandClassBase):
    COLORIDX_WARMWHITE = 0
    COLORIDX_COLDWHITE = 1
    COLORIDX_RED = 2
    COLORIDX_GREEN = 3
    COLORIDX_BLUE = 4
    COLORIDX_AMBER = 5
    COLORIDX_CYAN = 6
    COLORIDX_PURPLE = 7
    COLORIDX_INDEXCOLOR = 8

    PRESET_COLORS = [
        "Off",
        "Cool White",
        "Warm White",
        "Red",
        "Lime",
        "Blue",
        "Yellow",
        "Cyan",
        "Magenta",
        "Silver",
        "Gray",
        "Maroon",
        "Olive",
        "Green",
        "Purple",
        "Teal",
        "Navy",
        "Custom"
    ]

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SWITCH_COLOR]

    @staticmethod
    def __normalize_value(value):
        if value < 0x00:
            value = 0x00
        elif value > 0xFF:
            value = 0xFF

        return value

    @property
    def warm_white(self):
        for value in self[(None, COMMAND_CLASS_SWITCH_COLOR)]:
            if value.index == self.COLORIDX_WARMWHITE:
                return value.data

    @warm_white.setter
    def warm_white(self, value):
        value = self.__normalize_value(value)

        for val in self[(None, COMMAND_CLASS_SWITCH_COLOR)]:
            if val.index == self.COLORIDX_WARMWHITE:
                val.data = value
                break

    @property
    def cold_white(self):
        for value in self[(None, COMMAND_CLASS_SWITCH_COLOR)]:
            if value.index == self.COLORIDX_COLDWHITE:
                return value.data

    @cold_white.setter
    def cold_white(self, value):
        value = self.__normalize_value(value)

        for val in self[(None, COMMAND_CLASS_SWITCH_COLOR)]:
            if val.index == self.COLORIDX_COLDWHITE:
                val.data = value
                break

    @property
    def red(self):
        for value in self[(None, COMMAND_CLASS_SWITCH_COLOR)]:
            if value.index == self.COLORIDX_RED:
                return value.data

        return self._cmy_to_rgb(*self.cmy_color)[0]

    @red.setter
    def red(self, value):
        value = self.__normalize_value(value)

        for val in self[(None, COMMAND_CLASS_SWITCH_COLOR)]:
            if val.index == self.COLORIDX_RED:
                val.data = value
                break
        else:
            _, g, b = self._cmy_to_rgb(*self.cmy_color)
            self.cmy_color = self._rgb_to_cmy(value, g, b)

    @property
    def green(self):
        for value in self[(None, COMMAND_CLASS_SWITCH_COLOR)]:
            if value.index == self.COLORIDX_GREEN:
                return value.data

        return self._cmy_to_rgb(*self.cmy_color)[1]

    @green.setter
    def green(self, value):
        value = self.__normalize_value(value)

        for val in self[(None, COMMAND_CLASS_SWITCH_COLOR)]:
            if val.index == self.COLORIDX_GREEN:
                val.data = value
                break
        else:
            r, _, b = self._cmy_to_rgb(*self.cmy_color)
            self.cmy_color = self._rgb_to_cmy(r, value, b)

    @property
    def blue(self):
        for value in self[(None, COMMAND_CLASS_SWITCH_COLOR)]:
            if value.index == self.COLORIDX_BLUE:
                return value.data

        return self._cmy_to_rgb(*self.cmy_color)[2]

    @blue.setter
    def blue(self, value):
        value = self.__normalize_value(value)

        for val in self[(None, COMMAND_CLASS_SWITCH_COLOR)]:
            if val.index == self.COLORIDX_BLUE:
                val.data = value
                break
        else:
            r, g, _ = self._cmy_to_rgb(*self.cmy_color)
            self.rgb_color = self._rgb_to_cmy(r, g, value)

    @property
    def yellow(self):
        for value in self[(None, COMMAND_CLASS_SWITCH_COLOR)]:
            if value.index == self.COLORIDX_AMBER:
                return value.data

        return self._rgb_to_cmy(*self.rgb_color)[2]

    @yellow.setter
    def yellow(self, value):
        value = self.__normalize_value(value)

        for val in self[(None, COMMAND_CLASS_SWITCH_COLOR)]:
            if val.index == self.COLORIDX_AMBER:
                val.data = value
                break
        else:
            c, m, _ = self._rgb_to_cmy(*self.rgb_color)
            self.rgb_color = self._cmy_to_rgb(c, m, value)

    @property
    def cyan(self):
        for value in self[(None, COMMAND_CLASS_SWITCH_COLOR)]:
            if value.index == self.COLORIDX_CYAN:
                return value.data

        return self._rgb_to_cmy(*self.rgb_color)[0]

    @cyan.setter
    def cyan(self, value):
        value = self.__normalize_value(value)

        for val in self[(None, COMMAND_CLASS_SWITCH_COLOR)]:
            if val.index == self.COLORIDX_CYAN:
                val.data = value
                break
        else:
            _, m, y = self._rgb_to_cmy(*self.rgb_color)
            self.rgb_color = self._cmy_to_rgb(value, m, y)

    @property
    def magenta(self):
        for value in self[(None, COMMAND_CLASS_SWITCH_COLOR)]:
            if value.index == self.COLORIDX_PURPLE:
                return value.data

        return self._rgb_to_cmy(*self.rgb_color)[1]

    @magenta.setter
    def magenta(self, value):
        value = self.__normalize_value(value)

        for val in self[(None, COMMAND_CLASS_SWITCH_COLOR)]:
            if val.index == self.COLORIDX_PURPLE:
                val.data = value
                break
        else:
            c, _, y = self._rgb_to_cmy(*self.rgb_color)
            self.rgb_color = self._cmy_to_rgb(c, value, y)

    @property
    def preset_color(self):
        try:
            return self[('Color Index', COMMAND_CLASS_SWITCH_COLOR)].data
        except KeyError:
            return None

    @preset_color.setter
    def preset_color(self, value):
        if isinstance(value, int):
            try:
                value = self.PRESET_COLORS[value]
            except IndexError:
                return

        try:
            self[('Color Index', COMMAND_CLASS_SWITCH_COLOR)].data = value
        except KeyError:
            pass

    @property
    def color_duration(self):
        try:
            return self[('Duration', COMMAND_CLASS_SWITCH_COLOR)].data
        except KeyError:
            return None

    @color_duration.setter
    def color_duration(self, value):
        try:
            self[('Duration', COMMAND_CLASS_SWITCH_COLOR)].data = value
        except KeyError:
            pass

    @property
    def rgb_color(self):
        color = self.html_color.lstrip('#')
        return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))

    @rgb_color.setter
    def rgb_color(self, value):
        r, g, b = value

        def clamp(x):
            return max(0, min(x, 255))

        value = "#{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))

        self.html_color = value

    @property
    def cmy_color(self):
        for val in self[(None, COMMAND_CLASS_SWITCH_COLOR)]:
            if val.index == self.COLORIDX_PURPLE:
                return self.cyan, self.magenta, self.yellow

        return self._rgb_to_cmy(*self.rgb_color)

    @cmy_color.setter
    def cmy_color(self, value):
        for val in self[(None, COMMAND_CLASS_SWITCH_COLOR)]:
            if val.index == self.COLORIDX_PURPLE:
                self.cyan, self.magenta, self.yellow = value
                break
        else:
            self.rgb_color = self._cmy_to_rgb(*value)

    @property
    def color_channels(self):
        try:
            return self[('Color Channels', COMMAND_CLASS_SWITCH_COLOR)].data
        except KeyError:
            return None

    @color_channels.setter
    def color_channels(self, value):
        try:
            self[('Color Channels', COMMAND_CLASS_SWITCH_COLOR)].data = value
        except KeyError:
            pass

    @property
    def html_color(self):
        try:
            return self[('Color', COMMAND_CLASS_SWITCH_COLOR)].data
        except KeyError:
            return None

    @html_color.setter
    def html_color(self, value):
        value = value.lstrip('#')

        try:
            self[('Color', COMMAND_CLASS_SWITCH_COLOR)].data = value
        except KeyError:
            pass

    @property
    def hsv_color(self):
        import colorsys

        r, g, b = self.rgb_color
        return colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

    @hsv_color.setter
    def hsv_color(self, value):
        import colorsys

        self.rgb_color = tuple(
            int(round(i * 255.0)) for i in colorsys.hsv_to_rgb(*value)
        )

    @staticmethod
    def _rgb_to_cmy(r, g, b):
        if (r, g, b) == (0, 0, 0):
            return r, g, b

        c = 1.0 - r / 255.0
        m = 1.0 - g / 255.0
        y = 1.0 - b / 255.0

        k = min(c, m, y)
        c = ((c - k) / (1.0 - k)) * 255.0
        m = ((m - k) / (1.0 - k)) * 255.0
        y = ((y - k) / (1.0 - k)) * 255.0

        return int(round(c)), int(round(m)), int(round(y))

    @staticmethod
    def _cmy_to_rgb(c, m, y):

        r = 255.0 * (1.0 - c / 255.0)
        g = 255.0 * (1.0 - m / 255.0)
        b = 255.0 * (1.0 - y / 255.0)

        k = max(r, g, b)
        r *= 1.0 - k / 255.0
        g *= 1.0 - k / 255.0
        b *= 1.0 - k / 255.0

        return int(round(r)), int(round(g)), int(round(b))
