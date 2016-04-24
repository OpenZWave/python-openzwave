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
from cython.operator cimport dereference as deref
from libcpp cimport bool
#from libc.stdint cimport bint
from libcpp.vector cimport vector
from libc.stdint cimport uint32_t, int32_t, uint16_t, int16_t, uint8_t, int8_t
#from libcpp.string cimport string
from mylibc cimport string
from node cimport NodeData
from driver cimport DriverData_t, DriverData
from group cimport InstanceAssociation_t, InstanceAssociation
from driver cimport ControllerInterface, ControllerCommand, ControllerState, pfnControllerCallback_t
from notification cimport Notification, NotificationType, Type_Notification, Type_Group, Type_NodeEvent, const_notification, pfnOnNotification_t
from values cimport ValueGenre, ValueType, ValueID
from options cimport Options
from log cimport LogLevel
import os

ctypedef uint8_t** int_associations
ctypedef InstanceAssociation_t** struct_associations

cdef extern from "Manager.h" namespace "OpenZWave":

    cdef cppclass Manager:
        # // Destructor
        void Destroy()
        # // Configuration
        void WriteConfig(uint32_t homeid)
        Options* GetOptions()
        # // Drivers
        bool AddDriver(string serialport)
        bool RemoveDriver(string controllerPath)
        uint8_t GetControllerNodeId(uint32_t homeid)
        uint8_t GetSUCNodeId(uint32_t homeid)
        bool IsPrimaryController(uint32_t homeid)
        bool IsStaticUpdateController(uint32_t homeid)
        bool IsBridgeController(uint32_t homeid)
        string getVersionAsString()
        string getVersionLongAsString()
        string GetLibraryVersion(uint32_t homeid)
        string GetLibraryTypeName(uint32_t homeid)
        int32_t GetSendQueueCount( uint32_t homeId )
        void LogDriverStatistics( uint32_t homeId )
        void GetDriverStatistics( uint32_t homeId, DriverData* data )
        void GetNodeStatistics( uint32_t homeId, uint8_t nodeid, NodeData* data )
        ControllerInterface GetControllerInterfaceType( uint32_t homeId )
        string GetControllerPath( uint32_t homeId )
        # // Network
        void TestNetworkNode( uint32_t homeId, uint8_t nodeId, uint32_t count )
        void TestNetwork( uint32_t homeId, uint32_t count )
        void HealNetworkNode( uint32_t homeId, uint32_t nodeId, bool _doRR )
        void HealNetwork( uint32_t homeId, bool doRR)
        # // Polling
        uint32_t GetPollInterval()
        void SetPollInterval(uint32_t milliseconds, bIntervalBetweenPolls)
        bool EnablePoll(ValueID& valueId, uint8_t intensity)
        bool DisablePoll(ValueID& valueId)
        bool isPolled(ValueID& valueId)
        void SetPollIntensity( ValueID& valueId, uint8_t intensity)
        uint8_t GetPollIntensity(ValueID& valueId)
        # // Node Information
        bool RefreshNodeInfo(uint32_t homeid, uint8_t nodeid)
        bool RequestNodeState(uint32_t homeid, uint8_t nodeid)
        bool RequestNodeDynamic( uint32_t homeId, uint8_t nodeId )
        bool IsNodeListeningDevice(uint32_t homeid, uint8_t nodeid)
        bool IsNodeFrequentListeningDevice( uint32_t homeId, uint8_t nodeId )
        bool IsNodeBeamingDevice( uint32_t homeId, uint8_t nodeId )
        bool IsNodeRoutingDevice(uint32_t homeid, uint8_t nodeid)
        bool IsNodeSecurityDevice( uint32_t homeId, uint8_t nodeId )
        bool IsNodeZWavePlus( uint32_t homeId, uint8_t nodeId )
        uint32_t GetNodeMaxBaudRate(uint32_t homeid, uint8_t nodeid)
        uint8_t GetNodeVersion(uint32_t homeid, uint8_t nodeid)
        uint8_t GetNodeSecurity(uint32_t homeid, uint8_t nodeid)
        uint8_t GetNodeBasic(uint32_t homeid, uint8_t nodeid)
        uint8_t GetNodeGeneric(uint32_t homeid, uint8_t nodeid)
        uint8_t GetNodeSpecific(uint32_t homeid, uint8_t nodeid)
        string GetNodeType(uint32_t homeid, uint8_t nodeid)
        uint16_t GetNodeDeviceType(uint32_t homeid, uint8_t nodeid)
        string GetNodeDeviceTypeString(uint32_t homeid, uint8_t nodeid)
        uint8_t GetNodeRole(uint32_t homeid, uint8_t nodeid)
        string GetNodeRoleString(uint32_t homeid, uint8_t nodeid)
        uint8_t GetNodePlusType(uint32_t homeid, uint8_t nodeid)
        string GetNodePlusTypeString(uint32_t homeid, uint8_t nodeid)
        uint32_t GetNodeNeighbors(uint32_t homeid, uint8_t nodeid, uint8_t** nodeNeighbors)
        string GetNodeManufacturerName(uint32_t homeid, uint8_t nodeid)
        string GetNodeProductName(uint32_t homeid, uint8_t nodeid)
        string GetNodeName(uint32_t homeid, uint8_t nodeid)
        string GetNodeLocation(uint32_t homeid, uint8_t nodeid)
        string GetNodeManufacturerId(uint32_t homeid, uint8_t nodeid)
        string GetNodeProductType(uint32_t homeid, uint8_t nodeid)
        string GetNodeProductId(uint32_t homeid, uint8_t nodeid)
        void SetNodeManufacturerName(uint32_t homeid, uint8_t nodeid, string manufacturerName)
        void SetNodeProductName(uint32_t homeid, uint8_t nodeid, string productName)
        void SetNodeName(uint32_t homeid, uint8_t nodeid, string productName)
        void SetNodeLocation(uint32_t homeid, uint8_t nodeid, string location)
        void SetNodeOn(uint32_t homeid, uint8_t nodeid)
        void SetNodeOff(uint32_t homeid, uint8_t nodeid)
        void SetNodeLevel(uint32_t homeid, uint8_t nodeid, uint8_t level)
        bool IsNodeInfoReceived(uint32_t homeid, uint8_t nodeid)
        bool IsNodePlusInfoReceived(uint32_t homeid, uint8_t nodeid)
        bool GetNodeClassInformation( uint32_t homeId, uint8_t nodeId, uint8_t commandClassId,
                          string *className, uint8_t *classVersion)
        bool IsNodeAwake(uint32_t homeid, uint8_t nodeid)
        bool IsNodeFailed(uint32_t homeid, uint8_t nodeid)
        string GetNodeQueryStage(uint32_t homeid, uint8_t nodeid)
        uint8_t GetNodeIcon(uint32_t homeid, uint8_t nodeid)
        string GetNodeIconName(uint32_t homeid, uint8_t nodeid)
        # // Values
        string GetValueLabel(ValueID& valueid)
        void SetValueLabel(ValueID& valueid, string value)
        string GetValueUnits(ValueID& valueid)
        void SetValueUnits(ValueID& valueid, string value)
        string GetValueHelp(ValueID& valueid)
        void SetValueHelp(ValueID& valueid, string value)
        uint32_t GetValueMin(ValueID& valueid)
        uint32_t GetValueMax(ValueID& valueid)
        bool IsValueReadOnly(ValueID& valueid)
        bool IsValueWriteOnly(ValueID& valueid)
        bool IsValueSet(ValueID& valueid)
        bool IsValuePolled( ValueID& valueid )
        bool GetValueAsBool(ValueID& valueid, bool* o_value)
        bool GetValueAsByte(ValueID& valueid, uint8_t* o_value)
        bool GetValueAsFloat(ValueID& valueid, float* o_value)
        bool GetValueAsInt(ValueID& valueid, int32_t* o_value)
        bool GetValueAsShort(ValueID& valueid, int16_t* o_value)
        bool GetValueAsRaw(ValueID& valueid, uint8_t** o_value, uint8_t* o_length )
        bool GetValueAsString(ValueID& valueid, string* o_value)
        bool GetValueListSelection(ValueID& valueid, string* o_value)
        bool GetValueListSelection(ValueID& valueid, int32_t* o_value)
        bool GetValueListItems(ValueID& valueid, vector[string]* o_value)
        bool GetValueListValues(ValueID& valueid, vector[int32_t]* o_value)
        bool SetValue(ValueID& valueid, bool value)
        bool SetValue(ValueID& valueid, uint8_t value)
        bool SetValue(ValueID& valueid, float value)
        bool SetValue(ValueID& valueid, int32_t value)
        bool SetValue(ValueID& valueid, int16_t value)
        bool SetValue(ValueID& valueid, uint8_t* value, uint8_t length)
        bool SetValue(ValueID& valueid, string value)
        bool SetValueListSelection(ValueID& valueid, string selecteditem)
        bool RefreshValue(ValueID& valueid)
        void SetChangeVerified(ValueID& valueid, bool verify)
        bool GetChangeVerified(ValueID& valueid)
        bool PressButton(ValueID& valueid)
        bool ReleaseButton(ValueID& valueid)
        bool GetValueFloatPrecision(ValueID& valueid, uint8_t* o_value)
        # // Climate Control
        uint8_t GetNumSwitchPoints(ValueID& valueid)
        bool SetSwitchPoint(ValueID& valueid, uint8_t hours, uint8_t minutes, uint8_t setback)
        bool RemoveSwitchPoint(ValueID& valueid, uint8_t hours, uint8_t minutes)
        bool ClearSwitchPoints(ValueID& valueid)
        bool GetSwitchPoint(ValueID& valueid, uint8_t idx, uint8_t* o_hours, uint8_t* o_minutes, int8_t* o_setback)
        # // SwitchAll
        void SwitchAllOn(uint32_t homeid)
        void SwitchAllOff(uint32_t homeid)
        # // Configuration Parameters
        bool SetConfigParam(uint32_t homeid, uint8_t nodeid, uint8_t param, uint32_t value, uint8_t size)
        void RequestConfigParam(uint32_t homeid, uint8_t nodeid, uint8_t aram)
        void RequestAllConfigParams(uint32_t homeid, uint8_t nodeid)
        # // Groups
        uint8_t GetNumGroups(uint32_t homeid, uint8_t nodeid)
        uint32_t GetAssociations(uint32_t homeid, uint8_t nodeid, uint8_t groupidx, struct_associations o_associations)
