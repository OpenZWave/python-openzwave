# -*- coding: utf-8 -*-
#cython: c_string_type=unicode, c_string_encoding=utf8

"""
.. module:: libopenzwave

This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.

:platform: Unix, Windows, MacOS X
:sinopsis: openzwave C++

.. moduleauthor: bibi21000 aka Sebastien GALLET <bibi21000@gmail.com>
.. moduleauthor: Maarten Damen <m.damen@gmail.com>

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
from cython.operator cimport dereference as deref
from libcpp.map cimport map, pair
from libcpp cimport bool
#from libc.stdint cimport bint
from libcpp.vector cimport vector
from libc.stdint cimport uint16_t,  uint32_t, uint64_t, int32_t, int16_t, uint8_t, int8_t
from libc.stdlib cimport malloc, free
#from libcpp.string cimport string
from mylibc cimport string
#from vers cimport ozw_vers_major, ozw_vers_minor, ozw_vers_revision, ozw_version_string
from mylibc cimport PyEval_InitThreads, Py_Initialize
from group cimport InstanceAssociation_t, InstanceAssociation
from node cimport NodeData_t, NodeData
from node cimport SecurityFlag
from driver cimport DriverData_t, DriverData
from driver cimport ControllerCommand, ControllerState, ControllerError, pfnControllerCallback_t
from notification cimport Notification, NotificationType, NotificationCode
from notification cimport Type_Notification, Type_Group, Type_NodeEvent, Type_SceneEvent, Type_DriverReset, Type_DriverRemoved
from notification cimport Type_CreateButton, Type_DeleteButton, Type_ButtonOn, Type_ButtonOff
from notification cimport Type_ValueAdded, Type_ValueRemoved, Type_ValueChanged, Type_ValueRefreshed
from notification cimport Type_ControllerCommand
from notification cimport const_notification, pfnOnNotification_t
from values cimport ValueGenre, ValueType, ValueID
from options cimport Options, Create as CreateOptions, OptionType, OptionType_Invalid, OptionType_Bool, OptionType_Int, OptionType_String
from manager cimport Manager, Create as CreateManager, Get as GetManager
from manager cimport struct_associations, int_associations
from log cimport LogLevel
import os
import sys
import warnings
import six
from shutil import copyfile

# Set default logging handler to avoid "No handler found" warnings.
import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        """NullHandler logger for python 2.6"""
        def emit(self, record):
            pass
logger = logging.getLogger('libopenzwave')
logger.addHandler(NullHandler())

from pkg_resources import get_distribution, DistributionNotFound

cdef extern from 'pyversion.h':
    string PY_LIB_VERSION_STRING
    string PY_LIB_FLAVOR_STRING
    string PY_LIB_BACKEND_STRING
    string PY_LIB_DATE_STRING
    string PY_LIB_TIME_STRING

__version__ = PY_LIB_VERSION_STRING

#For historical ways of working
libopenzwave_location = 'not_installed'
libopenzwave_file = 'not_installed'
try:
    _dist = get_distribution('libopenzwave')
except DistributionNotFound:
    pass
else:
    libopenzwave_location = _dist.location
if libopenzwave_location == 'not_installed' :
   try:
        _dist = get_distribution('libopenzwave')
        libopenzwave_file = _dist.__file__
   except AttributeError:
        libopenzwave_file = 'not_installed'
   except DistributionNotFound:
        libopenzwave_file = 'not_installed'

cdef string str_to_cppstr(str s):
    if isinstance(s, unicode):
        b = s.encode('utf-8')
    else:
        b = s
    return string(b)

cdef cstr_to_str(s):
    if six.PY3 and not isinstance(s, str):
        return s.decode('utf-8')
    elif six.PY3:
        return s
    else:
        try:
            return s.encode('utf-8')
        except:
            try:
                return s.decode('utf-8')
            except:
                return s

class LibZWaveException(Exception):
    """
    Exception class for LibOpenZWave
    """
    def __init__(self, value):
        Exception.__init__(self)
        self.msg = "LibOpenZwave Generic Exception"
        self.value = value

    def __str__(self):
        return repr(self.msg+' : '+self.value)

# See http://www.electricmonk.nl/log/2011/08/14/redirect-stdout-and-stderr-to-a-logger-in-python/ for capturing console output of the c++ library
#     http://stackoverflow.com/questions/616645/how-do-i-duplicate-sys-stdout-to-a-log-file-in-python
#     https://github.com/nose-devs/nose/blob/master/nose/plugins/capture.py


#~ class StdOutToLogger(object):
#~     """
#~     Capture stdout and send it to logging.debug
#~     """
#~     def __init__(self):
#~         self.stdout = sys.stdout
#~         sys.stdout = self
#~
#~     def __del__(self):
#~         sys.stdout = self.stdout
#~         self.file.close()
#~
#~     def write(self, data):
#~         pass
#~         logger.debug(data)

PYLIBRARY = __version__
PY_OZWAVE_CONFIG_DIRECTORY = "config"
OZWAVE_CONFIG_DIRECTORY = "share/openzwave/config"
CWD_CONFIG_DIRECTORY = "openzwave/config"

class EnumWithDoc(str):
    """Enum helper"""
    def setDoc(self, doc):
        self.doc = doc
        return self

PyNotifications = [
    EnumWithDoc('ValueAdded').setDoc("A new node value has been added to OpenZWave's set. These notifications occur after a node has been discovered, and details of its command classes have been received.  Each command class may generate one or more values depending on the complexity of the item being represented."),
    EnumWithDoc('ValueRemoved').setDoc("A node value has been removed from OpenZWave's set.  This only occurs when a node is removed."),
    EnumWithDoc('ValueChanged').setDoc("A node value has been updated from the Z-Wave network and it is different from the previous value."),
    EnumWithDoc('ValueRefreshed').setDoc("A node value has been updated from the Z-Wave network."),
    EnumWithDoc('Group').setDoc("The associations for the node have changed. The application should rebuild any group information it holds about the node."),
    EnumWithDoc('NodeNew').setDoc("A new node has been found (not already stored in zwcfg*.xml file)."),
    EnumWithDoc('NodeAdded').setDoc("A new node has been added to OpenZWave's set.  This may be due to a device being added to the Z-Wave network, or because the application is initializing itself."),
    EnumWithDoc('NodeRemoved').setDoc("A node has been removed from OpenZWave's set.  This may be due to a device being removed from the Z-Wave network, or because the application is closing."),
    EnumWithDoc('NodeProtocolInfo').setDoc("Basic node information has been receievd, such as whether the node is a setening device, a routing device and its baud rate and basic, generic and specific types. It is after this notification that you can call Manager::GetNodeType to obtain a label containing the device description."),
    EnumWithDoc('NodeNaming').setDoc("One of the node names has changed (name, manufacturer, product)."),
    EnumWithDoc('NodeEvent').setDoc("A node has triggered an event.  This is commonly caused when a node sends a Basic_Set command to the controller.  The event value is stored in the notification."),
    EnumWithDoc('PollingDisabled').setDoc("Polling of a node has been successfully turned off by a call to Manager::DisablePoll."),
    EnumWithDoc('PollingEnabled').setDoc("Polling of a node has been successfully turned on by a call to Manager::EnablePoll."),
    EnumWithDoc('SceneEvent').setDoc("Scene Activation Set received."),
    EnumWithDoc('CreateButton').setDoc("Handheld controller button event created."),
    EnumWithDoc('DeleteButton').setDoc("Handheld controller button event deleted."),
    EnumWithDoc('ButtonOn').setDoc("Handheld controller button on pressed event."),
    EnumWithDoc('ButtonOff').setDoc("Handheld controller button off pressed event."),
    EnumWithDoc('DriverReady').setDoc("A driver for a PC Z-Wave controller has been added and is ready to use.  The notification will contain the controller's Home ID, which is needed to call most of the Manager methods."),
    EnumWithDoc('DriverFailed').setDoc("Driver failed to load."),
    EnumWithDoc('DriverReset').setDoc("All nodes and values for this driver have been removed.  This is sent instead of potentially hundreds of individual node and value notifications."),
    EnumWithDoc('EssentialNodeQueriesComplete').setDoc("The queries on a node that are essential to its operation have been completed. The node can now handle incoming messages."),
    EnumWithDoc('NodeQueriesComplete').setDoc("All the initialisation queries on a node have been completed."),
    EnumWithDoc('AwakeNodesQueried').setDoc("All awake nodes have been queried, so client application can expected complete data for these nodes."),
    EnumWithDoc('AllNodesQueriedSomeDead').setDoc("All nodes have been queried but some dead nodes found."),
    EnumWithDoc('AllNodesQueried').setDoc("All nodes have been queried, so client application can expected complete data."),
    EnumWithDoc('Notification').setDoc("A manager notification report."),
    EnumWithDoc('DriverRemoved').setDoc("The Driver is being removed."),
    EnumWithDoc('ControllerCommand').setDoc("When Controller Commands are executed, Notifications of Success/Failure etc are communicated via this Notification."),
    EnumWithDoc('NodeReset').setDoc("A node has been reset from OpenZWave's set.  The Device has been reset and thus removed from the NodeList in OZW."),
    ]

PyNotificationCodes = [
    EnumWithDoc('MsgComplete').setDoc("Completed messages."),
    EnumWithDoc('Timeout').setDoc("Messages that timeout will send a Notification with this code."),
    EnumWithDoc('NoOperation').setDoc("Report on NoOperation message sent completion."),
    EnumWithDoc('Awake').setDoc("Report when a sleeping node wakes."),
    EnumWithDoc('Sleep').setDoc("Report when a node goes to sleep."),
    EnumWithDoc('Dead').setDoc("Report when a node is presumed dead."),
    EnumWithDoc('Alive').setDoc("Report when a node is revived."),
    ]

PyGenres = [
    EnumWithDoc('Basic').setDoc("The 'level' as controlled by basic commands.  Usually duplicated by another command class."),
    EnumWithDoc('User').setDoc("Basic values an ordinary user would be interested in."),
    EnumWithDoc('Config').setDoc("Device-specific configuration parameters.  These cannot be automatically discovered via Z-Wave, and are usually described in the user manual instead."),
    EnumWithDoc('System').setDoc("Values of significance only to users who understand the Z-Wave protocol"),
    ]

PyValueTypes = [
    EnumWithDoc('Bool').setDoc("Boolean, true or false"),
    EnumWithDoc('Byte').setDoc("8-bit unsigned value"),
    EnumWithDoc('Decimal').setDoc("Represents a non-integer value as a string, to avoid floating point accuracy issues."),
    EnumWithDoc('Int').setDoc("32-bit signed value"),
    EnumWithDoc('List').setDoc("List from which one item can be selected"),
    EnumWithDoc('Schedule').setDoc("Complex type used with the Climate Control Schedule command class"),
    EnumWithDoc('Short').setDoc("16-bit signed value"),
    EnumWithDoc('String').setDoc("Text string"),
    EnumWithDoc('Button').setDoc("A write-only value that is the equivalent of pressing a button to send a command to a device"),
    EnumWithDoc('Raw').setDoc("Raw byte values"),
    ]

PyControllerState = [
    EnumWithDoc('Normal').setDoc("No command in progress."),
    EnumWithDoc('Starting').setDoc("The command is starting."),
    EnumWithDoc('Cancel').setDoc("The command was cancelled."),
    EnumWithDoc('Error').setDoc("Command invocation had error(s) and was aborted."),
    EnumWithDoc('Waiting').setDoc("Controller is waiting for a user action."),
    EnumWithDoc('Sleeping').setDoc("Controller command is on a sleep queue wait for device."),
    EnumWithDoc('InProgress').setDoc("The controller is communicating with the other device to carry out the command."),
    EnumWithDoc('Completed').setDoc("The command has completed successfully."),
    EnumWithDoc('Failed').setDoc("The command has failed."),
    EnumWithDoc('NodeOK').setDoc("Used only with ControllerCommand_HasNodeFailed to indicate that the controller thinks the node is OK."),
    EnumWithDoc('NodeFailed').setDoc("Used only with ControllerCommand_HasNodeFailed to indicate that the controller thinks the node has failed."),
    ]

PyControllerCommand = [
    EnumWithDoc('None').setDoc("No command."),
    EnumWithDoc('AddDevice').setDoc("Add a new device (but not a controller) to the Z-Wave network."),
    EnumWithDoc('CreateNewPrimary').setDoc("Add a new controller to the Z-Wave network.  The new controller will be the primary, and the current primary will become a secondary controller."),
    EnumWithDoc('ReceiveConfiguration').setDoc("Receive Z-Wave network configuration information from another controller."),
    EnumWithDoc('RemoveDevice').setDoc("Remove a new device (but not a controller) from the Z-Wave network."),
    EnumWithDoc('RemoveFailedNode').setDoc("Move a node to the controller's failed nodes list. This command will only work if the node cannot respond."),
    EnumWithDoc('HasNodeFailed').setDoc("Check whether a node is in the controller's failed nodes list."),
    EnumWithDoc('ReplaceFailedNode').setDoc("Replace a non-responding node with another. The node must be in the controller's list of failed nodes for this command to succeed."),
    EnumWithDoc('TransferPrimaryRole').setDoc("Make a different controller the primary."),
    EnumWithDoc('RequestNetworkUpdate').setDoc("Request network information from the SUC/SIS."),
    EnumWithDoc('RequestNodeNeighborUpdate').setDoc("Get a node to rebuild its neighbour list.  This method also does ControllerCommand_RequestNodeNeighbors."),
    EnumWithDoc('AssignReturnRoute').setDoc("Assign a network return routes to a device."),
    EnumWithDoc('DeleteAllReturnRoutes').setDoc("Delete all return routes from a device."),
    EnumWithDoc('SendNodeInformation').setDoc("Send a node information frame."),
    EnumWithDoc('ReplicationSend').setDoc("Send information from primary to secondary."),
    EnumWithDoc('CreateButton').setDoc("Create an id that tracks handheld button presses."),
    EnumWithDoc('DeleteButton').setDoc("Delete id that tracks handheld button presses."),
    ]

PyControllerError = [
    EnumWithDoc('None').setDoc("None."),
    EnumWithDoc('ButtonNotFound').setDoc("Button."),
    EnumWithDoc('NodeNotFound').setDoc("Button."),
    EnumWithDoc('NotBridge').setDoc("Button."),
    EnumWithDoc('NotSUC').setDoc("CreateNewPrimary."),
    EnumWithDoc('NotSecondary').setDoc("CreateNewPrimary."),
    EnumWithDoc('NotPrimary').setDoc("RemoveFailedNode, AddNodeToNetwork."),
    EnumWithDoc('IsPrimary').setDoc("ReceiveConfiguration."),
    EnumWithDoc('NotFound').setDoc("RemoveFailedNode."),
    EnumWithDoc('Busy').setDoc("RemoveFailedNode, RequestNetworkUpdate."),
    EnumWithDoc('Failed').setDoc("RemoveFailedNode, RequestNetworkUpdate."),
    EnumWithDoc('Disabled').setDoc("RequestNetworkUpdate error."),
    EnumWithDoc('Overflow').setDoc("RequestNetworkUpdate error."),
    ]

PyControllerInterface = [
    EnumWithDoc('Unknown').setDoc("Controller interface use unknown protocol."),
    EnumWithDoc('Serial').setDoc("Controller interface use serial protocol."),
    EnumWithDoc('Hid').setDoc("Controller interface use human interface device protocol."),
]

PyOptionType = [
    EnumWithDoc('Invalid').setDoc("Invalid type."),
    EnumWithDoc('Bool').setDoc("Boolean."),
    EnumWithDoc('Int').setDoc("Integer."),
    EnumWithDoc('String').setDoc("String."),
]

class EnumWithDocType(str):
    """Enum helper"""
    def setDocType(self, doc, stype):
        self.doc = doc
        self.type = stype
        return self

PyOptionList = {
    'ConfigPath' : {'doc' : "Path to the OpenZWave config folder.", 'type' : "String"},
    'UserPath' : {'doc' : "Path to the user's data folder.", 'type' : "String"},
    'Logging' : {'doc' : "Enable logging of library activity.", 'type' : "Bool"},
    'LogFileName' : {'doc' : "Name of the log file (can be changed via Log::SetLogFileName).", 'type' : "String"},
    'AppendLogFile' : {'doc' : "Append new session logs to existing log file (false = overwrite).", 'type' : "Bool"},
    'ConsoleOutput' : {'doc' : "Display log information on console (as well as save to disk).", 'type' : "Bool"},
    'SaveLogLevel' : {'doc' : "Save (to file) log messages equal to or above LogLevel_Detail.", 'type' : "Int"},
    'QueueLogLevel' : {'doc' : "Save (in RAM) log messages equal to or above LogLevel_Debug.", 'type' : "Int"},
    'DumpTriggerLevel' : {'doc' : "Default is to never dump RAM-stored log messages.", 'type' : "Int"},
    'Associate' : {'doc' : "Enable automatic association of the controller with group one of every device.", 'type' : "Bool"},
    'Exclude' : {'doc' : "Remove support for the listed command classes.", 'type' : "String"},
    'Include' : {'doc' : "Only handle the specified command classes. The Exclude option is ignored if anything is listed here.", 'type' : "String"},
    'NotifyTransactions' : {'doc' : "Notifications when transaction complete is reported.", 'type' : "Bool"},
    'Interface' : {'doc' : "Identify the serial port to be accessed (TODO: change the code so more than one serial port can be specified and HID).", 'type' : "String"},
    'SaveConfiguration' : {'doc' : "Save the XML configuration upon driver close.", 'type' : "Bool"},
    'DriverMaxAttempts' : {'doc' : ".", 'type' : "Int"},
    'PollInterval' : {'doc' : "30 seconds (can easily poll 30 values in this time; ~120 values is the effective limit for 30 seconds).", 'type' : "Int"},
    'IntervalBetweenPolls' : {'doc' : "If false, try to execute the entire poll list within the PollInterval time frame. If true, wait for PollInterval milliseconds between polls.", 'type' : "Bool"},
    'SuppressValueRefresh' : {'doc' : "If true, notifications for refreshed (but unchanged) values will not be sent.", 'type' : "Bool"},
    'PerformReturnRoutes' : {'doc' : "If true, return routes will be updated.", 'type' : "Bool"},
    'NetworkKey' : {'doc' : "Key used to negotiate and communicate with devices that support Security Command Class", 'type' : "String"},
    'RefreshAllUserCodes' : {'doc' : "If true, during startup, we refresh all the UserCodes the device reports it supports. If False, we stop after we get the first 'Available' slot (Some devices have 250+ usercode slots! - That makes our Session Stage Very Long ).", 'type' : "Bool"},
    'RetryTimeout' : {'doc' : "How long do we wait to timeout messages sent.", 'type' : "Int"},
    'EnableSIS' : {'doc' : "Automatically become a SUC if there is no SUC on the network.", 'type' : "Bool"},
    'AssumeAwake' : {'doc' : "Assume Devices that Support the Wakeup CC are awake when we first query them ...", 'type' : "Bool"},
    'NotifyOnDriverUnload' : {'doc' : "Should we send the Node/Value Notifications on Driver Unloading - Read comments in Driver::~Driver() method about possible race conditions.", 'type' : "Bool"},
    'SecurityStrategy' : {'doc' : "Should we encrypt CC's that are available via both clear text and Security CC?.", 'type' : "String", 'value' : 'SUPPORTED'},
    'CustomSecuredCC' : {'doc' : "What List of Custom CC should we always encrypt if SecurityStrategy is CUSTOM.", 'type' : "String", 'value' : '0x62,0x4c,0x63'},
    'EnforceSecureReception' : {'doc' : "If we recieve a clear text message for a CC that is Secured, should we drop the message", 'type' : "Bool"},
}

