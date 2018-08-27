# -*- coding: utf-8 -*-


"""
command_class.py

This is a very unique module. It handles a variety of things all at once.
It provides the user with command class names and it also matches those names
with a class that represents the actual command class.

By having the classes for each of the command classes it gives an organized
way of adding code that is specific to a specific command class. it removes
the need for a method to check a node to see if it is switch, or if you can
wake it.

this modules when imported for the first time places the instance of a class
object in sys.modules in place of the actual module it's self. This is done to
handle the routing of data that is needed to build a node class as well as
handle user import of command class constants. what I have done is made the
object act as a dict and when a command class is used in the same fashion as
you would to get the value from a dict the class representation of the command
class constant that is passed is returned. If command_class.py is imported as
a whole i used __getattr__ to return the proper object that is being requested.
This gives the means to access the objects that are in the module without the
handler changing anything about.

In the node.py file I have commented on how the nodes are built.

"""
import threading
import time

# ------------- ACTIVE -------------

# Alarm Silence Command Class - Active
# Application
COMMAND_CLASS_SILENCE_ALARM = 0x9D

# Anti-theft Command Class - Active
# Application
COMMAND_CLASS_ANTITHEFT = 0x5D

# Application Status Command Class - Active
# Management
# This Command Class MUST always be in the NIF if supported
COMMAND_CLASS_APPLICATION_STATUS = 0x22

# Association Command Class - Active
# Management
COMMAND_CLASS_ASSOCIATION = 0x85

# Association Command Configuration Command Class - Active
# Management
COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION = 0x9B

# Association Group Information (AGI) Command Class - Active
# Management
COMMAND_CLASS_ASSOCIATION_GRP_INFO = 0x59

# Barrier Operator Command Class - Active
# Application
COMMAND_CLASS_BARRIER_OPERATOR = 0x66

# Basic Command Class - Active
# Application
COMMAND_CLASS_BASIC = 0x20

# Basic Tariff Information Command Class - Active
# Application
COMMAND_CLASS_BASIC_TARIFF_INFO = 0x36

# Battery Command Class - Active
# Management
COMMAND_CLASS_BATTERY = 0x80

# Binary Switch Command Class - Active
# Application
COMMAND_CLASS_SWITCH_BINARY = 0x25

# Central Scene Command Class - Active
# Application
COMMAND_CLASS_CENTRAL_SCENE = 0x5B

# Clock Command Class - Active
# Application
COMMAND_CLASS_CLOCK = 0x81

# Color Switch Command Class - Active
# Application
COMMAND_CLASS_SWITCH_COLOR = 0x33

# Configuration Command Class - Active
# Application
COMMAND_CLASS_CONFIGURATION = 0x70

# Controller Replication Command Class - Active
# Application
COMMAND_CLASS_CONTROLLER_REPLICATION = 0x21

# Demand Control Plan Configuration Command Class - Active
# Application
COMMAND_CLASS_DCP_CONFIG = 0x3A

# Demand Control Plan Monitor Command Class - Active
# Application
COMMAND_CLASS_DCP_MONITOR = 0x3B

# Device Reset Locally Command Class - Active
# Management
COMMAND_CLASS_DEVICE_RESET_LOCALLY = 0x5A

# Door Lock Command Class - Active
# Application
COMMAND_CLASS_DOOR_LOCK = 0x62

# Door Lock Logging Command Class - Active
# Application
COMMAND_CLASS_DOOR_LOCK_LOGGING = 0x4C

# Energy Production Command Class - Active
# Application
COMMAND_CLASS_ENERGY_PRODUCTION = 0x90

# Entry Control Command Class - Active
# Application
COMMAND_CLASS_ENTRY_CONTROL = 0x6F

# Firmware Update Meta Data Command Class - Active
# Management
COMMAND_CLASS_FIRMWARE_UPDATE_MD = 0x7A

# Geographic Location Command Class - Active
# Application
COMMAND_CLASS_GEOGRAPHIC_LOCATION = 0x8C

# HRV Status Command Class - Active
# Application
COMMAND_CLASS_HRV_STATUS = 0x37

# HRV Control Command Class - Active
# Application
COMMAND_CLASS_HRV_CONTROL = 0x39

# Humidity Control Mode Command Class - Active
# Application
COMMAND_CLASS_HUMIDITY_CONTROL_MODE = 0x6D

# Humidity Control Operating State Command Class - Active
# Application
COMMAND_CLASS_HUMIDITY_CONTROL_OPERATING_STATE = 0x6E

# Humidity Control Setpoint Command Class - Active
# Application
COMMAND_CLASS_HUMIDITY_CONTROL_SETPOINT = 0x64

# Inclusion Controller Command Class - Active
# Network-Protocol
# This Command Class MUST always be in the NIF if supported
COMMAND_CLASS_INCLUSION_CONTROLLER = 0x74

# Indicator Command Class - Active
# Management
COMMAND_CLASS_INDICATOR = 0x87

# IP Association Command Class - Active
# Management
COMMAND_CLASS_IP_ASSOCIATION = 0x5C

# Irrigation Command Class - Active
# Application
COMMAND_CLASS_IRRIGATION = 0x6B

# Language Command Class - Active
# Application
COMMAND_CLASS_LANGUAGE = 0x89

# Mailbox Command Class - Active
# Network-Protocol
COMMAND_CLASS_MAILBOX = 0x69

# Manufacturer proprietary Command Class - Active
# Application
COMMAND_CLASS_MANUFACTURER_PROPRIETARY = 0x91

# Manufacturer Specific Command Class - Active
# Management
# Nodes MUST reply to Manufacturer Specific Get Commands received non-securely
# if S0 is the highest granted key (CC:0072.01.00.41.004)
COMMAND_CLASS_MANUFACTURER_SPECIFIC = 0x72

# Mark (Support/Control Mark) - Active
# N/A
# This marker is not an actual Command Class
COMMAND_CLASS_MARK = 0xEF

# Meter Command Class - Active
# Application
COMMAND_CLASS_METER = 0x32

# Meter Table Configuration Command Class - Active
# Application
COMMAND_CLASS_METER_TBL_CONFIG = 0x3C

# Meter Table Monitor Command Class - Active
# Application
COMMAND_CLASS_METER_TBL_MONITOR = 0x3D

# Meter Table Push Configuration Command Class - Active
# Application
COMMAND_CLASS_METER_TBL_PUSH = 0x3E

# Multi Channel Command Class - Active
# Transport-Encapsulation
COMMAND_CLASS_MULTI_CHANNEL = 0x60

# Multi Channel Association Command Class - Active
# Management
COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION = 0x8E

# Multi Command Command Class - Active
# Transport-Encapsulation
# This Command Class MUST always be in the NIF if supported
COMMAND_CLASS_MULTI_CMD = 0x8F

# Multilevel Sensor Command Class - Active
# Application
COMMAND_CLASS_SENSOR_MULTILEVEL = 0x31

# Multilevel Switch Command Class - Active
# Application
COMMAND_CLASS_SWITCH_MULTILEVEL = 0x26

# Network Management Basic Node Command Class - Active
# Network-Protocol
COMMAND_CLASS_NETWORK_MANAGEMENT_BASIC = 0x4D

# Network Management Inclusion Command Class - Active
# Network-Protocol
COMMAND_CLASS_NETWORK_MANAGEMENT_INCLUSION = 0x34

# Network Management Installation and Maintenance Command Class - Active
# Network-Protocol
NETWORK_MANAGEMENT_INSTALLATION_MAINTENANCE = 0x67

# Network Management Proxy Command Class - Active
# Network-Protocol
COMMAND_CLASS_NETWORK_MANAGEMENT_PROXY = 0x52

# No Operation Command Class - Active
# Network-Protocol
COMMAND_CLASS_NO_OPERATION = 0x00

# Node Naming and Location Command Class - Active
# Management
COMMAND_CLASS_NODE_NAMING = 0x77

# Node Provisioning Command Class - Active
# Network-Protocol
COMMAND_CLASS_NODE_PROVISIONING = 0x78

# Notification Command Class - Active
# Application
COMMAND_CLASS_NOTIFICATION = 0x71

# Powerlevel Command Class - Active
# Network-Protocol
COMMAND_CLASS_POWERLEVEL = 0x73

# Prepayment Command Class - Active
# Application
COMMAND_CLASS_PREPAYMENT = 0x3F

# Prepayment Encapsulation Command Class - Active
# Application
COMMAND_CLASS_PREPAYMENT_ENCAPSULATION = 0x41

# Protection Command Class - Active
# Application
COMMAND_CLASS_PROTECTION = 0x75

# Rate Table Configuration Command Class - Active
# Application
COMMAND_CLASS_RATE_TBL_CONFIG = 0x48

# Rate Table Monitor Command Class - Active
# Application
COMMAND_CLASS_RATE_TBL_MONITOR = 0x49

