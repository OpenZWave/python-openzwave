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
        uint32_t m_SOFCnt               # Number of SOF bytes received
        uint32_t m_ACKWaiting           # Number of unsolicited messages while waiting for an ACK
        uint32_t m_readAborts           # Number of times read were aborted due to timeouts
        uint32_t m_badChecksum          # Number of bad checksums
        uint32_t m_readCnt              # Number of messages successfully read
        uint32_t m_writeCnt             # Number of messages successfully sent
        uint32_t m_CANCnt               # Number of CAN bytes received
        uint32_t m_NAKCnt               # Number of NAK bytes received
        uint32_t m_ACKCnt               # Number of ACK bytes received
        uint32_t m_OOFCnt               # Number of bytes out of framing
        uint32_t m_dropped              # Number of messages dropped & not delivered
        uint32_t m_retries              # Number of messages retransmitted
        uint32_t m_callbacks            # Number of unexpected callbacks
        uint32_t m_badroutes            # Number of failed messages due to bad route response
        uint32_t m_noack                # Number of no ACK returned errors
        uint32_t m_netbusy              # Number of network busy/failure messages
        uint32_t m_nondelivery          # Number of messages not delivered to network
        uint32_t m_routedbusy           # Number of messages received with routed busy status
        uint32_t m_broadcastReadCnt     # Number of broadcasts read
        uint32_t m_broadcastWriteCnt    # Number of broadcasts sent

    cdef enum ControllerCommand:
        ControllerCommand_None = 0                          # No command.
        ControllerCommand_AddController = 1                 # Add a new controller to the Z-Wave network.  The new controller will be a secondary.
        ControllerCommand_AddDevice = 2                     # Add a new device (but not a controller) to the Z-Wave network.
        ControllerCommand_CreateNewPrimary = 3              # Add a new controller to the Z-Wave network.  The new controller will be the primary, and the current primary will become a secondary controller.
        ControllerCommand_ReceiveConfiguration = 4          # Receive Z-Wave network configuration information from another controller.
        ControllerCommand_RemoveController = 5              # Remove a controller from the Z-Wave network.
        ControllerCommand_RemoveDevice = 6                  # Remove a new device (but not a controller) from the Z-Wave network.
        ControllerCommand_RemoveFailedNode = 7              # Move a node to the controller's failed nodes list. This command will only work if the node cannot respond.
        ControllerCommand_HasNodeFailed = 8                 # Check whether a node is in the controller's failed nodes list.
        ControllerCommand_ReplaceFailedNode = 9             # Replace a non-responding node with another. The node must be in the controller's list of failed nodes for this command to succeed.
        ControllerCommand_TransferPrimaryRole = 10          # Make a different controller the primary.
        ControllerCommand_RequestNetworkUpdate = 11         # Request network information from the SUC/SIS.
        ControllerCommand_RequestNodeNeighborUpdate = 12    # Get a node to rebuild its neighbour list.  This method also does ControllerCommand_RequestNodeNeighbors.
        ControllerCommand_AssignReturnRoute = 13            # Assign a network return routes to a device.
        ControllerCommand_DeleteAllReturnRoutes = 14        # Delete all return routes from a device.
        ControllerCommand_CreateButton = 15                 # Create an id that tracks handheld button presses.
        ControllerCommand_DeleteButton = 16                 # Delete id that tracks handheld button presses.

    cdef enum ControllerState:
        ControllerState_Normal = 0          # No command in progress.
        ControllerState_Waiting = 1         # Controller is waiting for a user action.
        ControllerState_InProgress = 2      # The controller is communicating with the other device to carry out the command.
        ControllerState_Completed = 3       # The command has completed successfully.
        ControllerState_Failed = 4          # The command has failed.
        ControllerState_NodeOK = 5          # Used only with ControllerCommand_HasNodeFailed to indicate that the controller thinks the node is OK.
        ControllerState_NodeFailed = 6      # Used only with ControllerCommand_HasNodeFailed to indicate that the controller thinks the node has failed.

ctypedef DriverData DriverData_t

ctypedef void (*pfnControllerCallback_t)( ControllerState _state, void* _context )