PyStatDriver = {
    'SOFCnt' : "Number of SOF bytes received",
    'ACKWaiting' : "Number of unsolicited messages while waiting for an ACK",
    'readAborts' : "Number of times read were aborted due to timeouts",
    'badChecksum' : "Number of bad checksums",
    'readCnt' : "Number of messages successfully read",
    'writeCnt' : "Number of messages successfully sent",
    'CANCnt' : "Number of CAN bytes received",
    'NAKCnt' : "Number of NAK bytes received",
    'ACKCnt' : "Number of ACK bytes received",
    'OOFCnt' : "Number of bytes out of framing",
    'dropped' : "Number of messages dropped & not delivered",
    'retries' : "Number of messages retransmitted",
    'callbacks' : "Number of unexpected callbacks",
    'badroutes' : "Number of failed messages due to bad route response",
    'noack' : "Number of no ACK returned errors",
    'netbusy' : "Number of network busy/failure messages",
    'nondelivery' : "Number of messages not delivered to network",
    'routedbusy' : "Number of messages received with routed busy status",
    'broadcastReadCnt' : "Number of broadcasts read",
    'broadcastWriteCnt' : "Number of broadcasts sent",
    }

PyStatNode = {
    'sentCnt' : "Number of messages sent from this node",
    'sentFailed' : "Number of sent messages failed",
    'retries' : "Number of message retries",
    'receivedCnt' : "Number of messages received from this node",
    'receivedDups' : "Number of duplicated messages received",
    'receivedUnsolicited' : "Number of messages received unsolicited",
    'lastRequestRTT' : "Last message request RTT",
    'lastResponseRTT' : "Last message response RTT",
    'sentTS' : "Last message sent time",
    'receivedTS' : "Last message received time",
    'averageRequestRTT' : "Average Request round trip time",
    'averageResponseRTT' : "Average Response round trip time",
    'quality' : "Node quality measure",
    'lastReceivedMessage' : "Place to hold last received message",
    'errors' : "Count errors for dead node detection",
    }

PyLogLevels = {
    'Invalid' : {'doc':'Invalid Log Status', 'value':0},
    'None' : {'doc':'Disable all logging', 'value':1},
    'Always' : {'doc':'These messages should always be shown', 'value':2},
    'Fatal' : {'doc':'A likely fatal issue in the library', 'value':3},
    'Error' : {'doc':'A serious issue with the library or the network', 'value':4},
    'Warning' : {'doc':'A minor issue from which the library should be able to recover', 'value':5},
    'Alert' : {'doc':'Something unexpected by the library about which the controlling application should be aware', 'value':6},
    'Info' : {'doc':"Everything's working fine...these messages provide streamlined feedback on each message", 'value':7},
    'Detail' : {'doc':'Detailed information on the progress of each message', 'value':8},
    'Debug' : {'doc':'Very detailed information on progress that will create a huge log file quickly but this level (as others) can be queued and sent to the log only on an error or warning', 'value':9},
    'StreamDetail' : {'doc':'Will include low-level byte transfers from controller to buffer to application and back', 'value':10},
    'Internal' : {'doc':'Used only within the log class (uses existing timestamp, etc', 'value':11},
    }

cdef map[uint64_t, ValueID] values_map

cdef getValueFromType(Manager *manager, valueId):
    """
    Translate a value in the right type
    """
    cdef float type_float
    cdef bool type_bool
    cdef uint8_t type_byte
    cdef int32_t type_int
    cdef int16_t type_short
    cdef string type_string
    cdef vector[string] vect
    cdef uint8_t* vectraw = NULL
    cdef uint8_t size
    cdef string s
    c = ""
    ret = None
    if values_map.find(valueId) != values_map.end():
        datatype = PyValueTypes[values_map.at(valueId).GetType()]
        if datatype == "Bool":
            cret = manager.GetValueAsBool(values_map.at(valueId), &type_bool)
            ret = type_bool if cret else None
            return ret
        elif datatype == "Byte":
            cret = manager.GetValueAsByte(values_map.at(valueId), &type_byte)
            ret = type_byte if cret else None
            return ret
        elif datatype == "Raw":
            cret = manager.GetValueAsRaw(values_map.at(valueId), &vectraw, &size)
            if cret:
                for x in range (0, size):
                    c += chr(vectraw[x])
            ret = c if cret else None
            free(vectraw)
            return ret
        elif datatype == "Decimal":
            cret = manager.GetValueAsFloat(values_map.at(valueId), &type_float)
            ret = type_float if cret else None
            return ret
        elif datatype == "Int":
            cret = manager.GetValueAsInt(values_map.at(valueId), &type_int)
            ret = type_int if cret else None
            return ret
        elif datatype == "Short":
            cret = manager.GetValueAsShort(values_map.at(valueId), &type_short)
            ret = type_short if cret else None
            return ret
        elif datatype == "String":
            cret = manager.GetValueAsString(values_map.at(valueId), &type_string)
            ret = type_string.c_str() if cret else None
            return ret
        elif datatype == "Button":
            cret = manager.GetValueAsBool(values_map.at(valueId), &type_bool)
            ret = type_bool if cret else None
            return ret
        elif datatype == "List":
            cret = manager.GetValueListSelection(values_map.at(valueId), &type_string)
            ret = type_string.c_str() if cret else None
            return ret
        else :
            cret = manager.GetValueAsString(values_map.at(valueId), &type_string)
            ret = type_string.c_str() if cret else None
    logger.debug("getValueFromType return %s", ret)
    return ret

cdef delValueId(ValueID v, n):
    logger.debug("delValueId : ValueID : %s", v.GetId())
    if values_map.find(v.GetId()) != values_map.end():
        values_map.erase(values_map.find(v.GetId()))

cdef addValueId(ValueID v, n):
    logger.debug("addValueId : ValueID : %s", v.GetId())
    #check is a valid value
    if v.GetInstance() == 0:
        return
    logger.debug("addValueId : GetCommandClassId : %s, GetType : %s", v.GetCommandClassId(), v.GetType())
    cdef Manager *manager = GetManager()
    item = new pair[uint64_t, ValueID](v.GetId(), v)
    values_map.insert(deref(item))
    del item
    genre = PyGenres[v.GetGenre()]
    #handle basic value in different way
    if genre =="Basic":
        n['valueId'] = {'homeId' : v.GetHomeId(),
                    'nodeId' : v.GetNodeId(),
                    'commandClass' : PyManager.COMMAND_CLASS_DESC[v.GetCommandClassId()],
                    'instance' : v.GetInstance(),
                    'index' : v.GetIndex(),
                    'id' : v.GetId(),
                    'genre' : '',
                    'type' : PyValueTypes[v.GetType()],
                    'value' : None,
                    'label' : None,
                    'units' : None,
                    'readOnly': False,
                    }
    else:
        n['valueId'] = {'homeId' : v.GetHomeId(),
                        'nodeId' : v.GetNodeId(),
                        'commandClass' : PyManager.COMMAND_CLASS_DESC[v.GetCommandClassId()],
                        'instance' : v.GetInstance(),
                        'index' : v.GetIndex(),
                        'id' : v.GetId(),
                        'genre' : genre,
                        'type' : PyValueTypes[v.GetType()],
                        'value' : getValueFromType(manager,v.GetId()),
                        'label' : manager.GetValueLabel(v).c_str(),
                        'units' : manager.GetValueUnits(v).c_str(),
                        'readOnly': manager.IsValueReadOnly(v),
                        }
    logger.debug("addValueId : Notification : %s", n)

cdef void notif_callback(const_notification _notification, void* _context) with gil:
    """
    Notification callback to the C++ library

    """
    logger.debug("notif_callback : new notification")
    cdef Notification* notification = <Notification*>_notification
    logger.debug("notif_callback : Notification type : %s, nodeId : %s", notification.GetType(), notification.GetNodeId())
    try:
        n = {'notificationType' : PyNotifications[notification.GetType()],
             'homeId' : notification.GetHomeId(),
             'nodeId' : notification.GetNodeId(),
            }
    except:
        logger.exception("notif_callback exception")
    if notification.GetType() == Type_Group:
        try:
            n['groupIdx'] = notification.GetGroupIdx()
        except:
            logger.exception("notif_callback exception Type_Group")
    elif notification.GetType() == Type_NodeEvent:
        try:
            n['event'] = notification.GetEvent()
        except:
            logger.exception("notif_callback exception Type_NodeEvent")
            raise
    elif notification.GetType() == Type_Notification:
        try:
            n['notificationCode'] = notification.GetNotification()
        except:
            logger.exception("notif_callback exception Type_Notification")
            raise
    elif notification.GetType() == Type_ControllerCommand:
        try:
            state = notification.GetEvent()
            n['controllerStateInt'] = state
            n['controllerState'] = PyControllerState[state]
            n['controllerStateDoc'] = PyControllerState[state].doc
            #Notification is filled with error
            error = notification.GetNotification()
            n['controllerErrorInt'] = error
            n['controllerError'] = PyControllerError[error]
            n['controllerErrorDoc'] = PyControllerError[error].doc
        except:
            logger.exception("notif_callback exception Type_ControllerCommand")
            raise
    elif notification.GetType() in (Type_CreateButton, Type_DeleteButton, Type_ButtonOn, Type_ButtonOff):
        try:
            n['buttonId'] = notification.GetButtonId()
        except:
            logger.exception("notif_callback exception Type_CreateButton, Type_DeleteButton, Type_ButtonOn, Type_ButtonOff")
            raise
    elif notification.GetType() == Type_DriverRemoved:
        try:
            logger.debug("Notification : Type_DriverRemoved received : clean all valueids")
            values_map.empty()
        except:
            logger.exception("notif_callback exception Type_DriverRemoved")
            raise
    elif notification.GetType() == Type_DriverReset:
        try:
            logger.debug("Notification : Type_DriverReset received : clean all valueids")
            values_map.empty()
        except:
            logger.exception("notif_callback exception Type_DriverReset")
            raise
    elif notification.GetType() == Type_SceneEvent:
        try:
            n['sceneId'] = notification.GetSceneId()
        except:
            logger.exception("notif_callback exception Type_SceneEvent")
            raise
    elif notification.GetType() in (Type_ValueAdded, Type_ValueChanged, Type_ValueRefreshed):
        try:
            addValueId(notification.GetValueID(), n)
        except:
            logger.exception("notif_callback exception Type_ValueAdded, Type_ValueChanged, Type_ValueRefreshed")
            raise
    elif notification.GetType() == Type_ValueRemoved:
        try:
            n['valueId'] = {'id' : notification.GetValueID().GetId()}
        except:
            logger.exception("notif_callback exception Type_ValueRemoved")
            raise
    #elif notification.GetType() in (Type_PollingEnabled, Type_PollingDisabled):
    #    #Maybe we should enable/disable this
    #    addValueId(notification.GetValueID(), n)
    logger.debug("notif_callback : call callback context")
    (<object>_context)(n)
    if notification.GetType() == Type_ValueRemoved:
        try:
            delValueId(notification.GetValueID(), n)
        except:
            logger.exception("notif_callback exception Type_ValueRemoved delete")
            raise
    logger.debug("notif_callback : end")

cdef void ctrl_callback(ControllerState _state, ControllerError _error, void* _context) with gil:
    """
    Controller callback to the C++ library

    """
    c = {'state' : PyControllerState[_state],
         'message' : PyControllerState[_state].doc,
         'error' : _error,
         'error_msg' : PyControllerError[_error].doc,
        }
    logger.debug("ctrl_callback : Message: %s", c)
    (<object>_context)(c)

cpdef object driverData():
    cdef DriverData data

def configPath():
    '''
    Retrieve the config path. This directory hold the xml files.

    :return: A string containing the library config path or None.
    :rtype: str

    '''
    if os.path.isfile(os.path.join("/etc/openzwave/",'device_classes.xml')):
        #At first, check in /etc/openzwave
        return "/etc/openzwave/"
    elif os.path.isfile(os.path.join("/usr/local/etc/openzwave/",'device_classes.xml')):
        #Next, check in /usr/local/etc/openzwave
        return "/usr/local/etc/openzwave/"
    else :
        #Check in python_openzwave.resources
        dirn = None
        try:
            from pkg_resources import resource_filename
            dirn = resource_filename('python_openzwave.ozw_config', '__init__.py')
            dirn = os.path.dirname(dirn)
        except ImportError:
            dirn = None
        if dirn is not None  and os.path.isfile(os.path.join(dirn,'device_classes.xml')):
            #At first, check in /etc/openzwave
            return dirn
        elif os.path.isfile(os.path.join("openzwave/config",'device_classes.xml')):
            return os.path.abspath('openzwave/config')
        #For historical reasons.
        elif os.path.isdir(os.path.join("/usr",PY_OZWAVE_CONFIG_DIRECTORY)):
            return os.path.join("/usr",PY_OZWAVE_CONFIG_DIRECTORY)
        elif os.path.isdir(os.path.join("/usr/local",PY_OZWAVE_CONFIG_DIRECTORY)):
            return os.path.join("/usr/local",PY_OZWAVE_CONFIG_DIRECTORY)
        elif os.path.isdir(os.path.join("/usr",OZWAVE_CONFIG_DIRECTORY)):
            return os.path.join("/usr",OZWAVE_CONFIG_DIRECTORY)
        elif os.path.isdir(os.path.join("/usr/local",OZWAVE_CONFIG_DIRECTORY)):
            return os.path.join("/usr/local",OZWAVE_CONFIG_DIRECTORY)
        else:
            if os.path.isdir(os.path.join(os.path.dirname(libopenzwave_file),PY_OZWAVE_CONFIG_DIRECTORY)):
                return os.path.join(os.path.dirname(libopenzwave_file), PY_OZWAVE_CONFIG_DIRECTORY)
            if os.path.isdir(os.path.join(os.getcwd(),CWD_CONFIG_DIRECTORY)):
                return os.path.join(os.getcwd(),CWD_CONFIG_DIRECTORY)
            if os.path.isdir(os.path.join(libopenzwave_location,PY_OZWAVE_CONFIG_DIRECTORY)):
                return os.path.join(libopenzwave_location, PY_OZWAVE_CONFIG_DIRECTORY)
    return None

cdef class PyOptions:
    """
    Manage options manager
    """

    cdef readonly str _config_path
    cdef readonly str _user_path
    cdef readonly str _cmd_line

    cdef Options *options

    def __init__(self, config_path=None, user_path=None, cmd_line=None):
        """
        Create an option object and check that parameters are valid.

        :param device: The device to use
        :type device: str
        :param config_path: The openzwave config directory. If None, try to configure automatically.
        :type config_path: str
        :param user_path: The user directory
        :type user_path: str
        :param cmd_line: The "command line" options of the openzwave library
        :type cmd_line: str

        """
        if config_path is None:
            config_path = self.getConfigPath()
        if config_path is None:
            raise LibZWaveException("Can't autoconfigure path to config")
        if os.path.exists(config_path):
            if not os.path.exists(os.path.join(config_path, "zwcfg.xsd")):
                raise LibZWaveException("Can't retrieve zwcfg.xsd from %s" % config_path)
            self._config_path = config_path
        else:
            raise LibZWaveException("Can't find config directory %s" % config_path)
        if user_path is None:
            user_path = "."
        if os.path.exists(user_path):
            if os.access(user_path, os.W_OK)==True and os.access(user_path, os.R_OK)==True:
                self._user_path = user_path
            else:
                raise LibZWaveException("Can't write in user directory %s" % user_path)
        else:
            raise LibZWaveException("Can't find user directory %s" % user_path)
        if cmd_line is None:
            cmd_line=""
        self._cmd_line = cmd_line
        self.create(self._config_path, self._user_path, self._cmd_line)


    def create(self, str a, str b, str c):
        """
        .. _createoptions:

        Create an option object used to start the manager

        :param a: The path of the config directory
        :type a: str
        :param b: The path of the user directory
        :type b: str
        :param c: The "command line" options of the openzwave library
        :type c: str

        :see: destroyoptions_

        """
        self.options = CreateOptions(
            str_to_cppstr(a), str_to_cppstr(b), str_to_cppstr(c))
        return True

    def destroy(self):
        """
        .. _destroyoptions:

         Deletes the Options and cleans up any associated objects.
         The application is responsible for destroying the Options object,
         but this must not be done until after the Manager object has been
         destroyed.

        :return: The result of the operation.
        :rtype: bool

        :see: createoptions_

        """
        return self.options.Destroy()

    def lock(self):
        """
        .. _lock:

        Lock the options. Needed to start the manager

        :return: The result of the operation.
        :rtype: bool

        :see: areLocked_

        """
        if not os.path.isfile(os.path.join(self._user_path,'options.xml')):
            if os.path.isfile(os.path.join(self._config_path,'options.xml')):
                copyfile(os.path.join(self._config_path,'options.xml'), os.path.join(self._user_path,'options.xml'))
            else:
                logger.warning("Can't find options.xml in %s"%self._config_path)
        return self.options.Lock()

    def areLocked(self):
        '''
        .. _areLocked:

         Test whether the options have been locked.

        :return: true if the options have been locked.
        :rtype: boolean

        :see: lock_

        '''
        return self.options.AreLocked()

    def addOptionBool(self, str name, value):
        """
        .. _addOptionBool:

        Add a boolean option.

        :param name: The name of the option.
        :type name: str
        :param value: The value of the option.
        :type value: boolean
        :return: The result of the operation.
        :rtype: bool

        :see: addOption_, addOptionInt_, addOptionString_

        """
        return self.options.AddOptionBool(str_to_cppstr(name), value)

    def addOptionInt(self, str name, value):
        """
        .. _addOptionInt:

        Add an integer option.

        :param name: The name of the option.
        :type name: str
        :param value: The value of the option.
        :type value: boolean
        :return: The result of the operation.
        :rtype: bool

        :see: addOption_, addOptionBool_, addOptionString_

        """
        return self.options.AddOptionInt(str_to_cppstr(name), value)

    def addOptionString(self, str name, str value, append=False):
        """
        .. _addOptionString:

        Add a string option.

        :param name: The name of the option.  Option names are case insensitive and must be unique.
        :type name: str
        :param value: The value of the option.
        :type value: str
        :param append: Setting append to true will cause values read from the command line
         or XML file to be concatenated into a comma delimited set.  If _append is false,
         newer values will overwrite older ones.
        :type append: boolean
        :return: The result of the operation.
        :rtype: bool

        :see: addOption_, addOptionBool_, addOptionInt_

        """
        return self.options.AddOptionString(
            str_to_cppstr(name), str_to_cppstr(value), append)

    def addOption(self, name, value):
        """
        .. _addOption:

        Add an option.

        :param name: The name of the option.
        :type name: string
        :param value: The value of the option.
        :type value: boolean, integer, string
        :return: The result of the operation.
        :rtype: bool

        :see: addOptionBool_, addOptionInt_, addOptionString_

        """
        if name not in PyOptionList:
            return False
        if PyOptionList[name]['type'] == "String":
            return self.addOptionString(name, value)
        elif PyOptionList[name]['type'] == "Bool":
            return self.addOptionBool(name, value)
        elif PyOptionList[name]['type'] == "Int":
            return self.addOptionInt(name, value)
        return False

    def getOption(self, name):
        """
        .. _getOption:

        Retrieve option of a value.

        :param name: The name of the option.
        :type name: string
        :return: The value
        :rtype: boolean, integer, string or None

        :see: getOptionAsBool_, getOptionAsInt_, getOptionAsString_

        """
        if name not in PyOptionList:
            return None
        if PyOptionList[name]['type'] == "String":
            return self.getOptionAsString(name)
        elif PyOptionList[name]['type'] == "Bool":
            return self.getOptionAsBool(name)
        elif PyOptionList[name]['type'] == "Int":
            return self.getOptionAsInt(name)
        return False

    def getOptionAsBool(self, name):
        """
        .. _getOptionAsBool:

        Retrieve boolean value of an option.

        :param name: The name of the option.
        :type name: string
        :return: The value or None
        :rtype: boolean or None

        :see: getOption_, getOptionAsInt_, getOptionAsString_

        """
        cdef bool type_bool
        cret = self.options.GetOptionAsBool(str_to_cppstr(name), &type_bool)
        ret = type_bool if cret==True else None
        return ret

    def getOptionAsInt(self, name):
        """
        .. _getOptionAsInt:

        Retrieve integer value of an option.

        :param name: The name of the option.
        :type name: string
        :return: The value or None
        :rtype: Integer or None

        :see: getOption_, getOptionAsBool_, getOptionAsString_

        """
        cdef int32_t type_int
        cret = self.options.GetOptionAsInt(str_to_cppstr(name), &type_int)
        ret = type_int if cret==True else None
        return ret

    def getOptionAsString(self, name):
        """
        .. _getOptionAsString:

        Retrieve string value of an option.

        :param name: The name of the option.
        :type name: string
        :return: The value or None
        :rtype: String or None

        :see: getOption_, getOptionAsBool_, getOptionAsInt_

        """
        cdef string type_string
        cret = self.options.GetOptionAsString(str_to_cppstr(name), &type_string)
        ret = cstr_to_str(type_string.c_str()) if cret==True else None
        return ret

    def getConfigPath(self):
        '''
        .. _getConfigPath:

        Retrieve the config path. This directory hold the xml files.

        :return: A string containing the library config path or None.
        :rtype: str

        '''
        return configPath()