# Scene Activation Command Class - Active
# Application
COMMAND_CLASS_SCENE_ACTIVATION = 0x2B

# Scene Actuator Configuration Command Class - Active
# Application
COMMAND_CLASS_SCENE_ACTUATOR_CONF = 0x2C

# Scene Controller Configuration Command Class - Active
# Application
COMMAND_CLASS_SCENE_CONTROLLER_CONF = 0x2D

# Schedule Command Class - Active
# Application
COMMAND_CLASS_SCHEDULE = 0x53

# Screen Attributes Command Class - Active
# Application
COMMAND_CLASS_SCREEN_ATTRIBUTES = 0x93

# Screen Meta Data Command Class - Active
# Application
COMMAND_CLASS_SCREEN_MD = 0x92

# Security 0 Command Class - Active
# Transport-Encapsulation
COMMAND_CLASS_SECURITY = 0x98

# Security 2 Command Class - Active
# Transport-Encapsulation
# This Command Class MUST always be in the NIF if supported
COMMAND_CLASS_SECURITY_2 = 0x9F

# Security Mark (Unsecure/Secure Mark) - Active
# N/A
# This marker is not an actual Command Class
COMMAND_CLASS_SECURITY_SCHEME0_MARK = 0xF100

# Simple AV Control Command Class - Active
# Application
COMMAND_CLASS_SIMPLE_AV_CONTROL = 0x94

# Sound Switch Command Class - Active
# Application
COMMAND_CLASS_SOUND_SWITCH = 0x79

# Supervision Command Class - Active
# Transport-Encapsulation
# This Command Class MUST always be in the NIF if supported
COMMAND_CLASS_SUPERVISION = 0x6C

# Tariff Table Configuration Command Class - Active
# Application
COMMAND_CLASS_TARIFF_CONFIG = 0x4A

# Tariff Table Monitor Command Class - Active
# Application
COMMAND_CLASS_TARIFF_TBL_MONITOR = 0x4B

# Thermostat Fan Mode Command Class - Active
# Application
COMMAND_CLASS_THERMOSTAT_FAN_MODE = 0x44

# Thermostat Fan State Command Class - Active
# Application
COMMAND_CLASS_THERMOSTAT_FAN_STATE = 0x45

# Thermostat Mode Command Class - Active
# Application
COMMAND_CLASS_THERMOSTAT_MODE = 0x40

# Thermostat Operating State Command Class - Active
# Application
COMMAND_CLASS_THERMOSTAT_OPERATING_STATE = 0x42

# Thermostat Setback Command Class - Active
# Application
COMMAND_CLASS_THERMOSTAT_SETBACK = 0x47

# Thermostat Setpoint Command Class - Active
# Application
COMMAND_CLASS_THERMOSTAT_SETPOINT = 0x43

# Time Command Class - Active
# Application
# This Command Class MUST always be in the NIF if supported
COMMAND_CLASS_TIME = 0x8A

# Time Parameters Command Class - Active
# Application
COMMAND_CLASS_TIME_PARAMETERS = 0x8B

# Transport Service Command Class - Active
# Transport-Encapsulation
# This Command Class MUST always be in the NIF if supported
COMMAND_CLASS_TRANSPORT_SERVICE = 0x55

# User Code Command Class - Active
# Application
COMMAND_CLASS_USER_CODE = 0x63

# Version Command Class - Active
# Management
COMMAND_CLASS_VERSION = 0x86

# Wake Up Command Class - Active
# Management
COMMAND_CLASS_WAKE_UP = 0x84

# Window Covering Command Class - Active
# Application
COMMAND_CLASS_WINDOW_COVERING = 0x6A

# Z/IP Command Class - Active
# Network-Protocol
COMMAND_CLASS_ZIP = 0x23

# Z/IP 6LoWPAN Command Class - Active
# Network-Protocol
COMMAND_CLASS_ZIP_6LOWPAN = 0x4F

# Z/IP Gateway Command Class - Active
# Network-Protocol
COMMAND_CLASS_ZIP_GATEWAY = 0x5F

# Z/IP Naming and Location Command Class - Active
# Management
COMMAND_CLASS_ZIP_NAMING = 0x68

# Z/IP ND Command Class - Active
# Network-Protocol
COMMAND_CLASS_ZIP_ND = 0x58

# Z/IP Portal Command Class - Active
# Network-Protocol
COMMAND_CLASS_ZIP_PORTAL = 0x61

# Z-Wave Plus Info Command Class - Active
# Management
# This Command Class MUST always be in the NIF if supported
COMMAND_CLASS_ZWAVEPLUS_INFO = 0x5E

# ----------- DEPRECIATED ----------

# Alarm Command Class - Depreciated
# Application
# Alarm has been renamed/overloaded by the Notification Command Class
COMMAND_CLASS_ALARM = 0x71

# Alarm Sensor Command Class - Depreciated
# Application
COMMAND_CLASS_SENSOR_ALARM = 0x9C

# Binary Sensor Command Class - Depreciated
# Application
COMMAND_CLASS_SENSOR_BINARY = 0x30

# Climate Control Schedule Command Class - Depreciated
# Application
COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE = 0x46

# CRC-16 Encapsulation Command Class - Depreciated
# Transport-Encapsulation
# This Command Class MUST always be in the NIF if supported
COMMAND_CLASS_CRC_16_ENCAP = 0x56

# Grouping Name Command Class - Depreciated
# Management
COMMAND_CLASS_GROUPING_NAME = 0x7B

# Lock Command Class - Depreciated
# Application
COMMAND_CLASS_LOCK = 0x76

# Multilevel Toggle Switch Command Class - Depreciated
# Application
COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL = 0x29

# Proprietary Command Class - Depreciated
# Application
COMMAND_CLASS_PROPRIETARY = 0x88

# Pulse Meter Command Class - Depreciated
# Application
COMMAND_CLASS_METER_PULSE = 0x35

# Schedule Entry Lock Command Class - Depreciated
# Application
COMMAND_CLASS_SCHEDULE_ENTRY_LOCK = 0x4E

# ------------ OBSOLETE ------------

# All Switch Command Class - Obsolete
# Application
COMMAND_CLASS_SWITCH_ALL = 0x27

# Application Capability Command Class - Obsolete
# Management
COMMAND_CLASS_APPLICATION_CAPABILITY = 0x57

# Basic Window Covering Command Class - Obsolete
# Application
COMMAND_CLASS_BASIC_WINDOW_COVERING = 0x50

# Binary Toggle Switch Command Class - Obsolete
# Application
COMMAND_CLASS_SWITCH_TOGGLE_BINARY = 0x28

# Hail Command Class - Obsolete
# Management
COMMAND_CLASS_HAIL = 0x82

# IP Configuration Command Class - Obsolete
# Management
COMMAND_CLASS_IP_CONFIGURATION = 0x9A

# Move To Position Window Covering Command Class - Obsolete
# Application
COMMAND_CLASS_MTP_WINDOW_COVERING = 0x51

# Network Management Primary Command Class - Obsolete
# Network-Protocol
COMMAND_CLASS_NETWORK_MANAGEMENT_PRIMARY = 0x54

# Remote Association Activation Command Class - Obsolete
# Management
COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE = 0x7C

# Remote Association Configuration Command Class - Obsolete
# Management
COMMAND_CLASS_REMOTE_ASSOCIATION = 0x7D

# Sensor Configuration Command Class - Obsolete
# Application
COMMAND_CLASS_SENSOR_CONFIGURATION = 0x9E


