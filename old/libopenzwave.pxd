""" This file is part of py-openzwave project (https://github.com/maartendamen/py-openzwave).

License
=======

py-openzwave is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

py-openzwave is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with py-openzwave. If not, see U{http://www.gnu.org/licenses}.

@author: maartendamen
@author: bibi21000 <bibi21000@gmail.com>
@license: GPL(v3)
"""
from mylibc cimport uint32, uint64, int32, int16, uint8, int8
from mylibc cimport string
from libcpp cimport bool

cdef extern from *:
    ctypedef char* const_notification "OpenZWave::Notification const*"

ctypedef void (*pfnOnNotification_t)(const_notification _pNotification, void* _context )
        
cdef extern from "Options.h" namespace "OpenZWave":
    cdef cppclass Options:
        bool Lock()

cdef extern from "Options.h" namespace "OpenZWave::Options":
    Options* Create(string a, string b, string c)

cdef extern from "Driver.h" namespace "OpenZWave::Driver":

    cdef struct DriverData:
        uint32 s_SOFCnt                         # Number of SOF bytes received
        uint32 s_ACKWaiting                     # Number of unsolicited messages while waiting for an ACK
        uint32 s_readAborts                     # Number of times read were aborted due to timeouts
        uint32 s_badChecksum                    # Number of bad checksums
        uint32 s_readCnt                        # Number of messages successfully read
        uint32 s_writeCnt                       # Number of messages successfully sent
        uint32 s_CANCnt                         # Number of CAN bytes received
        uint32 s_NAKCnt                         # Number of NAK bytes received
        uint32 s_ACKCnt                         # Number of ACK bytes received
        uint32 s_OOFCnt                         # Number of bytes out of framing
        uint32 s_dropped                        # Number of messages dropped & not delivered
        uint32 s_retries                        # Number of messages retransmitted
        uint32 s_controllerReadCnt              # Number of controller messages read
        uint32 s_controllerWriteCnt             # Number of controller messages sent

ctypedef DriverData DriverData_t

cdef extern from "Notification.h" namespace "OpenZWave::Notification":

   cdef enum NotificationType:
        Type_ValueAdded = 0                     # A new node value has been added to OpenZWave's list. These notifications occur after a node has been discovered, and details of its command classes have been received.  Each command class may generate one or more values depending on the complexity of the item being represented.
        Type_ValueRemoved = 1                   # A node value has been removed from OpenZWave's list.  This only occurs when a node is removed.
        Type_ValueChanged = 2                   # A node value has been updated from the Z-Wave network and it is different from the previous value.
        Type_ValueRefreshed = 3                 # A node value has been updated from the Z-Wave network.
        Type_Group = 4                          # The associations for the node have changed. The application should rebuild any group information it holds about the node.
        Type_NodeNew = 5                        # A new node has been found (not already stored in zwcfg*.xml file)
        Type_NodeAdded = 6                      # A new node has been added to OpenZWave's list.  This may be due to a device being added to the Z-Wave network, or because the application is initializing itself.
        Type_NodeRemoved = 7                    # A node has been removed from OpenZWave's list.  This may be due to a device being removed from the Z-Wave network, or because the application is closing.
        Type_NodeProtocolInfo = 8               # Basic node information has been receievd, such as whether the node is a listening device, a routing device and its baud rate and basic, generic and specific types. It is after this notification that you can call Manager::GetNodeType to obtain a label containing the device description.
        Type_NodeNaming = 9                     # One of the node names has changed (name, manufacturer, product).
        Type_NodeEvent = 10                     # A node has triggered an event.  This is commonly caused when a node sends a Basic_Set command to the controller.  The event value is stored in the notification.
        Type_PollingDisabled = 11               # Polling of a node has been successfully turned off by a call to Manager::DisablePoll
        Type_PollingEnabled = 12                # Polling of a node has been successfully turned on by a call to Manager::EnablePoll
        Type_CreateButton = 13                  # Handheld controller button event created 
        Type_DeleteButton = 14                  # Handheld controller button event deleted 
        Type_ButtonOn = 15                      # Handheld controller button on pressed event
        Type_ButtonOff = 16                     # Handheld controller button off pressed event 
        Type_DriverReady = 17                   # A driver for a PC Z-Wave controller has been added and is ready to use.  The notification will contain the controller's Home ID, which is needed to call most of the Manager methods.
        Type_DriverFailed = 18                  # Driver failed to load
        Type_DriverReset = 19                   # All nodes and values for this driver have been removed.  This is sent instead of potentially hundreds of individual node and value notifications.
        Type_MsgComplete = 20                   # The last message that was sent is now complete.
        Type_EssentialNodeQueriesComplete = 21  # The queries on a node that are essential to its operation have been completed. The node can now handle incoming messages.
        Type_NodeQueriesComplete = 22           # All the initialisation queries on a node have been completed.
        Type_AwakeNodesQueried = 23             # All awake nodes have been queried, so client application can expected complete data for these nodes.
        Type_AllNodesQueried = 24               # All nodes have been queried, so client application can expected complete data.
        Type_Error = 25                         # An error has occured that we need to report.

cdef extern from "ValueID.h" namespace "OpenZWave":

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
        ValueType_Max = ValueType_Button    # The highest-number type defined.  Not to be used as a type itself.

    cdef cppclass ValueID:
        uint32 GetHomeId()
        uint8 GetNodeId()
        ValueGenre GetGenre()
        uint8 GetCommandClassId()
        uint8 GetInstance()
        uint8 GetIndex()
        ValueType GetType()
        uint64 GetId()

cdef extern from "Notification.h" namespace "OpenZWave":

    cdef cppclass Notification:
        NotificationType GetType()
        uint32 GetHomeId()
        uint8 GetNodeId()
        ValueID& GetValueID()
        uint8 GetGroupIdx()
        uint8 GetEvent()
        uint8 GetButtonId()
        uint8 GetErrorCode()
        uint8 GetByte()