cdef class RetAlloc:
    """
    Map an array of uint8_t used when retrieving sets.
    Allocate memory at init and free it when no more reference to it exist.
    Give it to lion as Nico0084 says : http://blog.naviso.fr/wordpress/wp-sphinxdoc/uploads/2011/11/MemoryLeaks3.jpg

    """
    cdef uint32_t siz
    cdef uint8_t* data

    def __cinit__(self,  uint32_t siz):
        self.siz = siz
        self.data = <uint8_t*>malloc(sizeof(uint8_t) * siz)

    def __dealloc__(self):
        free(self.data)

cdef class InstanceAssociationAlloc:
    """
    Map an array of InstanceAssociation_t used when retrieving sets of associationInstances.
    Allocate memory at init and free it when no more reference to it exist.
    Give it to lion as Nico0084 says : http://blog.naviso.fr/wordpress/wp-sphinxdoc/uploads/2011/11/MemoryLeaks3.jpg

    """
    cdef uint32_t siz
    cdef uint8_t* data

    def __cinit__(self,  uint32_t siz):
        self.siz = siz
        self.data = <uint8_t*>malloc(sizeof(uint8_t) * siz * 2)

    def __dealloc__(self):
        free(self.data)

cdef class PyManager:
    '''
The main public interface to OpenZWave.

A singleton class providing the main public interface to OpenZWave.  The
Manager class exposes all the functionality required to add Z-Wave support to
an application.  It handles the sending and receiving of Z-Wave messages as
well as the configuration of a Z-Wave network and its devices, freeing the
library user from the burden of learning the low-level details of the Z-Wave
protocol.

All Z-Wave functionality is accessed via the Manager class.  While this does
not make for the most efficient code structure, it does enable the library to
handle potentially complex and hard-to-debug issues such as multi-threading and
object lifespans behind the scenes. Application development is therefore
simplified and less prone to bugs.

There can be only one instance of the Manager class, and all applications will
start by calling Manager::Create static method to create that instance.  From
then on, a call to the Manager::Get static method will return the pointer to
the Manager object.  On application exit, Manager::Destroy should be called to
allow OpenZWave to clean up and delete any other objects it has created.

Once the Manager has been created, a call should be made to Manager::AddWatcher
to install a notification callback handler.  This handler will receive
notifications of Z-Wave network changes and updates to device values, and is an
essential element of OpenZWave.

Next, a call should be made to Manager::AddDriver for each Z-Wave controller
attached to the PC.  Each Driver will handle the sending and receiving of
messages for all the devices in its controller's Z-Wave network.  The Driver
will read any previously saved configuration and then query the Z-Wave
controller for any missing information.  Once that process is complete, a
DriverReady notification callback will be sent containing the Home ID of the
controller, which is required by most of the other Manager class methods.

After the DriverReady notification is sent, the Driver will poll each node on
the network to update information about each node.  After all "awake" nodes
have been polled, an "AllAwakeNodesQueried" notification is sent.  This is when
a client application can expect all of the node information (both static
information, like the physical device's capabilities, session information (like
[associations and/or names] and dynamic information (like temperature or on/off
state) to be available.  Finally, after all nodes (whether setening or
sleeping) have been polled, an "AllNodesQueried" notification is sent.
    '''
    COMMAND_CLASS_DESC = {
        0x00: 'COMMAND_CLASS_NO_OPERATION',
        0x20: 'COMMAND_CLASS_BASIC',
        0x21: 'COMMAND_CLASS_CONTROLLER_REPLICATION',
        0x22: 'COMMAND_CLASS_APPLICATION_STATUS',
        0x23: 'COMMAND_CLASS_ZIP_SERVICES',
        0x24: 'COMMAND_CLASS_ZIP_SERVER',
        0x25: 'COMMAND_CLASS_SWITCH_BINARY',
        0x26: 'COMMAND_CLASS_SWITCH_MULTILEVEL',
        0x27: 'COMMAND_CLASS_SWITCH_ALL',
        0x28: 'COMMAND_CLASS_SWITCH_TOGGLE_BINARY',
        0x29: 'COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL',
        0x2A: 'COMMAND_CLASS_CHIMNEY_FAN',
        0x2B: 'COMMAND_CLASS_SCENE_ACTIVATION',
        0x2C: 'COMMAND_CLASS_SCENE_ACTUATOR_CONF',
        0x2D: 'COMMAND_CLASS_SCENE_CONTROLLER_CONF',
        0x2E: 'COMMAND_CLASS_ZIP_CLIENT',
        0x2F: 'COMMAND_CLASS_ZIP_ADV_SERVICES',
        0x30: 'COMMAND_CLASS_SENSOR_BINARY',
        0x31: 'COMMAND_CLASS_SENSOR_MULTILEVEL',
        0x32: 'COMMAND_CLASS_METER',
        0x33: 'COMMAND_CLASS_COLOR',
        0x34: 'COMMAND_CLASS_ZIP_ADV_CLIENT',
        0x35: 'COMMAND_CLASS_METER_PULSE',
        0x3C: 'COMMAND_CLASS_METER_TBL_CONFIG',
        0x3D: 'COMMAND_CLASS_METER_TBL_MONITOR',
        0x3E: 'COMMAND_CLASS_METER_TBL_PUSH',
        0x38: 'COMMAND_CLASS_THERMOSTAT_HEATING',
        0x40: 'COMMAND_CLASS_THERMOSTAT_MODE',
        0x42: 'COMMAND_CLASS_THERMOSTAT_OPERATING_STATE',
        0x43: 'COMMAND_CLASS_THERMOSTAT_SETPOINT',
        0x44: 'COMMAND_CLASS_THERMOSTAT_FAN_MODE',
        0x45: 'COMMAND_CLASS_THERMOSTAT_FAN_STATE',
        0x46: 'COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE',
        0x47: 'COMMAND_CLASS_THERMOSTAT_SETBACK',
        0x4c: 'COMMAND_CLASS_DOOR_LOCK_LOGGING',
        0x4E: 'COMMAND_CLASS_SCHEDULE_ENTRY_LOCK',
        0x50: 'COMMAND_CLASS_BASIC_WINDOW_COVERING',
        0x51: 'COMMAND_CLASS_MTP_WINDOW_COVERING',
        0x56: 'COMMAND_CLASS_CRC_16_ENCAP',
        0x5A: 'COMMAND_CLASS_DEVICE_RESET_LOCALLY',
        0x5B: 'COMMAND_CLASS_CENTRAL_SCENE',
        0x5E: 'COMMAND_CLASS_ZWAVEPLUS_INFO',
        0x60: 'COMMAND_CLASS_MULTI_INSTANCE/CHANNEL',
        0x61: 'COMMAND_CLASS_DISPLAY',
        0x62: 'COMMAND_CLASS_DOOR_LOCK',
        0x63: 'COMMAND_CLASS_USER_CODE',
        0x64: 'COMMAND_CLASS_GARAGE_DOOR',
        0x66: 'COMMAND_CLASS_BARRIER_OPERATOR',
        0x70: 'COMMAND_CLASS_CONFIGURATION',
        0x71: 'COMMAND_CLASS_ALARM',
        0x72: 'COMMAND_CLASS_MANUFACTURER_SPECIFIC',
        0x73: 'COMMAND_CLASS_POWERLEVEL',
        0x75: 'COMMAND_CLASS_PROTECTION',
        0x76: 'COMMAND_CLASS_LOCK',
        0x77: 'COMMAND_CLASS_NODE_NAMING',
        0x78: 'COMMAND_CLASS_ACTUATOR_MULTILEVEL',
        0x79: 'COMMAND_CLASS_KICK',
        0x7A: 'COMMAND_CLASS_FIRMWARE_UPDATE_MD',
        0x7B: 'COMMAND_CLASS_GROUPING_NAME',
        0x7C: 'COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE',
        0x7D: 'COMMAND_CLASS_REMOTE_ASSOCIATION',
        0x80: 'COMMAND_CLASS_BATTERY',
        0x81: 'COMMAND_CLASS_CLOCK',
        0x82: 'COMMAND_CLASS_HAIL',
        0x83: 'COMMAND_CLASS_NETWORK_STAT',
        0x84: 'COMMAND_CLASS_WAKE_UP',
        0x85: 'COMMAND_CLASS_ASSOCIATION',
        0x86: 'COMMAND_CLASS_VERSION',
        0x87: 'COMMAND_CLASS_INDICATOR',
        0x88: 'COMMAND_CLASS_PROPRIETARY',
        0x89: 'COMMAND_CLASS_LANGUAGE',
        0x8A: 'COMMAND_CLASS_TIME',
        0x8B: 'COMMAND_CLASS_TIME_PARAMETERS',
        0x8C: 'COMMAND_CLASS_GEOGRAPHIC_LOCATION',
        0x8D: 'COMMAND_CLASS_COMPOSITE',
        0x8E: 'COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION',
        0x8F: 'COMMAND_CLASS_MULTI_CMD',
        0x90: 'COMMAND_CLASS_ENERGY_PRODUCTION',
        0x91: 'COMMAND_CLASS_MANUFACTURER_PROPRIETARY',
        0x92: 'COMMAND_CLASS_SCREEN_MD',
        0x93: 'COMMAND_CLASS_SCREEN_ATTRIBUTES',
        0x94: 'COMMAND_CLASS_SIMPLE_AV_CONTROL',
        0x95: 'COMMAND_CLASS_AV_CONTENT_DIRECTORY_MD',
        0x96: 'COMMAND_CLASS_AV_RENDERER_STATUS',
        0x97: 'COMMAND_CLASS_AV_CONTENT_SEARCH_MD',
        0x98: 'COMMAND_CLASS_SECURITY',
        0x99: 'COMMAND_CLASS_AV_TAGGING_MD',
        0x9A: 'COMMAND_CLASS_IP_CONFIGURATION',
        0x9B: 'COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION',
        0x9C: 'COMMAND_CLASS_SENSOR_ALARM',
        0x9D: 'COMMAND_CLASS_SILENCE_ALARM',
        0x9E: 'COMMAND_CLASS_SENSOR_CONFIGURATION',
        0xEF: 'COMMAND_CLASS_MARK',
        0xF0: 'COMMAND_CLASS_NON_INTEROPERABLE'
    }
    '''
    The command classes

    '''

    CALLBACK_DESC = ('value added','value removed','value changed','groups changed','new node','node added',
                     'node removed','node protocol info','node naming','node event','polling disabled',
                     'polling enabled','driver ready','driver reset','message complete','node queries complete',
                     'awake nodes queried','all nodes queried')

    cdef Manager *manager
    cdef object _watcherCallback
    cdef object _controllerCallback

    def create(self):
        '''
.. _create:

Creates the Manager singleton object.

The Manager provides the public interface to OpenZWave, exposing all the
functionality required to add Z-Wave support to an application. There can be
only one Manager in an OpenZWave application.  An Options object must be
created and Locked first, otherwise the call to Manager::Create will fail.
Once the Manager has been created, call AddWatcher to install a notification
callback handler, and then call the AddDriver method for each attached PC
Z-Wave controller in turn.

:see: destroy_
        '''
        #Commented to try to fix seg fault at import
        Py_Initialize()
        PyEval_InitThreads()
        self.manager = CreateManager()

    def destroy(self):
        '''
.. _destroy:

Deletes the Manager and cleans up any associated objects.

:see: create_
        '''
        self.manager.Destroy()

#
# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
# For saving the Z-Wave network configuration so that the entire network does not need to be
# polled every time the application starts.
#
    def writeConfig(self, homeid):
        '''
Saves the configuration of a PC Controller's Z-Wave network to the
application's user data folder.

This method does not normally need to be called, since OpenZWave will save the
state automatically during the shutdown process.  It is provided here only as
an aid to development. The configuration of each PC Controller's Z-Wave network
is stored in a separate file.  The filename consists of the 8 digit hexadecimal
version of the controller's Home ID, prefixed with the string "zwcfg_*".  This
convention allows OpenZWave to find the correct configuration file for a
controller, even if it is attached to a different serial port, USB device path,
etc.

:param homeid: The Home ID of the Z-Wave controller to save.
:type homeid: int

        '''
        self.manager.WriteConfig(homeid)
#
# -----------------------------------------------------------------------------
# Drivers
# -----------------------------------------------------------------------------
# Methods for adding and removing drivers and obtaining basic controller information.
#
    def addDriver(self, str serialport):
        '''
.. _addDriver:

Creates a new driver for a Z-Wave controller.

This method creates a Driver object for handling communications with a single
Z-Wave controller.  In the background, the driver first tries to read
configuration data saved during a previous run.  It then queries the controller
directly for any missing information, and a refresh of the set of nodes that
it controls.  Once this information has been received, a DriverReady
notification callback is sent, containing the Home ID of the controller.  This
Home ID is required by most of the OpenZWave Manager class methods.

:param serialport: The string used to open the controller.  On Windows this might be something like "\\.\\COM3", or on Linux "/dev/ttyUSB0".
:type serialport: str
:return: True if a new driver was created
:rtype: bool
:see: removeDriver_

        '''
        self.manager.AddDriver(str_to_cppstr(serialport))

    def removeDriver(self, str serialport):
        '''
.. _removeDriver:

Removes the driver for a Z-Wave controller, and closes the controller.

Drivers do not need to be explicitly removed before calling Destroy - this is
handled automatically.

:param serialport: The same string as was passed in the original call toAddDriver.
:type serialport: str
:return: True if the driver was removed, False if it could not be found.
:rtype: bool
:see: addDriver_

        '''
        self.manager.RemoveDriver(str_to_cppstr(serialport))

    def getControllerInterfaceType(self, homeid):
        '''
.._getControllerInterfaceType:
Retrieve controller interface type, Unknown, Serial, Hid

:param homeId: The Home ID of the Z-Wave controller.
:return: The controller interface type
:rtype: str

        '''
        type = self.manager.GetControllerInterfaceType(homeid)
        return PyControllerInterface[type]

    def getControllerPath(self, homeid):
        '''
.._getControllerPath:
Retrieve controller interface path, name or path used to open the controller hardware

:param homeId: The Home ID of the Z-Wave controller.
:return: The controller interface type
:rtype: str

        '''
        cdef string c_string = self.manager.GetControllerPath(homeid)
        return cstr_to_str(c_string.c_str())

    def getControllerNodeId(self, homeid):
        '''
.. _getControllerNodeId:

Get the node ID of the Z-Wave controller.

:param homeId: The Home ID of the Z-Wave controller.
:type homeId: int
:return: The node ID of the Z-Wave controller
:rtype: int

        '''
        return self.manager.GetControllerNodeId(homeid)

    def getSUCNodeId(self, homeid):
        '''
.. _getSUCNodeId:

Get the node ID of the Static Update Controller.

:param homeId: The Home ID of the Z-Wave controller.
:type homeId: int
:return: the node ID of the Z-Wave controller.
:rtype: int

        '''
        return self.manager.GetSUCNodeId(homeid)

    def isPrimaryController(self, homeid):
        '''
.. _isPrimaryController:

Query if the controller is a primary controller.

The primary controller is the main device used to configure and control a
Z-Wave network.  There can only be one primary controller - all other
controllers are secondary controllers.

The only difference between a primary and secondary controller is that the
primary is the only one that can be used to add or remove other devices.  For
this reason, it is usually better for the promary controller to be portable,
since most devices must be added when installed in their final location.

Calls to BeginControllerCommand will fail if the controller is not the primary.

:param homeId: The Home ID of the Z-Wave controller.
:type homeId: int
:return: True if it is a primary controller, False if not.
:rtype: bool
:see: isBridgeController_, isStaticUpdateController_

        '''
        return self.manager.IsPrimaryController(homeid)

    def isStaticUpdateController(self, homeid):
        '''
.. _isStaticUpdateController:

Query if the controller is a static update controller (SUC).

A Static Update Controller (SUC) is a controller that must never be moved in
normal operation and which can be used by other nodes to receive information
about network changes.

:param homeId: The Home ID of the Z-Wave controller.
:type homeId: int
:return: True if it is a static update controller, False if not.
:rtype: bool
:see: isBridgeController_, isPrimaryController_

        '''
        return self.manager.IsStaticUpdateController(homeid)

    def isBridgeController(self, homeid):
        '''
.. _isBridgeController:

Query if the controller is using the bridge controller library.

A bridge controller is able to create virtual nodes that can be associated
with other controllers to enable events to be passed on.

:param homeId: The Home ID of the Z-Wave controller.
:type homeId: int
:return: True if it is a bridge controller, False if not.
:rtype: bool
:see: isPrimaryController_, isStaticUpdateController_

        '''
        return self.manager.IsBridgeController(homeid)

    def getLibraryVersion(self, homeid):
        '''
.. _getLibraryVersion:

Get the version of the Z-Wave API library used by a controller.

:param homeId: The Home ID of the Z-Wave controller.
:type homeId: int
:return: A string containing the library version. For example, "Z-Wave 2.48".
:rtype: str
:see: getPythonLibraryVersion_, getLibraryTypeName_, getOzwLibraryVersion_

        '''
        cdef string c_string = self.manager.GetLibraryVersion(homeid)
        return cstr_to_str(c_string.c_str())

    def getPythonLibraryFlavor(self):
        '''
.. _getPythonLibraryFlavor:

Get the flavor of the python library.

:return: A string containing the python library flavor. For example, "embed".
:rtype: str
:see: getLibraryTypeName_, getLibraryVersion_, getOzwLibraryVersion_, getOzwLibraryLongVersion

        '''
        return "%s" % (PY_LIB_FLAVOR_STRING)

    def getPythonLibraryVersion(self):
        '''
.. _getPythonLibraryVersion:

Get the version of the python library.

:return: A string containing the python library version. For example, "python-openzwave version 0.1".
:rtype: str
:see: getLibraryTypeName_, getLibraryVersion_, getOzwLibraryVersion_, getOzwLibraryLongVersion

        '''
        return "python_openzwave version %s (%s-%s / %s - %s)" % (PYLIBRARY, PY_LIB_FLAVOR_STRING, PY_LIB_BACKEND_STRING, PY_LIB_DATE_STRING, PY_LIB_TIME_STRING)

    def getPythonLibraryVersionNumber(self):
        """
.. _getPythonLibraryVersionNumber:

Get the python library version number

:return: A string containing the python library version. For example, "0.1".
:rtype: str
:see: getLibraryTypeName_, getLibraryVersion_, getOzwLibraryVersion_, getOzwLibraryLongVersion

        """
        return PYLIBRARY

    def getOzwLibraryVersion(self):
        """
.. _getOzwLibraryVersion:

Get a string containing the openzwave library version.

:return: A string containing the library type.
:rtype: str
:see: getLibraryVersion_, getPythonLibraryVersion_, getLibraryTypeName_, getOzwLibraryLongVersion_

        """
        cdef string c_string = self.manager.getVersionAsString()
        return cstr_to_str(c_string.c_str())

    def getOzwLibraryLongVersion(self):
        """
.. _getOzwLibraryLongVersion:

Get a string containing the openzwave library version.

:return: A string containing the library type.
:rtype: str
:see: getLibraryVersion_, getPythonLibraryVersion_, getLibraryTypeName_, getOzwLibraryVersion_

        """
        cdef string c_string = self.manager.getVersionLongAsString()
        return cstr_to_str(c_string.c_str())

    def getOzwLibraryVersionNumber(self):
        '''
_getOzwLibraryVersionNumber: Get the openzwave library version number.

:return: A string containing the library type.
:rtype: str
:see: getLibraryVersion_, getPythonLibraryVersion_, getLibraryTypeName_

        '''
        cdef string c_string = self.manager.getVersionAsString()
        return cstr_to_str(c_string.c_str())

    def getLibraryTypeName(self, homeid):
        '''
.. _getLibraryTypeName:

Get a string containing the Z-Wave API library type used by a controller.

The possible library types are:

    - Static Controller
    - Controller
    - Enhanced Slave
    - Slave
    - Installer
    - Routing Slave
    - Bridge Controller
    - Device Under Test

The controller should never return a slave library type.  For a more efficient
test of whether a controller is a Bridge Controller, use the IsBridgeController
method.

:param homeId: The Home ID of the Z-Wave controller.
:type homeId: int
:return: A string containing the library type.
:rtype: str
:see: getLibraryVersion_, getPythonLibraryVersion_, getOzwLibraryVersion_

        '''
        cdef string c_string = self.manager.GetLibraryTypeName(homeid)
        return cstr_to_str(c_string.c_str())

    def getSendQueueCount(self, homeid):
        '''
.. _getSendQueueCount:

Get count of messages in the outgoing send queue.

:param homeId: The Home ID of the Z-Wave controller.
:type homeId: int
:return: Message count
:rtype: int

        '''
        return self.manager.GetSendQueueCount(homeid)

    def logDriverStatistics(self, homeid):
        '''
.. _logDriverStatistics:

Send current driver statistics to the log file.

:param homeid: The Home ID of the Z-Wave controller.
:type homeid: int

        '''
        self.manager.LogDriverStatistics(homeid)

