# -*- coding: utf-8 -*-
"""
This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.

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
from libc.stdint cimport uint32_t, int32_t, int16_t, uint8_t, int8_t
from libcpp cimport bool
#from libc.stdint cimport bint
#from libcpp.string cimport string
from mylibc cimport string

cdef extern from "Options.h" namespace "OpenZWave":
    cdef cppclass Options:
        bool Lock()
        bool AreLocked()
        bool Destroy()
        bool AddOptionBool(string name, bool default )
        bool AddOptionInt(string name, int32_t default )
        bool AddOptionString(string name, string default, bool append )
        bool GetOptionAsBool(string name, bool* o_option )
        bool GetOptionAsInt(string name, int32_t* o_option )
        bool GetOptionAsString(string name, string* o_option)
        OptionType GetType(string name)

    ctypedef enum OptionType:
        OptionType_Invalid = 0
        OptionType_Bool = 1
        OptionType_Int = 2
        OptionType_String = 3

cdef extern from "Options.h" namespace "OpenZWave::Options":
    Options* Create(string a, string b, string c)
