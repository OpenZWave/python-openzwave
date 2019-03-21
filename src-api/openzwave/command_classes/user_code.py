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

# User Code Command Class - Active
# Application
COMMAND_CLASS_USER_CODE = 0x63


# noinspection PyAbstractClass
class UserCode(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_USER_CODE]

    @property
    def user_codes_count(self):
        key = ('Code Count', COMMAND_CLASS_USER_CODE)
        try:
            return self[key].data
        except KeyError:
            return None

    def user_codes_refresh_all(self):
        key = ('Refresh All UserCodes', COMMAND_CLASS_USER_CODE)
        try:
            self[key].data = True
            return True
        except KeyError:
            return False

    @property
    def user_code_enrollment_code(self):
        key = ('Enrollment Code', COMMAND_CLASS_USER_CODE)
        try:
            return self[key].data
        except KeyError:
            return None

    @property
    def user_codes(self):
        """
        Retrieves the list of value to consider as usercodes.
        Filter rules are :

            command_class = 0x63
            genre = "User"
            type = "Raw"
            readonly = False
            writeonly = False

        :return: The list of user codes on this node
        :rtype: dict()

        """

        res = []
        for value in self[(None, COMMAND_CLASS_USER_CODE)]:
            if value.label.startswith('Code'):
                res += [self.Code(value)]
        return res


    class Code(object):

        def __init__(self, value):
            self.__value = value

        def get(self):
            return self.__value.data

        def set(self, code):
            self.__value.data = code

        def name(self):
            return self.__value.label

        def __getattr__(self, item):
            if item in self.__dict__:
                return self.__dict__[item]

            return getattr(self.__value, item)

        def __setattr__(self, key, value):
            if key.startswith('__'):
                object.__setattr__(self, key, value)
            else:
                setattr(self.__value, key, value)
