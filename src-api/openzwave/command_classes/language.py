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

# Language Command Class - Active
# Application
COMMAND_CLASS_LANGUAGE = 0x89


# noinspection PyAbstractClass
class Language(CommandClassBase):
    """
    Language Command Class

    symbol: `COMMAND_CLASS_LANGUAGE`
    """

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_LANGUAGE]

    __language_doc = """
        Language (`property`)

        :param value: language
        :type value: str
        :return: language or None if command failed
        :rtype: str, None
    """

    def __language_get(self):
        key = ('Language', COMMAND_CLASS_LANGUAGE)
        try:
            return self[key].data
        except KeyError:
            return None

    def __language_set(self, value):
        key = ('Language', COMMAND_CLASS_LANGUAGE)
        try:
            self[key].data = value
        except KeyError:
            pass

    language = property(
        __language_get,
        __language_set,
        doc=__language_doc
    )

    __country_doc = """
        Country (`property`)

        :param value: country
        :type value: str
        :return: country or None if command failed
        :rtype: str, None
    """

    def __country_get(self):
        key = ('Country', COMMAND_CLASS_LANGUAGE)
        try:
            return self[key].data
        except KeyError:
            return None

    def __country_set(self, value):
        key = ('Country', COMMAND_CLASS_LANGUAGE)
        try:
            self[key].data = value
        except KeyError:
            pass

    country = property(
        __country_get,
        __country_set,
        doc=__country_doc
    )