#-----------------------------------------------------------------------------
# Statistics interface
#-----------------------------------------------------------------------------
    def getDriverStatistics(self, homeId):
        '''
.. _getDriverStatistics:

Retrieve statistics from driver.

Statistics:

    * SOFCnt : Number of SOF bytes received
    * ACKWaiting : Number of unsolicited messages while waiting for an ACK
    * readAborts : Number of times read were aborted due to timeouts
    * badChecksum : Number of bad checksums
    * readCnt : Number of messages successfully read
    * writeCnt : Number of messages successfully sent
    * CANCnt : Number of CAN bytes received
    * NAKCnt : Number of NAK bytes received
    * ACKCnt : Number of ACK bytes received
    * OOFCnt : Number of bytes out of framing
    * dropped : Number of messages dropped & not delivered
    * retries : Number of messages retransmitted
    * callbacks : Number of unexpected callbacks
    * badroutes : Number of failed messages due to bad route response
    * noack : Number of no ACK returned errors
    * netbusy : Number of network busy/failure messages
    * nondelivery : Number of messages not delivered to network
    * routedbusy : Number of messages received with routed busy status
    * broadcastReadCnt : Number of broadcasts read
    * broadcastWriteCnt : Number of broadcasts sent

:param homeId: The Home ID of the Z-Wave controller.
:type homeId: int
:param data: Pointer to structure DriverData to return values
:type data: int
:return: A dict containing statistics of the driver.
:rtype: dict()
:see: getNodeStatistics_

       '''
        cdef DriverData_t data
        self.manager.GetDriverStatistics( homeId, &data );
        ret = {}
        ret['SOFCnt'] = data.m_SOFCnt
        ret['ACKWaiting'] = data.m_ACKWaiting
        ret['readAborts'] = data.m_readAborts
        ret['badChecksum'] = data.m_badChecksum
        ret['readCnt'] = data.m_readCnt
        ret['writeCnt'] = data.m_writeCnt
        ret['CANCnt'] = data.m_CANCnt
        ret['NAKCnt'] = data.m_NAKCnt
        ret['ACKCnt'] = data.m_ACKCnt
        ret['OOFCnt'] = data.m_OOFCnt
        ret['dropped'] = data.m_dropped
        ret['retries'] = data.m_retries
        ret['callbacks'] = data.m_callbacks
        ret['badroutes'] = data.m_badroutes
        ret['noack'] = data.m_noack
        ret['netbusy'] = data.m_netbusy
        ret['nondelivery'] = data.m_nondelivery
        ret['routedbusy'] = data.m_routedbusy
        ret['broadcastReadCnt'] = data.m_broadcastReadCnt
        ret['broadcastWriteCnt'] = data.m_broadcastWriteCnt
        return ret


# -----------------------------------------------------------------------------
# Network Commands
# -----------------------------------------------------------------------------
# Commands for Z-Wave network for testing, routing and other internal operations.
#



    def testNetworkNode(self, homeid, nodeid, count):
        '''
.. _testNetworkNode:

Test network node.

Sends a series of messages to a network node for testing network reliability.

:param homeid: The Home ID of the Z-Wave controller that manages the node.
:type homeid: int
:param nodeid: The ID of the node to query.
:type nodeid: int
:param count: This is the number of test messages to send.
:type count: int
:see: testNetwork_

        '''
        self.manager.TestNetworkNode(homeid, nodeid, count)

    def testNetwork(self, homeid, count):
        '''
.. _testNetwork:

Test network.

Sends a series of messages to every node on the network for testing network reliability.

:param homeid: The Home ID of the Z-Wave controller that manages the node.
:type homeid: int
:param count: This is the number of test messages to send.
:type count: int
:see: testNetworkNode_

        '''
        self.manager.TestNetwork(homeid, count)

    def healNetworkNode(self, homeid, nodeid,  upNodeRoute = False):
        '''
.. _healNetworkNode:

Heal network node by requesting the node rediscover their neighbors.
Sends a ControllerCommand_RequestNodeNeighborUpdate to the node.

:param homeid: The Home ID of the Z-Wave controller that manages the node.
:type homeid: int
:param nodeid: The ID of the node to query.
:type nodeid: int
:param upNodeRoute: Optional Whether to perform return routes initialization. (default = false).
:type upNodeRoute: bool
:see: healNetwork_
        '''
        self.manager.HealNetworkNode(homeid, nodeid,  upNodeRoute)

    def healNetwork(self, homeid, upNodeRoute = False):
        '''
.. _healNetwork:

Heal network by requesting nodes rediscover their neighbors.
Sends a ControllerCommand_RequestNodeNeighborUpdate to every node.
Can take a while on larger networks.

:param homeid: The Home ID of the Z-Wave controller that manages the node.
:type homeid: int
:param upNodeRoute: Optional Whether to perform return routes initialization. (default = false).
:type upNodeRoute: bool
:see: healNetworkNode_
        '''
        self.manager.HealNetwork(homeid, upNodeRoute)

# -----------------------------------------------------------------------------
# Polling Z-Wave devices
# -----------------------------------------------------------------------------
# Methods for controlling the polling of Z-Wave devices.  Modern devices will
# not require polling.  Some old devices need to be polled as the only way to
# detect status changes.
#
    def getPollInterval(self):
        '''
.. _getPollInterval:

Get the time period between polls of a nodes state

:return: The number of milliseconds between polls
:rtype: int
:see: setPollInterval_, enablePoll_, isPolled_, setPollIntensity_, disablePoll_, getPollIntensity_

        '''
        return self.manager.GetPollInterval()

    def setPollInterval(self, milliseconds, bIntervalBetweenPolls ):
        '''
.. _setPollInterval:

Set the time period between polls of a nodes state.

Due to patent concerns, some devices do not report state changes automatically
to the controller.  These devices need to have their state polled at regular
intervals.  The length of the interval is the same for all devices.  To even
out the Z-Wave network traffic generated by polling, OpenZWave divides the
polling interval by the number of devices that have polling enabled, and polls
each in turn.  It is recommended that if possible, the interval should not be
set shorter than the number of polled devices in seconds (so that the network
does not have to cope with more than one poll per second).

:param milliseconds: The length of the polling interval in milliseconds.
:type milliseconds: int
:param bIntervalBetweenPolls: If set to true (via SetPollInterval), the pollInterval will be interspersed between each poll (so a much smaller m_pollInterval like 100, 500, or 1,000 may be appropriate). If false, the library attempts to complete all polls within m_pollInterval
:type bIntervalBetweenPolls: bool
:see: getPollInterval_, enablePoll_, isPolled_, setPollIntensity_, disablePoll_, getPollIntensity_

        '''
        self.manager.SetPollInterval(milliseconds, bIntervalBetweenPolls)

    def enablePoll(self, id, intensity = 1):
        '''
.. _enablePoll:

Enable the polling of a device's state.

:param id: The ID of the value to start polling
:type id: int
:param intensity: The intensity of the poll
:type intensity: int
:return: True if polling was enabled.
:rtype: bool
:see: getPollInterval_, setPollInterval_, isPolled_, setPollIntensity_, disablePoll_, getPollIntensity_

        '''
        if values_map.find(id) != values_map.end():
            return self.manager.EnablePoll(values_map.at(id), intensity)
        else :
            return False

    def disablePoll(self, id):
        '''
.. _disablePoll:

Disable polling of a value.

:param id: The ID of the value to disable polling.
:type id: int
:return: True if polling was disabled.
:rtype: bool
:see: getPollInterval_, setPollInterval_, enablePoll_, isPolled_, setPollIntensity_, getPollIntensity_

        '''
        if values_map.find(id) != values_map.end():
            return self.manager.DisablePoll(values_map.at(id))
        else :
            return False

    def isPolled(self, id):
        '''
.. _isPolled:

Check polling status of a value

:param id: The ID of the value to check polling.
:type id: int
:return: True if polling is active.
:rtype: bool
:see: getPollInterval_, setPollInterval_, enablePoll_, setPollIntensity_, disablePoll_, getPollIntensity_

        '''
        if values_map.find(id) != values_map.end():
            return self.manager.isPolled(values_map.at(id))
        else :
            return False

    def getPollIntensity(self, id):
        '''
.. _getPollIntensity:

Get the intensity with which this value is polled (0=none, 1=every time through the list, 2-every other time, etc).
:param id: The ID of a value.
:type id: int
:return: A integer containing the poll intensity
:rtype: int
:see: getPollInterval_, setPollInterval_, enablePoll_, setPollIntensity_, disablePoll_, isPolled_

       '''
        if values_map.find(id) != values_map.end():
            intensity = self.manager.GetPollIntensity(values_map.at(id))
            return intensity
        else :
            return 0

    def setPollIntensity(self, id, intensity):
        '''
.. _setPollIntensity:

Set the frequency of polling (0=none, 1=every time through the set, 2-every other time, etc)

:param id: The ID of the value whose intensity should be set
:type id: int
:param intensity: the intensity of the poll
:type intensity: int
:see: getPollInterval_, setPollInterval_, enablePoll_, isPolled_, disablePoll_, getPollIntensity_

        '''
        if values_map.find(id) != values_map.end():
            self.manager.SetPollIntensity(values_map.at(id), intensity)