ALARM = COMMAND_CLASS_ALARM
ANTITHEFT = COMMAND_CLASS_ANTITHEFT
APPLICATION_CAPABILITY = COMMAND_CLASS_APPLICATION_CAPABILITY
APPLICATION_STATUS = COMMAND_CLASS_APPLICATION_STATUS
ASSOCIATION = COMMAND_CLASS_ASSOCIATION
ASSOCIATION_COMMAND_CONFIGURATION = (
    COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION
)
ASSOCIATION_GRP_INFO = COMMAND_CLASS_ASSOCIATION_GRP_INFO
BARRIER_OPERATOR = COMMAND_CLASS_BARRIER_OPERATOR
BASIC = COMMAND_CLASS_BASIC
BASIC_TARIFF_INFO = COMMAND_CLASS_BASIC_TARIFF_INFO
BASIC_WINDOW_COVERING = COMMAND_CLASS_BASIC_WINDOW_COVERING
BATTERY = COMMAND_CLASS_BATTERY
CENTRAL_SCENE = COMMAND_CLASS_CENTRAL_SCENE
CLIMATE_CONTROL_SCHEDULE = COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE
CLOCK = COMMAND_CLASS_CLOCK
CONFIGURATION = COMMAND_CLASS_CONFIGURATION
CONTROLLER_REPLICATION = COMMAND_CLASS_CONTROLLER_REPLICATION
CRC_16_ENCAP = COMMAND_CLASS_CRC_16_ENCAP
DCP_CONFIG = COMMAND_CLASS_DCP_CONFIG
DCP_MONITOR = COMMAND_CLASS_DCP_MONITOR
DEVICE_RESET_LOCALLY = COMMAND_CLASS_DEVICE_RESET_LOCALLY
DOOR_LOCK = COMMAND_CLASS_DOOR_LOCK
DOOR_LOCK_LOGGING = COMMAND_CLASS_DOOR_LOCK_LOGGING
ENERGY_PRODUCTION = COMMAND_CLASS_ENERGY_PRODUCTION
ENTRY_CONTROL = COMMAND_CLASS_ENTRY_CONTROL
FIRMWARE_UPDATE_MD = COMMAND_CLASS_FIRMWARE_UPDATE_MD
GEOGRAPHIC_LOCATION = COMMAND_CLASS_GEOGRAPHIC_LOCATION
GROUPING_NAME = COMMAND_CLASS_GROUPING_NAME
HAIL = COMMAND_CLASS_HAIL
HRV_CONTROL = COMMAND_CLASS_HRV_CONTROL
HRV_STATUS = COMMAND_CLASS_HRV_STATUS
HUMIDITY_CONTROL_MODE = COMMAND_CLASS_HUMIDITY_CONTROL_MODE
HUMIDITY_CONTROL_OPERATING_STATE = (
    COMMAND_CLASS_HUMIDITY_CONTROL_OPERATING_STATE
)
HUMIDITY_CONTROL_SETPOINT = COMMAND_CLASS_HUMIDITY_CONTROL_SETPOINT
INCLUSION_CONTROLLER = COMMAND_CLASS_INCLUSION_CONTROLLER
INDICATOR = COMMAND_CLASS_INDICATOR
IP_ASSOCIATION = COMMAND_CLASS_IP_ASSOCIATION
IP_CONFIGURATION = COMMAND_CLASS_IP_CONFIGURATION
IRRIGATION = COMMAND_CLASS_IRRIGATION
LANGUAGE = COMMAND_CLASS_LANGUAGE
LOCK = COMMAND_CLASS_LOCK
MAILBOX = COMMAND_CLASS_MAILBOX
MANUFACTURER_PROPRIETARY = COMMAND_CLASS_MANUFACTURER_PROPRIETARY
MANUFACTURER_SPECIFIC = COMMAND_CLASS_MANUFACTURER_SPECIFIC
MARK = COMMAND_CLASS_MARK
METER = COMMAND_CLASS_METER
METER_PULSE = COMMAND_CLASS_METER_PULSE
METER_TBL_CONFIG = COMMAND_CLASS_METER_TBL_CONFIG
METER_TBL_MONITOR = COMMAND_CLASS_METER_TBL_MONITOR
METER_TBL_PUSH = COMMAND_CLASS_METER_TBL_PUSH
MTP_WINDOW_COVERING = COMMAND_CLASS_MTP_WINDOW_COVERING
MULTI_CHANNEL = COMMAND_CLASS_MULTI_CHANNEL
MULTI_CHANNEL_ASSOCIATION = COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION
MULTI_CMD = COMMAND_CLASS_MULTI_CMD
NETWORK_MANAGEMENT_BASIC = COMMAND_CLASS_NETWORK_MANAGEMENT_BASIC
NETWORK_MANAGEMENT_INCLUSION = COMMAND_CLASS_NETWORK_MANAGEMENT_INCLUSION
NETWORK_MANAGEMENT_PRIMARY = COMMAND_CLASS_NETWORK_MANAGEMENT_PRIMARY
NETWORK_MANAGEMENT_PROXY = COMMAND_CLASS_NETWORK_MANAGEMENT_PROXY
NODE_NAMING = COMMAND_CLASS_NODE_NAMING
NODE_PROVISIONING = COMMAND_CLASS_NODE_PROVISIONING
NOTIFICATION = COMMAND_CLASS_NOTIFICATION
NO_OPERATION = COMMAND_CLASS_NO_OPERATION
POWERLEVEL = COMMAND_CLASS_POWERLEVEL
PREPAYMENT = COMMAND_CLASS_PREPAYMENT
PREPAYMENT_ENCAPSULATION = COMMAND_CLASS_PREPAYMENT_ENCAPSULATION
PROPRIETARY = COMMAND_CLASS_PROPRIETARY
PROTECTION = COMMAND_CLASS_PROTECTION
RATE_TBL_CONFIG = COMMAND_CLASS_RATE_TBL_CONFIG
RATE_TBL_MONITOR = COMMAND_CLASS_RATE_TBL_MONITOR
REMOTE_ASSOCIATION = COMMAND_CLASS_REMOTE_ASSOCIATION
REMOTE_ASSOCIATION_ACTIVATE = COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE
SCENE_ACTIVATION = COMMAND_CLASS_SCENE_ACTIVATION
SCENE_ACTUATOR_CONF = COMMAND_CLASS_SCENE_ACTUATOR_CONF
SCENE_CONTROLLER_CONF = COMMAND_CLASS_SCENE_CONTROLLER_CONF
SCHEDULE = COMMAND_CLASS_SCHEDULE
SCHEDULE_ENTRY_LOCK = COMMAND_CLASS_SCHEDULE_ENTRY_LOCK
SCREEN_ATTRIBUTES = COMMAND_CLASS_SCREEN_ATTRIBUTES
SCREEN_MD = COMMAND_CLASS_SCREEN_MD
SECURITY = COMMAND_CLASS_SECURITY
SECURITY_2 = COMMAND_CLASS_SECURITY_2
SECURITY_SCHEME0_MARK = COMMAND_CLASS_SECURITY_SCHEME0_MARK
SENSOR_ALARM = COMMAND_CLASS_SENSOR_ALARM
SENSOR_BINARY = COMMAND_CLASS_SENSOR_BINARY
SENSOR_CONFIGURATION = COMMAND_CLASS_SENSOR_CONFIGURATION
SENSOR_MULTILEVEL = COMMAND_CLASS_SENSOR_MULTILEVEL
SILENCE_ALARM = COMMAND_CLASS_SILENCE_ALARM
SIMPLE_AV_CONTROL = COMMAND_CLASS_SIMPLE_AV_CONTROL
SOUND_SWITCH = COMMAND_CLASS_SOUND_SWITCH
SUPERVISION = COMMAND_CLASS_SUPERVISION
SWITCH_ALL = COMMAND_CLASS_SWITCH_ALL
SWITCH_BINARY = COMMAND_CLASS_SWITCH_BINARY
SWITCH_COLOR = COMMAND_CLASS_SWITCH_COLOR
SWITCH_MULTILEVEL = COMMAND_CLASS_SWITCH_MULTILEVEL
SWITCH_TOGGLE_BINARY = COMMAND_CLASS_SWITCH_TOGGLE_BINARY
SWITCH_TOGGLE_MULTILEVEL = COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL
TARIFF_CONFIG = COMMAND_CLASS_TARIFF_CONFIG
TARIFF_TBL_MONITOR = COMMAND_CLASS_TARIFF_TBL_MONITOR
THERMOSTAT_FAN_MODE = COMMAND_CLASS_THERMOSTAT_FAN_MODE
THERMOSTAT_FAN_STATE = COMMAND_CLASS_THERMOSTAT_FAN_STATE
THERMOSTAT_MODE = COMMAND_CLASS_THERMOSTAT_MODE
THERMOSTAT_OPERATING_STATE = COMMAND_CLASS_THERMOSTAT_OPERATING_STATE
THERMOSTAT_SETBACK = COMMAND_CLASS_THERMOSTAT_SETBACK
THERMOSTAT_SETPOINT = COMMAND_CLASS_THERMOSTAT_SETPOINT
TIME = COMMAND_CLASS_TIME
TIME_PARAMETERS = COMMAND_CLASS_TIME_PARAMETERS
TRANSPORT_SERVICE = COMMAND_CLASS_TRANSPORT_SERVICE
USER_CODE = COMMAND_CLASS_USER_CODE
VERSION = COMMAND_CLASS_VERSION
WAKE_UP = COMMAND_CLASS_WAKE_UP
WINDOW_COVERING = COMMAND_CLASS_WINDOW_COVERING
ZIP_6LOWPAN = COMMAND_CLASS_ZIP_6LOWPAN
ZIP_GATEWAY = COMMAND_CLASS_ZIP_GATEWAY
ZIP_NAMING = COMMAND_CLASS_ZIP_NAMING
ZIP_ND = COMMAND_CLASS_ZIP_ND
ZIP_PORTAL = COMMAND_CLASS_ZIP_PORTAL
ZWAVEPLUS_INFO = COMMAND_CLASS_ZWAVEPLUS_INFO


