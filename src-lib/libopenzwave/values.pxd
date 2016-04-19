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
from libc.stdint cimport uint32_t, uint64_t, int32_t, int16_t, uint8_t, int8_t

cdef extern from "ValueID.h" namespace "OpenZWave::ValueID":

    cdef enum ValueGenre:
        ValueGenre_Basic = 0                # The 'level' as controlled by basic commands.  Usually duplicated by another command class.
        ValueGenre_User = 1                 # Basic values an ordinary user would be interested in.
        ValueGenre_Config = 2               # Device-specific configuration parameters.  These cannot be automatically discovered via Z-Wave, and are usually described in the user manual instead.
        ValueGenre_System = 3               # Values of significance only to users who understand the Z-Wave protocol.
        ValueGenre_Count = 4                # A count of the number of genres defined.  Not to be used as a genre itself.

    cdef enum ValueType:
        ValueType_Bool = 0                  # Boolean, true or false
        ValueType_Byte = 1                  # 8-bit unsigned value
        ValueType_Decimal = 2               # Represents a non-integer value as a string, to avoid floating point accuracy issues.
        ValueType_Int = 3                   # 32-bit signed value
        ValueType_List = 4                  # List from which one item can be selected
        ValueType_Schedule = 5              # Complex type used with the Climate Control Schedule command class
        ValueType_Short = 6                 # 16-bit signed value
        ValueType_String = 7                # Text string
        ValueType_Button = 8                # A write-only value that is the equivalent of pressing a button to send a command to a device
        ValueType_Raw = 9                   # Used as a list of Bytes
        ValueType_Max = ValueType_Raw       # The highest-number type defined.  Not to be used as a type itself.

cdef extern from "ValueID.h" namespace "OpenZWave":
    cdef cppclass ValueID:
        uint32_t GetHomeId()
        uint8_t GetNodeId()
        ValueGenre GetGenre()
        uint8_t GetCommandClassId()
        uint8_t GetInstance()
        uint8_t GetIndex()
        ValueType GetType()
        uint64_t GetId()