#
# -----------------------------------------------------------------------------
# Node information
# -----------------------------------------------------------------------------
# Methods for accessing information on individual nodes..
#

    def getNodeStatistics(self, homeId, nodeId):
        '''
.. _getNodeStatistics:

Retrieve statistics per node

Statistics:

    cdef struct NodeData:
        * sentCnt                              # Number of messages sent from this node.
        * sentFailed                           # Number of sent messages failed
        * retries                                # Number of message retries
        * receivedCnt                        # Number of messages received from this node.
        * receivedDups                      # Number of duplicated messages received;
        * receivedUnsolicited             # Number of messages received unsolicited
        * sentTS                                # Last message sent time
        * receivedTS                          # Last message received time
        * lastRequestRTT                    # Last message request RTT
        * averageRequestRTT             # Average Request Round Trip Time (ms).
        * lastResponseRTT                  # Last message response RTT
        * averageResponseRTT           #Average Reponse round trip time.
        * quality                                # Node quality measure
        * lastReceivedMessage[254]   # Place to hold last received message

:param homeId: The Home ID of the Z-Wave controller.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:param data: Pointer to structure NodeData to return values
:type data: int
:return: A dict containing statistics of the node.
:rtype: dict()
:see: getDriverStatistics_

       '''

        cdef NodeData_t data
        self.manager.GetNodeStatistics( homeId, nodeId, &data );
        ret = {}
        ret['sentCnt'] = data.m_sentCnt
        ret['sentFailed'] = data.m_sentFailed
        ret['retries'] = data.m_retries
        ret['receivedCnt'] = data.m_receivedCnt
        ret['receivedDups'] = data.m_receivedDups
        ret['receivedUnsolicited'] = data.m_receivedUnsolicited
        ret['sentTS'] = data.m_sentTS.c_str()
        ret['receivedTS'] = data.m_receivedTS.c_str()
        ret['lastRequestRTT'] = data.m_lastRequestRTT
        ret['averageRequestRTT'] = data.m_averageRequestRTT
        ret['lastResponseRTT'] = data.m_lastResponseRTT
        ret['averageResponseRTT'] = data.m_averageResponseRTT
        ret['quality'] = data.m_quality
        ret['lastReceivedMessage'] = []
        for i in range( 0, 254) :
            ret['lastReceivedMessage'] .append(data.m_lastReceivedMessage[i])
        return ret

    def requestNodeDynamic(self, homeid, nodeid):
        '''
.. _requestNodeDynamic:

Trigger the fetching of fixed data about a node.

Causes the nodes data to be obtained from the Z-Wave network in the same way
as if it had just been added.  This method would normally be called
automatically by OpenZWave, but if you know that a node has been changed,
calling this method will force a refresh of the data held by the library.  This
can be especially useful for devices that were asleep when the application was
first run.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: True if the request was sent successfully.
:rtype: bool

        '''
        return self.manager.RequestNodeDynamic(homeid, nodeid)

    def refreshNodeInfo(self, homeid, nodeid):
        '''
.. _refreshNodeInfo:

Trigger the fetching of fixed data about a node.

Causes the nodes data to be obtained from the Z-Wave network in the same way
as if it had just been added.  This method would normally be called
automatically by OpenZWave, but if you know that a node has been changed,
calling this method will force a refresh of the data held by the library.  This
can be especially useful for devices that were asleep when the application was
first run.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: True if the request was sent successfully.
:rtype: bool

        '''
        return self.manager.RefreshNodeInfo(homeid, nodeid)

    def requestNodeState(self, homeid, nodeid):
        '''
.. _requestNodeState:

Trigger the fetching of just the dynamic value data for a node.
Causes the node's values to be requested from the Z-Wave network. This is the
same as the query state starting from the dynamic state.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: True if the request was sent successfully.
:rtype: bool

        '''
        return self.manager.RequestNodeState(homeid, nodeid)

    def isNodeBeamingDevice(self, homeid, nodeid):
        '''
.. _isNodeBeamingDevice:

Get whether the node is a beam capable device.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: True if the node is a beaming device
:rtype: bool
:see: isNodeListeningDevice_, isNodeFrequentListeningDevice_, isNodeSecurityDevice_, isNodeRoutingDevice_

        '''
        return self.manager.IsNodeBeamingDevice(homeid, nodeid)


    def isNodeListeningDevice(self, homeid, nodeid):
        '''
.. _isNodeListeningDevice:

Get whether the node is a setening device that does not go to sleep

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: True if it is a setening node.
:rtype: bool
:see: isNodeBeamingDevice_, isNodeFrequentListeningDevice_, isNodeSecurityDevice_, isNodeRoutingDevice_

        '''
        return self.manager.IsNodeListeningDevice(homeid, nodeid)

    def isNodeFrequentListeningDevice(self, homeid, nodeid):
        '''
.. _isNodeFrequentListeningDevice:

Get whether the node is a frequent setening device that goes to sleep but
can be woken up by a beam. Useful to determine node and controller consistency.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: True if it is a frequent setening node.
:rtype: bool
:see: isNodeBeamingDevice_, isNodeListeningDevice_, isNodeSecurityDevice_, isNodeRoutingDevice_

        '''
        return self.manager.IsNodeFrequentListeningDevice(homeid, nodeid)

    def isNodeSecurityDevice(self, homeid, nodeid):
        '''
.. _isNodeSecurityDevice:

Get the security attribute for a node. True if node supports security features.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: True if security features implemented.
:rtype: bool
:see: isNodeBeamingDevice_, isNodeListeningDevice_, isNodeFrequentListeningDevice_, isNodeRoutingDevice_

        '''
        return self.manager.IsNodeSecurityDevice(homeid, nodeid)

    def isNodeRoutingDevice(self, homeid, nodeid):
        '''
.. _isNodeRoutingDevice:

Get whether the node is a routing device that passes messages to other nodes

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: True if the node is a routing device
:rtype: bool
:see: isNodeBeamingDevice_, isNodeListeningDevice_, isNodeFrequentListeningDevice_, isNodeSecurityDevice_

        '''
        return self.manager.IsNodeRoutingDevice(homeid, nodeid)

    def getNodeMaxBaudRate(self, homeid, nodeid):
        '''
.. _getNodeMaxBaudRate:

Get the maximum baud rate of a nodes communications

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: The baud rate in bits per second.
:rtype: int

        '''
        return self.manager.GetNodeMaxBaudRate(homeid, nodeid)

    def getNodeVersion(self, homeid, nodeid):
        '''
.. _getNodeVersion:

Get the version number of a node

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: The node version number
:rtype: int

        '''
        return self.manager.GetNodeVersion(homeid, nodeid)

    def getNodeSecurity(self, homeid, nodeid):
        '''
.. _getNodeSecurity:

Get the security byte for a node.  Bit meanings are still to be determined.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: The node security byte
:rtype: int
:see: getNodeType_, getNodeSpecific_, getNodeGeneric_, getNodeBasic_

        '''
        return self.manager.GetNodeSecurity(homeid, nodeid)

    def getNodeBasic(self, homeid, nodeid):
        '''
.. _getNodeBasic:

Get the basic type of a node.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: The node basic type.
:rtype: int
:see: getNodeType_, getNodeSpecific_, getNodeGeneric_, getNodeSecurity_

        '''
        return self.manager.GetNodeBasic(homeid, nodeid)

    def getNodeGeneric(self, homeid, nodeid):
        '''
.. _getNodeGeneric:

Get the generic type of a node.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: The node generic type.
:rtype: int
:see: getNodeType_, getNodeSpecific_, getNodeBasic_, getNodeSecurity_

        '''
        return self.manager.GetNodeGeneric(homeid, nodeid)

    def getNodeSpecific(self, homeid, nodeid):
        '''
.. _getNodeSpecific:

Get the specific type of a node.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type homeId: int
:return: int -- The node specific type.
:see: getNodeType_, getNodeGeneric_, getNodeBasic_, getNodeSecurity_

        '''
        return self.manager.GetNodeSpecific(homeid, nodeid)

    def getNodeType(self, homeid, nodeid):
        '''
.. _getNodeType:

Get a human-readable label describing the node

The label is taken from the Z-Wave specific, generic or basic type, depending
on which of those values are specified by the node.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: A string containing the label text.
:rtype: str
:see: getNodeSpecific_, getNodeGeneric_, getNodeBasic_, getNodeSecurity_

        '''
        cdef string c_string = self.manager.GetNodeType(homeid, nodeid)
        return cstr_to_str(c_string.c_str())

    def getNodeNeighbors(self, homeid, nodeid):
        '''
.. _getNodeNeighbors:

Get the bitmap of this node's neighbors.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: A set containing neighboring node IDs
:rtype: set()

        '''
        data = set()
        #Allocate memory for the c++ function
        #Return value is pointer to uint8_t[]
        cdef uint8_t** dbuf = <uint8_t**>malloc(sizeof(uint8_t)*29)
        #Get the number of neigbors
        cdef uint32_t count = self.manager.GetNodeNeighbors(homeid, nodeid, dbuf)
        if count == 0:
            #Don't need to allocate memory.
            free(dbuf)
            return data
        #Allocate memory for the returned values
        cdef RetAlloc retuint8 = RetAlloc(count)
        cdef uint8_t* p
        cdef uint32_t start = 0
        if count:
            try:
                p = dbuf[0] # p is now pointing at first element of array
                for i in range(start, count):
                    #cdef uint8_t = retuint8[i]
                    retuint8.data[i] = p[0]
                    data.add(retuint8.data[i])
                    p += 1
            finally:
                #Free memory
                free(dbuf)
                pass
        return data

    def getNodeManufacturerName(self, homeid, nodeid):
        '''
        .. _getNodeManufacturerName:

Get the manufacturer name of a device

The manufacturer name would normally be handled by the Manufacturer Specific
commmand class, taking the manufacturer ID reported by the device and using it
to look up the name from the manufacturer_specific.xml file in the OpenZWave
config folder.  However, there are some devices that do not support the command
class, so to enable the user to manually set the name, it is stored with the
node data and accessed via this method rather than being reported via a command
class Value object.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: A string containing the nodes manufacturer name.
:rtype: str
:see: setNodeManufacturerName_, getNodeProductName_, setNodeProductName_, \
    getNodeManufacturerId_, getNodeProductId_, getNodeProductType_

        '''
        cdef string manufacturer_string = self.manager.GetNodeManufacturerName(homeid, nodeid)
        return cstr_to_str(manufacturer_string.c_str())

    def getNodeProductName(self, homeid, nodeid):
        '''
.. _getNodeProductName:

Get the product name of a device

The product name would normally be handled by the Manufacturer Specific
commmand class, taking the product Type and ID reported by the device and using
it to look up the name from the manufacturer_specific.xml file in the OpenZWave
config folder.  However, there are some devices that do not support the command
class, so to enable the user to manually set the name, it is stored with the
node data and accessed via this method rather than being reported via a command
class Value object.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: str -- A string containing the nodes product name.
:see: setNodeProductName_, getNodeManufacturerName_, setNodeManufacturerName_, \
    getNodeManufacturerId_, getNodeProductId_, getNodeProductType_

        '''
        cdef string productname_string = self.manager.GetNodeProductName(homeid, nodeid)
        return cstr_to_str(productname_string.c_str())

    def getNodeName(self, homeid, nodeid):
        '''
.. _getNodeName:

Get the name of a node

The node name is a user-editable label for the node that would normally be
handled by the Node Naming commmand class, but many devices do not support it.
So that a node can always be named, OpenZWave stores it with the node data, and
provides access through this method and SetNodeName, rather than reporting it
via a command class Value object.  The maximum length of a node name is 16
characters.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: str -- A string containing the node name.
:see: setNodeName_, getNodeLocation_, setNodeLocation_

        '''
        cdef string c_string = self.manager.GetNodeName(homeid, nodeid)
        return cstr_to_str(c_string.c_str())

    def getNodeLocation(self, homeid, nodeid):
        '''
.. _getNodeLocation:

Get the location of a node

The node location is a user-editable string that would normally be handled by
the Node Naming commmand class, but many devices do not support it.  So that a
node can always report its location, OpenZWave stores it with the node data,
and provides access through this method and SetNodeLocation, rather than
reporting it via a command class Value object.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: str -- A string containing the nodes location.
:see: setNodeLocation_, getNodeName_, setNodeName_

        '''
        cdef string c_string = self.manager.GetNodeLocation(homeid, nodeid)
        return cstr_to_str(c_string.c_str())

    def getNodeManufacturerId(self, homeid, nodeid):
        '''
.. _getNodeManufacturerId:

Get the manufacturer ID of a device

The manufacturer ID is a four digit hex code and would normally be handled by
the Manufacturer-Specific commmand class, but not all devices support it.
Although the value reported by this method will be an empty string if the
command class is not supported and cannot be set by the user, the manufacturer
ID is still stored with the node data (rather than being reported via a command
class Value object) to retain a consistent approach with the other manufacturer
specific data.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: A string containing the nodes manufacturer ID, or an empty string if the manufactuer-specific command class is not supported by the device.
:rtype: str
:see: getNodeProductType_, getNodeProductId_, getNodeManufacturerName_, setNodeManufacturerName_, \
    getNodeProductName_, setNodeProductName_

        '''
        cdef string c_string = self.manager.GetNodeManufacturerId(homeid, nodeid)
        return cstr_to_str(c_string.c_str())

    def getNodeProductType(self, homeid, nodeid):
        '''
.. _getNodeProductType:

Get the product type of a device

The product type is a four digit hex code and would normally be handled by the
Manufacturer Specific commmand class, but not all devices support it.  Although
the value reported by this method will be an empty string if the command class
is not supported and cannot be set by the user, the product type is still
stored with the node data (rather than being reported via a command class Value
object) to retain a consistent approach with the other manufacturer specific
data.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: A string containing the nodes product type, or an empty string if the manufactuer-specific command class is not supported by the device.
:rtype: str
:see: getNodeManufacturerId_, getNodeProductId_, getNodeManufacturerName_, setNodeManufacturerName_, \
    getNodeProductName_, setNodeProductName_

        '''
        cdef string c_string = self.manager.GetNodeProductType(homeid, nodeid)
        return cstr_to_str(c_string.c_str())

    def getNodeProductId(self, homeid, nodeid):
        '''
.. _getNodeProductId:

Get the product ID of a device

The product ID is a four digit hex code and would normally be handled by the
Manufacturer-Specific commmand class, but not all devices support it.  Although
the value reported by this method will be an empty string if the command class
is not supported and cannot be set by the user, the product ID is still stored
with the node data (rather than being reported via a command class Value
object)  to retain a consistent approach with the other manufacturer specific
data.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: A string containing the nodes product ID, or an empty string if the manufactuer-specific command class is not supported by the device.
:rtype: str
:see: getNodeManufacturerId_, getNodeProductType_, getNodeManufacturerName_, setNodeManufacturerName_, getNodeProductName_, setNodeProductName_

        '''
        cdef string c_string = self.manager.GetNodeProductId(homeid, nodeid)
        return cstr_to_str(c_string.c_str())

    def setNodeManufacturerName(self, homeid, nodeid, str manufacturerName):
        '''
.. _setNodeManufacturerName:

Set the manufacturer name of a device

The manufacturer name would normally be handled by the Manufacturer Specific
commmand class, taking the manufacturer ID reported by the device and using it
to look up the name from the manufacturer_specific.xml file in the OpenZWave
config folder.  However, there are some devices that do not support the command
class, so to enable the user to manually set the name, it is stored with the
node data and accessed via this method rather than being reported via a command
class Value object.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:param manufacturerName: A string containing the nodess manufacturer name.
:type manufacturerName: str
:see: getNodeManufacturerName_, getNodeProductName_, setNodeProductName_

        '''
        self.manager.SetNodeManufacturerName(
            homeid, nodeid, str_to_cppstr(manufacturerName))

    def setNodeProductName(self, homeid, nodeid, str productName):
        '''
.. _setNodeProductName:

Set the product name of a device

The product name would normally be handled by the Manufacturer Specific
commmand class, taking the product Type and ID reported by the device and using
it to look up the name from the manufacturer_specific.xml file in the OpenZWave
config folder.  However, there are some devices that do not support the command
class, so to enable the user to manually set the name, it is stored with the
node data and accessed via this method rather than being reported via a command
class Value object.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:param productName: A string containing the nodes product name.
:type productName: str
:see: getNodeProductName_, getNodeManufacturerName_, setNodeManufacturerName_

        '''
        self.manager.SetNodeProductName(homeid, nodeid, str_to_cppstr(productName))

    def setNodeName(self, homeid, nodeid, str name):
        '''
.. _setNodeName:

Set the name of a node

The node name is a user-editable label for the node that would normally be
handled by the Node Naming commmand class, but many devices do not support it.
So that a node can always be named, OpenZWave stores it with the node data, and
provides access through this method and GetNodeName, rather than reporting it
via a command class Value object.  If the device does support the Node Naming
command class, the new name will be sent to the node.  The maximum length of a
node name is 16 characters.

:param homeI: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:param nodeName: A string containing the nodes name.
:type nodeName: str
:see: getNodeName_, getNodeLocation_, setNodeLocation_

        '''
        self.manager.SetNodeName(homeid, nodeid, str_to_cppstr(name))

    def setNodeLocation(self, homeid, nodeid, str location):
        '''
.. _setNodeLocation:

Set the location of a node

The node location is a user-editable string that would normally be handled by
the Node Naming commmand class, but many devices do not support it.  So that a
node can always report its location, OpenZWave stores it with the node data,
and provides access through this method and GetNodeLocation, rather than
reporting it via a command class Value object.  If the device does support the
Node Naming command class, the new location will be sent to the node.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:param location: A string containing the nodes location.
:type location: int
:see: getNodeLocation_, getNodeName_, setNodeName_

        '''
        self.manager.SetNodeLocation(homeid, nodeid, str_to_cppstr(location))

    def setNodeOn(self, homeid, nodeid):
        '''
.. _setNodeOn:

Turns a node on

This is a helper method to simplify basic control of a node.  It is the
equivalent of changing the level reported by the nodes Basic command class to
255, and will generate a ValueChanged notification from that class.  This
command will turn on the device at its last known level, if supported by the
device, otherwise it will turn it on at 100%.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to be changed.
:type nodeId: int
:see: setNodeOff_, setNodeLevel_

        '''

        self.manager.SetNodeOn(homeid, nodeid)

    def setNodeOff(self, homeid, nodeid):
        '''
.. _setNodeOff:

Turns a node off

This is a helper method to simplify basic control of a node.  It is the
equivalent of changing the level reported by the nodes Basic command class to
zero, and will generate a ValueChanged notification from that class.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to be changed.
:type nodeId: int
:see: setNodeOn_, setNodeLevel_

        '''
        self.manager.SetNodeOff(homeid, nodeid)

    def setNodeLevel(self, homeid, nodeid, level):
        '''
.. _setNodeLevel:

Sets the basic level of a node

This is a helper method to simplify basic control of a node.  It is the
equivalent of changing the value reported by the nodes Basic command class
and will generate a ValueChanged notification from that class.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to be changed.
:type nodeId: int
:param level: The level to set the node.  Valid values are 0-99 and 255.  Zero is off and 99 is fully on.  255 will turn on the device at its last known level (if supported).
:type level: int
:see: setNodeOn_, setNodeOff_

        '''
        self.manager.SetNodeLevel(homeid, nodeid, level)

    def isNodeInfoReceived(self, homeid, nodeid):
        '''
.. _isNodeInfoReceived:

Get whether the node information has been received

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: bool -- True if the node information has been received yet

        '''
        return self.manager.IsNodeInfoReceived(homeid, nodeid)

    def getNodeRole(self, homeid, nodeid):
        '''
.. _getNodeRole:

Get the node role as reported in the Z-Wave+ Info report.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: The node version number
:rtype: int

        '''
        return self.manager.GetNodeRole(homeid, nodeid)

    def getNodeRoleString(self, homeId, nodeId):
        '''
.. getNodeRoleString:

Get the node role (string) as reported in the Z-Wave+ Info report.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: name of current query stage as a string.
:rtype: str

        '''
        cdef string c_string = self.manager.GetNodeRoleString(homeId, nodeId)
        return cstr_to_str(c_string.c_str())

    def getNodeDeviceType(self, homeid, nodeid):
        '''
.. _getNodeDeviceType:

Get the node DeviceType as reported in the Z-Wave+ Info report.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: The node version number
:rtype: int

        '''
        return self.manager.GetNodeDeviceType(homeid, nodeid)

    def getNodeDeviceTypeString(self, homeId, nodeId):
        '''
.. getNodeRoleString:

Get the node DeviceType (string) as reported in the Z-Wave+ Info report.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: name of current query stage as a string.
:rtype: str

        '''
        cdef string c_string = self.manager.GetNodeDeviceTypeString(homeId, nodeId)
        return cstr_to_str(c_string.c_str())

    def getNodePlusType(self, homeid, nodeid):
        '''
.. _getNodePlusType:

Get the node plus type as reported in the Z-Wave+ Info report.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: The node version number
:rtype: int

        '''
        return self.manager.GetNodePlusType(homeid, nodeid)

    def getNodePlusTypeString(self, homeId, nodeId):
        '''
.. getNodePlusTypeString:

Get the node plus type (string) as reported in the Z-Wave+ Info report.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: name of current query stage as a string.
:rtype: str

        '''
        cdef string c_string = self.manager.GetNodePlusTypeString(homeId, nodeId)
        return cstr_to_str(c_string.c_str())

    def getNodeClassInformation(self, homeid, nodeid, commandClassId, className = None, classVersion = None):
        '''
.. _getNodeClassInformation:

Helper method to return whether a particular class is available in a node

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:param commandClassId: control class to query
:type commandClassId: int
:param className: (optional, default=None) specific name of class to query
:type className: str
:param classVersion: (optional, default=None) specific class version
:type classVersion: int
:return: True if the node does have the class instantiated, will return name & version
:rtype: bool

        '''
        cdef string oclassName
        cdef uint8_t oclassVersion
        ret=self.manager.GetNodeClassInformation(homeid, nodeid, commandClassId, &oclassName, &oclassVersion)
        if ret :
            className = oclassName.c_str()
            classVersion = oclassVersion
            return ret
        else :
            return False


    def isNodeAwake(self, homeId, nodeId):
        '''
.. _isNodeAwake: Get whether the node is awake or asleep

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: True if the node is awake.
:rtype: bool

        '''
        return self.manager.IsNodeAwake(homeId, nodeId)


    def isNodeFailed(self, homeId, nodeId):
        '''
.. isNodeFailed:

Get whether the node is working or has failed

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: True if the node has failed and is no longer part of the network.
:rtype: bool

        '''
        return self.manager.IsNodeFailed(homeId, nodeId)


    def isNodeZWavePlus(self, homeId, nodeId):
        '''
.. isNodeZWavePlus:

Get whether the node is a ZWave+ one

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: True if the node has failed and is no longer part of the network.
:rtype: bool

        '''
        return self.manager.IsNodeZWavePlus(homeId, nodeId)


    def getNodeQueryStage(self, homeId, nodeId):
        '''
.. getNodeQueryStage: Get whether the node's query stage as a string

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: name of current query stage as a string.
:rtype: str

        '''
        cdef string c_string = self.manager.GetNodeQueryStage(homeId, nodeId)
        return cstr_to_str(c_string.c_str())


    def getNodeQueryStageCode(self, queryStage):
        '''
.. getNodeQueryStageCode: Get code value from a query stage description

:param queryStage: The query stage description.
:type queryStage: str
:return: code value.
:rtype: int

        '''
        if queryStage == "ProtocolInfo":
            # Retrieve protocol information
            # QueryStage_ProtocolInfo
            return 0
        elif queryStage == "Probe":
            # Ping device to see if alive
            # QueryStage_Probe
            return 1
        elif queryStage == "WakeUp":
            # Start wake up process if a sleeping node
            # QueryStage_WakeUp
            return 2
        elif queryStage == "ManufacturerSpecific1":
            # Retrieve manufacturer name and product ids if ProtocolInfo lets us
            # QueryStage_ManufacturerSpecific1
            return 3
        elif queryStage == "NodeInfo":
            # Retrieve info about supported, controlled command classes
            # QueryStage_NodeInfo
            return 4
        elif queryStage == "ManufacturerSpecific2":
            # Retrieve manufacturer name and product ids
            # QueryStage_ManufacturerSpecific2
            return 5
        elif queryStage == "Versions":
            # Retrieve version information
            # QueryStage_Versions
            return 6
        elif queryStage == "Instances":
            # Retrieve information about multiple command class instances
            # QueryStage_Instances
            return 7
        elif queryStage == "Static":
            # Retrieve static information (doesn't change)
            # QueryStage_Static
            return 8
        elif queryStage == "Probe1":
            # Ping a device upon starting with configuration
            # QueryStage_Probe1
            return 9
        elif queryStage == "Associations":
            # Retrieve information about associations
            # QueryStage_Associations
            return 10
        elif queryStage == "Neighbors":
            # Retrieve node neighbor list
            # QueryStage_Neighbors
            return 11
        elif queryStage == "Session":
            # Retrieve session information (changes infrequently)
            # QueryStage_Session
            return 12
        elif queryStage == "Dynamic":
            # Retrieve dynamic information (changes frequently)
            # QueryStage_Dynamic
            return 13
        elif queryStage == "Configuration":
            # Retrieve configurable parameter information (only done on request)
            # QueryStage_Configuration
            return 14
        elif queryStage == "Complete":
            # Query process is completed for this node
            # QueryStage_Complete
            return 15
        elif queryStage == "None":
            # Query process hasn't started for this node
            # QueryStage_None
            return 16
        return None