class CommandClassBase(object):

    def __init__(self):
        self._cls_ids = getattr(self, '_cls_ids', [])
        self.values = getattr(self, 'values', {})
        self._network = getattr(self, '_network', None)

    def get_values(self, *_, **__):
        raise NotImplementedError


class Alarm(CommandClassBase):

    ALARM_TYPES = [
        'General',
        'Smoke',
        'Carbon Monoxide',
        'Carbon Dioxide',
        'Heat',
        'Flood',
        'Access Control',
        'Burglar',
        'Power Management',
        'System',
        'Emergency',
        'Clock',
        'Appliance',
        'HomeHealth'
    ]

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_ALARM]

    @property
    def source(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_ALARM and
                value.label == 'SourceNodeId'
            ):
                return self._network.nodes[value.data]

    @property
    def alarm_type(self):

        for value in self.values.values():
            if (
                value == COMMAND_CLASS_ALARM and
                value.label == 'Alarm Type'
            ):
                alarm_type = value.data
                break
        else:
            return

        for value in self.values.values():
            if (
                value == COMMAND_CLASS_ALARM and
                value.label in self.ALARM_TYPES and
                value.data == alarm_type
            ):
                return value.label

    @property
    def alarm_level(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_ALARM and
                value.label == 'Alarm Level'
            ):
                return value.data


class Antitheft(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_ANTITHEFT]


class ApplicationCapability(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_APPLICATION_CAPABILITY]


class ApplicationStatus(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_APPLICATION_STATUS]


class Association(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_ASSOCIATION]

    def get_max_associations(self, groupidx):
        return self.get_max_associations(groupidx)


class AssociationCommandConfiguration(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION]


class AssociationGrpInfo(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_ASSOCIATION_GRP_INFO]

    @property
    def groups(self):
        return self.groups()

    def groups_to_dict(self, extras=('all',)):
        return self.groups_to_dict(extras)


class BarrierOperator(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_BARRIER_OPERATOR]


class Basic(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_BASIC]


class BasicTariffInfo(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_BASIC_TARIFF_INFO]


class BasicWindowCovering(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_BASIC_WINDOW_COVERING]

        self.open = self.Open(self)
        self.close = self.Close(self)


    class Open(object):
        def __init__(self, parent):
            self.__parent = parent

        def __enter__(self):
            for value in self.__parent.values:
                if (
                    value == COMMAND_CLASS_BASIC_WINDOW_COVERING and
                    value.label == 'Open'
                ):
                    value.data = True
            return self

        def __exit__(self, *_):
            for value in self.__parent.values:
                if (
                    value == COMMAND_CLASS_BASIC_WINDOW_COVERING and
                    value.label == 'Open'
                ):
                    value.data = False


    class Close(object):
        def __init__(self, parent):
            self.__parent = parent

        def __enter__(self):
            for value in self.__parent.values:
                if (
                    value == COMMAND_CLASS_BASIC_WINDOW_COVERING and
                    value.label == 'Close'
                ):
                    value.data = True
            return self

        def __exit__(self, *_):
            for value in self.__parent.values:
                if (
                    value == COMMAND_CLASS_BASIC_WINDOW_COVERING and
                    value.label == 'Close'
                ):
                    value.data = False


class Battery(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_BATTERY]

    def get_battery_level(self, value_id=None):
        """
        The battery level of this node.

        :param value_id: The value to retrieve state. If None, retrieve the first value
        :type value_id: int
        :return: The level of this battery
        :rtype: int
        """
        battery_levels = self.battery_levels
        if value_id is None:
            for val in battery_levels:
                return battery_levels[val].data
        elif value_id in battery_levels:
            return battery_levels[value_id].data
        return None

    @property
    def battery_levels(self):
        """
        Retrieve the list of values to consider as batteries.
        Filter rules are :

            command_class = 0x80
            genre = "User"
            type = "Byte"
            readonly = True
            writeonly = False

        :return: The list of switches on this node
        :rtype: dict()
        """
        return self.get_values(
            class_id=COMMAND_CLASS_BATTERY,
            genre='User',
            type='Byte',
            readonly=True,
            writeonly=False
        )


class CentralScene(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_CENTRAL_SCENE]


class ClimateControlSchedule(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE]


class Clock(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_CLOCK]

    @property
    def hour(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_CLOCK and
                value.label == 'Hour'
            ):
                return value.data

    @hour.setter
    def hour(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_CLOCK and
                val.label == 'Hour'
            ):
                val.data = value

    @property
    def day(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_CLOCK and
                value.label == 'Day'
            ):
                return value.data

    @day.setter
    def day(self, value):
        if value in self.DAYS:
            for val in self.values.values():
                if (
                    val == COMMAND_CLASS_CLOCK and
                    val.label == 'Day'
                ):
                    val.data = value

    @property
    def minute(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_CLOCK and
                value.label == 'Minute'
            ):
                return value.data

    @minute.setter
    def minute(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_CLOCK and
                val.label == 'Minute'
            ):
                val.data = value

    @property
    def DAYS(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_CLOCK and
                value.label == 'Day'
            ):
                return value.data_items


class Configuration(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_CONFIGURATION]

    def get_configs(self, readonly='All', writeonly='All'):
        """
        Retrieve the list of configuration parameters.

        Filter rules are :
            command_class = 0x70
            genre = "Config"
            readonly = "All" (default) or as passed in arg

        :param readonly: whether to retrieve readonly configs
        :param writeonly: whether to retrieve writeonly configs
        :return: The list of configuration parameters
        :rtype: dict()
        """
        return self.get_values(
            class_id=0x70,
            genre='Config',
            readonly=readonly,
            writeonly=writeonly
        )

    def set_config(self, value_id, value):
        """
        Set config to value (using value value_id)

        :param value_id: The value to retrieve state
        :type value_id: int
        :param value: Appropriate value for given config
        :type value: any
        """
        if value_id in self.get_configs(readonly=False):
            self.values[value_id].data = value
            return True
        return False

    def get_config(self, value_id=None):
        """
        Set config to value (using value value_id)

        :param value_id: The value to retrieve value. If None, retrieve the first value
        :type value_id: int
        :return: The level of this battery
        :rtype: int
        """
        if value_id is None:
            for val in self.get_configs():
                return self.values[val].data
        elif value_id in self.get_configs():
            return self.values[value_id].data
        return None


class ControllerReplication(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_CONTROLLER_REPLICATION]

    @property
    def replication_node_id(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_CONTROLLER_REPLICATION and
                value.label == 'Node'
            ):
                return value.data

    @replication_node_id.setter
    def replication_node_id(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_CONTROLLER_REPLICATION and
                val.label == 'Node'
            ):
                val.data = value

    @property
    def functions(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_CONTROLLER_REPLICATION and
                value.label == 'Functions'
            ):
                return value.data

    @functions.setter
    def functions(self, value):
        if value in self.FUNCTIONS:
            for val in self.values.values():
                if (
                    val == COMMAND_CLASS_CONTROLLER_REPLICATION and
                    val.label == 'Functions'
                ):
                    val.data = value

    @property
    def FUNCTIONS(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_CONTROLLER_REPLICATION and
                value.label == 'Functions'
            ):
                return value.data_items
        return []

    def replicate(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_CONTROLLER_REPLICATION and
                value.label == 'Replicate'
            ):
                event = threading.Event()
                value.data = True
                event.wait(0.1)
                value.data = False


class Crc16Encap(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_CRC_16_ENCAP]


class DcpConfig(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_DCP_CONFIG]


class DcpMonitor(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_DCP_MONITOR]


class DeviceResetLocally(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_DEVICE_RESET_LOCALLY]


class DoorLock(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_DOOR_LOCK]

    @property
    def lock(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_DOOR_LOCK and
                value.label == 'Lock'
            ):
                return value.data

    @lock.setter
    def lock(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_DOOR_LOCK and
                val.label == 'Lock'
            ):
                val.data = value
                break


class DoorLockLogging(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_DOOR_LOCK_LOGGING]

    @property
    def doorlock_logs(self):

        res = []
        for value in self.values.values():
            if value == COMMAND_CLASS_DOOR_LOCK_LOGGING:
                res += [value.data]
        return res


class EnergyProduction(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_ENERGY_PRODUCTION]


class EntryControl(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_ENTRY_CONTROL]


class FirmwareUpdateMd(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_FIRMWARE_UPDATE_MD]


class GeographicLocation(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_GEOGRAPHIC_LOCATION]


class GroupingName(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_GROUPING_NAME]


class Hail(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_HAIL]


class HrvControl(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_HRV_CONTROL]


