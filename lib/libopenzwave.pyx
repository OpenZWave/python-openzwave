"""
.. module:: libopenzwave

This file is part of **python-openzwave** project http://code.google.com/p/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave wrapper

.. moduleauthor:: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com>
.. moduleauthor:: Maarten Damen <m.damen@gmail.com>

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
from mylibc cimport uint32, uint64, int32, int16, uint8, int8
from mylibc cimport string
from mylibc cimport malloc, free
from mylibc cimport PyEval_InitThreads
from driver cimport DriverData_t, DriverData
from notification cimport Notification, NotificationType, Type_Group, Type_NodeEvent
from notification cimport const_notification, pfnOnNotification_t
from values cimport ValueGenre, ValueType, ValueID
from options cimport Options, Create
import os

PYLIBRARY = "0.2.1"
OZWAVE_CONFIG_DIRECTORY = "share/python-openzwave/config"

cdef extern from "Manager.h" namespace "OpenZWave":

    cdef cppclass Manager:
        # // Configuration
        void WriteConfig(uint32 homeid)
        Options* GetOptions()
        # // Drivers
        bint AddDriver(string serialport)
        bint RemoveDriver(string controllerPath)
        uint8 GetControllerNodeId(uint32 homeid)
        bint IsPrimaryController(uint32 homeid)
        bint IsStaticUpdateController(uint32 homeid)
        bint IsBridgeController(uint32 homeid)
        string GetLibraryVersion(uint32 homeid)
        string GetLibraryTypeName(uint32 homeid)
        int32 GetSendQueueCount( uint32 homeId )
        void LogDriverStatistics( uint32 homeId )
        void GetDriverStatistics( uint32 homeId, DriverData* data )
        # // Polling
        uint32 GetPollInterval()
        void SetPollInterval(uint32 milliseconds, bIntervalBetweenPolls)
        bint EnablePoll(ValueID& valueId, uint8 intensity)
        bool DisablePoll(ValueID& valueId)
        bool isPolled(ValueID& valueId)
        void SetPollIntensity( ValueID& valueId, uint8 intensity)
        # // Node Information
        bool RefreshNodeInfo(uint32 homeid, uint8 nodeid)
        bool RequestNodeState(uint32 homeid, uint8 nodeid)
        bool RequestNodeDynamic( uint32 homeId, uint8 nodeId )
        bool IsNodeListeningDevice(uint32 homeid, uint8 nodeid)
        bool IsNodeFrequentListeningDevice( uint32 homeId, uint8 nodeId )
        bool IsNodeBeamingDevice( uint32 homeId, uint8 nodeId )
        bool IsNodeRoutingDevice(uint32 homeid, uint8 nodeid)
        bool IsNodeSecurityDevice( uint32 homeId, uint8 nodeId )
        uint32 GetNodeMaxBaudRate(uint32 homeid, uint8 nodeid)
        uint8 GetNodeVersion(uint32 homeid, uint8 nodeid)
        uint8 GetNodeSecurity(uint32 homeid, uint8 nodeid)
        uint8 GetNodeBasic(uint32 homeid, uint8 nodeid)
        uint8 GetNodeGeneric(uint32 homeid, uint8 nodeid)
        uint8 GetNodeSpecific(uint32 homeid, uint8 nodeid)
        string GetNodeType(uint32 homeid, uint8 nodeid)
        uint32 GetNodeNeighbors(uint32 homeid, uint8 nodeid, uint8** nodeNeighbors)
        string GetNodeManufacturerName(uint32 homeid, uint8 nodeid)
        string GetNodeProductName(uint32 homeid, uint8 nodeid)
        string GetNodeName(uint32 homeid, uint8 nodeid)
        string GetNodeLocation(uint32 homeid, uint8 nodeid)
        string GetNodeManufacturerId(uint32 homeid, uint8 nodeid)
        string GetNodeProductType(uint32 homeid, uint8 nodeid)
        string GetNodeProductId(uint32 homeid, uint8 nodeid)
        void SetNodeManufacturerName(uint32 homeid, uint8 nodeid, string manufacturerName)
        void SetNodeProductName(uint32 homeid, uint8 nodeid, string productName)
        void SetNodeName(uint32 homeid, uint8 nodeid, string productName)
        void SetNodeLocation(uint32 homeid, uint8 nodeid, string location)
        void SetNodeOn(uint32 homeid, uint8 nodeid)
        void SetNodeOff(uint32 homeid, uint8 nodeid)
        void SetNodeLevel(uint32 homeid, uint8 nodeid, uint8 level)
        bool IsNodeInfoReceived(uint32 homeid, uint8 nodeid)
        bool GetNodeClassInformation( uint32 homeId, uint8 nodeId, uint8 commandClassId,
                          string *className = NULL, uint8 *classVersion = NULL)
        # // Values
        string GetValueLabel(ValueID& valueid)
        void SetValueLabel(ValueID& valueid, string value)
        string GetValueUnits(ValueID& valueid)
        void SetValueUnits(ValueID& valueid, string value)
        string GetValueHelp(ValueID& valueid)
        void SetValueHelp(ValueID& valueid, string value)
        uint32 GetValueMin(ValueID& valueid)
        uint32 GetValueMax(ValueID& valueid)
        bool IsValueReadOnly(ValueID& valueid)
        bool IsValueWriteOnly(ValueID& valueid)
        bool IsValueSet(ValueID& valueid)
        bool IsValuePolled( ValueID& valueid )
        bool GetValueAsBool(ValueID& valueid, bool* o_value)
        bool GetValueAsByte(ValueID& valueid, uint8* o_value)
        bool GetValueAsFloat(ValueID& valueid, float* o_value)
        bool GetValueAsInt(ValueID& valueid, int32* o_value)
        bool GetValueAsShort(ValueID& valueid, int16* o_value)
        bool GetValueAsString(ValueID& valueid, string* o_value)
        bool GetValueListSelection(ValueID& valueid, string* o_value)
        bool GetValueListSelection(ValueID& valueid, uint32* o_value)
        #bool GetValueListItems(ValueID& valueid, vector<string>* o_value)
        bool SetValue(ValueID& valueid, bool value)
        bool SetValue(ValueID& valueid, uint8 value)
        bool SetValue(ValueID& valueid, float value)
        bool SetValue(ValueID& valueid, int32 value)
        bool SetValue(ValueID& valueid, int16 value)
        bool SetValue(ValueID& valueid, string value)
        bool SetValueListSelection(ValueID& valueid, string selecteditem)
        bool RefreshValue(ValueID& valueid)
        void SetChangeVerified(ValueID& valueid, bool verify)
        bool PressButton(ValueID& valueid)
        bool ReleaseButton(ValueID& valueid)
        # // Climate Control
        uint8 GetNumSwitchPoints(ValueID& valueid)
        bool SetSwitchPoint(ValueID& valueid, uint8 hours, uint8 minutes, uint8 setback)
        bool RemoveSwitchPoint(ValueID& valueid, uint8 hours, uint8 minutes)
        bool ClearSwitchPoints(ValueID& valueid)
        bool GetSwitchPoint(ValueID& valueid, uint8 idx, uint8* o_hours, uint8* o_minutes, int8* o_setback)
        # // SwitchAll
        void SwitchAllOn(uint32 homeid)
        void SwitchAllOff(uint32 homeid)
        # // Configuration Parameters
        bool SetConfigParam(uint32 homeid, uint8 nodeid, uint8 param, uint32 value, uint8 size = 2)
        void RequestConfigParam(uint32 homeid, uint8 nodeid, uint8 aram)
        void RequestAllConfigParams(uint32 homeid, uint8 nodeid)
        # // Groups
        uint8 GetNumGroups(uint32 homeid, uint8 nodeid)
        uint32 GetAssociations(uint32 homeid, uint8 nodeid, uint8 groupidx, uint8** o_associations)
        uint8 GetMaxAssociations(uint32 homeid, uint8 nodeid, uint8 groupidx)
        string GetGroupLabel(uint32 homeid, uint8 nodeid, uint8 groupidx)
        void AddAssociation(uint32 homeid, uint8 nodeid, uint8 groupidx, uint8 targetnodeid)
        void RemoveAssociation(uint32 homeid, uint8 nodeid, uint8 groupidx, uint8 targetnodeid)
        bool AddWatcher(pfnOnNotification_t notification, void* context)
        bool RemoveWatcher(pfnOnNotification_t notification, void* context)
        # // Controller Commands
        void ResetController(uint32 homeid)
        void SoftReset(uint32 homeid)
        #bool BeginControllerCommand(uint32 homeid, Driver::ControllerCommand _command, Driver::pfnControllerCallback_t _callback = NULL, void* _context = NULL, bool _highPower = false, uint8 _nodeId = 0xff )
        bool CancelControllerCommand(uint32 homeid)
        # // Scene commands
        uint8 GetNumScenes()
        uint8 GetAllScenes(uint8** sceneIds)
        uint8 CreateScene()
        bool RemoveScene(uint8 sceneId)
        bool AddSceneValue( uint8 sceneId, ValueID& valueId, bool value)
        bool AddSceneValue( uint8 sceneId, ValueID& valueId, uint8 value)
        bool AddSceneValue( uint8 sceneId, ValueID& valueId, float value )
        bool AddSceneValue( uint8 sceneId, ValueID& valueId, int32 value )
        bool AddSceneValue( uint8 sceneId, ValueID& valueId, int16 value )
        bool AddSceneValue( uint8 sceneId, ValueID& valueId, string value )
        bool AddSceneValueListSelection( uint8 sceneId, ValueID& valueId, string value )
        bool AddSceneValueListSelection( uint8 sceneId, ValueID& valueId, int32 value )
        bool RemoveSceneValue( uint8 sceneId, ValueID& valueId )
        #int SceneGetValues( uint8 sceneId, vector<ValueID>* o_value )
        bool SceneGetValueAsBool( uint8 sceneId, ValueID& valueId, bool value )
        bool SceneGetValueAsByte( uint8 sceneId, ValueID& valueId, uint8* o_value )
        bool SceneGetValueAsFloat( uint8 sceneId, ValueID& valueId, float* o_value )
        bool SceneGetValueAsInt( uint8 sceneId, ValueID& valueId, int32* o_value )
        bool SceneGetValueAsShort( uint8 sceneId, ValueID& valueId, int16* o_value )
        bool SceneGetValueAsString( uint8 sceneId, ValueID& valueId, string* o_value )
        bool SceneGetValueListSelection( uint8 sceneId, ValueID& valueId, string* o_value )
        bool SceneGetValueListSelection( uint8 sceneId, ValueID& valueId, int32* o_value )
        bool SetSceneValue( uint8 sceneId, ValueID& valueId, bool value )
        bool SetSceneValue( uint8 sceneId, ValueID& valueId, uint8 value )
        bool SetSceneValue( uint8 sceneId, ValueID& valueId, float value )
        bool SetSceneValue( uint8 sceneId, ValueID& valueId, int32 value )
        bool SetSceneValue( uint8 sceneId, ValueID& valueId, int16 value )
        bool SetSceneValue( uint8 sceneId, ValueID& valueId, string value )
        bool SetSceneValueListSelection( uint8 sceneId, ValueID& valueId, string value )
        bool SetSceneValueListSelection( uint8 sceneId, ValueID& valueId, int32 value )
        string GetSceneLabel( uint8 sceneId )
        void SetSceneLabel( uint8 sceneId, string value )
        bool SceneExists( uint8 sceneId )
        bool ActivateScene( uint8 sceneId )

cdef extern from "Manager.h" namespace "OpenZWave::Manager":
    Manager* Create()
    Manager* Get()

cdef class PyOptions:
    cdef Options *options

    def create(self, char *a, char *b, char *c):
        self.options = Create(string(a), string(b), string(c))

    def lock(self):
        return self.options.Lock()

class EnumWithDoc(str):
    def setDoc(self, doc):
        self.__doc__ = doc
        return self

PyNotifications = [
    EnumWithDoc('ValueAdded').setDoc("A new node value has been added to OpenZWave's list. These notifications occur after a node has been discovered, and details of its command classes have been received.  Each command class may generate one or more values depending on the complexity of the item being represented."),
    EnumWithDoc('ValueRemoved').setDoc("A node value has been removed from OpenZWave's list.  This only occurs when a node is removed."),
    EnumWithDoc('ValueChanged').setDoc("A node value has been updated from the Z-Wave network and it is different from the previous value."),
    EnumWithDoc('ValueRefreshed').setDoc("A node value has been updated from the Z-Wave network."),
    EnumWithDoc('Group').setDoc("The associations for the node have changed. The application should rebuild any group information it holds about the node."),
    EnumWithDoc('NodeNew').setDoc("A new node has been found (not already stored in zwcfg*.xml file)."),
    EnumWithDoc('NodeAdded').setDoc("A new node has been added to OpenZWave's list.  This may be due to a device being added to the Z-Wave network, or because the application is initializing itself."),
    EnumWithDoc('NodeRemoved').setDoc("A node has been removed from OpenZWave's list.  This may be due to a device being removed from the Z-Wave network, or because the application is closing."),
    EnumWithDoc('NodeProtocolInfo').setDoc("Basic node information has been receievd, such as whether the node is a listening device, a routing device and its baud rate and basic, generic and specific types. It is after this notification that you can call Manager::GetNodeType to obtain a label containing the device description."),
    EnumWithDoc('NodeNaming').setDoc("One of the node names has changed (name, manufacturer, product)."),
    EnumWithDoc('NodeEvent').setDoc("A node has triggered an event.  This is commonly caused when a node sends a Basic_Set command to the controller.  The event value is stored in the notification."),
    EnumWithDoc('PollingDisabled').setDoc("Polling of a node has been successfully turned off by a call to Manager::DisablePoll."),
    EnumWithDoc('PollingEnabled').setDoc("Polling of a node has been successfully turned on by a call to Manager::EnablePoll."),
    EnumWithDoc('CreateButton').setDoc("Handheld controller button event created."),
    EnumWithDoc('DeleteButton').setDoc("Handheld controller button event deleted."),
    EnumWithDoc('ButtonOn').setDoc("Handheld controller button on pressed event."),
    EnumWithDoc('ButtonOff').setDoc("Handheld controller button off pressed event."),
    EnumWithDoc('DriverReady').setDoc("A driver for a PC Z-Wave controller has been added and is ready to use.  The notification will contain the controller's Home ID, which is needed to call most of the Manager methods."),
    EnumWithDoc('DriverFailed').setDoc("Driver failed to load."),
    EnumWithDoc('riverReset').setDoc("All nodes and values for this driver have been removed.  This is sent instead of potentially hundreds of individual node and value notifications."),
    EnumWithDoc('MsgComplete').setDoc("The last message that was sent is now complete."),
    EnumWithDoc('EssentialNodeQueriesComplete').setDoc("The queries on a node that are essential to its operation have been completed. The node can now handle incoming messages."),
    EnumWithDoc('NodeQueriesComplete').setDoc("All the initialisation queries on a node have been completed."),
    EnumWithDoc('AwakeNodesQueried').setDoc("All awake nodes have been queried, so client application can expected complete data for these nodes."),
    EnumWithDoc('AllNodesQueried').setDoc("All nodes have been queried, so client application can expected complete data."),
    EnumWithDoc('Error').setDoc("An error has occured that we need to report."),
    ]


PyGenres = [
    EnumWithDoc('Basic').setDoc(  "The 'level' as controlled by basic commands.  Usually duplicated by another command class."),
    EnumWithDoc('User').setDoc(   "Basic values an ordinary user would be interested in."),
    EnumWithDoc('Config').setDoc( "Device-specific configuration parameters.  These cannot be automatically discovered via Z-Wave, and are usually described in the user manual instead."),
    EnumWithDoc('System').setDoc( "Values of significance only to users who understand the Z-Wave protocol"),
    ]

PyValueTypes = [
    EnumWithDoc('Bool').setDoc(     "Boolean, true or false"),
    EnumWithDoc('Byte').setDoc(     "8-bit unsigned value"),
    EnumWithDoc('Decimal').setDoc(  "Represents a non-integer value as a string, to avoid floating point accuracy issues."),
    EnumWithDoc('Int').setDoc(      "32-bit signed value"),
    EnumWithDoc('List').setDoc(     "List from which one item can be selected"),
    EnumWithDoc('Schedule').setDoc( "Complex type used with the Climate Control Schedule command class"),
    EnumWithDoc('Short').setDoc(    "16-bit signed value"),
    EnumWithDoc('String').setDoc(   "Text string"),
    EnumWithDoc('Button').setDoc(   "A write-only value that is the equivalent of pressing a button to send a command to a device"),
    ]

cdef map[uint64, ValueID] values_map

cdef getValueFromType(Manager *manager, valueId):
        cdef float type_float
        cdef bool type_bool
        cdef uint8 type_byte
        cdef int32 type_int
        cdef int16 type_short
        cdef string type_string
        ret = None
        if values_map.find(valueId) != values_map.end():
            datatype = PyValueTypes[values_map.at(valueId).GetType()]

            if datatype == "Bool":
                cret = manager.GetValueAsBool(values_map.at(valueId), &type_bool)
                ret = type_bool if cret else None
            elif datatype == "Byte":
                cret = manager.GetValueAsByte(values_map.at(valueId), &type_byte)
                ret = type_byte if cret else None
            elif datatype == "Decimal":
                cret = manager.GetValueAsFloat(values_map.at(valueId), &type_float)
                ret = type_float if cret else None
            elif datatype == "Int":
                cret = manager.GetValueAsInt(values_map.at(valueId), &type_int)
                ret = type_int if cret else None
            elif datatype == "Short":
                cret = manager.GetValueAsShort(values_map.at(valueId), &type_short)
                ret = type_short if cret else None
            elif datatype == "String":
                cret = manager.GetValueAsString(values_map.at(valueId), &type_string)
                ret = type_string.c_str() if cret else None
            else :
                cret = manager.GetValueAsString(values_map.at(valueId), &type_string)
                ret = type_string.c_str() if cret else None

        return ret

cdef addValueId(ValueID v, n):
    #cdef string value
    cdef string label
    cdef string units
    cdef Manager *manager = Get()
    #manager.GetValueAsString(v, &value)
    label = manager.GetValueLabel(v)
    units = manager.GetValueUnits(v)
    n['valueId'] = {'homeId' : v.GetHomeId(),
                    'nodeId' : v.GetNodeId(),
                    'commandClass' : PyManager.COMMAND_CLASS_DESC[v.GetCommandClassId()],
                    'instance' : v.GetInstance(),
                    'index' : v.GetIndex(),
                    'id' : v.GetId(),
                    'genre' : PyGenres[v.GetGenre()],
                    'type' : PyValueTypes[v.GetType()],
#                    'value' : value.c_str(),
                    'value' : getValueFromType(manager,v.GetId()),
                    'label' : label.c_str(),
                    'units' : units.c_str(),
                    'readOnly': manager.IsValueReadOnly(v),
                    }

    values_map.insert ( pair[uint64, ValueID] (v.GetId(), v))

cdef void callback(const_notification _notification, void* _context) with gil:
    cdef Notification* notification = <Notification*>_notification

    n = {'notificationType' : PyNotifications[notification.GetType()],
         'homeId' : notification.GetHomeId(),
         'nodeId' : notification.GetNodeId(),
         }
    if notification.GetType() == Type_Group:
        n['groupIdx'] = notification.GetGroupIdx()
    if notification.GetType() == Type_NodeEvent:
        n['event'] = notification.GetEvent()

    addValueId(notification.GetValueID(), n)
    (<object>_context)(n)

cpdef object driverData():
    cdef DriverData data

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
state) to be available.  Finally, after all nodes (whether listening or
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
        0x33: 'COMMAND_CLASS_ZIP_ADV_SERVER',
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
        0x60: 'COMMAND_CLASS_MULTI_CHANNEL_V2',
        0x62: 'COMMAND_CLASS_DOOR_LOCK',
        0x63: 'COMMAND_CLASS_USER_CODE',
        0x70: 'COMMAND_CLASS_CONFIGURATION',
        0x71: 'COMMAND_CLASS_ALARM',
        0x72: 'COMMAND_CLASS_MANUFACTURER_SPECIFIC',
        0x73: 'COMMAND_CLASS_POWERLEVEL',
        0x75: 'COMMAND_CLASS_PROTECTION',
        0x76: 'COMMAND_CLASS_LOCK',
        0x77: 'COMMAND_CLASS_NODE_NAMING',
        0x7A: 'COMMAND_CLASS_FIRMWARE_UPDATE_MD',
        0x7B: 'COMMAND_CLASS_GROUPING_NAME',
        0x7C: 'COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE',
        0x7D: 'COMMAND_CLASS_REMOTE_ASSOCIATION',
        0x80: 'COMMAND_CLASS_BATTERY',
        0x81: 'COMMAND_CLASS_CLOCK',
        0x82: 'COMMAND_CLASS_HAIL',
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
        0x8E: 'COMMAND_CLASS_MULTI_INSTANCE_ASSOCIATION',
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
        '''
        self.manager = Create()
        PyEval_InitThreads()
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

:param homeId: The Home ID of the Z-Wave controller to save.
:type homeId: int

        '''
        self.manager.WriteConfig(homeid)
#
# -----------------------------------------------------------------------------
# Drivers
# -----------------------------------------------------------------------------
# Methods for adding and removing drivers and obtaining basic controller information.
#
    def addDriver(self, char *serialport):
        '''
.. _addDriver:

Creates a new driver for a Z-Wave controller.

This method creates a Driver object for handling communications with a single
Z-Wave controller.  In the background, the driver first tries to read
configuration data saved during a previous run.  It then queries the controller
directly for any missing information, and a refresh of the list of nodes that
it controls.  Once this information has been received, a DriverReady
notification callback is sent, containing the Home ID of the controller.  This
Home ID is required by most of the OpenZWave Manager class methods.

:param serialport: The string used to open the controller.  On Windows this might be something like "\\.\\COM3", or on Linux "/dev/ttyUSB0".
:type serialport: str
:returns: bool -- True if a new driver was created
:see: removeDriver_
        '''
        self.manager.AddDriver(string(serialport))

    def removeDriver(self, char *serialport):
        '''
.. _removeDriver:

Removes the driver for a Z-Wave controller, and closes the controller.

Drivers do not need to be explicitly removed before calling Destroy - this is
handled automatically.

:param serialport: The same string as was passed in the original call toAddDriver.
:type serialport: str
:returns: bool -- True if the driver was removed, False if it could not be found.
:see: addDriver_
        '''
        self.manager.RemoveDriver(string(serialport))

    def getControllerNodeId(self, homeid):
        '''
.. _getControllerNodeId:

Get the node ID of the Z-Wave controller.

:param homeId: The Home ID of the Z-Wave controller.
:type homeId: int
:returns: int -- the node ID of the Z-Wave controller
        '''
        return self.manager.GetControllerNodeId(homeid)

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
:returns: bool -- True if it is a primary controller, False if not.
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
:returns: bool -- True if it is a static update controller, False if not.
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
:returns: bool -- True if it is a bridge controller, False if not.
        '''
        return self.manager.IsBridgeController(homeid)

    def getLibraryVersion(self, homeid):
        '''
.. _getLibraryVersion:

Get the version of the Z-Wave API library used by a controller.

:param homeId: The Home ID of the Z-Wave controller.
:type homeId: int
:returns: str -- A string containing the library version. For example, "Z-Wave 2.48".
:see: getLibraryConfigPath_, getLibraryTypeName_, getPythonLibraryVersion_, getLibraryTypeName_
        '''
        cdef string c_string = self.manager.GetLibraryVersion(homeid)
        return c_string.c_str()

    def getLibraryConfigPath(self):
        '''
.. _getLibraryConfigPath:

Retrieve the libray config path. This the directory holding the xml files.

:returns: str -- A string containing the library config path or None.
:see: getLibraryVersion_, getLibraryTypeName_, getPythonLibraryVersion_, getLibraryTypeName_
        '''
        if os.path.exists(os.path.join("/usr",OZWAVE_CONFIG_DIRECTORY)):
            return os.path.join("/usr",OZWAVE_CONFIG_DIRECTORY)
        elif os.path.exists(os.path.join("/usr/local",OZWAVE_CONFIG_DIRECTORY)):
            return os.path.join("/usr/local",OZWAVE_CONFIG_DIRECTORY)
        else:
            return None

    def getPythonLibraryVersion(self):
        '''
.. _getPythonLibraryVersion:

Get the version of the python library.

:returns: str -- A string containing the python library version. For example, "0.1".
:see: getLibraryVersion_, getLibraryTypeName_, getLibraryConfigPath_, getLibraryTypeName_
        '''
        return PYLIBRARY

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
:returns: str -- A string containing the library type.
:see: getLibraryVersion_, getPythonLibraryVersion_, getLibraryConfigPath_
        '''
        cdef string c_string = self.manager.GetLibraryTypeName(homeid)
        return c_string.c_str()

    def getSendQueueCount(self, homeid):
        '''
.. _getSendQueueCount:

Get count of messages in the outgoing send queue.

:param homeId: The Home ID of the Z-Wave controller.
:type homeId: int
:returns: int -- Message count
        '''
        return self.manager.GetSendQueueCount(homeid)

    def logDriverStatistics(self, homeid):
        '''
.. _logDriverStatistics:

Send current driver statistics to the log file.

:param homeId: The Home ID of the Z-Wave controller.
:type homeId: int
        '''
        self.manager.LogDriverStatistics(homeid)

#-----------------------------------------------------------------------------
# Statistics interface
#-----------------------------------------------------------------------------
    def getDriverStatistics(self, homeId):
        '''
Retrieve statistics from driver.

Statistics:
        s_SOFCnt                         Number of SOF bytes received
        s_ACKWaiting                     Number of unsolicited messages while waiting for an ACK
        s_readAborts                     Number of times read were aborted due to timeouts
        s_badChecksum                    Number of bad checksums
        s_readCnt                        Number of messages successfully read
        s_writeCnt                       Number of messages successfully sent
        s_CANCnt                         Number of CAN bytes received
        s_NAKCnt                         Number of NAK bytes received
        s_ACKCnt                         Number of ACK bytes received
        s_OOFCnt                         Number of bytes out of framing
        s_dropped                        Number of messages dropped & not delivered
        s_retries                        Number of messages retransmitted
        s_controllerReadCnt              Number of controller messages read
        s_controllerWriteCnt             Number of controller messages sent

:param homeId: The Home ID of the Z-Wave controller.
:type homeId: int
:param data: Pointer to structure DriverData to return values
:type data: int
:return dict(): A dict containing statistics of the driver.
:see: setNodeName
       '''
        cdef DriverData_t data
        self.manager.GetDriverStatistics( homeId, &data );
        ret = {}
        ret['s_SOFCnt'] = data.s_SOFCnt
        ret['s_ACKWaiting'] = data.s_ACKWaiting
        ret['s_readAborts'] = data.s_readAborts
        ret['s_badChecksum'] = data.s_badChecksum
        ret['s_readCnt'] = data.s_readCnt
        ret['s_writeCnt'] = data.s_writeCnt
        ret['s_CANCnt'] = data.s_CANCnt
        ret['s_NAKCnt'] = data.s_NAKCnt
        ret['s_ACKCnt'] = data.s_ACKCnt
        ret['s_OOFCnt'] = data.s_OOFCnt
        ret['s_dropped'] = data.s_dropped
        ret['s_retries'] = data.s_retries
        ret['s_controllerReadCnt'] = data.s_controllerReadCnt
        ret['s_controllerWriteCnt'] = data.s_controllerWriteCnt
        return ret

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

:returns: int -- The number of milliseconds between polls
:see: setPollInterval_, enablePoll_, isPolled_, setPollIntensity_, disablePoll_
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
:param bIntervalBetweenPolls: Don't know what it is.
:type bIntervalBetweenPolls: bool
:see: getPollInterval_, enablePoll_, isPolled_, setPollIntensity_, disablePoll_

        '''
        self.manager.SetPollInterval(milliseconds, bIntervalBetweenPolls)

    def enablePoll(self, id, intensity):
        '''
.. _enablePoll:

Enable the polling of a device's state.

:param id: The ID of the value to start polling
:type id: int
:param intensity: The intensity of the poll
:type intensity: int
:returns: bool -- True if polling was enabled.
:see: getPollInterval_, setPollInterval_, isPolled_, setPollIntensity_, disablePoll_
        '''
        if values_map.find(id) != values_map.end():
            return self.manager.EnablePoll(values_map.at(id), intensity)
        else :
            return False

    def disablePoll(self, id):
        '''
.. _disablePoll:

Disable the polling of a device's state.

:param id: Disable the polling of a device's state.
:type id: int
:returns: bool -- True if polling was disabled.
:see: getPollInterval_, setPollInterval_, enablePoll_, isPolled_, setPollIntensity_
        '''
        if values_map.find(id) != values_map.end():
            return self.manager.DisablePoll(values_map.at(id))
        else :
            return False

    def isPolled(self, id):
        '''
.. _isPolled:

Determine the polling of a device's state.

:param id: The ID of the value to check polling.
:type id: int
:return: bool -- True if polling is active.
:see: getPollInterval_, setPollInterval_, enablePoll_, setPollIntensity_, disablePoll_
        '''
        if values_map.find(id) != values_map.end():
            return self.manager.isPolled(values_map.at(id))
        else :
            return False

    def setPollIntensity(self, id, intensity):
        '''
.. _setPollIntensity:

Set the frequency of polling (0=none, 1=every time through the list, 2-every other time, etc)

:param id: The ID of the value whose intensity should be set
:type id: int
:param intensity: the intensity of the poll
:type intensity: int
:returns: bool -- True if polling is active.
:see: getPollInterval_, setPollInterval_, enablePoll_, isPolled_, disablePoll_
        '''
        if values_map.find(id) != values_map.end():
            self.manager.SetPollIntensity(values_map.at(id), intensity)

#
# -----------------------------------------------------------------------------
# Node information
# -----------------------------------------------------------------------------
# Methods for accessing information on indivdual nodes.
#

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
:returns: bool -- True if the request was sent successfully.
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
:returns: bool -- True if the request was sent successfully.
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
:returns: bool -- True if the request was sent successfully.
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
:returns: bool -- True if the node is a beaming device
        '''
        return self.manager.IsNodeBeamingDevice(homeid, nodeid)


    def isNodeListeningDevice(self, homeid, nodeid):
        '''
.. _isNodeListeningDevice:

Get whether the node is a listening device that does not go to sleep

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:returns: bool -- True if it is a listening node.
        '''
        return self.manager.IsNodeListeningDevice(homeid, nodeid)

    def isNodeFrequentListeningDevice(self, homeid, nodeid):
        '''
.. _isNodeFrequentListeningDevice:

Get whether the node is a frequent listening device that goes to sleep but
can be woken up by a beam. Useful to determine node and controller consistency.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:returns: bool -- True if it is a frequent listening node.
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
:returns: bool -- True if security features implemented.
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
:returns: bool -- True if the node is a routing device
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
:returns: int -- The baud rate in bits per second.
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
:returns: int -- The node version number
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
:returns: int -- The node security byte
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
:returns: int -- The node basic type.
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
:returns: int -- The node generic type.
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
:returns: int -- The node specific type.
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
:returns: str -- A string containing the label text.
        '''
        cdef string c_string = self.manager.GetNodeType(homeid, nodeid)
        return c_string.c_str()

    def getNodeNeighborsOld(self, homeid, nodeid):
        '''
.. _getNodeNeighborsOld:

Get the bitmap of this node's neighbors.

Old release. Do not free memory after allocating it.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:returns: tuple - A tuple containing neighboring node IDs
        '''
        retval = None
        # TODO: proper initialization of this pointer.  Underlying code creates new uint8[] at this address, but segfaults if passed in value is null.  Boy, is my C rusty.
        cdef uint8** dbuf = <uint8**>malloc(sizeof(uint8))
        # return value is pointer to uint8[]
        cdef uint32 count = self.manager.GetNodeNeighbors(homeid, nodeid, dbuf)
        cdef uint8* p
        cdef uint32 start = 0
        if count:
            try:
                data = list()
                p = dbuf[0] # p is now pointing at first element of array
                for i in range(start, count):
                    data.add(p[0])
                    p += 1
                retval = tuple(data)
            finally:
                # TODO: caller is responsible for deleting returned array via call to delete()
                pass
        return retval

    def getNodeNeighbors(self, homeid, nodeid):
        '''
.. _getNodeNeighbors:

Get the bitmap of this node's neighbors.

    uint32 GetNodeNeighbors( uint32 const _homeId, uint8 const _nodeId, uint8** _nodeNeighbors );
    /**
    * brief Get the bitmap of this node's neighbors
    *
    * param _homeId The Home ID of the Z-Wave controller that manages the node.
    * param _nodeId The ID of the node to query.
    * param _nodeNeighbors An array of 29 uint8s to hold the neighbor bitmap
    */

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node to query.
:type nodeId: int
:returns: list() - A set containing neighboring node IDs
        '''
        data = list()
        #Allocate memory
        cdef uint8** dbuf = <uint8**>malloc(sizeof(uint8)*29)
        # return value is pointer to uint8[]
        cdef uint32 count = self.manager.GetNodeNeighbors(homeid, nodeid, dbuf)
        #Allocate memory for the returned values
        cdef uint8* retuint8 = <uint8*>malloc(sizeof(uint8)*count)
        cdef uint8* p
        cdef uint32 start = 0
        if count:
            try:
                p = dbuf[0] # p is now pointing at first element of array
                for i in range(start, count):
                    retuint8[i] = p[0]
                    data.add(retuint8[i])
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
:returns: str -- A string containing the nodes manufacturer name.
:see: setNodeManufacturerName_, getNodeProductName_, setNodeProductName_
        '''
        cdef string manufacturer_string = self.manager.GetNodeManufacturerName(homeid, nodeid)
        return manufacturer_string.c_str()

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
:returns: str -- A string containing the nodes product name.
:see: setNodeProductName_, getNodeManufacturerName_, setNodeManufacturerName_
        '''
        cdef string productname_string = self.manager.GetNodeProductName(homeid, nodeid)
        return productname_string.c_str()

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
:returns: str -- A string containing the node name.
:see: setNodeName_, getNodeLocation_, setNodeLocation_
        '''
        cdef string c_string = self.manager.GetNodeName(homeid, nodeid)
        return c_string.c_str()

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
:returns: str -- A string containing the nodes location.
:see: setNodeLocation, getNodeName, setNodeName
        '''
        cdef string c_string = self.manager.GetNodeLocation(homeid, nodeid)
        return c_string.c_str()

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
:returns: str -- A string containing the nodes manufacturer ID, or an empty string if the manufactuer-specific command class is not supported by the device.
:see: getNodeProductType, getNodeProductId, getNodeManufacturerName, getNodeProductName
        '''
        cdef string c_string = self.manager.GetNodeManufacturerId(homeid, nodeid)
        return c_string.c_str()

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
:returns: str -- A string containing the nodes product type, or an empty string if the manufactuer-specific command class is not supported by the device.
:see: getNodeManufacturerId_, getNodeProductId_, getNodeManufacturerName_, getNodeProductName_
        '''
        cdef string c_string = self.manager.GetNodeProductType(homeid, nodeid)
        return c_string.c_str()

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
:returns: str -- A string containing the nodes product ID, or an empty string if the manufactuer-specific command class is not supported by the device.
:see: getNodeManufacturerId_, getNodeProductType_, getNodeManufacturerName_, getNodeProductName_
        '''
        cdef string c_string = self.manager.GetNodeProductId(homeid, nodeid)
        return c_string.c_str()

    def setNodeManufacturerName(self, homeid, nodeid, char *manufacturerName):
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
        self.manager.SetNodeManufacturerName(homeid, nodeid, string(manufacturerName))

    def setNodeProductName(self, homeid, nodeid, char *productName):
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
        self.manager.SetNodeProductName(homeid, nodeid, string(productName))

    def setNodeName(self, homeid, nodeid, char *name):
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
        self.manager.SetNodeName(homeid, nodeid, string(name))

    def setNodeLocation(self, homeid, nodeid, char *location):
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
        self.manager.SetNodeLocation(homeid, nodeid, string(location))

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
:see: setNodeOff, setNodeLevel
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
:see: setNodeOn, setNodeLevel
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
:see: setNodeOn, setNodeOff
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
:returns: bool -- True if the node information has been received yet
        '''
        return self.manager.IsNodeInfoReceived(homeid, nodeid)


    def getNodeClassInformation(self, homeid, nodeid, commandClassId, className, classVersion):
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
:returns: bool -- True if the node does have the class instantiated, will return name & version
        '''
        cdef uint8 oclassVersion
        cdef string oclassName
        ret=self.manager.GetNodeClassInformation(homeid, nodeid, commandClassId)
        if ret :
            className = oclassName.c_str()
            classVersion = oclassVersion
            return ret
        else :
            return False
        return

#
# -----------------------------------------------------------------------------
# Values
# -----------------------------------------------------------------------------
# Methods for accessing device values.  All the methods require a ValueID, which will have been provided
# in the ValueAdded Notification callback when the the value was first discovered by OpenZWave.

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
:returns: int -- An integer representing the result of the operation  0 : The C method fails, 1 : The C method succeed, 2 : Can't find id in the map
        '''
        cdef float type_float
        cdef bool type_bool
        cdef uint8 type_byte
        cdef int32 type_int
        cdef int16 type_short
        cdef string type_string
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
                type_string = string(value)
                cret = self.manager.SetValue(values_map.at(id), type_string)
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
:returns: bool -- True if the driver and node were found; false otherwise
        '''
        return self.manager.RefreshValue(values_map.at(id))

    def getValueLabel(self, id):
        '''
.. _getValueLabel:

Gets the user-friendly label for the value

:param id: The ID of a value.
:type id: int
:returns: str -- A string containing the user-friendly label of the value
 :see: setValueLabel_
       '''
        cdef string c_string
        if values_map.find(id) != values_map.end():
            c_string = self.manager.GetValueLabel(values_map.at(id))
            return c_string.c_str()
        else :
            return None

    def setValueLabel(self, id, char *label):
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
            self.manager.SetValueLabel(values_map.at(id), string(label))

    def getValueUnits(self, id):
        '''
.. _getValueUnits:

Gets the units that the value is measured in.

:param id: The ID of a value.
:type id: int
:returns: str -- A string containing the value of the units.
:see: getValueUnits_
        '''
        cdef string c_string
        if values_map.find(id) != values_map.end():
            c_string = self.manager.GetValueUnits(values_map.at(id))
            return c_string.c_str()
        else :
            return None

    def setValueUnits(self, id, char *unit):
        '''
.. _setValueUnits:

Sets the units that the value is measured in.

:param id: The ID of a value.
:type id: int
:param label: The new value of the units.
:type label: str
:see: setValueUnits_
        '''
        if values_map.find(id) != values_map.end():
            self.manager.SetValueUnits(values_map.at(id), string(unit))

    def getValueHelp(self, id):
        '''
.. _getValueHelp:

Gets a help string describing the value's purpose and usage.

:param id: The ID of a value.
:type id: int
:returns: str -- A string containing the value help text.
:see: getValueHelp
        '''
        cdef string c_string
        if values_map.find(id) != values_map.end():
            c_string = self.manager.GetValueHelp(values_map.at(id))
            return c_string.c_str()
        else :
            return None

    def setValueHelp(self, id, char *help):
        '''
.. _setValueHelp:

Sets a help string describing the value's purpose and usage.

:param id: the ID of a value.
:type id: int
:param help: The new value of the help text.
:type help: str
:see: setValueHelp
        '''
        if values_map.find(id) != values_map.end():
            self.manager.SetValueHelp(values_map.at(id), string(help))

    def getValueMin(self, id):
        '''
.. _getValueMin:

Gets the minimum that this value may contain.

:param id: The ID of a value.
:type id: int
:returns: int -- The value minimum.
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
:returns: int -- The value maximum.
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
:returns: bool -- True if the value cannot be changed by the user.
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
:returns: bool -- True if the value can only be written to and not read.
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
:returns: bool -- True if the value has actually been set by a status message from the device, rather than simply being the default.
:see: getValue_, getValueAsBool_, getValueAsByte_, \
getValueAsFloat_, getValueAsShort_, getValueAsInt_, getValueAsString_
        '''
        if values_map.find(id) != values_map.end():
            return self.manager.IsValueSet(values_map.at(id))
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
:returns: multiple -- Depending of the type of the valueId, None otherwise
:see: isValueSet_, getValueAsBool_, getValueAsByte_, \
getValueAsFloat_, getValueAsShort_, getValueAsInt_, getValueAsString_

        '''
        return getValueFromType(self.manager,id)

    def getValueAsBool(self, id):
        '''
.. _getValueAsBool:

Gets a value as a bool.

TODO : Use getValueFromType(self.manager,id) when it will be ok

:param id: The ID of a value.
:type id: int
:see: isValueSet_, getValue_, getValueAsByte_, \
getValueAsFloat_, getValueAsShort_, getValueAsInt_, getValueAsString_
        '''
        cdef bool type_bool

        if values_map.find(id) != values_map.end():
            if self.manager.GetValueAsBool(values_map.at(id), &type_bool):
                return type_bool
            else :
                return None
        else :
            return None

    def getValueAsByte(self, id):
        '''
.. _getValueAsByte:

Gets a value as an 8-bit unsigned integer.

TODO : Use getValueFromType(self.manager,id) when it will be ok

:param id: The ID of a value.
:type id: int
:see: isValueSet_, getValue_, getValueAsBool_, \
getValueAsFloat_, getValueAsShort_, getValueAsInt_, getValueAsString_
        '''
        cdef uint8 type_byte

        if values_map.find(id) != values_map.end():
            if self.manager.GetValueAsByte(values_map.at(id), &type_byte):
                return type_byte
            else :
                return None
        else :
            return None

    def getValueAsFloat(self, id):
        '''
.. _getValueAsFloat:

Gets a value as a float.

TODO : Use getValueFromType(self.manager,id) when it will be ok

:param id: The ID of a value.
:type id: int
:see: isValueSet_, getValue_, getValueAsBool_, getValueAsByte_, \
getValueAsShort_, getValueAsInt_, getValueAsString_
        '''
        cdef float type_float

        if values_map.find(id) != values_map.end():
            if self.manager.GetValueAsFloat(values_map.at(id), &type_float):
                return type_float
            else :
                return None
        else :
            return None

    def getValueAsShort(self, id):
        '''
.. _getValueAsShort:

Gets a value as a 16-bit signed integer.

TODO : Use getValueFromType(self.manager,id) when it will be ok

:param id: The ID of a value.
:type id: int
:returns: int -- The value.
:see: isValueSet_, getValue_, getValueAsBool_, getValueAsByte_, \
getValueAsFloat_, getValueAsInt_, getValueAsString_
        '''
        cdef int16 type_short

        if values_map.find(id) != values_map.end():
            if self.manager.GetValueAsShort(values_map.at(id), &type_short):
                return type_short
            else :
                return None
        else :
            return None

    def getValueAsInt(self, id):
        '''
.. _getValueAsInt:

Gets a value as a 32-bit signed integer.

TODO : Use getValueFromType(self.manager,id) when it will be ok

:param id: The ID of a value.
:type id: int
:returns: int -- The value.
:see: isValueSet_, getValue_, getValueAsBool_, getValueAsByte_, \
getValueAsFloat_, getValueAsShort_, getValueAsString_
        '''
        cdef int32 type_int

        if values_map.find(id) != values_map.end():
            if self.manager.GetValueAsInt(values_map.at(id), &type_int):
                return type_int
            else :
                return None
        else :
            return None

    def getValueAsString(self, id):
        '''
.. _getValueAsString:

Gets a value as a string.

TODO : Use getValueFromType(self.manager,id) when it will be ok

:param id: The ID of a value.
:type id: int
:returns: str -- The value.
:see: isValueSet_, getValue_, getValueAsBool_, getValueAsByte_, \
getValueAsFloat_, getValueAsShort_, getValueAsInt_
        '''
        cdef string type_string

        if values_map.find(id) != values_map.end():
            if self.manager.GetValueAsString(values_map.at(id), &type_string):
                return type_string.c_str()
            else :
                return None
        else :
            return None

#        bool GetValueListSelection(ValueID& valueid, string* o_value)
#        bool GetValueListSelection(ValueID& valueid, uint32* o_value)
#        bool GetValueListItems(ValueID& valueid, vector<string>* o_value)
#        bool SetValue(ValueID& valueid, uint8 value)
#        bool SetValue(ValueID& valueid, float value)
#        bool SetValue(ValueID& valueid, uint16 value)
#        bool SetValue(ValueID& valueid, uint32 value)
#        bool SetValue(ValueID& valueid, string value)
#        bool SetValueListSelection(ValueID& valueid, string selecteditem)

    def pressButton(self, id):
        '''
.. _pressButton:

Starts an activity in a device.
Since buttons are write-only values that do not report a state,
no notification callbacks are sent.

:param id: The ID of an integer value.
:type id: int
:returns: bool -- True if the activity was started. Returns false if the value is not a ValueID::ValueType_Button. The type can be tested with a call to ValueID::GetType.
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
:returns: bool -- True if the activity was stopped. Returns false if the value is not a ValueID::ValueType_Button. The type can be tested with a call to ValueID::GetType.

        '''
        if values_map.find(id) != values_map.end():
            return self.manager.ReleaseButton(values_map.at(id))
        else :
            return False

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
:returns: bool -- True if the switch point is set.
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
:returns: bool -- True if the switch point is removed.
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
:returns: bool -- True if all switch points are clear.
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
:returns: bool -- True if successful.  Returns False if the value is not a ValueID::ValueType_Schedule. The type can be tested with a call to ValueID::GetType.
:see: setSwitchPoint_, removeSwitchPoint_, clearSwitchPoints_, getNumSwitchPoints_
        '''
        cdef uint8 ohours
        cdef uint8 ominutes
        cdef int8 osetback
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
:returns: The number of switch points defined in this schedule.  Returns zero if the value is not a ValueID::ValueType_Schedule. The type can be tested with a call to ValueID::GetType.
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
    def setConfigParam(self, homeid, nodeid, param, value):
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
:returns: bool -- True if the a message setting the value was sent to the device.
:see: requestConfigParam_, requestAllConfigParams_
        '''
        return self.manager.SetConfigParam(homeid, nodeid, param, value)

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
:see: requestAllConfigParams_, setConfigParam_, valueID_, notification_
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
:see: requestConfigParam_, setConfigParam_, valueID_, notification_
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
:returns: int -- The number of groups.
:see: getAssociations, getMaxAssociations, addAssociation, removeAssociation
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
:returns: set -- A set containing IDs of members of the group
:see: getNumGroups, addAssociation, removeAssociation, getMaxAssociations
        '''
        retval = None
        cdef uint32 size = self.manager.GetMaxAssociations(homeid, nodeid, groupidx)
        #Allocate memory
        cdef uint8** dbuf = <uint8**>malloc(sizeof(uint8) * size)
        # return value is pointer to uint8[]
        cdef uint32 count = self.manager.GetAssociations(homeid, nodeid, groupidx, dbuf)
        cdef uint8* retuint8 = <uint8*>malloc(sizeof(uint8)*count)
        cdef uint8* p
        cdef uint32 start = 0
        if count:
            try:
                data = list()
                p = dbuf[0] # p is now pointing at first element of array
                for i in range(start, count):
                    retuint8[i] = p[0]
                    data.add(retuint8[i])
                    p += 1
                retval = tuple(data)
            finally:
                # Free memory
                free(dbuf)
                pass
        return retval

    def getMaxAssociations(self, homeid, nodeid, groupidx):
        '''
.. _getMaxAssociations:

Gets the maximum number of associations for a group.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node whose associations we are interested in.
:type nodeId: int
:param groupIdx: One-based index of the group (because Z-Wave product manuals use one-based group numbering).
:type groupIdx: int
:returns: int -- The maximum number of nodes that can be associated into the group.
:see: getNumGroups, addAssociation, removeAssociation, getAssociations
        '''
        return self.manager.GetMaxAssociations(homeid, nodeid, groupidx)

    def getGroupLabel(self, homeid, nodeid, groupidx):
        '''
Returns a label for the particular group of a node.

.. _getGroupLabel:

This label is populated by the device specific configuration files.

:param homeId: The Home ID of the Z-Wave controller that manages the node.
:type homeId: int
:param nodeId: The ID of the node whose associations are to be changed.
:type nodeId: int
:param groupIdx: One-based index of the group (because Z-Wave product manuals use one-based group numbering).
:type groupIdx: int
:see: getNumGroups_, getAssociations_, getMaxAssociations_, addAssociation_
        '''
        cdef string c_string = self.manager.GetGroupLabel(homeid, nodeid, groupidx)
        return c_string.c_str()

    def addAssociation(self, homeid, nodeid, groupidx, targetnodeid):
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
:see: getNumGroups, getAssociations, getMaxAssociations, removeAssociation
        '''
        self.manager.AddAssociation(homeid, nodeid, groupidx, targetnodeid)

    def removeAssociation(self, homeid, nodeid, groupidx, targetnodeid):
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
:see: getNumGroups, getAssociations, getMaxAssociations, addAssociation
        '''
        self.manager.AddAssociation(homeid, nodeid, groupidx, targetnodeid)
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
:see: removeWatcher_, notification_
        '''
        self._watcherCallback = pythonfunc # need to keep a reference to this
        if not self.manager.AddWatcher(callback, <void*>pythonfunc):
            raise ValueError("call to AddWatcher failed")
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

#        #bool BeginControllerCommand(uint32 homeid, Driver::ControllerCommand _command, Driver::pfnControllerCallback_t _callback = NULL, void* _context = NULL, bool _highPower = false, uint8 _nodeId = 0xff )

    def cancelControllerCommand(self, homeid):
        '''
.. _cancelControllerCommand:

Cancels any in-progress command running on a controller.

:param homeId: The Home ID of the Z-Wave controller.
:type homeId: int
:returns: bool -- True if a command was running and was cancelled.
:see: beginControllerCommand_
        '''
        return self.manager.CancelControllerCommand(homeid)

#-----------------------------------------------------------------------------
# Scene commands
#-----------------------------------------------------------------------------

    def getNumScenes(self):
        '''
.. _getNumScenes:

Gets the number of scenes that have been defined

:returns: int -- The number of scenes.
:see: getAllScenes_, sceneExists_, \
createScene_, removeScene_, activateScene_, \
getSceneLabel_, setSceneLabel_ \
removeSceneValue_, addSceneValue_, setSceneValue_, \
sceneGetValues_, SceneGetValueAsBool_, sceneGetValueAsByte_, \
sceneGetValueAsFloat_, sceneGetValueAsInt_, sceneGetValueAsShort_, \
sceneGetValueAsString_
       '''
        return self.manager.GetNumScenes()

    def getAllScenes(self):
        '''
.. _getAllScenes:

Gets a list of all the SceneIds

:returns: list() -- A list() containing neighboring scene IDs
:see: getNumScenes_, sceneExists_, \
createScene_, removeScene_, activateScene_, \
getSceneLabel_, setSceneLabel_ \
removeSceneValue_, addSceneValue_, setSceneValue_, \
sceneGetValues_, SceneGetValueAsBool_, sceneGetValueAsByte_, \
sceneGetValueAsFloat_, sceneGetValueAsInt_, sceneGetValueAsShort_, \
sceneGetValueAsString_
        '''
        retval = None
        cdef uint32 size = self.manager.GetNumScenes()
        # Allocate memory
        cdef uint8** dbuf = <uint8**>malloc(sizeof(uint8)*size)
        # return value is pointer to uint8[]
        cdef uint32 count = self.manager.GetAllScenes(dbuf)
        cdef uint8* retuint8 = <uint8*>malloc(sizeof(uint8)*count)
        cdef uint8* p
        cdef uint32 start = 0
        if count:
            try:
                data = list()
                p = dbuf[0] # p is now pointing at first element of array
                for i in range(start, count):
                    retuint8[i] = p[0]
                    data.add(retuint8[i])
                    p += 1
                retval = data
            finally:
                # Free memory
                free(dbuf)
                pass
        return retval

    def createScene(self):
        '''
.. _createScene:

Create a new Scene passing in Scene ID

:returns: int -- Scene ID used to reference the scene. 0 is failure result.
:see: getNumScenes_, getAllScenes_, sceneExists_, \
removeScene_, activateScene_, \
getSceneLabel_, setSceneLabel_ \
removeSceneValue_, addSceneValue_, setSceneValue_, \
sceneGetValues_, SceneGetValueAsBool_, sceneGetValueAsByte_, \
sceneGetValueAsFloat_, sceneGetValueAsInt_, sceneGetValueAsShort_, \
sceneGetValueAsString_
       '''
        return self.manager.CreateScene()

    def removeScene(self, homeid):
        '''
.. _removeScene:

Remove an existing Scene.

:param sceneId: The unique Scene ID to be removed.
:type sceneId: int
:returns: bool -- True if scene was removed.
:see: getNumScenes_, getAllScenes_, sceneExists_, \
createScene_, activateScene_, \
getSceneLabel_, setSceneLabel_ \
removeSceneValue_, addSceneValue_, setSceneValue_, \
sceneGetValues_, SceneGetValueAsBool_, sceneGetValueAsByte_, \
sceneGetValueAsFloat_, sceneGetValueAsInt_, sceneGetValueAsShort_, \
sceneGetValueAsString_
        '''
        return self.manager.RemoveScene(homeid)

    def addSceneValue(self, uint8 sceneid, id, value):
        '''
.. _addSceneValue:

Add a ValueID of value to an existing scene.

Actually I don't know how to use it :)

:param sceneId: The ID of a scene.
:type id: int
:param valueId: The ID of a value.
:type valueId: int
:param value: The value to set
:type value: bool, int, float, string
:returns: int -- An integer representing the result of the operation
    0 : The C method fails
    1 : The C method succeed
    2 : Can't find id in the map
:see: getNumScenes_, getAllScenes_, sceneExists_, \
createScene_, removeScene_, activateScene_, \
getSceneLabel_, setSceneLabel_ \
removeSceneValue_, setSceneValue_, \
sceneGetValues_, SceneGetValueAsBool_, sceneGetValueAsByte_, \
sceneGetValueAsFloat_, sceneGetValueAsInt_, sceneGetValueAsShort_, \
sceneGetValueAsString_
        '''
        cdef float type_float
        cdef bool type_bool
        cdef uint8 type_byte
        cdef int32 type_int
        cdef int16 type_short
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
        return ret

    def setSceneValue(self, uint8 sceneid, id, value):
        '''
.. _setSceneValue:

Set a value to an existing scene's ValueID.

:param sceneId: The ID of a scene.
:type id: int
:param valueId: The ID of a value.
:type valueId: int
:param value: The value to set
:type value: bool, int, float, string
:returns: int -- An integer representing the result of the operation
    0 : The C method fails
    1 : The C method succeed
    2 : Can't find id in the map
:see: getNumScenes_, getAllScenes_, sceneExists_, \
createScene_, removeScene_, activateScene_, \
getSceneLabel_, setSceneLabel_ \
removeSceneValue_, addSceneValue_, \
sceneGetValues_, SceneGetValueAsBool_, sceneGetValueAsByte_, \
sceneGetValueAsFloat_, sceneGetValueAsInt_, sceneGetValueAsShort_, \
sceneGetValueAsString_
        '''
        cdef float type_float
        cdef bool type_bool
        cdef uint8 type_byte
        cdef int32 type_int
        cdef int16 type_short
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
        return ret

    def getSceneLabel(self, sceneid):
        '''
.. _getSceneLabel:

Returns a label for the particular scene.

:param sceneId: The ID of a scene.
:type sceneId: int
:param value: The value to set
:type value: int
:returns: str -- The label string.
:see: getNumScenes_, getAllScenes_, sceneExists_, \
createScene_, removeScene_, activateScene_, \
setSceneLabel_ \
removeSceneValue_, addSceneValue_, setSceneValue_, \
sceneGetValues_, SceneGetValueAsBool_, sceneGetValueAsByte_, \
sceneGetValueAsFloat_, sceneGetValueAsInt_, sceneGetValueAsShort_, \
sceneGetValueAsString_
        '''
        cdef string c_string = self.manager.GetSceneLabel(sceneid)
        return c_string.c_str()

    def setSceneLabel(self, sceneid, char *label):
        '''
.. _setSceneLabel:

Sets a label for the particular scene.

:param sceneId: The ID of the scene.
:type sceneId: int
:param value: The new value of the label.
:type value: int
:see: getNumScenes_, getAllScenes_, sceneExists_, \
createScene_, removeScene_, activateScene_, \
getSceneLabel_ \
removeSceneValue_, addSceneValue_, setSceneValue_, \
sceneGetValues_, SceneGetValueAsBool_, sceneGetValueAsByte_, \
sceneGetValueAsFloat_, sceneGetValueAsInt_, sceneGetValueAsShort_, \
sceneGetValueAsString_
        '''
        self.manager.SetSceneLabel(sceneid, string(label))

    def sceneExists(self, sceneid):
        '''
.. _sceneExists:

Check if a Scene ID is defined.

:param sceneId: The ID of the scene to check.
:type sceneId: int
:returns: bool -- True if Scene ID exists.
:see: getNumScenes_, getAllScenes_, \
createScene_, removeScene_, activateScene_, \
getSceneLabel_, setSceneLabel_ \
removeSceneValue_, addSceneValue_, setSceneValue_, \
sceneGetValues_, SceneGetValueAsBool_, sceneGetValueAsByte_, \
sceneGetValueAsFloat_, sceneGetValueAsInt_, sceneGetValueAsShort_, \
sceneGetValueAsString_
        '''
        return self.manager.SceneExists(sceneid)

    def activateScene(self, sceneid):
        '''
.. _activateScene:

Activate given scene to perform all its actions.

:param sceneId: The ID of the scene to activate.
:type sceneId: int
:returns: bool -- True if it is successful.
:see: getNumScenes_, getAllScenes_, sceneExists_, \
createScene_, removeScene_, \
getSceneLabel_, setSceneLabel_ \
removeSceneValue_, addSceneValue_, setSceneValue_, \
sceneGetValues_, SceneGetValueAsBool_, sceneGetValueAsByte_, \
sceneGetValueAsFloat_, sceneGetValueAsInt_, sceneGetValueAsShort_, \
sceneGetValueAsString_
        '''
        return self.manager.ActivateScene(sceneid)