#~ cython overloading problem
#~ src-lib/libopenzwave/libopenzwave.pyx:3739:58: no suitable method found
#~         uint32_t GetAssociations(uint32_t homeid, uint8_t nodeid, uint8_t groupidx, int_associations o_associations)
        uint8_t GetMaxAssociations(uint32_t homeid, uint8_t nodeid, uint8_t groupidx)
        string GetGroupLabel(uint32_t homeid, uint8_t nodeid, uint8_t groupidx)
        void AddAssociation(uint32_t homeid, uint8_t nodeid, uint8_t groupidx, uint8_t targetnodeid, uint8_t instance)
        void RemoveAssociation(uint32_t homeid, uint8_t nodeid, uint8_t groupidx, uint8_t targetnodeid, uint8_t instance)
        bool AddWatcher(pfnOnNotification_t notification, void* context)
        bool RemoveWatcher(pfnOnNotification_t notification, void* context)
        # void NotifyWatchers(Notification*)
        # // Controller Commands
        void ResetController(uint32_t homeid)
        void SoftReset(uint32_t homeid)
        #Deprecated
        bool BeginControllerCommand(uint32_t homeid, ControllerCommand _command, pfnControllerCallback_t _callback, void* _context, bool _highPower, uint8_t _nodeId, uint8_t _arg )
        bool CancelControllerCommand(uint32_t homeid)
        bool AddNode(uint32_t homeid, bool _doSecurity)

        bool RemoveNode(uint32_t homeid)
        bool RemoveFailedNode(uint32_t homeid, uint8_t nodeid)
        bool HasNodeFailed(uint32_t homeid, uint8_t nodeid)
        bool ReplaceFailedNode(uint32_t homeid, uint8_t nodeid)
        bool AssignReturnRoute(uint32_t homeid, uint8_t nodeid)
        bool RequestNodeNeighborUpdate(uint32_t homeid, uint8_t nodeid)
        bool RequestNetworkUpdate(uint32_t homeid, uint8_t nodeid)
        bool ReplicationSend(uint32_t homeid, uint8_t nodeid)
        bool DeleteAllReturnRoutes(uint32_t homeid, uint8_t nodeid)
        bool SendNodeInformation(uint32_t homeid, uint8_t nodeid)
        bool CreateNewPrimary(uint32_t homeid)
        bool TransferPrimaryRole(uint32_t homeid)
        bool ReceiveConfiguration(uint32_t homeid)
        bool CreateButton(uint32_t homeid, uint8_t nodeid, uint8_t buttonid)
        bool DeleteButton(uint32_t homeid, uint8_t nodeid, uint8_t buttonid)
        # // Scene commands
        uint8_t GetNumScenes()
        uint8_t GetAllScenes(uint8_t** sceneIds)
        uint8_t CreateScene()
        void RemoveAllScenes( uint32_t _homeId )
        bool RemoveScene(uint8_t sceneId)
        bool AddSceneValue( uint8_t sceneId, ValueID& valueId, bool value)
        bool AddSceneValue( uint8_t sceneId, ValueID& valueId, uint8_t value)
        bool AddSceneValue( uint8_t sceneId, ValueID& valueId, float value )
        bool AddSceneValue( uint8_t sceneId, ValueID& valueId, int32_t value )
        bool AddSceneValue( uint8_t sceneId, ValueID& valueId, int16_t value )
        bool AddSceneValue( uint8_t sceneId, ValueID& valueId, string value )
        bool AddSceneValueListSelection( uint8_t sceneId, ValueID& valueId, string value )
        bool AddSceneValueListSelection( uint8_t sceneId, ValueID& valueId, int32_t value )
        bool RemoveSceneValue( uint8_t sceneId, ValueID& valueId )
        int SceneGetValues( uint8_t sceneId, vector[ValueID]* o_value )
        bool SceneGetValueAsBool( uint8_t sceneId, ValueID& valueId, bool* value )
        bool SceneGetValueAsByte( uint8_t sceneId, ValueID& valueId, uint8_t* o_value )
        bool SceneGetValueAsFloat( uint8_t sceneId, ValueID& valueId, float* o_value )
        bool SceneGetValueAsInt( uint8_t sceneId, ValueID& valueId, int32_t* o_value )
        bool SceneGetValueAsShort( uint8_t sceneId, ValueID& valueId, int16_t* o_value )
        bool SceneGetValueAsString( uint8_t sceneId, ValueID& valueId, string* o_value )
        bool SceneGetValueListSelection( uint8_t sceneId, ValueID& valueId, string* o_value )
        bool SceneGetValueListSelection( uint8_t sceneId, ValueID& valueId, int32_t* o_value )
        bool SetSceneValue( uint8_t sceneId, ValueID& valueId, bool value )
        bool SetSceneValue( uint8_t sceneId, ValueID& valueId, uint8_t value )
        bool SetSceneValue( uint8_t sceneId, ValueID& valueId, float value )
        bool SetSceneValue( uint8_t sceneId, ValueID& valueId, int32_t value )
        bool SetSceneValue( uint8_t sceneId, ValueID& valueId, int16_t value )
        bool SetSceneValue( uint8_t sceneId, ValueID& valueId, string value )
        bool SetSceneValueListSelection( uint8_t sceneId, ValueID& valueId, string value )
        bool SetSceneValueListSelection( uint8_t sceneId, ValueID& valueId, int32_t value )
        string GetSceneLabel( uint8_t sceneId )
        void SetSceneLabel( uint8_t sceneId, string value )
        bool SceneExists( uint8_t sceneId )
        bool ActivateScene( uint8_t sceneId )

cdef extern from "Manager.h" namespace "OpenZWave::Manager":
    Manager* Create()
    Manager* Get()