class HrvStatus(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        self._cls_ids += [COMMAND_CLASS_HRV_STATUS]


class HumidityControlMode(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_HUMIDITY_CONTROL_MODE]


class HumidityControlOperatingState(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_HUMIDITY_CONTROL_OPERATING_STATE]


class HumidityControlSetpoint(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_HUMIDITY_CONTROL_SETPOINT]


class InclusionController(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_INCLUSION_CONTROLLER]


class Indicator(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_INDICATOR]


class IpAssociation(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_IP_ASSOCIATION]


class IpConfiguration(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_IP_CONFIGURATION]


class Irrigation(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_IRRIGATION]


class Language(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_LANGUAGE]


class Lock(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_LOCK]


class Mailbox(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_MAILBOX]


class ManufacturerProprietary(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_MANUFACTURER_PROPRIETARY]


class ManufacturerSpecific(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_MANUFACTURER_SPECIFIC]


class Mark(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_MARK]


class Meter(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_METER]


class MeterPulse(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_METER_PULSE]


class MeterTblConfig(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_METER_TBL_CONFIG]


class MeterTblMonitor(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_METER_TBL_MONITOR]


class MeterTblPush(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_METER_TBL_PUSH]


class MtpWindowCovering(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_MTP_WINDOW_COVERING]


class MultiChannel(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_MULTI_CHANNEL]


class MultiChannelAssociation(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION]


class MultiCmd(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_MULTI_CMD]


class NetworkManagementBasic(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_NETWORK_MANAGEMENT_BASIC]


class NetworkManagementInclusion(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_NETWORK_MANAGEMENT_INCLUSION]


class NetworkManagementPrimary(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_NETWORK_MANAGEMENT_PRIMARY]


class NetworkManagementProxy(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_NETWORK_MANAGEMENT_PROXY]


class NodeNaming(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_NODE_NAMING]


class NodeProvisioning(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_NODE_PROVISIONING]


class Notification(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_NOTIFICATION]


class NoOperation(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_NO_OPERATION]


class Powerlevel(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_POWERLEVEL]

    def get_power_level(self, value_id=None):
        """
        The power level of this node.

        :param value_id: The value to retrieve state. If None, retrieve the first value
        :type value_id: int
        :return: The power level
        :rtype: int
        """
        power_levels = self.power_levels
        if value_id is None:
            for val in power_levels:
                return power_levels[val].data
        elif value_id in power_levels:
            return power_levels[value_id].data
        return None

    @property
    def power_levels(self):
        """
        Retrieve the list of values to consider as power_levels.
        Filter rules are :

            command_class = 0x73
            genre = "User"
            type = "Byte"
            readonly = True
            writeonly = False

        :return: The list of switches on this node
        :rtype: dict()
        """
        return self.get_values(
            class_id=COMMAND_CLASS_POWERLEVEL,
            genre='User',
            type='Byte',
            readonly=True,
            writeonly=False
        )

    def test_power_level(self, db):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_POWERLEVEL and
                value.label == 'Test Powerlevel'
            ):
                value.data = db
                break

    def test_node(self):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_POWERLEVEL and
                val.label == 'Test Node'
            ):
                val.data = 1

    @property
    def acked_frames(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_POWERLEVEL and
                value.label == 'Acked Frames'
            ):
                return value.data

    @property
    def frame_count(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_POWERLEVEL and
                value.label == 'Frame Count'
            ):
                return value.data


class Prepayment(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_PREPAYMENT]


class PrepaymentEncapsulation(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_PREPAYMENT_ENCAPSULATION]


class Proprietary(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_PROPRIETARY]


class Protection(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_PROTECTION]

    @property
    def protections(self):
        """
        Retrieve the list of values to consider as protection.
        Filter rules are :

            command_class = 0x75
            genre = "User"
            readonly = True
            writeonly = False

        :return: The list of switches on this node
        :rtype: dict()

        """
        return self.get_values(
            class_id=COMMAND_CLASS_PROTECTION,
            genre='System',
            type='List',
            readonly=False,
            writeonly=False
        )

    def set_protection(self, value_id, value):
        """
        The command 0x75 (COMMAND_CLASS_PROTECTION) of this node.
        Set protection to value (using value value_id).

        :param value_id: The value to set protection
        :type value_id: int
        :param value: A predefined string
        :type value: str

        """
        protections = self.protections
        if value_id in protections:
            protections[value_id].data = value
            return True
        return False

    def get_protection_item(self, value_id):
        """
        The command 0x75 (COMMAND_CLASS_PROTECTION) of this node.
        Return the current value (using value value_id) of a protection.

        :param value_id: The value to retrieve protection value
        :type value_id: int
        :return: The value of the value
        :rtype: str

        """
        protections = self.protections
        if value_id in protections:
            return protections[value_id].data

    def get_protection_items(self, value_id):
        """
        The command 0x75 (COMMAND_CLASS_PROTECTION) of this node.
        Return the all the possible values (using value value_id) of a protection.

        :param value_id: The value to retrieve items list
        :type value_id: int
        :return: The value of the value
        :rtype: set()

        """
        protections = self.protections
        if value_id in protections:
            return protections[value_id].data_items


class RateTblConfig(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_RATE_TBL_CONFIG]


class RateTblMonitor(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_RATE_TBL_MONITOR]


class RemoteAssociation(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_REMOTE_ASSOCIATION]


class RemoteAssociationActivate(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE]


class SceneActivation(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SCENE_ACTIVATION]


class SceneActuatorConf(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SCENE_ACTUATOR_CONF]


class SceneControllerConf(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SCENE_CONTROLLER_CONF]


class Schedule(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SCHEDULE]


class ScheduleEntryLock(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SCHEDULE_ENTRY_LOCK]


class ScreenAttributes(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SCREEN_ATTRIBUTES]


class ScreenMd(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SCREEN_MD]


class Security(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SECURITY]

    @property
    def is_secure(self):
        for value in self.values.values():
            if value.label == 'Secured' and value == COMMAND_CLASS_SECURITY:
                return value.data
        return False


class Security2(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SECURITY_2]


class SecurityScheme0Mark(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SECURITY_SCHEME0_MARK]


class SensorAlarm(CommandClassBase):
    SENSOR_TYPES = [
        'General',
        'Smoke',
        'Carbon Monoxide',
        'Carbon Dioxide',
        'Heat',
        'Flood'
    ]

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SENSOR_ALARM]

    @property
    def sensor_types(self):
        res = []
        for value in self.values.values():
            if (
                value.label in self.SENSOR_TYPES and
                value == COMMAND_CLASS_SENSOR_ALARM
            ):
                res += [value.label]
        return res

    @property
    def states(self):
        res = {}
        for value in self.values.values():
            if (
                value.label in self.SENSOR_TYPES and
                value == COMMAND_CLASS_SENSOR_ALARM
            ):
                res[value.label] = value.data
        return res


class SensorBinary(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SENSOR_BINARY]

    @property
    def state(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SENSOR_BINARY and
                value.label == 'Sensor'
            ):
                return value.data


class SensorConfiguration(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SENSOR_CONFIGURATION]


class SensorMultilevel(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SENSOR_MULTILEVEL]


class SilenceAlarm(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SILENCE_ALARM]


class SimpleAvControl(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SIMPLE_AV_CONTROL]


class SoundSwitch(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SOUND_SWITCH]


class Supervision(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SUPERVISION]


class SwitchAll(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SWITCH_ALL]

    def set_switch_all(self, value_id, value):
        """
        The command 0x27 (COMMAND_CLASS_SWITCH_ALL) of this node.
        Set switches_all to value (using value value_id).

        :param value_id: The value to retrieve state
        :type value_id: int
        :param value: A predefined string
        :type value: str

        """
        if value_id in self.values:
            self.values[value_id].data = value
            return True
        return False

    def get_switch_all_state(self, value_id):
        """
        The command 0x27 (COMMAND_CLASS_SWITCH_ALL) of this node.
        Return the state (using value value_id) of a switch or a dimmer.

        :param value_id: The value to retrieve state
        :type value_id: int
        :return: The state of the value
        :rtype: bool

        """
        if value_id in self.values:
            instance = self.values[value_id].instance
            for switch in self.values:
                if self.values[switch].instance == instance:
                    return self.values[switch].data
            for dimmer in self.values:
                if self.values[dimmer].instance == instance:
                    if self.values[dimmer].data == 0:
                        return False
                    else:
                        return True
        return None

    def get_switch_all_item(self, value_id):
        """
        The command 0x27 (COMMAND_CLASS_SWITCH_ALL) of this node.
        Return the current value (using value value_id) of a switch_all.

        :param value_id: The value to retrieve switch_all value
        :type value_id: int
        :return: The value of the value
        :rtype: str

        """
        if value_id in self.values:
            return self.values[value_id].data
        return None

    def get_switch_all_items(self, value_id):
        """
        The command 0x27 (COMMAND_CLASS_SWITCH_ALL) of this node.
        Return the all the possible values (using value value_id) of a switch_all.

        :param value_id: The value to retrieve items list
        :type value_id: int
        :return: The value of the value
        :rtype: set()

        """
        if value_id in self.values:
            return self.values[value_id].data_items
        return None


