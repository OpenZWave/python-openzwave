# -*- coding: utf-8 -*-
"""
This file is part of **python-openzwave**
project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :synopsis: openzwave API

.. moduleauthor: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com> &
 kdschlosser aka Kevin Schlosser

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

# command_class.py
#
# This is a very unique module. It handles a variety of things all at once.
# It provides the user with command class names and it also matches those names
# with a class that represents the actual command class.
#
# By having the classes for each of the command classes it gives an organized
# way of adding code that is specific to a specific command class. it removes
# the need for a method to check a node to see if it is switch, or if you can
# wake it.
#
# this modules when imported for the first time places the instance of a class
# object in sys.modules in place of the actual module it's self. This is done
# to handle the routing of data that is needed to build a node class as well as
# handle user import of command class constants. what I have done is made the
# object act as a dict and when a command class is used in the same fashion as
# you would to get the value from a dict the class representation of the
# command class constant that is passed is returned. If command_class.py is
# imported as a whole i used __getattr__ to return the proper object that is
# being requested. This gives the means to access the objects that are in the
# module without the handler changing anything about.
#
# In the node.py file I have commented on how the nodes are built.

from .command_class_base import EmptyCommandClass

from .silence_alarm import (
    COMMAND_CLASS_SILENCE_ALARM,
    SilenceAlarm
)
from .antitheft import (
    COMMAND_CLASS_ANTITHEFT,
    Antitheft
)
from .application_status import (
    COMMAND_CLASS_APPLICATION_STATUS,
    ApplicationStatus
)
from .association import (
    COMMAND_CLASS_ASSOCIATION,
    Association
)
from .association_command_configuration import (
    COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION,
    AssociationCommandConfiguration
)
from .association_grp_info import (
    COMMAND_CLASS_ASSOCIATION_GRP_INFO,
    AssociationGrpInfo
)
from .barrier_operator import (
    COMMAND_CLASS_BARRIER_OPERATOR,
    BarrierOperator
)
from .basic import (
    COMMAND_CLASS_BASIC,
    Basic
)
from .basic_tariff_info import (
    COMMAND_CLASS_BASIC_TARIFF_INFO,
    BasicTariffInfo
)
from .battery import (
    COMMAND_CLASS_BATTERY,
    Battery
)
from .switch_binary import (
    COMMAND_CLASS_SWITCH_BINARY,
    SwitchBinary
)
from .central_scene import (
    COMMAND_CLASS_CENTRAL_SCENE,
    CentralScene
)
from .clock import (
    COMMAND_CLASS_CLOCK,
    Clock
)
from .switch_color import (
    COMMAND_CLASS_SWITCH_COLOR,
    SwitchColor
)
from .configuration import (
    COMMAND_CLASS_CONFIGURATION,
    Configuration
)
from .controller_replication import (
    COMMAND_CLASS_CONTROLLER_REPLICATION,
    ControllerReplication
)
from .dcp_config import (
    COMMAND_CLASS_DCP_CONFIG,
    DcpConfig
)
from .dcp_monitor import (
    COMMAND_CLASS_DCP_MONITOR,
    DcpMonitor
)
from .device_reset_locally import (
    COMMAND_CLASS_DEVICE_RESET_LOCALLY,
    DeviceResetLocally
)
from .door_lock import (
    COMMAND_CLASS_DOOR_LOCK,
    DoorLock
)
from .door_lock_logging import (
    COMMAND_CLASS_DOOR_LOCK_LOGGING,
    DoorLockLogging
)
from .energy_production import (
    COMMAND_CLASS_ENERGY_PRODUCTION,
    EnergyProduction
)
from .entry_control import (
    COMMAND_CLASS_ENTRY_CONTROL,
    EntryControl
)
from .firmware_update_md import (
    COMMAND_CLASS_FIRMWARE_UPDATE_MD,
    FirmwareUpdateMd
)
from .geographic_location import (
    COMMAND_CLASS_GEOGRAPHIC_LOCATION,
    GeographicLocation
)
from .hrv_status import (
    COMMAND_CLASS_HRV_STATUS,
    HrvStatus
)
from .hrv_control import (
    COMMAND_CLASS_HRV_CONTROL,
    HrvControl
)
from .humidity_control_mode import (
    COMMAND_CLASS_HUMIDITY_CONTROL_MODE,
    HumidityControlMode
)
from .humidity_control_operating_state import (
    COMMAND_CLASS_HUMIDITY_CONTROL_OPERATING_STATE,
    HumidityControlOperatingState
)
from .humidity_control_setpoint import (
    COMMAND_CLASS_HUMIDITY_CONTROL_SETPOINT,
    HumidityControlSetpoint
)
from .inclusion_controller import (
    COMMAND_CLASS_INCLUSION_CONTROLLER,
    InclusionController
)
from .indicator import (
    COMMAND_CLASS_INDICATOR,
    Indicator
)
from .ip_association import (
    COMMAND_CLASS_IP_ASSOCIATION,
    IpAssociation
)
from .irrigation import (
    COMMAND_CLASS_IRRIGATION,
    Irrigation
)
from .language import (
    COMMAND_CLASS_LANGUAGE,
    Language
)
from .mailbox import (
    COMMAND_CLASS_MAILBOX,
    Mailbox
)
from .manufacturer_proprietary import (
    COMMAND_CLASS_MANUFACTURER_PROPRIETARY,
    ManufacturerProprietary
)
from .manufacturer_specific import (
    COMMAND_CLASS_MANUFACTURER_SPECIFIC,
    ManufacturerSpecific
)
from .mark import (
    COMMAND_CLASS_MARK,
    Mark
)
from .meter import (
    COMMAND_CLASS_METER,
    Meter
)
from .meter_tbl_config import (
    COMMAND_CLASS_METER_TBL_CONFIG,
    MeterTblConfig
)
from .meter_tbl_monitor import (
    COMMAND_CLASS_METER_TBL_MONITOR,
    MeterTblMonitor
)
from .meter_tbl_push import (
    COMMAND_CLASS_METER_TBL_PUSH,
    MeterTblPush
)
from .multi_channel import (
    COMMAND_CLASS_MULTI_CHANNEL,
    MultiChannel
)
from .multi_channel_association import (
    COMMAND_CLASS_MULTI_CHANNEL_ASSOCIATION,
    MultiChannelAssociation
)
from .multi_cmd import (
    COMMAND_CLASS_MULTI_CMD,
    MultiCmd
)
from .sensor_multilevel import (
    COMMAND_CLASS_SENSOR_MULTILEVEL,
    SensorMultilevel
)
from .switch_multilevel import (
    COMMAND_CLASS_SWITCH_MULTILEVEL,
    SwitchMultilevel
)
from .network_management_basic import (
    COMMAND_CLASS_NETWORK_MANAGEMENT_BASIC,
    NetworkManagementBasic
)
from .network_management_inclusion import (
    COMMAND_CLASS_NETWORK_MANAGEMENT_INCLUSION,
    NetworkManagementInclusion
)
from .network_management_installation_maintenance import (
    NETWORK_MANAGEMENT_INSTALLATION_MAINTENANCE,
    NetworkManagementInstallationMaintenance
)
from .network_management_proxy import (
    COMMAND_CLASS_NETWORK_MANAGEMENT_PROXY,
    NetworkManagementProxy
)
from .no_operation import (
    COMMAND_CLASS_NO_OPERATION,
    NoOperation
)
from .node_naming import (
    COMMAND_CLASS_NODE_NAMING,
    NodeNaming
)
from .node_provisioning import (
    COMMAND_CLASS_NODE_PROVISIONING,
    NodeProvisioning
)
from .notification import (
    COMMAND_CLASS_NOTIFICATION,
    Notification
)
from .powerlevel import (
    COMMAND_CLASS_POWERLEVEL,
    Powerlevel
)
from .prepayment import (
    COMMAND_CLASS_PREPAYMENT,
    Prepayment
)
from .prepayment_encapsulation import (
    COMMAND_CLASS_PREPAYMENT_ENCAPSULATION,
    PrepaymentEncapsulation
)
from .protection import (
    COMMAND_CLASS_PROTECTION,
    Protection
)
from .rate_tbl_config import (
    COMMAND_CLASS_RATE_TBL_CONFIG,
    RateTblConfig
)
from .rate_tbl_monitor import (
    COMMAND_CLASS_RATE_TBL_MONITOR,
    RateTblMonitor
)
from .scene_activation import (
    COMMAND_CLASS_SCENE_ACTIVATION,
    SceneActivation
)
from .scene_actuator_conf import (
    COMMAND_CLASS_SCENE_ACTUATOR_CONF,
    SceneActuatorConf
)
from .scene_controller_conf import (
    COMMAND_CLASS_SCENE_CONTROLLER_CONF,
    SceneControllerConf
)
from .schedule import (
    COMMAND_CLASS_SCHEDULE,
    Schedule
)
from .screen_attributes import (
    COMMAND_CLASS_SCREEN_ATTRIBUTES,
    ScreenAttributes
)
from .screen_md import (
    COMMAND_CLASS_SCREEN_MD,
    ScreenMd
)
from .security import (
    COMMAND_CLASS_SECURITY,
    Security
)
from .security_2 import (
    COMMAND_CLASS_SECURITY_2,
    Security2
)
from .security_scheme0_mark import (
    COMMAND_CLASS_SECURITY_SCHEME0_MARK,
    SecurityScheme0Mark
)
from .simple_av_control import (
    COMMAND_CLASS_SIMPLE_AV_CONTROL,
    SimpleAvControl
)
from .sound_switch import (
    COMMAND_CLASS_SOUND_SWITCH,
    SoundSwitch
)
from .supervision import (
    COMMAND_CLASS_SUPERVISION,
    Supervision
)
from .tariff_config import (
    COMMAND_CLASS_TARIFF_CONFIG,
    TariffConfig
)
from .tariff_tbl_monitor import (
    COMMAND_CLASS_TARIFF_TBL_MONITOR,
    TariffTblMonitor
)
from .thermostat_fan_mode import (
    COMMAND_CLASS_THERMOSTAT_FAN_MODE,
    ThermostatFanMode
)
from .thermostat_fan_state import (
    COMMAND_CLASS_THERMOSTAT_FAN_STATE,
    ThermostatFanState
)
from .thermostat_mode import (
    COMMAND_CLASS_THERMOSTAT_MODE,
    ThermostatMode
)
from .thermostat_operating_state import (
    COMMAND_CLASS_THERMOSTAT_OPERATING_STATE,
    ThermostatOperatingState
)
from .thermostat_setback import (
    COMMAND_CLASS_THERMOSTAT_SETBACK,
    ThermostatSetback
)
from .thermostat_setpoint import (
    COMMAND_CLASS_THERMOSTAT_SETPOINT,
    ThermostatSetpoint
)
from .time import (
    COMMAND_CLASS_TIME,
    Time
)
from .time_parameters import (
    COMMAND_CLASS_TIME_PARAMETERS,
    TimeParameters
)
from .transport_service import (
    COMMAND_CLASS_TRANSPORT_SERVICE,
    TransportService
)
from .user_code import (
    COMMAND_CLASS_USER_CODE,
    UserCode
)
from .version import (
    COMMAND_CLASS_VERSION,
    Version
)
from .wake_up import (
    COMMAND_CLASS_WAKE_UP,
    WakeUp
)
from .window_covering import (
    COMMAND_CLASS_WINDOW_COVERING,
    WindowCovering
)
from .zip import (
    COMMAND_CLASS_ZIP,
    ZIP
)
from .zip_6lowpan import (
    COMMAND_CLASS_ZIP_6LOWPAN,
    ZIP6Lowpan
)
from .zip_gateway import (
    COMMAND_CLASS_ZIP_GATEWAY,
    ZIPGateway
)
from .zip_naming import (
    COMMAND_CLASS_ZIP_NAMING,
    ZIPNaming
)
from .zip_nd import (
    COMMAND_CLASS_ZIP_ND,
    ZIPND
)
from .zip_portal import (
    COMMAND_CLASS_ZIP_PORTAL,
    ZIPPortal
)
from .zwave_plus_info import (
    COMMAND_CLASS_ZWAVE_PLUS_INFO,
    ZwavePlusInfo
)
from .alarm import (
    COMMAND_CLASS_ALARM,
    Alarm
)
from .sensor_alarm import (
    COMMAND_CLASS_SENSOR_ALARM,
    SensorAlarm
)
from .sensor_binary import (
    COMMAND_CLASS_SENSOR_BINARY,
    SensorBinary
)
from .climate_control_schedule import (
    COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE,
    ClimateControlSchedule
)
from .crc_16_encap import (
    COMMAND_CLASS_CRC_16_ENCAP,
    Crc16Encap
)
from .grouping_name import (
    COMMAND_CLASS_GROUPING_NAME,
    GroupingName
)
from .lock import (
    COMMAND_CLASS_LOCK,
    Lock
)
from .switch_toggle_multilevel import (
    COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL,
    SwitchToggleMultilevel
)
from .proprietary import (
    COMMAND_CLASS_PROPRIETARY,
    Proprietary
)
from .meter_pulse import (
    COMMAND_CLASS_METER_PULSE,
    MeterPulse
)
from .schedule_entry_lock import (
    COMMAND_CLASS_SCHEDULE_ENTRY_LOCK,
    ScheduleEntryLock
)
from .switch_all import (
    COMMAND_CLASS_SWITCH_ALL,
    SwitchAll
)
from .application_capability import (
    COMMAND_CLASS_APPLICATION_CAPABILITY,
    ApplicationCapability
)
from .basic_window_covering import (
    COMMAND_CLASS_BASIC_WINDOW_COVERING,
    BasicWindowCovering
)
from .switch_toggle_binary import (
    COMMAND_CLASS_SWITCH_TOGGLE_BINARY,
    SwitchToggleBinary
)
from .hail import (
    COMMAND_CLASS_HAIL,
    Hail
)
from .ip_configuration import (
    COMMAND_CLASS_IP_CONFIGURATION,
    IpConfiguration
)
from .mtp_window_covering import (
    COMMAND_CLASS_MTP_WINDOW_COVERING,
    MtpWindowCovering
)
from .network_management_primary import (
    COMMAND_CLASS_NETWORK_MANAGEMENT_PRIMARY,
    NetworkManagementPrimary
)
from .remote_association_activate import (
    COMMAND_CLASS_REMOTE_ASSOCIATION_ACTIVATE,
    RemoteAssociationActivate
)
from .remote_association import (
    COMMAND_CLASS_REMOTE_ASSOCIATION,
    RemoteAssociation
)
from .sensor_configuration import (
    COMMAND_CLASS_SENSOR_CONFIGURATION,
    SensorConfiguration
)


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
ZWAVE_PLUS_INFO = COMMAND_CLASS_ZWAVE_PLUS_INFO


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
            COMMAND_CLASS_ZWAVE_PLUS_INFO: ZwavePlusInfo,
            NETWORK_MANAGEMENT_INSTALLATION_MAINTENANCE: (
                NetworkManagementInstallationMaintenance
            ),
            '__original_module__': mod
        }
        self.__dict__ = mod.__dict__
        dict.__init__(self)

        for key, value in kwargs.items():
            self[key] = value

        sys.modules[__name__] = self

    def __missing__(self, key):
        self[key] = value = EmptyCommandClass
        return value


cc = CommandClasses()
