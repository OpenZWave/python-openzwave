"""
This file is part of **python-openzwave** project http://code.google.com/p/python-openzwave.

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
from mylibc cimport uint32, uint64, int32, int16, uint8, int8

cdef extern from "Log.h" namespace "OpenZWave":

   cdef enum LogLevel:
        LogLevel_None       # Disable all logging
        LogLevel_Always     # These messages should always be shown
        LogLevel_Fatal      # A likely fatal issue in the library
        LogLevel_Error      # A serious issue with the library or the network
        LogLevel_Warning    # A minor issue from which the library should be able to recover
        LogLevel_Alert      # Something unexpected by the library about which the controlling application should be aware
        LogLevel_Info       # Everything's working fine...these messages provide streamlined feedback on each message
        LogLevel_Detail     # Detailed information on the progress of each message
        LogLevel_Debug      # Very detailed information on progress that will create a huge log file quickly
                            # But this level (as others) can be queued and sent to the log only on an error or warning
        LogLevel_Internal   # Used only within the log class (uses existing timestamp, etc.)
