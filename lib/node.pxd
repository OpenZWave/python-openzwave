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

cdef extern from "Node.h" namespace "OpenZWave::Node":

    cdef enum SecurityFlag:
        SecurityFlag_Security = 0x01,
        SecurityFlag_Controller = 0x02,
        SecurityFlag_SpecificDevice = 0x04,
        SecurityFlag_RoutingSlave = 0x08,
        SecurityFlag_BeamCapability = 0x10,
        SecurityFlag_Sensor250ms = 0x20,
        SecurityFlag_Sensor1000ms = 0x40,
        SecurityFlag_OptionalFunctionality = 0x80

#    cdef struct NodeData:
#        uint32_t m_sentCnt                      # Number of messages sent from this node.
#        uint32_t m_sentFailed                   # Number of sent messages failed
#        uint32_t m_retries                      # Number of message retries
#        uint32_t m_receivedCnt                  # Number of messages received from this node.
#        uint32_t m_receivedDups                 # Number of duplicated messages received;
#        uint32_t m_lastRTT                      # Last message rtt
#        TimeStamp m_sentTS                      # Last message sent time
#        TimeStamp m_receivedTS                  # Last message received time
#        uint32_t m_averageRTT                   # Average round trip time.
#        uint8_t m_quality                       # Node quality measure
#        uint8_t m_lastReceivedMessage[254]      # Place to hold last received message
#        list<CommandClassData> m_ccData         #Unknown