class SwitchBinary(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SWITCH_BINARY]

    @property
    def state(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_BINARY and
                value.label == 'Switch'
            ):
                return value.data

    @state.setter
    def state(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_SWITCH_BINARY and
                val.label == 'Switch'
            ):
                    val.data = value
                    break


class SwitchColor(CommandClassBase):
    COLORIDX_WARMWHITE = 0
    COLORIDX_COLDWHITE = 1
    COLORIDX_RED = 2
    COLORIDX_GREEN = 3
    COLORIDX_BLUE = 4
    COLORIDX_AMBER = 5
    COLORIDX_CYAN = 6
    COLORIDX_PURPLE = 7
    COLORIDX_INDEXCOLOR = 8

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SWITCH_COLOR]

    @property
    def warm_white(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_COLOR and
                value.index == self.COLORIDX_WARMWHITE
            ):
                return value.data

    @warm_white.setter
    def warm_white(self, value):
        if value < 0x00:
            value = 0x00
        elif value > 0xFF:
            value = 0xFF

        for val in self.values.values():
            if (
                val == COMMAND_CLASS_SWITCH_COLOR and
                val.index == self.COLORIDX_WARMWHITE
            ):
                val.data = value

    @property
    def cold_white(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_COLOR and
                value.index == self.COLORIDX_COLDWHITE
            ):
                return value.data

    @cold_white.setter
    def cold_white(self, value):
        if value < 0x00:
            value = 0x00
        elif value > 0xFF:
            value = 0xFF

        for val in self.values.values():
            if (
                val == COMMAND_CLASS_SWITCH_COLOR and
                val.index == self.COLORIDX_COLDWHITE
            ):
                val.data = value

    @property
    def red(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_COLOR and
                value.index == self.COLORIDX_RED
            ):
                return value.data

    @red.setter
    def red(self, value):
        if value < 0x00:
            value = 0x00
        elif value > 0xFF:
            value = 0xFF

        for val in self.values.values():
            if (
                val == COMMAND_CLASS_SWITCH_COLOR and
                val.index == self.COLORIDX_RED
            ):
                val.data = value

    @property
    def green(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_COLOR and
                value.index == self.COLORIDX_GREEN
            ):
                return value.data

    @green.setter
    def green(self, value):
        if value < 0x00:
            value = 0x00
        elif value > 0xFF:
            value = 0xFF

        for val in self.values.values():
            if (
                val == COMMAND_CLASS_SWITCH_COLOR and
                val.index == self.COLORIDX_GREEN
            ):
                val.data = value

    @property
    def blue(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_COLOR and
                value.index == self.COLORIDX_BLUE
            ):
                return value.data

    @blue.setter
    def blue(self, value):
        if value < 0x00:
            value = 0x00
        elif value > 0xFF:
            value = 0xFF

        for val in self.values.values():
            if (
                val == COMMAND_CLASS_SWITCH_COLOR and
                val.index == self.COLORIDX_BLUE
            ):
                val.data = value

    @property
    def amber(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_COLOR and
                value.index == self.COLORIDX_AMBER
            ):
                return value.data

    @amber.setter
    def amber(self, value):
        if value < 0x00:
            value = 0x00
        elif value > 0xFF:
            value = 0xFF

        for val in self.values.values():
            if (
                val == COMMAND_CLASS_SWITCH_COLOR and
                val.index == self.COLORIDX_AMBER
            ):
                val.data = value

    @property
    def cyan(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_COLOR and
                value.index == self.COLORIDX_CYAN
            ):
                return value.data

    @cyan.setter
    def cyan(self, value):
        if value < 0x00:
            value = 0x00
        elif value > 0xFF:
            value = 0xFF

        for val in self.values.values():
            if (
                val == COMMAND_CLASS_SWITCH_COLOR and
                val.index == self.COLORIDX_CYAN
            ):
                val.data = value

    @property
    def purple(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_COLOR and
                value.index == self.COLORIDX_PURPLE
            ):
                return value.data

    @purple.setter
    def purple(self, value):
        if value < 0x00:
            value = 0x00
        elif value > 0xFF:
            value = 0xFF

        for val in self.values.values():
            if (
                val == COMMAND_CLASS_SWITCH_COLOR and
                val.index == self.COLORIDX_PURPLE
            ):
                val.data = value

    @property
    def index_color(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_COLOR and
                value.index == self.COLORIDX_INDEXCOLOR
            ):
                return value.data

    @index_color.setter
    def index_color(self, value):
        if value < 0x00:
            value = 0x00
        elif value > 0xFF:
            value = 0xFF

        for val in self.values.values():
            if (
                val == COMMAND_CLASS_SWITCH_COLOR and
                val.index == self.COLORIDX_INDEXCOLOR
            ):
                val.data = value


class SwitchMultilevel(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SWITCH_MULTILEVEL]

        self._ramping_event = threading.Event()
        self._ramping_lock = threading.Lock()

    def ramp_up(self, level, speed=0.17, step=1):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_MULTILEVEL and
                value.label == 'Level'
            ):
                break
        else:
            return

        self._ramping_event.set()

        def do(val, stp, spd, lvl):
            with self._ramping_lock:
                self._ramping_event.clear()

                while not self._ramping_event.isSet():

                    new_level = val.data + stp
                    start = time.time()

                    with val as event:
                        val.data = new_level
                        event.wait(spd)

                    if val.data >= lvl:
                        break

                    stop = time.time()

                    finish = (stop - start) * 1000
                    if finish < spd * 1000:
                        self._ramping_event.wait(
                            ((spd * 1000) - finish) / 1000)

        t = threading.Thread(target=do, args=(value, step, speed, level))
        t.daemon = True
        t.start()

    def ramp_down(self, level, speed=0.17, step=1):

        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_MULTILEVEL and
                value.label == 'Level'
            ):
                break
        else:
            return

        self._ramping_event.set()

        def do(val, stp, spd, lvl):
            with self._ramping_lock:
                self._ramping_event.clear()

                while not self._ramping_event.isSet():

                    new_level = val.data - stp
                    start = time.time()

                    with val as event:
                        val.data = new_level
                        event.wait(spd)

                    if val.data <= lvl:
                        break

                    stop = time.time()

                    finish = (stop - start) * 1000
                    if finish < spd * 1000:
                        self._ramping_event.wait(
                            ((spd * 1000) - finish) / 1000)

        t = threading.Thread(target=do, args=(value, step, speed, level))
        t.daemon = True
        t.start()

    @property
    def level(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_MULTILEVEL and
                value.label == 'Level'
            ):
                return value.data

    @level.setter
    def level(self, value):
        if 99 < value < 255:
            value = 99
        elif value < 0:
            value = 0

        self._ramping_event.set()

        for val in self.values.values():
            if (
                val == COMMAND_CLASS_SWITCH_MULTILEVEL and
                val.label == 'Level'
            ):
                val.data = value
                break


class SwitchToggleBinary(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SWITCH_TOGGLE_BINARY]

    def toggle(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_BINARY and
                value.label == 'Toggle Switch'
            ):
                value.data = True
                return

    def toggle_all(self):
        if COMMAND_CLASS_MULTI_CHANNEL in self._cls_ids:
            for value in self.values.values():
                if (
                    value == COMMAND_CLASS_SWITCH_BINARY and
                    value.label == 'Toggle Switch'
                ):
                    value.data = True


class SwitchToggleMultilevel(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        self._cls_ids += [COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL]

    def toggle(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL and
                value.label == 'Level'
            ):
                if value.data:
                    value.data = 0
                else:
                    value.data = 255

    def toggle_all(self):
        if COMMAND_CLASS_MULTI_CHANNEL in self._cls_ids:
            for value in self.values.values():
                if (
                    value == COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL and
                    value.label == 'Level'
                ):
                    if value.data:
                        value.data = 0
                    else:
                        value.data = 255


class TariffConfig(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_TARIFF_CONFIG]


class TariffTblMonitor(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_TARIFF_TBL_MONITOR]


class ThermostatFanMode(CommandClassBase):
    FAN_MODES = [
        'Auto Low',
        'On Low',
        'Auto High',
        'On High',
        'Circulate',
     ]

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_THERMOSTAT_FAN_MODE]

    @property
    def fan_mode(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_THERMOSTAT_FAN_MODE and
                value.label == 'Fan Mode'
            ):
                return value.data

    @fan_mode.setter
    def fan_mode(self, value):
        if value in self.FAN_MODES:
            for val in self.values.values():
                if (
                    val == COMMAND_CLASS_THERMOSTAT_FAN_MODE and
                    val.label == 'Fan Mode'
                ):
                    val.data = value


