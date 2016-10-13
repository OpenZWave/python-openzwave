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
from values cimport ValueID
#from libcpp.string cimport string
from mylibc cimport string

cdef extern from *:
    ctypedef char* const_notification "OpenZWave::Notification const*"

ctypedef void (*pfnOnNotification_t)(const_notification _pNotification, void* _context )

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
        Type_SceneEvent = 13                    # Scene Activation Set received
        Type_CreateButton = 14                  # Handheld controller button event created
        Type_DeleteButton = 15                  # Handheld controller button event deleted
        Type_ButtonOn = 16                      # Handheld controller button on pressed event
        Type_ButtonOff = 17                     # Handheld controller button off pressed event
        Type_DriverReady = 18                   # A driver for a PC Z-Wave controller has been added and is ready to use.  The notification will contain the controller's Home ID, which is needed to call most of the Manager methods.
        Type_DriverFailed = 19                  # Driver failed to load
        Type_DriverReset = 20                   # All nodes and values for this driver have been removed.  This is sent instead of potentially hundreds of individual node and value notifications.
        Type_EssentialNodeQueriesComplete = 21  # The queries on a node that are essential to its operation have been completed. The node can now handle incoming messages.
        Type_NodeQueriesComplete = 22           # All the initialisation queries on a node have been completed.
        Type_AwakeNodesQueried = 23             # All awake nodes have been queried, so client application can expected complete data for these nodes.
        Type_AllNodesQueriedSomeDead = 24       # All nodes have been queried but some dead nodes found.
        Type_AllNodesQueried = 25               # All nodes have been queried, so client application can expected complete data.
        Type_Notification = 26                  # A manager notification report.
        Type_DriverRemoved = 27                 # The Driver is being removed. (either due to Error or by request) Do Not Call Any Driver Related Methods after receiving this call.
        Type_ControllerCommand = 28             # When Controller Commands are executed, Notifications of Success/Failure etc are communicated via this Notification * Notification::GetEvent returns Driver::ControllerCommand and Notification::GetNotification returns Driver::ControllerState

cdef extern from "Notification.h" namespace "OpenZWave::Notification":

    cdef enum NotificationCode:
        Code_MsgComplete = 0                    # Completed messages.
        Code_Timeout = 1                        # Messages that timeout will send a Notification with this code.
        Code_NoOperation = 2                    # Report on NoOperation message sent completion.
        Code_Awake = 3                          # Report when a sleeping node wakes.
        Code_Sleep = 4                          # Report when a node goes to sleep.
        Code_Dead = 5                           # Report when a node is presumed dead.
        Code_Alive = 6                          # Report when a node is revived.

cdef extern from "Notification.h" namespace "OpenZWave":

    cdef cppclass Notification:
        NotificationType GetType()
        uint32_t GetHomeId()
        uint8_t GetNodeId()
        ValueID& GetValueID()
        uint8_t GetGroupIdx()
        uint8_t GetEvent()
        uint8_t GetButtonId()
        uint8_t GetSceneId()
        uint8_t GetNotification()
        uint8_t GetByte()
