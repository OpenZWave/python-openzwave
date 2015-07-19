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
#from libcpp.string cimport string
from mylibc cimport string
from libcpp cimport bool
#from libc.stdint cimport bint

cdef extern from "Driver.h" namespace "OpenZWave::Driver":

    cdef enum  ControllerInterface:       # Specifies the controller's hardware interface
        ControllerInterface_Unknown = 0
        ControllerInterface_Serial = 1          # Serial protocol
        ControllerInterface_Hid = 2             # Human interface device protocol

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
        ControllerCommand_None = 0,                        # No command. */
        ControllerCommand_AddDevice = 1                    # Add a new device or controller to the Z-Wave network. */
        ControllerCommand_CreateNewPrimary = 2             # Add a new controller to the Z-Wave network. Used when old primary fails. Requires SUC. */
        ControllerCommand_ReceiveConfiguration = 3         # Receive Z-Wave network configuration information from another controller. */
        ControllerCommand_RemoveDevice = 4                 # Remove a device or controller from the Z-Wave network. */
        ControllerCommand_RemoveFailedNode = 5             # Move a node to the controller's failed nodes list. This command will only work if the node cannot respond. */
        ControllerCommand_HasNodeFailed = 6                # Check whether a node is in the controller's failed nodes list. */
        ControllerCommand_ReplaceFailedNode = 7            # Replace a non-responding node with another. The node must be in the controller's list of failed nodes for this command to succeed. */
        ControllerCommand_TransferPrimaryRole = 8          # Make a different controller the primary. */
        ControllerCommand_RequestNetworkUpdate = 9         # Request network information from the SUC/SIS. */
        ControllerCommand_RequestNodeNeighborUpdate = 10   # Get a node to rebuild its neighbour list.  This method also does RequestNodeNeighbors */
        ControllerCommand_AssignReturnRoute = 11           # Assign a network return routes to a device. */
        ControllerCommand_DeleteAllReturnRoutes = 12       # Delete all return routes from a device. */
        ControllerCommand_SendNodeInformation = 13         # Send a node information frame */
        ControllerCommand_ReplicationSend = 14             # Send information from primary to secondary */
        ControllerCommand_CreateButton = 15                # Create an id that tracks handheld button presses */
        ControllerCommand_DeleteButton = 16                # Delete id that tracks handheld button presses */

    cdef enum ControllerState:
        ControllerState_Normal = 0                         # No command in progress. */
        ControllerState_Starting = 1                       # The command is starting. */
        ControllerState_Cancel = 2                         # The command was cancelled. */
        ControllerState_Error = 3                          # Command invocation had error(s) and was aborted */
        ControllerState_Waiting = 4                        # Controller is waiting for a user action. */
        ControllerState_Sleeping = 5                       # Controller command is on a sleep queue wait for device. */
        ControllerState_InProgress = 6                     # The controller is communicating with the other device to carry out the command. */
        ControllerState_Completed = 7                      # The command has completed successfully. */
        ControllerState_Failed = 8                         # The command has failed. */
        ControllerState_NodeOK = 9                         # Used only with ControllerCommand_HasNodeFailed to indicate that the controller thinks the node is OK. */
        ControllerState_NodeFailed = 10                    # Used only with ControllerCommand_HasNodeFailed to indicate that the controller thinks the node has failed. */

    cdef enum ControllerError:
        ControllerError_None = 0
        ControllerError_ButtonNotFound = 1                # Button */
        ControllerError_NodeNotFound = 2                  # Button */
        ControllerError_NotBridge = 3                     # Button */
        ControllerError_NotSUC = 4                        # CreateNewPrimary */
        ControllerError_NotSecondary = 5                  # CreateNewPrimary */
        ControllerError_NotPrimary = 6                    # RemoveFailedNode, AddNodeToNetwork */
        ControllerError_IsPrimary = 7                     # ReceiveConfiguration */
        ControllerError_NotFound = 8                      # RemoveFailedNode */
        ControllerError_Busy = 9                          # RemoveFailedNode, RequestNetworkUpdate */
        ControllerError_Failed = 10                       # RemoveFailedNode, RequestNetworkUpdate */
        ControllerError_Disabled = 11                     # RequestNetworkUpdate error */
        ControllerError_Overflow = 12                     # RequestNetworkUpdate error */

ctypedef DriverData DriverData_t

ctypedef void (*pfnControllerCallback_t)( ControllerState _state, ControllerError _error, void* _context )