#
# -----------------------------------------------------------------------------
# Values
# -----------------------------------------------------------------------------
# Methods for accessing device values.  All the methods require a ValueID, which will have been provided
# in the ValueAdded Notification callback when the the value was first discovered by OpenZWave.
#        bool SetValue(ValueID& valueid, uint8_t value)
#        bool SetValue(ValueID& valueid, float value)
#        bool SetValue(ValueID& valueid, uint16 value)
#        bool SetValue(ValueID& valueid, uint32_t value)
#        bool SetValue(ValueID& valueid, string value)
#        bool SetValueListSelection(ValueID& valueid, string selecteditem)

    def setValue(self, id, value):
        '''
.. _setValue:

Sets the value of a device valueid.
Due to the possibility of a device being asleep, the command is assumed to suceeed, and the value
held by the node is updated directly.  This will be reverted by a future status message from the device
if the Z-Wave message actually failed to get through.  Notification callbacks will be sent in both cases.

:param id: The ID of a value.
:type id: int
:param value: The value to set.
:type value: int
:return: An integer representing the result of the operation  0 : The C method fails, 1 : The C method succeed, 2 : Can't find id in the map
:rtype: int

        '''
        cdef float type_float
        cdef bool type_bool
        cdef uint8_t type_byte
        cdef int32_t type_int
        cdef int16_t type_short
        cdef string type_string
        cdef uint8_t* type_raw
        ret = 2
        if values_map.find(id) != values_map.end():
            datatype = PyValueTypes[values_map.at(id).GetType()]
            if datatype == "Bool":
                type_bool = value
                cret = self.manager.SetValue(values_map.at(id), type_bool)
                ret = 1 if cret else 0
            elif datatype == "Byte":
                type_byte = value
                cret = self.manager.SetValue(values_map.at(id), type_byte)
                ret = 1 if cret else 0
            elif datatype == "Raw":
                type_raw = <uint8_t*> malloc(len(value)*sizeof(uint8_t))
                for x in range(0, len(value)):
                    #print value[x]
                    type_raw[x] = ord(value[x])
                cret = self.manager.SetValue(values_map.at(id), type_raw, len(value))
                ret = 1 if cret else 0
                free(type_raw)
            elif datatype == "Decimal":
                type_float = value
                cret = self.manager.SetValue(values_map.at(id), type_float)
                ret = 1 if cret else 0
            elif datatype == "Int":
                type_int = value
                cret = self.manager.SetValue(values_map.at(id), type_int)
                ret = 1 if cret else 0
            elif datatype == "Short":
                type_short = value
                cret = self.manager.SetValue(values_map.at(id), type_short)
                ret = 1 if cret else 0
            elif datatype == "String":
                if six.PY3:
                    type_string = str_to_cppstr(value)
                else:
                    type_string = str_to_cppstr(string(value))
                cret = self.manager.SetValue(values_map.at(id), type_string)
                ret = 1 if cret else 0
            elif datatype == "Button":
                type_bool = value
                cret = self.manager.SetValue(values_map.at(id), type_bool)
                ret = 1 if cret else 0
            elif datatype == "List":
                logger.debug("SetValueListSelection %s", value)
                if six.PY3:
                    type_string = str_to_cppstr(value)
                else:
                    type_string = str_to_cppstr(string(value))
                cret = self.manager.SetValueListSelection(values_map.at(id), type_string)
                logger.debug("SetValueListSelection %s", cret)
                ret = 1 if cret else 0
        return ret

    def refreshValue(self, id):
        '''
.. _refreshValue:

Refreshes the specified value from the Z-Wave network.
A call to this function causes the library to send a message to the network to retrieve the current value
of the specified ValueID (just like a poll, except only one-time, not recurring).

:param id: The unique identifier of the value to be refreshed.
:type id: int
:return: bool -- True if the driver and node were found; false otherwise

        '''
        return self.manager.RefreshValue(values_map.at(id))

    def getValueLabel(self, id):
        '''
.. _getValueLabel:

Gets the user-friendly label for the value

:param id: The ID of a value.
:type id: int
:return: A string containing the user-friendly label of the value
:rtype: str
:see: setValueLabel_

       '''
        cdef string c_string
        if values_map.find(id) != values_map.end():
            c_string = self.manager.GetValueLabel(values_map.at(id))
            return cstr_to_str(c_string.c_str())
        else :
            return None

    def setValueLabel(self, id, str label):
        '''
.. _setValueLabel:

Sets the user-friendly label for the value

:param id: The ID of a value.
:type id: int
:param label: The label of the value.
:type label: str
:see: getValueLabel_

        '''
        if values_map.find(id) != values_map.end():
            self.manager.SetValueLabel(values_map.at(id), str_to_cppstr(label))

    def getValueUnits(self, id):
        '''
.. _getValueUnits:

Gets the units that the value is measured in.

:param id: The ID of a value.
:type id: int
:return: A string containing the value of the units.
:rtype: str
:see: setValueUnits_

        '''
        cdef string c_string
        if values_map.find(id) != values_map.end():
            c_string = self.manager.GetValueUnits(values_map.at(id))
            return cstr_to_str(c_string.c_str())
        else :
            return None

    def setValueUnits(self, id, str unit):
        '''
.. _setValueUnits:

Sets the units that the value is measured in.

:param id: The ID of a value.
:type id: int
:param label: The new value of the units.
:type label: str
:see: getValueUnits_

        '''
        if values_map.find(id) != values_map.end():
            self.manager.SetValueUnits(values_map.at(id), str_to_cppstr(unit))

    def getValueHelp(self, id):
        '''
.. _getValueHelp:

Gets a help string describing the value's purpose and usage.

:param id: The ID of a value.
:type id: int
:return: A string containing the value help text.
:rtype: str
:see: setValueHelp_

        '''
        cdef string c_string
        if values_map.find(id) != values_map.end():
            c_string = self.manager.GetValueHelp(values_map.at(id))
            return cstr_to_str(c_string.c_str())
        else :
            return None

    def setValueHelp(self, id, str help):
        '''
.. _setValueHelp:

Sets a help string describing the value's purpose and usage.

:param id: the ID of a value.
:type id: int
:param help: The new value of the help text.
:type help: str
:see: getValueHelp_

        '''
        if values_map.find(id) != values_map.end():
            self.manager.SetValueHelp(values_map.at(id), str_to_cppstr(help))

    def getValueMin(self, id):
        '''
.. _getValueMin:

Gets the minimum that this value may contain.

:param id: The ID of a value.
:type id: int
:return: The value minimum.
:rtype: int
:see: getValueMax_

        '''
        if values_map.find(id) != values_map.end():
            return self.manager.GetValueMin(values_map.at(id))
        else :
            return None

    def getValueMax(self, id):
        '''
.. _getValueMax:

Gets the maximum that this value may contain.

:param id: The ID of a value.
:type id: int
:return: The value maximum.
:rtype: int
:see: getValueMin_

        '''
        if values_map.find(id) != values_map.end():
            return self.manager.GetValueMax(values_map.at(id))
        else :
            return None

    def isValueReadOnly(self, id):
        '''
.. _isValueReadOnly:

Test whether the value is read-only.

:param id: The ID of a value.
:type id: int
:return: True if the value cannot be changed by the user.
:rtype: bool
:see: isValueWriteOnly_

        '''
        if values_map.find(id) != values_map.end():
            return self.manager.IsValueReadOnly(values_map.at(id))
        else :
            return None

    def isValueWriteOnly(self, id):
        '''
.. _isValueWriteOnly:

Test whether the value is write-only.

:param id: The ID of a value.
:type id: int
:return: True if the value can only be written to and not read.
:rtype: bool
:see: isValueReadOnly_

        '''
        if values_map.find(id) != values_map.end():
            return self.manager.IsValueWriteOnly(values_map.at(id))
        else :
            return None

    def isValueSet(self, id):
        '''
.. _isValueSet:

Test whether the value has been set.

:param id: the ID of a value.
:type id: int
:return: True if the value has actually been set by a status message from the device, rather than simply being the default.
:rtype: bool
:see: getValue_, getValueAsBool_, getValueAsByte_, getValueListItems_, \
getValueAsFloat_, getValueAsShort_, getValueAsInt_, getValueAsString_, \
getValueType_, getValueInstance_, getValueIndex_

        '''
        if values_map.find(id) != values_map.end():
            return self.manager.IsValueSet(values_map.at(id))
        else :
            return None

    def isValuePolled(self, id):
        '''
.. _isValuePolled:

Test whether the value is currently being polled.

:param id: the ID of a value.
:type id: int
:return: True if the value is being polled, otherwise false.
:rtype: bool

        '''
        if values_map.find(id) != values_map.end():
            return self.manager.IsValuePolled(values_map.at(id))
        else :
            return None

    def getValueGenre(self, id):
        '''
.. _getValueGenre:

Get the genre of the value.  The genre classifies a value to enable
low-level system or configuration parameters to be filtered out
by the application

:param id: The ID of a value.
:type id: int
:return: A string containing the type of the value
:rtype: str
:see: isValueSet_, getValueAsBool_, getValueAsByte_, getValueListItems_, \
getValueListSelectionStr_ , getValueListSelectionNum_, \
getValueAsFloat_, getValueAsShort_, getValueAsInt_, getValueCommandClass_,\
getValueAsString_, getValue_, getValueType_, getValueInstance_, getValueIndex_

       '''
        if values_map.find(id) != values_map.end():
            genre = PyGenres[values_map.at(id).GetGenre()]
            return genre
        else :
            return None

    def getValueCommandClass(self, id):
        '''
.. _getValueCommandClass:

Get the command class instance of this value.  It is possible for there to be
multiple instances of a command class, although currently it appears that
only the SensorMultilevel command class ever does this.  Knowledge of
instances and command classes is not required to use OpenZWave, but this
information is exposed in case it is of interest.


:param id: The ID of a value.
:type id: int
:return: The command class of the value
:rtype: int
:see: isValueSet_, getValueAsBool_, getValueAsByte_, getValueListItems_, \
getValueListSelectionStr_ , getValueListSelectionNum_, \
getValueAsFloat_, getValueAsShort_, getValueAsInt_, getValueGenre_, \
getValueAsString_, getValue_, getValueType_, getValueInstance_, getValueIndex_

       '''
        if values_map.find(id) != values_map.end():
            cmd_cls = values_map.at(id).GetCommandClassId()
            return cmd_cls
        else :
            return None

    def getValueInstance(self, id):
        '''
.. _getValueInstance:

Get the command class instance of this value.  It is possible for there to be
multiple instances of a command class, although currently it appears that
only the SensorMultilevel command class ever does this.

:param id: The ID of a value.
:type id: int
:return: A string containing the type of the value
:rtype: str
:see: isValueSet_, getValueAsBool_, getValueAsByte_, getValueListItems_, \
getValueListSelectionStr_ , getValueListSelectionNum_, \
getValueAsFloat_, getValueAsShort_, getValueAsInt_, getValueCommandClass_, \
getValueAsString_, getValue_, getValueType_, getValueIndex_

       '''
        if values_map.find(id) != values_map.end():
            genre = values_map.at(id).GetInstance()
            return genre
        else :
            return None

    def getValueIndex(self, id):
        '''
.. _getValueIndex:

Get the value index.  The index is used to identify one of multiple
values created and managed by a command class.  In the case of configurable
parameters (handled by the configuration command class), the index is the
same as the parameter ID.

:param id: The ID of a value.
:type id: int
:return: A string containing the type of the value
:rtype: str
:see: isValueSet_, getValueAsBool_, getValueAsByte_, getValueListItems_, \
getValueListSelectionStr_ , getValueListSelectionNum_, \
getValueAsFloat_, getValueAsShort_, getValueAsInt_, getValueCommandClass_, \
getValueAsString_, getValue_, getValueType_

       '''
        if values_map.find(id) != values_map.end():
            genre = values_map.at(id).GetIndex()
            return genre
        else :
            return None

    def getValueType(self, id):
        '''
.. _getValueType:

Gets the type of the value

:param id: The ID of a value.
:type id: int
:return: A string containing the type of the value
:rtype: str
:see: isValueSet_, getValueAsBool_, getValueAsByte_, getValueListItems_, \
getValueListSelectionStr_ , getValueListSelectionNum_, \
getValueAsFloat_, getValueAsShort_, getValueAsInt_, getValueAsString_, \
getValue_, getValueInstance_, getValueIndex_, getValueCommandClass_

       '''
        if values_map.find(id) != values_map.end():
            datatype = PyValueTypes[values_map.at(id).GetType()]
            return datatype
        else :
            return None

    def getValue(self, id):
        '''
.. _getValue:

Gets a value.

:param id: The ID of a value.
:type id: int
:param value: The value to set.
:type value: int
:return: Depending of the type of the valueId, None otherwise
:rtype: variable
:see: isValueSet_, getValueAsBool_, getValueAsByte_, getValueListItems_, \
getValueListSelectionStr_ , getValueListSelectionNum_, \
getValueAsFloat_, getValueAsShort_, getValueAsInt_, getValueAsString_, \
getValueType_, getValueInstance_, getValueIndex_, getValueCommandClass_

        '''
        return getValueFromType(self.manager,id)

    def getValueAsBool(self, id):
        '''
.. _getValueAsBool:

Gets a value as a bool.

:param id: The ID of a value.
:type id: int
:return: The value
:rtype: bool
:see: isValueSet_, getValue_, getValueAsByte_, getValueListItems_, \
getValueListSelectionStr_ , getValueListSelectionNum_, \
getValueAsFloat_, getValueAsShort_, getValueAsInt_, getValueAsString_, \
getValueType_, getValueInstance_, getValueIndex_, getValueCommandClass_

        '''
        return getValueFromType(self.manager,id)

    def getValueAsByte(self, id):
        '''
.. _getValueAsByte:

Gets a value as an 8-bit unsigned integer.

:param id: The ID of a value.
:type id: int
:return: The value
:rtype: int
:see: isValueSet_, getValue_, getValueAsBool_, getValueListItems_, \
getValueListSelectionStr_ , getValueListSelectionNum_, \
getValueAsFloat_, getValueAsShort_, getValueAsInt_, getValueAsString_, \
getValueType_, getValueInstance_, getValueIndex_, getValueCommandClass_

        '''
        return getValueFromType(self.manager,id)

    def getValueAsFloat(self, id):
        '''
.. _getValueAsFloat:

Gets a value as a float.

:param id: The ID of a value.
:type id: int
:return: The value
:rtype: float
:see: isValueSet_, getValue_, getValueAsBool_, getValueAsByte_, \
getValueListSelectionStr_ , getValueListSelectionNum_, \
getValueAsShort_, getValueAsInt_, getValueAsString_, getValueListItems_, \
getValueType_, getValueInstance_, getValueIndex_

        '''
        return getValueFromType(self.manager,id)

    def getValueAsShort(self, id):
        '''
.. _getValueAsShort:

Gets a value as a 16-bit signed integer.

:param id: The ID of a value.
:type id: int
:return: The value
:rtype: int
:see: isValueSet_, getValue_, getValueAsBool_, getValueAsByte_, \
getValueListSelectionStr_ , getValueListSelectionNum_, \
getValueAsFloat_, getValueAsInt_, getValueAsString_, getValueListItems_, \
getValueType_, getValueInstance_, getValueIndex_

        '''
        return getValueFromType(self.manager,id)

    def getValueAsInt(self, id):
        '''
.. _getValueAsInt:

Gets a value as a 32-bit signed integer.

:param id: The ID of a value.
:type id: int
:return: The value
:rtype: int
:see: isValueSet_, getValue_, getValueAsBool_, getValueAsByte_, \
getValueListSelectionStr_ , getValueListSelectionNum_, \
getValueAsFloat_, getValueAsShort_, getValueAsString_, getValueListItems_, \
getValueType_, getValueInstance_, getValueIndex_

        '''
        return getValueFromType(self.manager,id)

    def getValueAsString(self, id):
        '''
.. _getValueAsString:

Gets a value as a string.

:param id: The ID of a value.
:type id: int
:return: The value
:rtype: str
:see: isValueSet_, getValue_, getValueAsBool_, getValueAsByte_, \
getValueListSelectionStr_ , getValueListSelectionNum_, \
getValueAsFloat_, getValueAsShort_, getValueAsInt_, getValueListItems_, \
getValueType_, getValueInstance_, getValueIndex_

        '''
        return getValueFromType(self.manager,id)

    def getValueAsRaw(self, id):
        '''
.. _getValueAsRaw:

Gets a value as raw.

:param id: The ID of a value.
:type id: int
:return: The value
:rtype: str
:see: isValueSet_, getValue_, getValueAsBool_, getValueAsByte_, \
getValueListSelectionStr_ , getValueListSelectionNum_, \
getValueAsFloat_, getValueAsShort_, getValueAsInt_, getValueListItems_, \
getValueType_, getValueInstance_, getValueIndex_

        '''
        return getValueFromType(self.manager,id)

    def getValueListSelectionStr(self,  id):
        '''
.. _getValueListSelectionStr:

Gets value of items from a list value

:param id: The ID of a value.
:type id: int
:return: The value
:rtype: str
:see: isValueSet_, getValue_, getValueAsBool_, getValueAsByte_, \
getValueListSelectionNum_, getValueListItems_,\
getValueAsFloat_, getValueAsShort_, getValueAsInt_, getValueAsString_, \
getValueType_, getValueInstance_, getValueIndex_
    '''
        return getValueFromType(self.manager,id)

    def getValueListSelectionNum(self,  id):
        '''
.. _getValueListSelectionNum:

Gets value of items from a list value

:param id: The ID of a value.
:type id: int
:return: The value
:rtype: int
:see: isValueSet_, getValue_, getValueAsBool_, getValueAsByte_, \
getValueListSelectionStr_, getValueListItems_,\
getValueAsFloat_, getValueAsShort_, getValueAsInt_, getValueAsString_, \
getValueType_, getValueInstance_, getValueIndex_
    '''
        cdef int32_t type_int
        ret=-1
        if values_map.find(id) != values_map.end():
            if self.manager.GetValueListSelection(values_map.at(id), &type_int):
                ret = type_int
        #print "//////// Value Num list item : " ,  ret
        return ret

    def getValueListItems(self, id):
        '''
.. _getValueListItems:

Gets the list of items from a list value

:param id: The ID of a value.
:type id: int
:return: The list of possible values
:rtype: set()
:see: isValueSet_, getValue_, getValueAsBool_, getValueAsByte_, \
getValueListSelectionStr_ , getValueListSelectionNum_ \
getValueAsFloat_, getValueAsShort_, getValueAsInt_, getValueAsString_, \
getValueType_, getValueInstance_, getValueIndex_

        '''
        cdef vector[string] vect
        ret = set()
        if values_map.find(id) != values_map.end():
            if self.manager.GetValueListItems(values_map.at(id), &vect):
                while not vect.empty() :
                    temp = vect.back()
                    ret.add(temp.c_str())
                    vect.pop_back();
        return ret

    def getValueListValues(self, id):
        '''
.. _getValueListValues:

Gets the list of values from a list value.

:param id: The ID of a value.
:type id: int
:return: The list of values
:rtype: set()
:see: isValueSet_, getValue_, getValueAsBool_, getValueAsByte_, \
getValueListSelectionStr_ , getValueListSelectionNum_ \
getValueAsFloat_, getValueAsShort_, getValueAsInt_, getValueAsString_, \
getValueType_, getValueInstance_, getValueIndex_

        '''
        cdef vector[int32_t] vect
        ret = set()
        if values_map.find(id) != values_map.end():
            if self.manager.GetValueListValues(values_map.at(id), &vect):
                while not vect.empty() :
                    temp = vect.back()
                    ret.add(temp)
                    vect.pop_back();
        return ret

    def pressButton(self, id):
        '''
.. _pressButton:

Starts an activity in a device.
Since buttons are write-only values that do not report a state,
no notification callbacks are sent.

:param id: The ID of an integer value.
:type id: int
:return: True if the activity was started. Returns false if the value is not a ValueID::ValueType_Button. The type can be tested with a call to ValueID::GetType.
:rtype: bool
:see: releaseButton_

        '''
        if values_map.find(id) != values_map.end():
            return self.manager.PressButton(values_map.at(id))
        else :
            return False

    def releaseButton(self, id):
        '''
.. _releaseButton:

Stops an activity in a device.
Since buttons are write-only values that do not report a state,
no notification callbacks are sent.

:param id: the ID of an integer value.
:type id: int
:return: True if the activity was stopped. Returns false if the value is not a ValueID::ValueType_Button. The type can be tested with a call to ValueID::GetType.
:rtype: bool
:see: pressButton_

        '''
        if values_map.find(id) != values_map.end():
            return self.manager.ReleaseButton(values_map.at(id))
        else :
            return False


    def getValueFloatPrecision(self, id):
        '''
.. _getValueFloatPrecision: Gets a float value's precision

:param id: The unique identifier of the value.
:type id: int
:return: a float value's precision.
:rtype: int

        '''
        cdef uint8_t precision
        if values_map.find(id) != values_map.end():
            success = self.manager.GetValueFloatPrecision(values_map.at(id), &precision)
            return precision if success else None
        return None

    def getChangeVerified(self, id):
        '''
.. _getChangeVerified: determine if value changes upon a refresh should be verified.

If so, the library will immediately refresh the value a second time whenever a change is observed.
This helps to filter out spurious data reported occasionally by some devices.

:param id:  The unique identifier of the value whose changes should or should not be verified.
:type id: int
:return: True if is verified.
:rtype: bool

        '''

        if values_map.find(id) != values_map.end():
            return self.manager.GetChangeVerified(values_map.at(id))
        return False

    def setChangeVerified(self, id, verify ):
        '''
.. _setChangeVerified: Sets a flag indicating whether value changes noted upon a refresh should be verified.

If so, the library will immediately refresh the value a second time whenever a change is observed. This helps to filter out spurious data reported occasionally by some devices.

:param id: The unique identifier of the value whose changes should or should not be verified.
:type id: int
:param verify: if true, verify changes; if false, don't verify changes
:type verify: bool

        '''

        if values_map.find(id) != values_map.end():
            self.manager.SetChangeVerified(values_map.at(id), verify)

#
# -----------------------------------------------------------------------------
# Climate Control Schedules
# -----------------------------------------------------------------------------
# Methods for accessing schedule values.  All the methods require a ValueID, which will have been provided
# in the ValueAdded Notification callback when the the value was first discovered by OpenZWave.
# The ValueType_Schedule is a specialized Value used to simplify access to the switch point schedule
# information held by a setback thermostat that supports the Climate Control Schedule command class.
# Each schedule contains up to nine switch points for a single day, consisting of a time in
# hours and minutes (24 hour clock) and a setback in tenths of a degree Celsius.  The setback value can
# range from -128 (-12.8C) to 120 (12.0C).  There are two special setback values - 121 is used to set
# Frost Protection mode, and 122 is used to set Energy Saving mode.
# The switch point methods only modify OpenZWave's copy of the schedule information.  Once all changes
# have been made, they are sent to the device by calling SetSchedule.
#
    def setSwitchPoint(self, id, hours, minutes, setback):
        '''
.. _setSwitchPoint:

Set a switch point in the schedule.

:param id: The unique identifier of the schedule value.
:type id: int
:param hours: The hours part of the time when the switch point will trigger. The time is set using the 24-hour clock, so this value must be between 0 and 23.
:type hours: int
:param minutes: The minutes part of the time when the switch point will trigger.  This value must be between 0 and 59.
:type minutes: int
:param setback: The setback in tenths of a degree Celsius.  The setback value can range from -128 (-12.8C) to 120 (12.0C).  There are two special setback values - 121 is used to set Frost Protection mode, and 122 is used to set Energy Saving mode.
:type setback: int
:return: True if the switch point is set.
:rtype: bool
:see: removeSwitchPoint_, clearSwitchPoints_, getSwitchPoint_, getNumSwitchPoints_

        '''
        if values_map.find(id) != values_map.end():
            return self.manager.SetSwitchPoint(values_map.at(id), hours, minutes, setback)
        else :
            return False

    def removeSwitchPoint(self, id, hours, minutes):
        '''
.. _removeSwitchPoint:

Remove a switch point from the schedule

:param id: The unique identifier of the schedule value.
:type id: int
:param hours: The hours part of the time when the switch point will trigger.  The time is set using the 24-hour clock, so this value must be between 0 and 23.
:type hours: int
:param minutes: The minutes part of the time when the switch point will trigger.  This value must be between 0 and 59.
:type minutes: int
:return: True if the switch point is removed.
:rtype: bool
:see: setSwitchPoint_, clearSwitchPoints_, getSwitchPoint_, getNumSwitchPoints_

        '''
        if values_map.find(id) != values_map.end():
            return self.manager.RemoveSwitchPoint(values_map.at(id), hours, minutes)
        else :
            return False

    def clearSwitchPoints(self, id):
        '''
.. _clearSwitchPoints:

Clears all switch points from the schedule

:param id: The unique identifier of the schedule value.
:type id: int
:return: True if all switch points are clear.
:rtype: bool
:see: setSwitchPoint_, removeSwitchPoint_, getSwitchPoint_, getNumSwitchPoints_

        '''
        if values_map.find(id) != values_map.end():
            self.manager.ClearSwitchPoints(values_map.at(id))

    def getSwitchPoint(self, id, idx, hours, minutes, setback):
        '''
.. _getSwitchPoint:

Gets switch point data from the schedule

:param id: The unique identifier of the schedule value.
:type id: int
:param idx: The index of the switch point, between zero and one less than the value returned by GetNumSwitchPoints.
:type idx: int
:param hours: An integer that will be filled with the hours part of the switch point data.
:type hours: int
:param minutes: An integer that will be filled with the minutes part of the switch point data.
:type minutes: int
:param setback: An integer that will be filled with the setback value.  This can range from -128 (-12.8C)to 120 (12.0C).  There are two special setback values - 121 is used to set Frost Protection mode, and 122 is used to set Energy Saving mode.
:type setback: int
:return: True if successful.  Returns False if the value is not a ValueID::ValueType_Schedule. The type can be tested with a call to ValueID::GetType.
:rtype: bool
:see: setSwitchPoint_, removeSwitchPoint_, clearSwitchPoints_, getNumSwitchPoints_

        '''
        cdef uint8_t ohours
        cdef uint8_t ominutes
        cdef int8_t osetback
        if values_map.find(id) != values_map.end():
            ret=self.manager.GetSwitchPoint(values_map.at(id), idx, \
                &ohours, &ominutes, &osetback)
            if ret :
                hours = ohours
                minutes = ominutes
                setback = osetback
            return ret
        else :
            return False