class ThermostatFanState(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_THERMOSTAT_FAN_STATE]

    @property
    def fan_state(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_THERMOSTAT_FAN_STATE and
                value.label == 'Fan State'
            ):
                return value.data


class ThermostatMode(CommandClassBase):
    MODES = [
        'Off',
        'Heat',
        'Cool',
        'Auto',
        'Aux Heat',
        'Resume',
        'Fan Only',
        'Furnace',
        'Dry Air',
        'Moist Air',
        'Auto Changeover',
        'Heat Econ',
        'Cool Econ',
        'Away',
    ]

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_THERMOSTAT_MODE]

    @property
    def operating_mode(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_THERMOSTAT_MODE
                and value.label == 'Mode'
            ):
                return value.data

    @operating_mode.setter
    def operating_mode(self, value):
        if value in self.MODES:
            for val in self.values.values():
                if (
                    val == COMMAND_CLASS_THERMOSTAT_MODE
                    and val.label == 'Mode'
                ):
                    val.data = value


class ThermostatOperatingState(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_THERMOSTAT_OPERATING_STATE]

    @property
    def operating_state(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_THERMOSTAT_OPERATING_STATE
                and value.label == 'Operating State'
            ):
                return value.data


class ThermostatSetback(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_THERMOSTAT_SETBACK]


class ThermostatSetpoint(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_THERMOSTAT_SETPOINT]

    @property
    def away_heating(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                value.label == 'Away Heating'
            ):
                return value.data

    @away_heating.setter
    def away_heating(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Away Heating'
            ):
                val.data = value

    @property
    def cooling_econ(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                value.label == 'Cooling Econ'
            ):
                return value.data

    @cooling_econ.setter
    def cooling_econ(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Cooling Econ'
            ):
                val.data = value

    @property
    def heating_econ(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                value.label == 'Heating Econ'
            ):
                return value.data

    @heating_econ.setter
    def heating_econ(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Heating Econ'
            ):
                val.data = value

    @property
    def auto_changeover(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                value.label == 'Auto Changeover'
            ):
                return value.data

    @auto_changeover.setter
    def auto_changeover(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Auto Changeover'
            ):
                val.data = value

    @property
    def moist_air(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                value.label == 'Moist Air'
            ):
                return value.data

    @moist_air.setter
    def moist_air(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Moist Air'
            ):
                val.data = value

    @property
    def dry_air(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                value.label == 'Dry Air'
            ):
                return value.data

    @dry_air.setter
    def dry_air(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Dry Air'
            ):
                val.data = value

    @property
    def furnace(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                value.label == 'Furnace'
            ):
                return value.data

    @furnace.setter
    def furnace(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Furnace'
            ):
                val.data = value

    @property
    def heat(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                value.label == 'Heating 1'
            ):
                return value.data

    @heat.setter
    def heat(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Heating 1'
            ):
                val.data = value

    @property
    def cool(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                value.label == 'Cooling 1'
            ):
                return value.data

    @cool.setter
    def cool(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Cooling 1'
            ):
                val.data = value


class Time(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_TIME]


class TimeParameters(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_TIME_PARAMETERS]

    @property
    def date(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_TIME_PARAMETERS and
                value.label == 'Date'
            ):
                return value.data

    @property
    def time(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_TIME_PARAMETERS and
                value.label == 'Time'
            ):
                return value.data

    def set_date_time(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_TIME_PARAMETERS and
                value.label == 'Set Date/Time'
            ):
                event = threading.Event()
                value.data = True
                event.wait(0.1)
                value.data = False
                break


class TransportService(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_TRANSPORT_SERVICE]


class UserCode(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_USER_CODE]

    @property
    def codes(self):
        """
        Retrieves the list of value to consider as usercodes.
        Filter rules are :

            command_class = 0x63
            genre = "User"
            type = "Raw"
            readonly = False
            writeonly = False

        :return: The list of user codes on this node
        :rtype: dict()

        """
        return self.get_values(
            class_id=COMMAND_CLASS_USER_CODE,
            type='Raw',
            genre='User',
            readonly=False,
            writeonly=False,
        )

    def get_code(self, index):
        """
        Retrieve particular usercode value by index.
        Certain values such as user codes have index start from 0
        to max number of usercode supported and is useful for getting
        usercodes by the index.

        :param index: The index of usercode value
        :type index: int
        :return: The user code at given index on this node
        :rtype: ZWaveValue

        """
        codes = self.codes
        for code in codes.values():
            if code.index == index:
                return code.data

    def set_code(self, value_id, value):
        """
        The command 0x63 (COMMAND_CLASS_USER_CODE) of this node.
        Sets usercode to value (using value_id).

        :param value_id: The value to retrieve state from
        :type value_id: int
        :param value: User Code as string
        :type value: str

        """
        codes = self.codes
        if value_id in codes:
            codes[value_id].data = value
            return True
        return False

    def set_code_at_index(self, index, value):
        """
        The command 0x63 (COMMAND_CLASS_USER_CODE) of this node.
        Sets usercode to value (using index of value)

        :param index: The index of value to retrieve state from
        :type index: int
        :param value: User Code as string
        :type value: str

        """
        codes = self.codes
        for code in codes.values():
            if code.index == index:
                code.data = value
                return True
        return False


class Version(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_VERSION]

    @property
    def library_version(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_VERSION and
                value.label == 'Library Version'
            ):
                return value.data

    @property
    def protocol_version(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_VERSION and
                value.label == 'Protocol Version'
            ):
                return value.data

    @property
    def application_version(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_VERSION and
                value.label == 'Application Version'
            ):
                return value.data


class WakeUp(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_WAKE_UP]

    @property
    def wakeup_interval_min(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_WAKE_UP and
                value.label == 'Minimum Wake-up Interval'
            ):
                return value.data

    @wakeup_interval_min.setter
    def wakeup_interval_min(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_WAKE_UP and
                val.label == 'Minimum Wake-up Interval'
            ):
                val.data = value

    @property
    def wakeup_interval_max(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_WAKE_UP and
                value.label == 'Maximum Wake-up Interval'
            ):
                return value.data

    @wakeup_interval_max.setter
    def wakeup_interval_max(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_WAKE_UP and
                val.label == 'Maximum Wake-up Interval'
            ):
                val.data = value

    @property
    def wakeup_interval_default(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_WAKE_UP and
                value.label == 'Default Wake-up Interval'
            ):
                return value.data

    @wakeup_interval_default.setter
    def wakeup_interval_default(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_WAKE_UP and
                val.label == 'Default Wake-up Interval'
            ):
                val.data = value

    @property
    def wakeup_interval_step(self):
        for value in self.values.values():
            if (
                value == COMMAND_CLASS_WAKE_UP and
                value.label == 'Wake-up Interval Step'
            ):
                return value.data

    @wakeup_interval_step.setter
    def wakeup_interval_step(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_WAKE_UP and
                val.label == 'Wake-up Interval Step'
            ):
                val.data = value


class WindowCovering(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_WINDOW_COVERING]


class ZIP(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_ZIP]


class ZIP6Lowpan(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_ZIP_6LOWPAN]


class ZIPGateway(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_ZIP_GATEWAY]


class ZIPNaming(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_ZIP_NAMING]


class ZIPND(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_ZIP_ND]


class ZIPPortal(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_ZIP_PORTAL]


class ZwaveplusInfo(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_ZWAVEPLUS_INFO]


