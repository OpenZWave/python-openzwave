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

cdef extern from "Log.h" namespace "OpenZWave":

   cdef enum LogLevel:
        LogLevel_None          = 0    # Disable all logging
        LogLevel_Always        = 1    # These messages should always be shown
        LogLevel_Fatal         = 2    # A likely fatal issue in the library
        LogLevel_Error         = 3    # A serious issue with the library or the network
        LogLevel_Warning       = 4    # A minor issue from which the library should be able to recover
        LogLevel_Alert         = 5    # Something unexpected by the library about which the controlling application should be aware
        LogLevel_Info          = 6    # Everything's working fine...these messages provide streamlined feedback on each message
        LogLevel_Detail        = 7    # Detailed information on the progress of each message
        LogLevel_Debug         = 8    # Very detailed information on progress that will create a huge log file quickly
                                      # But this level (as others) can be queued and sent to the log only on an error or warning
        LogLevel_StreamDetail  = 9    # Will include low-level byte transfers from controller to buffer to application and back
        LogLevel_Internal      = 10    # Used only within the log class (uses existing timestamp, etc.)