#        return False

    def getNumSwitchPoints(self, id):
        '''
.. _getNumSwitchPoints:

Get the number of switch points defined in a schedule

:param id: The unique identifier of the schedule value.
:type id: int
:return: The number of switch points defined in this schedule.  Returns zero if the value is not a ValueID::ValueType_Schedule. The type can be tested with a call to ValueID::GetType.
:rtype: int
:see: setSwitchPoint_, removeSwitchPoint_, clearSwitchPoints_, getSwitchPoint_

        '''
        if values_map.find(id) != values_map.end():
            return self.manager.GetNumSwitchPoints(values_map.at(id))
        else :
            return 0

#
# -----------------------------------------------------------------------------
# SwitchAll
# -----------------------------------------------------------------------------
# Methods for switching all devices on or off together.  The devices must support
# the SwitchAll command class.  The command is first broadcast to all nodes, and
# then followed up with individual commands to each node (because broadcasts are
# not routed, the message might not otherwise reach all the nodes).
#
    def switchAllOn(self, homeid):
        '''
.. _switchAllOn:

Switch all devices on.  All devices that support the SwitchAll command class
will be turned on.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:see: switchAllOff_

        '''
        self.manager.SwitchAllOn(homeid)

    def switchAllOff(self, homeid):
        '''
.. _switchAllOff:

Switch all devices off.  All devices that support the SwitchAll command class
will be turned off.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:see: switchAllOn_

        '''
        self.manager.SwitchAllOff(homeid)

# -----------------------------------------------------------------------------
# Configuration Parameters
# -----------------------------------------------------------------------------
# Methods for accessing device configuration parameters.  Configuration parameters are values
# that are managed by the Configuration command class.  The values are device-specific and are
# not reported by the devices. Information on parameters  is provided only in the device user
# manual.
#
# An ongoing task for the OpenZWave project is to create XML files describing the available
# parameters for every Z-Wave.  See the config folder in the project source code for examples.
#
    def setConfigParam(self, homeid, nodeid, param, value, size=2):
        '''
.. _setConfigParam:

Set the value of a configurable parameter in a device.

Some devices have various parameters that can be configured to control the
device behaviour.  These are not reported by the device over the Z-Wave network
but can usually be found in the devices user manual.  This method returns
immediately, without waiting for confirmation from the device that the change
has been made.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to configure.
:type nodeId: int
:param param: The index of the parameter.
:type param: int
:param value: The value to which the parameter should be set.
:type value: int
:param size: Is an optional number of bytes to be sent for the parameter value. Defaults to 2.
:type size: int
:return: True if the message setting the value was sent to the device.
:rtype: bool
:see: requestConfigParam_, requestAllConfigParams_

        '''
        return self.manager.SetConfigParam(homeid, nodeid, param, value, size)

    def requestConfigParam(self, homeid, nodeid, param):
        '''
.. _requestConfigParam:

Request the value of a configurable parameter from a device.

Some devices have various parameters that can be configured to control the
device behaviour.  These are not reported by the device over the Z-Wave network
but can usually be found in the devices user manual.  This method requests
the value of a parameter from the device, and then returns immediately,
without waiting for a response.  If the parameter index is valid for this
device, and the device is awake, the value will eventually be reported via a
ValueChanged notification callback.  The ValueID reported in the callback will
have an index set the same as _param and a command class set to the same value
as returned by a call to Configuration::StaticGetCommandClassId.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to configure.
:type nodeId: int
:param param: The index of the parameter.
:type param: int
:see: requestAllConfigParams_, setConfigParam_

        '''
        self.manager.RequestConfigParam(homeid, nodeid, param)

    def requestAllConfigParams(self, homeid, nodeid):
        '''
.. _requestAllConfigParams:

Request the values of all known configurable parameters from a device.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to configure.
:type nodeId: int
:see: requestConfigParam_, setConfigParam_

        '''
        self.manager.RequestAllConfigParams(homeid, nodeid)
#
# -----------------------------------------------------------------------------
# Groups (wrappers for the Node methods)
# -----------------------------------------------------------------------------
# Methods for accessing device association groups.
#
    def getNumGroups(self, homeid, nodeid):
        '''
.. _getNumGroups:

Gets the number of association groups reported by this node

In Z-Wave, groups are numbered starting from one.  For example, if a call to
GetNumGroups returns 4, the _groupIdx value to use in calls to GetAssociations
AddAssociation and RemoveAssociation will be a number between 1 and 4.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node whose groups we are interested in.
:type nodeId: int
:return: The number of groups.
:rtype: int
:see: getAssociations_, getMaxAssociations_, addAssociation_, removeAssociation_

        '''
        return self.manager.GetNumGroups(homeid, nodeid)

    def getAssociations(self, homeid, nodeid, groupidx):
        '''
.. _getAssociations:

Gets the associations for a group

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node whose associations we are interested in.
:type nodeId: int
:param groupIdx: one-based index of the group (because Z-Wave product manuals use one-based group numbering).
:type groupIdx: int
:return: A set containing IDs of members of the group
:rtype: set()
:see: getNumGroups_, addAssociation_, removeAssociation_, getMaxAssociations_
        '''
#~ cython overloading problem
#~ src-lib/libopenzwave/libopenzwave.pyx:3739:58: no suitable method found
#~
#~
#~         data = set()
#~         cdef uint32_t size = self.manager.GetMaxAssociations(homeid, nodeid, groupidx)
#~         #Allocate memory
#~         cdef int_associations dbuf = <int_associations>malloc(sizeof(uint8_t) * size)
#~         # return value is pointer to uint8_t[]
#~         cdef uint32_t count = self.manager.GetAssociations(homeid, nodeid, groupidx, dbuf)
#~         if count == 0:
#~             #Don't need to allocate memory.
#~             free(dbuf)
#~             return data
#~         cdef RetAlloc retuint8 = RetAlloc(count)
#~         cdef uint8_t* p
#~         cdef uint32_t start = 0
#~         if count:
#~             try:
#~                 p = dbuf[0] # p is now pointing at first element of array
#~                 for i in range(start, count):
#~                     retuint8.data[i] = p[0]
#~                     data.add(retuint8.data[i])
#~                     p += 1
#~             finally:
#~                 # Free memory
#~                 free(dbuf)
#~                 pass
#~         return data
        return [ x[0] for x in self.getAssociationsInstances(homeid, nodeid, groupidx) if x[1] == 0x00 ]

    def getAssociationsInstances(self, homeid, nodeid, groupidx):
        '''
.. _getAssociationsInstances:

Gets the associationsInstances for a group

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node whose associations we are interested in.
:type nodeId: int
:param groupIdx: one-based index of the group (because Z-Wave product manuals use one-based group numbering).
:type groupIdx: int
:return: A set containing tuples containing the node_id and the instance
:rtype: set((node_id,instance))
:see: getNumGroups_, addAssociation_, removeAssociation_, getMaxAssociations_

        '''
        data = set()
        cdef uint32_t size = self.manager.GetMaxAssociations(homeid, nodeid, groupidx)
        #Allocate memory
        cdef struct_associations dbuf = <struct_associations>malloc(sizeof(InstanceAssociation_t) * size)
        # return value is pointer to uint8_t[]
        cdef uint32_t count = self.manager.GetAssociations(homeid, nodeid, groupidx, dbuf)
        if count == 0:
            #Don't need to allocate memory.
            free(dbuf)
            return data
        cdef InstanceAssociationAlloc retassinst = InstanceAssociationAlloc(count)
        cdef InstanceAssociation_t* p
        cdef uint32_t start = 0
        if count:
            try:
                p = dbuf[0] # p is now pointing at first element of array
                for i in range(start, count):
                    retassinst.data[2*i] = p[0].m_nodeId
                    retassinst.data[2*i+1] = p[0].m_instance
                    data.add((retassinst.data[2*i],retassinst.data[2*i+1]))
                    p += 1
            finally:
                # Free memory
                free(dbuf)
                pass
        return data

    def getMaxAssociations(self, homeid, nodeid, groupidx):
        '''
.. _getMaxAssociations:

Gets the maximum number of associations for a group.

:param homeid: The Home ID of the Z-Wave controller that manages the node.
:type homeid: int
:param nodeid: The ID of the node whose associations we are interested in.
:type nodeid: int
:param groupidx: One-based index of the group (because Z-Wave product manuals use one-based group numbering).
:type groupidx: int
:return: The maximum number of nodes that can be associated into the group.
:rtype: int
:see: getNumGroups_, addAssociation_, removeAssociation_, getAssociations_

        '''
        return self.manager.GetMaxAssociations(homeid, nodeid, groupidx)

    def getGroupLabel(self, homeid, nodeid, groupidx):
        '''
Returns a label for the particular group of a node.

.. _getGroupLabel:

This label is populated by the device specific configuration files.

:param homeid: The Home ID of the Z-Wave controller that manages the node.
:type homeid: int
:param nodeid: The ID of the node whose associations are to be changed.
:type nodeid: int
:param groupidx: One-based index of the group (because Z-Wave product manuals use one-based group numbering).
:type groupidx: int
:return: The label for the particular group of a node.
:rtype: str
:see: getNumGroups_, getAssociations_, getMaxAssociations_, addAssociation_

        '''
        cdef string c_string = self.manager.GetGroupLabel(homeid, nodeid, groupidx)
        return cstr_to_str(c_string.c_str())

    def addAssociation(self, homeid, nodeid, groupidx, targetnodeid, instance=0x00):
        '''
.. _addAssociation:

Adds a node to an association group.

Due to the possibility of a device being asleep, the command is assumed to
suceeed, and the association data held in this class is updated directly.  This
will be reverted by a future Association message from the device if the Z-Wave
message actually failed to get through.  Notification callbacks will be sent in
both cases.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node whose associations are to be changed.
:type nodeId: int
:param groupIdx: One-based index of the group (because Z-Wave product manuals use one-based group numbering).
:type groupIdx: int
:param targetNodeId: Identifier for the node that will be added to the association group.
:type targetNodeId: int
:param instance: Identifier for the instance that will be added to the association group.
:type instance: int
:see: getNumGroups_, getAssociations_, getMaxAssociations_, removeAssociation_

        '''
        self.manager.AddAssociation(homeid, nodeid, groupidx, targetnodeid, instance)

    def removeAssociation(self, homeid, nodeid, groupidx, targetnodeid, instance=0x00):
        '''
.. _removeAssociation:

Removes a node from an association group.

Due to the possibility of a device being asleep, the command is assumed to
succeed, and the association data held in this class is updated directly.  This
will be reverted by a future Association message from the device if the Z-Wave
message actually failed to get through.   Notification callbacks will be sent
in both cases.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node whose associations are to be changed.
:type nodeId: int
:param groupIdx: One-based index of the group (because Z-Wave product manuals use one-based group numbering).
:type groupIdx: int
:param targetNodeId: Identifier for the node that will be removed from the association group.
:type targetNodeId: int
:param instance: Identifier for the instance that will be added to the association group.
:type instance: int
:see: getNumGroups_, getAssociations_, getMaxAssociations_, addAssociation_

        '''
        self.manager.RemoveAssociation(homeid, nodeid, groupidx, targetnodeid, instance)
#
# -----------------------------------------------------------------------------
# Notifications
# -----------------------------------------------------------------------------
# For notification of changes to the Z-Wave network or device values and associations.
#
    def addWatcher(self, pythonfunc):
        '''
.. _addWatcher:

Add a notification watcher.

In OpenZWave, all feedback from the Z-Wave network is sent to the application
via callbacks.  This method allows the application to add a notification
callback handler, known as a "watcher" to OpenZWave.  An application needs only
add a single watcher - all notifications will be reported to it.

:param pythonfunc: Watcher pointer to a function that will be called by the notification system.
:type pythonfunc: callback
:see: removeWatcher_

        '''
        self._watcherCallback = pythonfunc # need to keep a reference to this
        if not self.manager.AddWatcher(notif_callback, <void*>pythonfunc):
            raise ValueError("call to AddWatcher failed")

    def removeWatcher(self, pythonfunc):
        '''
.. _removeWatcher:

Remove a notification watcher.

:param pythonfunc: Watcher pointer to a function
:type pythonfunc: callback
:see: addWatcher_

        '''
        if not self.manager.RemoveWatcher(notif_callback, <void*>self._watcherCallback):
            raise ValueError("call to RemoveWatcher failed")
        else:
            self._watcherCallback = None


