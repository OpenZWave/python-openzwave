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
from cython.operator cimport dereference as deref
from libcpp cimport bool
from mylibc cimport uint32, uint64, int32, int16, uint8, int8
from mylibc cimport string
from mylibc cimport malloc, free
from driver cimport DriverData_t, DriverData
from notification cimport Notification, NotificationType, Type_Group, Type_NodeEvent
from notification cimport const_notification, pfnOnNotification_t
from values cimport ValueGenre, ValueType, ValueID
from options cimport Options, Create
from log cimport LogLevel
import os

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
                          string *className, uint8 *classVersion)
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
        bool SetConfigParam(uint32 homeid, uint8 nodeid, uint8 param, uint32 value, uint8 size)
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