class NetworkManagementInstallationMaintenance(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [NETWORK_MANAGEMENT_INSTALLATION_MAINTENANCE]


class EmptyCommandClass(CommandClassBase):
    pass


class CommandClasses(dict):

    def __init__(self):

        import sys
        mod = sys.modules[__name__]

        kwargs = {
            COMMAND_CLASS_ALARM: Alarm,
            COMMAND_CLASS_ANTITHEFT: Antitheft,
            COMMAND_CLASS_APPLICATION_CAPABILITY: ApplicationCapability,
            COMMAND_CLASS_APPLICATION_STATUS: ApplicationStatus,
            COMMAND_CLASS_ASSOCIATION: Association,
            COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION: (
                AssociationCommandConfiguration
            ),
            COMMAND_CLASS_ASSOCIATION_GRP_INFO: AssociationGrpInfo,
            COMMAND_CLASS_BARRIER_OPERATOR: BarrierOperator,
            COMMAND_CLASS_BASIC: Basic,
            COMMAND_CLASS_BASIC_TARIFF_INFO: BasicTariffInfo,
            COMMAND_CLASS_BASIC_WINDOW_COVERING: BasicWindowCovering,
            COMMAND_CLASS_BATTERY: Battery,
            COMMAND_CLASS_CENTRAL_SCENE: CentralScene,
            COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE: ClimateControlSchedule,
            COMMAND_CLASS_CLOCK: Clock,
            COMMAND_CLASS_CONFIGURATION: Configuration,
            COMMAND_CLASS_CONTROLLER_REPLICATION: ControllerReplication,
            COMMAND_CLASS_CRC_16_ENCAP: Crc16Encap,
            COMMAND_CLASS_DCP_CONFIG: DcpConfig,
            COMMAND_CLASS_DCP_MONITOR: DcpMonitor,
            COMMAND_CLASS_DEVICE_RESET_LOCALLY: DeviceResetLocally,
            COMMAND_CLASS_DOOR_LOCK: DoorLock,
            COMMAND_CLASS_DOOR_LOCK_LOGGING: DoorLockLogging,
            COMMAND_CLASS_ENERGY_PRODUCTION: EnergyProduction,
            COMMAND_CLASS_ENTRY_CONTROL: EntryControl,
            COMMAND_CLASS_FIRMWARE_UPDATE_MD: FirmwareUpdateMd,
            COMMAND_CLASS_GEOGRAPHIC_LOCATION: GeographicLocation,
            COMMAND_CLASS_GROUPING_NAME: GroupingName,
            COMMAND_CLASS_HAIL: Hail,
            COMMAND_CLASS_HRV_CONTROL: HrvControl,
            COMMAND_CLASS_HRV_STATUS: HrvStatus,
            COMMAND_CLASS_HUMIDITY_CONTROL_MODE: HumidityControlMode,
            COMMAND_CLASS_HUMIDITY_CONTROL_OPERATING_STATE: (
                HumidityControlOperatingState
            ),
            COMMAND_CLASS_HUMIDITY_CONTROL_SETPOINT: HumidityControlSetpoint,
            COMMAND_CLASS_INCLUSION_CONTROLLER: InclusionController,
            COMMAND_CLASS_INDICATOR: Indicator,
            COMMAND_CLASS_IP_ASSOCIATION: IpAssociation,
            COMMAND_CLASS_IP_CONFIGURATION: IpConfiguration,
            COMMAND_CLASS_IRRIGATION: Irrigation,
            COMMAND_CLASS_LANGUAGE: Language,
            COMMAND_CLASS_LOCK: Lock,
            COMMAND_CLASS_MAILBOX: Mailbox,
            COMMAND_CLASS_MANUFACTURER_PROPRIETARY: ManufacturerProprietary,
            COMMAND_CLASS_MANUFACTURER_SPECIFIC: ManufacturerSpecific,
            COMMAND_CLASS_MARK: Mark,
            COMMAND_CLASS_METER: Meter,
            COMMAND_CLASS_METER_PULSE: MeterPulse,
            COMMAND_CLASS_METER_TBL_CONFIG: MeterTblConfig,
            COMMAND_CLASS_METER_TBL_MONITOR: MeterTblMonitor,
            COMMAND_CLASS_METER_TBL_PUSH: MeterTblPush,
            COMMAND_CLASS_MTP_WINDOW_COVERING: MtpWindowCovering,
            COMMAND_CLASS_MULTI_CHANNEL: MultiChannel,
            COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION: MultiChannelAssociation,
            COMMAND_CLASS_MULTI_CMD: MultiCmd,
            COMMAND_CLASS_NETWORK_MANAGEMENT_BASIC: NetworkManagementBasic,
            COMMAND_CLASS_NETWORK_MANAGEMENT_INCLUSION: (
                NetworkManagementInclusion
            ),
            COMMAND_CLASS_NETWORK_MANAGEMENT_PRIMARY: NetworkManagementPrimary,
            COMMAND_CLASS_NETWORK_MANAGEMENT_PROXY: NetworkManagementProxy,
            COMMAND_CLASS_NODE_NAMING: NodeNaming,
            COMMAND_CLASS_NODE_PROVISIONING: NodeProvisioning,
            COMMAND_CLASS_NOTIFICATION: Notification,
            COMMAND_CLASS_NO_OPERATION: NoOperation,
            COMMAND_CLASS_POWERLEVEL: Powerlevel,
            COMMAND_CLASS_PREPAYMENT: Prepayment,
            COMMAND_CLASS_PREPAYMENT_ENCAPSULATION: PrepaymentEncapsulation,
            COMMAND_CLASS_PROPRIETARY: Proprietary,
            COMMAND_CLASS_PROTECTION: Protection,
            COMMAND_CLASS_RATE_TBL_CONFIG: RateTblConfig,
            COMMAND_CLASS_RATE_TBL_MONITOR: RateTblMonitor,
            COMMAND_CLASS_REMOTE_ASSOCIATION: RemoteAssociation,
            COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE: (
                RemoteAssociationActivate
            ),
            COMMAND_CLASS_SCENE_ACTIVATION: SceneActivation,
            COMMAND_CLASS_SCENE_ACTUATOR_CONF: SceneActuatorConf,
            COMMAND_CLASS_SCENE_CONTROLLER_CONF: SceneControllerConf,
            COMMAND_CLASS_SCHEDULE: Schedule,
            COMMAND_CLASS_SCHEDULE_ENTRY_LOCK: ScheduleEntryLock,
            COMMAND_CLASS_SCREEN_ATTRIBUTES: ScreenAttributes,
            COMMAND_CLASS_SCREEN_MD: ScreenMd,
            COMMAND_CLASS_SECURITY: Security,
            COMMAND_CLASS_SECURITY_2: Security2,
            COMMAND_CLASS_SECURITY_SCHEME0_MARK: SecurityScheme0Mark,
            COMMAND_CLASS_SENSOR_ALARM: SensorAlarm,
            COMMAND_CLASS_SENSOR_BINARY: SensorBinary,
            COMMAND_CLASS_SENSOR_CONFIGURATION: SensorConfiguration,
            COMMAND_CLASS_SENSOR_MULTILEVEL: SensorMultilevel,
            COMMAND_CLASS_SILENCE_ALARM: SilenceAlarm,
            COMMAND_CLASS_SIMPLE_AV_CONTROL: SimpleAvControl,
            COMMAND_CLASS_SOUND_SWITCH: SoundSwitch,
            COMMAND_CLASS_SUPERVISION: Supervision,
            COMMAND_CLASS_SWITCH_ALL: SwitchAll,
            COMMAND_CLASS_SWITCH_BINARY: SwitchBinary,
            COMMAND_CLASS_SWITCH_COLOR: SwitchColor,
            COMMAND_CLASS_SWITCH_MULTILEVEL: SwitchMultilevel,
            COMMAND_CLASS_SWITCH_TOGGLE_BINARY: SwitchToggleBinary,
            COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL: SwitchToggleMultilevel,
            COMMAND_CLASS_TARIFF_CONFIG: TariffConfig,
            COMMAND_CLASS_TARIFF_TBL_MONITOR: TariffTblMonitor,
            COMMAND_CLASS_THERMOSTAT_FAN_MODE: ThermostatFanMode,
            COMMAND_CLASS_THERMOSTAT_FAN_STATE: ThermostatFanState,
            COMMAND_CLASS_THERMOSTAT_MODE: ThermostatMode,
            COMMAND_CLASS_THERMOSTAT_OPERATING_STATE: ThermostatOperatingState,
            COMMAND_CLASS_THERMOSTAT_SETBACK: ThermostatSetback,
            COMMAND_CLASS_THERMOSTAT_SETPOINT: ThermostatSetpoint,
            COMMAND_CLASS_TIME: Time,
            COMMAND_CLASS_TIME_PARAMETERS: TimeParameters,
            COMMAND_CLASS_TRANSPORT_SERVICE: TransportService,
            COMMAND_CLASS_USER_CODE: UserCode,
            COMMAND_CLASS_VERSION: Version,
            COMMAND_CLASS_WAKE_UP: WakeUp,
            COMMAND_CLASS_WINDOW_COVERING: WindowCovering,
            COMMAND_CLASS_ZIP: ZIP,
            COMMAND_CLASS_ZIP_6LOWPAN: ZIP6Lowpan,
            COMMAND_CLASS_ZIP_GATEWAY: ZIPGateway,
            COMMAND_CLASS_ZIP_NAMING: ZIPNaming,
            COMMAND_CLASS_ZIP_ND: ZIPND,
            COMMAND_CLASS_ZIP_PORTAL: ZIPPortal,
            COMMAND_CLASS_ZWAVEPLUS_INFO: ZwaveplusInfo,
            NETWORK_MANAGEMENT_INSTALLATION_MAINTENANCE: (
                NetworkManagementInstallationMaintenance
            ),
            '__original_module__': mod
        }
        self.__dict__ = mod.__dict__
        dict.__init__(self, **kwargs)
        sys.modules[__name__] = self

    def __missing__(self, key):
        value = EmptyCommandClass
        self.__setitem__(key, value)
        return value


cc = CommandClasses()