#
# -----------------------------------------------------------------------------
# Controller commands
# ----------------------------------------------------------------------------
# Commands for Z-Wave network management using the PC Controller.
#
    def resetController(self, homeid):
        '''
.. _resetController:

Hard Reset a PC Z-Wave Controller.

Resets a controller and erases its network configuration settings.  The
controller becomes a primary controller ready to add devices to a new network.

:param homeId: The Home ID of the Z-Wave controller to be reset.
:type homeId: int
:see: softResetController_

        '''
        values_map.clear()
        self.manager.ResetController(homeid)

    def softResetController(self, homeid):
        '''
.. _softResetController:

Soft Reset a PC Z-Wave Controller.

Resets a controller without erasing its network configuration settings.

:param homeId: The Home ID of the Z-Wave controller to be reset.
:type homeId: int
:see: resetController_

        '''
        self.manager.SoftReset(homeid)

    def cancelControllerCommand(self, homeid):
        '''
.. _cancelControllerCommand:

Cancels any in-progress command running on a controller.

:param homeId: The Home ID of the Z-Wave controller.
:type homeId: int
:return: True if a command was running and was cancelled.
:rtype: bool
:see: beginControllerCommand_

        '''
        return self.manager.CancelControllerCommand(homeid)

    def beginControllerCommand(self, homeId, command, pythonfunc,\
            highPower=False, nodeId=0xff, arg=0):

        '''

.. _beginControllerCommand:

Start a controller command process.

Commands :

     - Driver::ControllerCommand_AddDevice - Add a new device or controller to the Z-Wave network.
     - Driver::ControllerCommand_CreateNewPrimary - Create a new primary controller when old primary fails. Requires SUC.
     - Driver::ControllerCommand_ReceiveConfiguration - Receive network configuration information from primary controller. Requires secondary.
     - Driver::ControllerCommand_RemoveDevice - Remove a device or controller from the Z-Wave network.
     - Driver::ControllerCommand_RemoveFailedNode - Remove a node from the network. The node must not be responding
       and be on the controller's failed node list.
     - Driver::ControllerCommand_HasNodeFailed - Check whether a node is in the controller's failed nodes list.
     - Driver::ControllerCommand_ReplaceFailedNode - Replace a failed device with another. If the node is not in
       the controller's failed nodes list, or the node responds, this command will fail.
     - Driver:: ControllerCommand_TransferPrimaryRole - Add a new controller to the network and
       make it the primary.  The existing primary will become a secondary controller.
     - Driver::ControllerCommand_RequestNetworkUpdate - Update the controller with network information from the SUC/SIS.
     - Driver::ControllerCommand_RequestNodeNeighborUpdate - Get a node to rebuild its neighbour list.  This method also does RequestNodeNeighbors afterwards.
     - Driver::ControllerCommand_AssignReturnRoute - Assign a network return route to a device.
     - Driver::ControllerCommand_DeleteAllReturnRoutes - Delete all network return routes from a device.
     - Driver::ControllerCommand_SendNodeInformation - Send a node information frame.
     - Driver::ControllerCommand_ReplicationSend - Send information from primary to secondary
     - Driver::ControllerCommand_CreateButton - Create a handheld button id.
     - Driver::ControllerCommand_DeleteButton - Delete a handheld button id.

Callbacks :

    - Driver::ControllerState_Waiting, the controller is waiting for a user action.  A notice should be displayed \
      to the user at this point, telling them what to do next. \
      For the add, remove, replace and transfer primary role commands, the user needs to be told to press the \
      inclusion button on the device that  is going to be added or removed.  For ControllerCommand_ReceiveConfiguration, \
      they must set their other controller to send its data, and for ControllerCommand_CreateNewPrimary, set the other \
      controller to learn new data.
    - Driver::ControllerState_InProgress - the controller is in the process of adding or removing the chosen node.  It is now too late to cancel the command.
    - Driver::ControllerState_Complete - the controller has finished adding or removing the node, and the command is complete.
    - Driver::ControllerState_Failed - will be sent if the command fails for any reason.

:param homeId: The Home ID of the Z-Wave controller.
:type homeId: int
:param command: The command to be sent to the controller.
:type command: ControllerCommand
:param callback: Pointer to a function that will be called at various stages during the command process \
to notify the user of progress or to request actions on the user's part.  Defaults to NULL.
:type callback: pfnControllerCallback_t
:param context: Pointer to user defined data that will be passed into to the callback function.  Defaults to NULL.
:type context:
:param highPower: Used only with the AddDevice, AddController, RemoveDevice and RemoveController commands. \
Usually when adding or removing devices, the controller operates at low power so that the controller must \
be physically close to the device for security reasons.  If _highPower is true, the controller will \
operate at normal power levels instead.  Defaults to false.
:type highPower: bool
:param nodeId: Used only with the ReplaceFailedNode command, to specify the node that is going to be replaced.
:type nodeId: int
:param arg:
:type arg: int
:return: True if the command was accepted and has started.
:rtype: bool
:see: cancelControllerCommand_
        '''

        self._controllerCallback = pythonfunc # need to keep a reference to this
        return self.manager.BeginControllerCommand(homeId, command, \
                 ctrl_callback, <void*>pythonfunc, highPower, nodeId, arg)

    def createNewPrimary(self, homeid):
        '''
.. _createNewPrimary:

Create a new primary controller when old primary fails. Requires SUC.

This command Creates a new Primary Controller when the Old Primary has Failed. Requires a SUC on the network to function.

Results of the CreateNewPrimary Command will be send as a Notification with the Notification type as
Notification::Type_ControllerCommand

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:return: True if the request was sent successfully.
:rtype: bool

        '''
        return self.manager.CreateNewPrimary(homeid)

    def transferPrimaryRole(self, homeid):
        '''
.. _transferPrimaryRole:

Add a new controller to the network and make it the primary.

The existing primary will become a secondary controller.

Results of the TransferPrimaryRole Command will be send as a Notification with the Notification type as
Notification::Type_ControllerCommand

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:return: True if the request was sent successfully.
:rtype: bool

        '''
        return self.manager.TransferPrimaryRole(homeid)

    def receiveConfiguration(self, homeid):
        '''
.. _receiveConfiguration:

Receive network configuration information from primary controller. Requires secondary.

This command prepares the controller to recieve Network Configuration from a Secondary Controller.

Results of the ReceiveConfiguration Command will be send as a Notification with the Notification type as
Notification::Type_ControllerCommand

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:return: True if the request was sent successfully.
:rtype: bool

        '''
        return self.manager.ReceiveConfiguration(homeid)

    def addNode(self, homeid, doSecurity):
        '''
.. _addNode:

Start the Inclusion Process to add a Node to the Network.

The Status of the Node Inclusion is communicated via Notifications. Specifically, you should
monitor ControllerCommand Notifications.

Results of the AddNode Command will be send as a Notification with the Notification type as
Notification::Type_ControllerCommand

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param doSecurity: Whether to initialize the Network Key on the device if it supports the Security CC
:type doSecurity: bool
:return: True if the request was sent successfully.
:rtype: bool

        '''
        return self.manager.AddNode(homeid, doSecurity)

    def removeNode(self, homeid):
        '''
.. _removeNode:

Remove a Device from the Z-Wave Network

The Status of the Node Removal is communicated via Notifications. Specifically, you should
monitor ControllerCommand Notifications.

Results of the RemoveNode Command will be send as a Notification with the Notification type as
Notification::Type_ControllerCommand

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param doSecurity: Whether to initialize the Network Key on the device if it supports the Security CC
:type doSecurity: bool
:return: True if the request was sent successfully.
:rtype: bool

        '''
        return self.manager.RemoveNode(homeid)

    def removeFailedNode(self, homeid, nodeid):
        '''
.. _removeFailedNode:

Check if the Controller Believes a Node has Failed.

This is different from the IsNodeFailed call in that we test the Controllers Failed Node List, whereas the IsNodeFailed is testing
our list of Failed Nodes, which might be different.

The Results will be communicated via Notifications. Specifically, you should monitor the ControllerCommand notifications

Results of the RemoveFailedNode Command will be send as a Notification with the Notification type as
Notification::Type_ControllerCommand

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: True if the request was sent successfully.
:rtype: bool

        '''
        return self.manager.RemoveFailedNode(homeid, nodeid)

    def hasNodeFailed(self, homeid, nodeid):
        '''
.. _hasNodeFailed:

Ask a Node to update its Neighbor Tables

This command will ask a Node to update its Neighbor Tables.

Results of the HasNodeFailed Command will be send as a Notification with the Notification type as
Notification::Type_ControllerCommand

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: True if the request was sent successfully.
:rtype: bool

        '''
        return self.manager.HasNodeFailed(homeid, nodeid)

    def requestNodeNeighborUpdate(self, homeid, nodeid):
        '''
.. _requestNodeNeighborUpdate:

Ask a Node to update its Neighbor Tables

This command will ask a Node to update its Neighbor Tables.

Results of the RequestNodeNeighborUpdate Command will be send as a Notification with the Notification type as
Notification::Type_ControllerCommand

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: True if the request was sent successfully.
:rtype: bool

        '''
        return self.manager.RequestNodeNeighborUpdate(homeid, nodeid)

    def assignReturnRoute(self, homeid, nodeid):
        '''
.. _assignReturnRoute:

Ask a Node to update its update its Return Route to the Controller

This command will ask a Node to update its Return Route to the Controller

Results of the AssignReturnRoute Command will be send as a Notification with the Notification type as
Notification::Type_ControllerCommand

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: True if the request was sent successfully.
:rtype: bool

        '''
        return self.manager.AssignReturnRoute(homeid, nodeid)

    def deleteAllReturnRoutes(self, homeid, nodeid):
        '''
.. _deleteAllReturnRoutes:

Ask a Node to delete all Return Route.

This command will ask a Node to delete all its return routes, and will rediscover when needed.

Results of the DeleteAllReturnRoutes Command will be send as a Notification with the Notification type as
Notification::Type_ControllerCommand

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: True if the request was sent successfully.
:rtype: bool

        '''
        return self.manager.DeleteAllReturnRoutes(homeid, nodeid)

    def sendNodeInformation(self, homeid, nodeid):
        '''
.. _sendNodeInformation:

Create a new primary controller when old primary fails. Requires SUC.

This command Creates a new Primary Controller when the Old Primary has Failed. Requires a SUC on the network to function

Results of the SendNodeInformation Command will be send as a Notification with the Notification type as
Notification::Type_ControllerCommand

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: True if the request was sent successfully.
:rtype: bool

        '''
        return self.manager.SendNodeInformation(homeid, nodeid)

    def replaceFailedNode(self, homeid, nodeid):
        '''
.. _replaceFailedNode:

Replace a failed device with another.

If the node is not in the controller's failed nodes list, or the node responds, this command will fail.

You can check if a Node is in the Controllers Failed node list by using the HasNodeFailed method.

Results of the ReplaceFailedNode Command will be send as a Notification with the Notification type as
Notification::Type_ControllerCommand

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: True if the request was sent successfully.
:rtype: bool

        '''
        return self.manager.ReplaceFailedNode(homeid, nodeid)

    def requestNetworkUpdate(self, homeid, nodeid):
        '''
.. _requestNetworkUpdate:

Update the controller with network information from the SUC/SIS.

Results of the RequestNetworkUpdate Command will be send as a Notification with the Notification type as
Notification::Type_ControllerCommand

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: True if the request was sent successfully.
:rtype: bool

        '''
        return self.manager.RequestNetworkUpdate(homeid, nodeid)

    def replicationSend(self, homeid, nodeid):
        '''
.. _replicationSend:

Create a handheld button id.

Only intended for Bridge Firmware Controllers.

Results of the ReplicationSend Command will be send as a Notification with the Notification type as
Notification::Type_ControllerCommand

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:param buttonid: the ID of the Button to query.
:type buttonid: int
:return: True if the request was sent successfully.
:rtype: bool

        '''
        return self.manager.ReplicationSend(homeid, nodeid)

    def createButton(self, homeid, nodeid, buttonid):
        '''
.. _createButton:

Create a handheld button id.

Only intended for Bridge Firmware Controllers.

Results of the CreateButton Command will be send as a Notification with the Notification type as
Notification::Type_ControllerCommand

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:param buttonid: the ID of the Button to query.
:type buttonid: int
:return: True if the request was sent successfully.
:rtype: bool

        '''
        return self.manager.CreateButton(homeid, nodeid, buttonid)

    def deleteButton(self, homeid, nodeid, buttonid):
        '''
.. _deleteButton:

Delete a handheld button id.

Only intended for Bridge Firmware Controllers.

Results of the CreateButton Command will be send as a Notification with the Notification type as
Notification::Type_ControllerCommand

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:return: True if the request was sent successfully.
:rtype: bool

        '''
        return self.manager.DeleteButton(homeid, nodeid, buttonid)

#-----------------------------------------------------------------------------
# Scene commands
#-----------------------------------------------------------------------------

    def getNumScenes(self):
        '''
.. _getNumScenes:

Gets the number of scenes that have been defined

:return: The number of scenes.
:rtype: int
:see: getAllScenes_, sceneExists_, \
createScene_, removeScene_, activateScene_, \
getSceneLabel_, setSceneLabel_, \
removeSceneValue_, addSceneValue_, setSceneValue_, \
sceneGetValues_, removeAllScenes_

       '''
        return self.manager.GetNumScenes()

    def getAllScenes(self):
        '''
.. _getAllScenes:

Gets a set of all the SceneIds

:return: A set() containing neighboring scene IDs
:rtype: set()
:see: getNumScenes_, sceneExists_, \
createScene_, removeScene_, activateScene_, \
getSceneLabel_, setSceneLabel_, \
removeSceneValue_, addSceneValue_, setSceneValue_, \
sceneGetValues_, removeAllScenes_

        '''
        data = set()
        cdef uint32_t size = self.manager.GetNumScenes()
        # Allocate memory
        cdef uint8_t** dbuf = <uint8_t**>malloc(sizeof(uint8_t)*size)
        # return value is pointer to uint8_t[]
        cdef uint32_t count = self.manager.GetAllScenes(dbuf)
        if count == 0:
            #Don't need to allocate memory.
            free(dbuf)
            return data
        cdef RetAlloc retuint8 = RetAlloc(count)
        cdef uint8_t* p
        cdef uint32_t start = 0
        if count:
            try:
                p = dbuf[0] # p is now pointing at first element of array
                for i in range(start, count):
                    retuint8.data[i] = p[0]
                    data.add(retuint8.data[i])
                    p += 1
            finally:
                # Free memory
                free(dbuf)
                pass
        return data

    def removeAllScenes(self, homeid):
        '''
.. _removeAllScenes:

Delete all scenes.

:param homeid: The Home ID of the Z-Wave controller that manages the node.
:type homeid: int
:see: getNumScenes_, getAllScenes_, sceneExists_, \
removeScene_, activateScene_, getSceneLabel_, setSceneLabel_, \
removeSceneValue_, addSceneValue_, setSceneValue_, \
sceneGetValues_

       '''
        self.manager.RemoveAllScenes(homeid)

    def removeScene(self, sceneId):
        '''
.. _removeScene:

Remove an existing Scene.

:param sceneId: The unique Scene ID to be removed.
:type sceneId: int
:return: True if scene was removed.
:rtype: bool
:see: getNumScenes_, getAllScenes_, sceneExists_, \
createScene_, activateScene_, getSceneLabel_, setSceneLabel_, \
removeSceneValue_, addSceneValue_, setSceneValue_, \
sceneGetValues_, removeAllScenes_

        '''
        return self.manager.RemoveScene(sceneId)

    def createScene(self):
        '''
.. _createScene:

Create a Scene.

:return: Scene ID used to reference the scene. 0 is failure result.
:rtype: id
:see: getNumScenes_, getAllScenes_, sceneExists_, \
removeScene_, activateScene_, getSceneLabel_, setSceneLabel_, \
removeSceneValue_, addSceneValue_, setSceneValue_, \
sceneGetValues_, removeAllScenes_

        '''
        return self.manager.CreateScene()

    def sceneGetValues(self, uint8_t id):
        '''
.. _sceneGetValues:

Retrieve the list of values from a scene.

:param id: The ID of a scene.
:type id: int
:rtype: dict()
:return: A dict containing : {valueid : value, ...}
:see: getNumScenes_, getAllScenes_, sceneExists_, \
createScene_, removeScene_, getSceneLabel_, setSceneLabel_, \
removeSceneValue_, addSceneValue_, setSceneValue_, \
sceneGetValues_, removeAllScenes_
        '''
        cdef float type_float
        cdef bool type_bool
        cdef uint8_t type_byte
        cdef int32_t type_int
        cdef int16_t type_short
        cdef string type_string
        cdef vector[string] strvect
        cdef ValueID* cvalueID
        cdef vector[ValueID] vect
        ret = dict()
        if self.manager.SceneGetValues(id, &vect):
            while not vect.empty() :
                cvalueID = &vect.back()
                datatype = PyValueTypes[cvalueID.GetType()]
                value_data = None
                value_id = cvalueID.GetId()
                if datatype == "Bool":
                    cret = self.manager.SceneGetValueAsBool(id, deref(cvalueID), &type_bool)
                    value_data = type_bool if cret else None
                elif datatype == "Byte":
                    cret = self.manager.SceneGetValueAsByte(id, deref(cvalueID), &type_byte)
                    value_data = type_byte if cret else None
                elif datatype == "Decimal":
                    cret = self.manager.SceneGetValueAsFloat(id, deref(cvalueID), &type_float)
                    value_data = type_float if cret else None
                elif datatype == "Int":
                    cret = self.manager.SceneGetValueAsInt(id, deref(cvalueID), &type_int)
                    value_data = type_int if cret else None
                elif datatype == "Short":
                    cret = self.manager.SceneGetValueAsShort(id, deref(cvalueID), &type_short)
                    value_data = type_short if cret else None
                elif datatype == "String":
                    cret = self.manager.SceneGetValueAsString(id, deref(cvalueID), &type_string)
                    value_data = type_string.c_str() if cret else None
                elif datatype == "Button":
                    cret = self.manager.SceneGetValueAsBool(id, deref(cvalueID), &type_bool)
                    value_data = type_bool if cret else None
                elif datatype == "List":
                    cret = self.manager.SceneGetValueListSelection(id, deref(cvalueID), &type_string)
                    value_data = type_string.c_str() if cret else None
                else :
                    cret = self.manager.SceneGetValueAsString(id, deref(cvalueID), &type_string)
                    value_data = type_string.c_str() if cret else None
                ret[value_id] = value_data
                vect.pop_back();
        return ret


    def addSceneValue(self, uint8_t sceneid, id, value):
        '''
.. _addSceneValue:

Add a ValueID of value to an existing scene.

Actually I don't know how to use it :)

:param sceneid: The ID of a scene.
:type sceneid: int
:param id: The ID of a value.
:type id: int
:param value: The value to set
:type value: bool, int, float, string
:return: An integer representing the result of the operation
    0 : The C method fails
    1 : The C method succeed
    2 : Can't find id in the map
:rtype: int
:see: getNumScenes_, getAllScenes_, sceneExists_, removeAllScenes_, \
createScene_, removeScene_, activateScene_, getSceneLabel_, setSceneLabel_, \
removeSceneValue_, setSceneValue_, sceneGetValues_

        '''
        cdef float type_float
        cdef bool type_bool
        cdef uint8_t type_byte
        cdef int32_t type_int
        cdef int16_t type_short
        cdef string type_string
        ret = 2
        if values_map.find(id) != values_map.end():
            datatype = PyValueTypes[values_map.at(id).GetType()]
            if datatype == "Bool":
                type_bool = value
                cret = self.manager.AddSceneValue(sceneid, values_map.at(id), type_bool)
                ret = 1 if cret else 0
            elif datatype == "Byte":
                type_byte = value
                cret = self.manager.AddSceneValue(sceneid, values_map.at(id), type_byte)
                ret = 1 if cret else 0
            elif datatype == "Decimal":
                type_float = value
                cret = self.manager.AddSceneValue(sceneid, values_map.at(id), type_float)
                ret = 1 if cret else 0
            elif datatype == "Int":
                type_int = value
                cret = self.manager.AddSceneValue(sceneid, values_map.at(id), type_int)
                ret = 1 if cret else 0
            elif datatype == "Short":
                type_short = value
                cret = self.manager.AddSceneValue(sceneid, values_map.at(id), type_short)
                ret = 1 if cret else 0
            elif datatype == "String":
                type_string = string(value)
                cret = self.manager.AddSceneValue(sceneid, values_map.at(id), type_string)
                ret = 1 if cret else 0
            elif datatype == "Button":
                type_bool = value
                cret = self.manager.AddSceneValue(sceneid, values_map.at(id), type_bool)
                ret = 1 if cret else 0
            elif datatype == "List":
                type_string = string(value)
                cret = self.manager.AddSceneValueListSelection(sceneid, values_map.at(id), type_string)
                ret = 1 if cret else 0
        return ret

    def removeSceneValue(self, uint8_t sceneid, id):
        '''
.. _removeSceneValue:

Remove the Value ID from an existing scene.

:param sceneid: The ID of a scene.
:type sceneid: int
:param id: The ID of a value.
:type id: int
:return: True if succee. False otherwise
:rtype: bool
:see: getNumScenes_, getAllScenes_, sceneExists_, removeAllScenes_, \
createScene_, removeScene_, activateScene_, \
getSceneLabel_, setSceneLabel_, removeSceneValue_, setSceneValue_, \
sceneGetValues_

        '''
        if values_map.find(id) != values_map.end():
            return self.manager.RemoveSceneValue(sceneid, values_map.at(id))
        return False

    def setSceneValue(self, uint8_t sceneid, id, value):
        '''
.. _setSceneValue:

Set a value to an existing scene's ValueID.

:param sceneid: The ID of a scene.
:type sceneid: int
:param id: The ID of a value.
:type id: int
:param value: The value to set
:type value: bool, int, float, string
:return: An integer representing the result of the operation
    0 : The C method fails
    1 : The C method succeed
    2 : Can't find id in the map
:rtype: int
:see: getNumScenes_, getAllScenes_, sceneExists_, removeAllScenes_, \
createScene_, removeScene_, activateScene_, \
getSceneLabel_, setSceneLabel_, removeSceneValue_, addSceneValue_, \
sceneGetValues_

        '''
        cdef float type_float
        cdef bool type_bool
        cdef uint8_t type_byte
        cdef int32_t type_int
        cdef int16_t type_short
        cdef string type_string
        ret = 2
        if values_map.find(id) != values_map.end():
            datatype = PyValueTypes[values_map.at(id).GetType()]
            if datatype == "Bool":
                type_bool = value
                cret = self.manager.SetSceneValue(sceneid, values_map.at(id), type_bool)
                ret = 1 if cret else 0
            elif datatype == "Byte":
                type_byte = value
                cret = self.manager.SetSceneValue(sceneid, values_map.at(id), type_byte)
                ret = 1 if cret else 0
            elif datatype == "Decimal":
                type_float = value
                cret = self.manager.SetSceneValue(sceneid, values_map.at(id), type_float)
                ret = 1 if cret else 0
            elif datatype == "Int":
                type_int = value
                cret = self.manager.SetSceneValue(sceneid, values_map.at(id), type_int)
                ret = 1 if cret else 0
            elif datatype == "Short":
                type_short = value
                cret = self.manager.SetSceneValue(sceneid, values_map.at(id), type_short)
                ret = 1 if cret else 0
            elif datatype == "String":
                type_string = string(value)
                cret = self.manager.SetSceneValue(sceneid, values_map.at(id), type_string)
                ret = 1 if cret else 0
            elif datatype == "Button":
                type_bool = value
                cret = self.manager.SetSceneValue(sceneid, values_map.at(id), type_bool)
                ret = 1 if cret else 0
            elif datatype == "List":
                type_string = string(value)
                cret = self.manager.SetSceneValueListSelection(sceneid, values_map.at(id), type_string)
                ret = 1 if cret else 0
        return ret

    def getSceneLabel(self, sceneid):
        '''
.. _getSceneLabel:

Returns a label for the particular scene.

:param sceneId: The ID of a scene.
:type sceneId: int
:param value: The value to set
:type value: int
:return: The label string.
:rtype: str
:see: getNumScenes_, getAllScenes_, sceneExists_, removeAllScenes_, \
createScene_, removeScene_, activateScene_, \
setSceneLabel_, removeSceneValue_, addSceneValue_, setSceneValue_, \
sceneGetValues_

        '''
        cdef string c_string = self.manager.GetSceneLabel(sceneid)
        return cstr_to_str(c_string.c_str())

    def setSceneLabel(self, sceneid, str label):
        '''
.. _setSceneLabel:

Sets a label for the particular scene.

:param sceneId: The ID of the scene.
:type sceneId: int
:param value: The new value of the label.
:type value: int
:see: getNumScenes_, getAllScenes_, sceneExists_, removeAllScenes_, \
createScene_, removeScene_, activateScene_, \
getSceneLabel_, removeSceneValue_, addSceneValue_, setSceneValue_, \
sceneGetValues_

        '''
        self.manager.SetSceneLabel(sceneid, str_to_cppstr(label))

    def sceneExists(self, sceneid):
        '''
.. _sceneExists:

Check if a Scene ID is defined.

:param sceneId: The ID of the scene to check.
:type sceneId: int
:return: True if Scene ID exists.
:rtype: bool
:see: getNumScenes_, getAllScenes_, removeAllScenes_, \
createScene_, removeScene_, activateScene_, \
getSceneLabel_, setSceneLabel_, removeSceneValue_, addSceneValue_, \
setSceneValue_, sceneGetValues_

        '''
        return self.manager.SceneExists(sceneid)

    def activateScene(self, sceneid):
        '''
.. _activateScene:

Activate given scene to perform all its actions.

:param sceneId: The ID of the scene to activate.
:type sceneId: int
:return: True if it is successful.
:rtype: bool
:see: getNumScenes_, getAllScenes_, sceneExists_, removeAllScenes_, \
createScene_, removeScene_, getSceneLabel_, setSceneLabel_, \
removeSceneValue_, addSceneValue_, setSceneValue_, \
sceneGetValues_

        '''
        return self.manager.ActivateScene(sceneid)
