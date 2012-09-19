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
from libc.stdint cimport uint32_t, uint64_t, int32_t, int16_t, uint8_t, int8_t
from mylibc cimport string
from libcpp cimport bool

cdef extern from "Driver.h" namespace "OpenZWave::Driver":

    cdef struct DriverData:
        uint32_t s_SOFCnt                         # Number of SOF bytes received
        uint32_t s_ACKWaiting                     # Number of unsolicited messages while waiting for an ACK
        uint32_t s_readAborts                     # Number of times read were aborted due to timeouts
        uint32_t s_badChecksum                    # Number of bad checksums
        uint32_t s_readCnt                        # Number of messages successfully read
        uint32_t s_writeCnt                       # Number of messages successfully sent
        uint32_t s_CANCnt                         # Number of CAN bytes received
        uint32_t s_NAKCnt                         # Number of NAK bytes received
        uint32_t s_ACKCnt                         # Number of ACK bytes received
        uint32_t s_OOFCnt                         # Number of bytes out of framing
        uint32_t s_dropped                        # Number of messages dropped & not delivered
        uint32_t s_retries                        # Number of messages retransmitted
        uint32_t s_controllerReadCnt              # Number of controller messages read
        uint32_t s_controllerWriteCnt             # Number of controller messages sent

ctypedef DriverData DriverData_t

