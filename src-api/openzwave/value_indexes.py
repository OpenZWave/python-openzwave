# -*- coding: utf-8 -*-
"""
.. module:: openzwave.value_indexes

This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave API

.. moduleauthor: Kevin Schlosser (@kdschlosser)

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


COMMAND_CLASS_NOTIFICATION = 0x71
COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION = 0x9B
COMMAND_CLASS_BARRIER_OPERATOR = 0x66
COMMAND_CLASS_BASIC = 0x20
COMMAND_CLASS_BASIC_WINDOW_COVERING = 0x50
COMMAND_CLASS_BATTERY = 0x80
COMMAND_CLASS_CENTRAL_SCENE = 0x5B
COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE = 0x46
COMMAND_CLASS_CLOCK = 0x81
COMMAND_CLASS_SWITCH_COLOR = 0x33
COMMAND_CLASS_CONFIGURATION = 0x70
COMMAND_CLASS_CONTROLLER_REPLICATION = 0x21
COMMAND_CLASS_DOOR_LOCK = 0x62
COMMAND_CLASS_DOOR_LOCK_LOGGING = 0x4C
COMMAND_CLASS_ENERGY_PRODUCTION = 0x90
COMMAND_CLASS_INDICATOR = 0x87
COMMAND_CLASS_LANGUAGE = 0x89
COMMAND_CLASS_LOCK = 0x76
COMMAND_CLASS_MANUFACTURER_PROPRIETARY = 0x91
COMMAND_CLASS_MANUFACTURER_SPECIFIC = 0x72
COMMAND_CLASS_METER = 0x32
COMMAND_CLASS_METER_PULSE = 0x35
COMMAND_CLASS_POWERLEVEL = 0x73
COMMAND_CLASS_PROTECTION = 0x75
COMMAND_CLASS_SCENE_ACTIVATION = 0x2B
COMMAND_CLASS_SECURITY = 0x98
COMMAND_CLASS_SENSOR_ALARM = 0x9C
COMMAND_CLASS_SENSOR_BINARY = 0x30
COMMAND_CLASS_SENSOR_MULTILEVEL = 0x31
COMMAND_CLASS_SIMPLE_AV_CONTROL = 0x94
COMMAND_CLASS_SOUND_SWITCH = 0x79
COMMAND_CLASS_SWITCH_ALL = 0x27
COMMAND_CLASS_SWITCH_BINARY = 0x25
COMMAND_CLASS_SWITCH_MULTILEVEL = 0x26
COMMAND_CLASS_SWITCH_TOGGLE_BINARY = 0x28
COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL = 0x29
COMMAND_CLASS_THERMOSTAT_FAN_MODE = 0x44
COMMAND_CLASS_THERMOSTAT_FAN_STATE = 0x45
COMMAND_CLASS_THERMOSTAT_MODE = 0x40
COMMAND_CLASS_THERMOSTAT_OPERATING_STATE = 0x42
COMMAND_CLASS_THERMOSTAT_SETPOINT = 0x43
COMMAND_CLASS_TIME_PARAMETERS = 0x8B
COMMAND_CLASS_USER_CODE = 0x63
COMMAND_CLASS_VERSION = 0x86
COMMAND_CLASS_WAKE_UP = 0x84
COMMAND_CLASS_ZWAVE_PLUS_INFO = 0x5E


class EmptyValueIndexes(object):
    max_index = -1


class ValueIndexMapping(list):

    def __init__(self, command_class):

        if command_class in _index_mapping:
            self._indexes = _index_mapping[command_class]

        else:
            self._indexes = EmptyValueIndexes

        list.__init__(self, [None] * self._indexes.max_entry + 1)

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if item == 'indexes':
            return self._indexes

        if hasattr(self._indexes, item):
            index = getattr(self._indexes, item)
            return self[index]

        raise AttributeError(item)

    def __setattr__(self, key, value):
        if key.startswith('_'):
            object.__setattr__(self, key, value)
        elif hasattr(self._indexes, key):
                index = getattr(self._indexes, key)
                self[index] = value
        else:
            raise AttributeError(key)

    def __getitem__(self, item):
        if item < len(self):
            return self[item]

        return None

    def __setitem__(self, key, value):
        if key >= len(self):
            self.extend([None] * (len(self) - key))

        self[key] = value


class ValueIndexes:

    class Alarm:
        # noinspection PyPep8
        """
        1 COMMAND_CLASS_NOTIFICATION 0x71 Notification CC id
        2 NOTIFICATION_REPORT 0x05 Notification Report command id
        3 V1 Alarm Type 0x00 Not implemented
        4 V1 Alarm Level 0x00 Not implemented
        5 Reserved 0x00 Reserved field
        6 Notification Status 0xFF Unsolicited report is activated
        7 Notification Type 0x01 Smoke Alarm
        8 Notification Event 0x01 Smoke Detected
        9 Sequence Number /Event Parameters Length 0x1A Sequence Number is appended /Event Parm Length = 10
        10 Event Parm 1 0x77 Node Naming & Location CC id
        11 Event Parm 2 0x06 Node Location Report command id
        12 Event Parm 3 0x00 Cmd Parm: Char = ASCII
        13 Event Parm 4 0x4B Cmd Parm: Node Location Char 1 = K
        14 Event Parm 5 0x49 Cmd Parm: Node Location Char 2 = I
        15 Event Parm 6 0x54 Cmd Parm: Node Location Char 3 = T
        16 Event Parm 7 0x43 Cmd Parm: Node Location Char 4 = C
        17 Event Parm 8 0x48 Cmd Parm: Node Location Char 5 = H
        18 Event Parm 9 0x45 Cmd Parm: Node Location Char 6 = E
        19 Event Parm 10 0x4E Cmd Parm: Node Location Char 7 = N
        20 Sequence Number 0x0F Sequence Number = 15


        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |Name          |Index |Event/ |State Variable        |State After  |Notification              |Value |Version |Event/State Parameters                     |Description                              |
        |              |      |State  |                      |Notification |Name                      |      |        |                                           |                                         |
        +==============+======+=======+======================+=============+==========================+======+========+===========================================+=========================================+
        |Smoke Alarm   |0x01  |State  |(Refer to parameters) |N/A          |State idle                |0x00  |V4      |Notification value for the state variable  |                                         |
        |              |      |       |                      |             |                          |      |        |going to idle. (V5)                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Sensor status         |Idle         |Smoke detected (location  |0x01  |V2      |Node Location Report (Node Naming and      |                                         |
        |              |      |       |                      |             |provided)                 |      |        |Location Command Class)                    |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Sensor status         |Idle         |Smoke detected            |0x02  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Alarm status          |Idle         |Smoke alarm test          |0x03  |V3      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Alarm status          |Idle         |Alarm silenced            |0x06  |V8      |                                           |This event may be issued by an alarm     |
        |              |      |       |                      |             |                          |      |        |                                           |device to advertise that the alarm has   |
        |              |      |       |                      |             |                          |      |        |                                           |been silenced by a local user event.     |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Maintenance status    |Idle         |Replacement required      |0x04  |V5      |                                           |This event may be issued by an alarm     |
        |              |      |       |                      |             |                          |      |        |                                           |device to advertise that its physical    |
        |              |      |       |                      |             |                          |      |        |                                           |components are no more reliable, e.g.    |
        |              |      |       |                      |             |                          |      |        |                                           |because of clogged filters.              |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Maintenance status    |Idle         |Replacement required,     |0x05  |V8      |                                           |This event may be issued by an alarm     |
        |              |      |       |                      |             |End-of-life               |      |        |                                           |device to advertise that the device has  |
        |              |      |       |                      |             |                          |      |        |                                           |reached the end of its designed          |
        |              |      |       |                      |             |                          |      |        |                                           |lifetime. The device should no longer be |
        |              |      |       |                      |             |                          |      |        |                                           |used.                                    |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Periodic inspection   |Idle         |Maintenance required,     |0x07  |V8      |                                           |This event may be issued by an alarm     |
        |              |      |       |status                |             |planned periodic          |      |        |                                           |device to advertise that the device has  |
        |              |      |       |                      |             |inspection                |      |        |                                           |reached the end of a designed            |
        |              |      |       |                      |             |                          |      |        |                                           |maintenance interval. The device is      |
        |              |      |       |                      |             |                          |      |        |                                           |should be serviced in order to stay      |
        |              |      |       |                      |             |                          |      |        |                                           |reliable.                                |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Dust in device status |Idle         |Maintenance required,     |0x08  |V8      |                                           |This event may be issued by an alarm     |
        |              |      |       |                      |             |dust in device            |      |        |                                           |device to advertise that the device has  |
        |              |      |       |                      |             |                          |      |        |                                           |detected dust in its sensor. The device  |
        |              |      |       |                      |             |                          |      |        |                                           |is not reliable until it has been        |
        |              |      |       |                      |             |                          |      |        |                                           |serviced.                                |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |N/A    |N/A                   |N/A          |Unknown event/state       |0xFE  |V2      |                                           |                                         |
        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |CO Alarm      |0x02  |State  |(Refer to parameters) |N/A          |State idle                |0x00  |V4      |Notification value for the state variable  |                                         |
        |              |      |       |                      |             |                          |      |        |going to idle. (V5)                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Sensor status         |Idle         |Carbon monoxide detected  |0x01  |V2      |Node Location Report (Node Naming and      |                                         |
        |              |      |       |                      |             |(location provided)       |      |        |Location Command Class)                    |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Sensor status         |Idle         |Carbon monoxide detected  |0x02  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Test status           |N/A          |Carbon monoxide test      |0x03  |V5      |0x01 = Test OK 0x02 = Test Failed          |The Carbon monoxide Test event may be    |
        |              |      |       |                      |             |                          |      |        |                                           |issued by an alarm device to advertise   |
        |              |      |       |                      |             |                          |      |        |                                           |that the test mode of the device has     |
        |              |      |       |                      |             |                          |      |        |                                           |been activated. The activation may be    |
        |              |      |       |                      |             |                          |      |        |                                           |manual or via signaling. A receiving     |
        |              |      |       |                      |             |                          |      |        |                                           |application SHOULD NOT activate any      |
        |              |      |       |                      |             |                          |      |        |                                           |alarms in response to this event.        |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Maintenance status    |Idle         |Replacement required      |0x04  |V5      |                                           |This event may be issued by an alarm     |
        |              |      |       |                      |             |                          |      |        |                                           |device to advertise that its physical    |
        |              |      |       |                      |             |                          |      |        |                                           |components are no more reliable, e.g.    |
        |              |      |       |                      |             |                          |      |        |                                           |because of clogged filters.              |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Maintenance status    |Idle         |Replacement required,     |0x05  |V8      |                                           |                                         |
        |              |      |       |                      |             |End-of-life               |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Alarm status          |Idle         |Alarm silenced            |0x06  |V8      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Periodic inspection   |Idle         |Maintenance required,     |0x07  |V8      |                                           |                                         |
        |              |      |       |status                |             |planned periodic          |      |        |                                           |                                         |
        |              |      |       |                      |             |inspection                |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |N/A    |N/A                   |N/A          |Unknown event/state       |0xFE  |V2      |                                           |                                         |
        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |CO2 Alarm     |0x03  |State  |(Refer to parameters) |N/A          |State idle                |0x00  |V4      |Notification value for the state variable  |                                         |
        |              |      |       |                      |             |                          |      |        |going to idle. (V5)                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Sensor status         |Idle         |Carbon dioxide detected   |0x01  |V2      |Node Location Report (Node Naming and      |                                         |
        |              |      |       |                      |             |(location provided)       |      |        |Location Command Class)                    |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Sensor status         |Idle         |Carbon dioxide detected   |0x02  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Test status           |N/A          |Carbon dioxide test       |0x03  |V5      |0x01 = Test OK 0x02 = Test Failed          |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Maintenance status    |Idle         |Replacement required      |0x04  |V5      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Maintenance status    |Idle         |Replacement required,     |0x05  |V8      |                                           |                                         |
        |              |      |       |                      |             |End-of-life               |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Alarm status          |Idle         |Alarm silenced            |0x06  |V8      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Periodic inspection   |Idle         |Maintenance required,     |0x07  |V8      |                                           |                                         |
        |              |      |       |status                |             |planned periodic          |      |        |                                           |                                         |
        |              |      |       |                      |             |inspection                |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |N/A    |N/A                   |N/A          |Unknown event/state       |0xFE  |V2      |                                           |                                         |
        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |Heat Alarm    |0x04  |State  |(Refer to parameters) |N/A          |State idle                |0x00  |V4      |Notification value for the state variable  |                                         |
        |              |      |       |                      |             |                          |      |        |going to idle. (V5)                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Heat sensor status    |Idle         |Overheat detected         |0x01  |V2      |Node Location Report (Node Naming and      |                                         |
        |              |      |       |                      |             |(location provided)       |      |        |Location Command Class)                    |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Heat sensor status    |Idle         |Overheat detected         |0x02  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Heat sensor status    |Idle         |Under heat detected       |0x05  |V2      |Node Location Report (Node Naming and      |                                         |
        |              |      |       |                      |             |(location provided)       |      |        |Location Command Class)                    |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Heat sensor status    |Idle         |Under heat detected       |0x06  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Rapid temperature rise    |0x03  |V2      |Node Location Report (Node Naming and      |                                         |
        |              |      |       |                      |             |(location provided)       |      |        |Location Command Class)                    |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Rapid temperature rise    |0x04  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Rapid temperature fall    |0x0C  |V8      |Node Location Report (Node Naming and      |                                         |
        |              |      |       |                      |             |(location provided)       |      |        |Location Command Class)                    |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Rapid temperature fall    |0x0D  |V8      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Alarm status          |Idle         |Heat alarm test           |0x07  |V8      |                                           |This event may be issued by an alarm     |
        |              |      |       |                      |             |                          |      |        |                                           |device to advertise that the local test  |
        |              |      |       |                      |             |                          |      |        |                                           |function has been activated.             |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Alarm status          |Idle         |Alarm silenced            |0x09  |V8      |                                           |This event may be issued by an alarm     |
        |              |      |       |                      |             |                          |      |        |                                           |device to advertise that the alarm has   |
        |              |      |       |                      |             |                          |      |        |                                           |been silenced by a local user event.     |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Maintenance status    |Idle         |Replacement required,     |0x08  |V8      |                                           |This event may be issued by an alarm     |
        |              |      |       |                      |             |End-of-life               |      |        |                                           |device to advertise that the device has  |
        |              |      |       |                      |             |                          |      |        |                                           |reached the end of its designed          |
        |              |      |       |                      |             |                          |      |        |                                           |lifetime. The device should no longer be |
        |              |      |       |                      |             |                          |      |        |                                           |used.                                    |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Dust in device status |Idle         |Maintenance required,     |0x0A  |V8      |                                           |This event may be issued by an alarm     |
        |              |      |       |                      |             |dust in device            |      |        |                                           |device to advertise that the device has  |
        |              |      |       |                      |             |                          |      |        |                                           |detected dust in its sensor. The device  |
        |              |      |       |                      |             |                          |      |        |                                           |is not reliable until it has been        |
        |              |      |       |                      |             |                          |      |        |                                           |serviced.                                |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Periodic inspection   |Idle         |Maintenance required,     |0x0B  |V8      |                                           |This event may be issued by an alarm     |
        |              |      |       |status                |             |planned periodic          |      |        |                                           |device to advertise that the device has  |
        |              |      |       |                      |             |inspection                |      |        |                                           |reached the end of a designed            |
        |              |      |       |                      |             |                          |      |        |                                           |maintenance interval. The device is      |
        |              |      |       |                      |             |                          |      |        |                                           |should be serviced in order to stay      |
        |              |      |       |                      |             |                          |      |        |                                           |reliable.                                |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |N/A    |N/A                   |N/A          |Unknown event/state       |0xFE  |V2      |                                           |                                         |
        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |Water Alarm   |0x05  |State  |(Refer to parameters) |N/A          |State idle                |0x00  |V4      |Notification value for the state variable  |                                         |
        |              |      |       |                      |             |                          |      |        |going to idle. (V5)                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Sensor status         |Idle         |Water leak detected       |0x01  |V2      |Node Location Report (Node Naming and      |                                         |
        |              |      |       |                      |             |(location provided)       |      |        |Location Command Class)                    |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Sensor status         |Idle         |Water leak detected       |0x02  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Water level dropped       |0x03  |V2      |                                           |                                         |
        |              |      |       |                      |             |(location provided)       |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Water level dropped       |0x04  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Maintenance status    |Idle         |Replace water filter      |0x05  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Water flow            |Idle         |Water flow alarm          |0x06  |V7      |Event Parameter 1 byte =                   |                                         |
        |              |      |       |alarm status          |             |                          |      |        |    0x01: No data                          |                                         |
        |              |      |       |                      |             |                          |      |        |    0x02: Below low threshold              |                                         |
        |              |      |       |                      |             |                          |      |        |    0x03: Above high threshold             |                                         |
        |              |      |       |                      |             |                          |      |        |    0x04: Max                              |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Water pressure        |Idle         |Water pressure alarm      |0x07  |V7      |Event Parameter 1 byte =                   |                                         |
        |              |      |       |alarm status          |             |                          |      |        |    0x01: No data                          |                                         |
        |              |      |       |                      |             |                          |      |        |    0x02: Below low threshold              |                                         |
        |              |      |       |                      |             |                          |      |        |    0x03: Above high threshold             |                                         |
        |              |      |       |                      |             |                          |      |        |    0x04: Max                              |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Water temperature     |Idle         |Water temperature alarm   |0x08  |V8      |Event Parameter 1 byte =                   |                                         |
        |              |      |       |alarm status          |             |                          |      |        |    0x01: No data                          |                                         |
        |              |      |       |                      |             |                          |      |        |    0x02: Below low threshold              |                                         |
        |              |      |       |                      |             |                          |      |        |    0x03: Above high threshold             |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Water level alarm     |Idle         |Water level alarm         |0x09  |V8      |Event Parameter 1 byte =                   |                                         |
        |              |      |       |status                |             |                          |      |        |    0x01: No data                          |                                         |
        |              |      |       |                      |             |                          |      |        |    0x02: Below low threshold              |                                         |
        |              |      |       |                      |             |                          |      |        |    0x03: Above high threshold             |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Pump status           |idle         |Sump pump active          |0x0A  |V8      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Pump status           |idle         |Sump pump failure         |0x0B  |V8      |                                           |This state may be used to indicate that  |
        |              |      |       |                      |             |                          |      |        |                                           |the pump does not function as expected   |
        |              |      |       |                      |             |                          |      |        |                                           |or is disconnected                       |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |N/A    |N/A                   |N/A          |Unknown event/state       |0xFE  |V2      |                                           |                                         |
        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |Access        |0x06  |State  |(Refer to parameters) |N/A          |State idle                |0x00  |V4      |Notification value for the state variable  |                                         |
        |Control       |      |       |                      |             |                          |      |        |going to idle. (V5)                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Manual lock operation     |0x01  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Manual unlock operation   |0x02  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |RF lock operation         |0x03  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |RF unlock operation       |0x04  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Keypad lock operation     |0x05  |V2      |User Code Report (User Code Command Class  |                                         |
        |              |      |       |                      |             |                          |      |        |V1)                                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Keypad unlock operation   |0x06  |V2      |User Code Report (User Code Command Class  |                                         |
        |              |      |       |                      |             |                          |      |        |V1)                                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Manual not fully locked   |0x07  |V3      |                                           |                                         |
        |              |      |       |                      |             |operation                 |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |RF not fully locked       |0x08  |V3      |                                           |                                         |
        |              |      |       |                      |             |operation                 |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Auto lock locked          |0x09  |V3      |                                           |                                         |
        |              |      |       |                      |             |operation                 |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Auto lock not fully       |0x0A  |V3      |                                           |                                         |
        |              |      |       |                      |             |locked operation          |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Lock state            |Idle         |Lock jammed               |0x0B  |V3      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |All user codes deleted    |0x0C  |V3      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Single user code deleted  |0x0D  |V3      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |New user code added       |0x0E  |V3      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |New user code not added   |0x0F  |V3      |                                           |                                         |
        |              |      |       |                      |             |due to duplicate code     |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Keypad state          |Idle         |Keypad temporary disabled |0x10  |V3      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Keypad state          |Idle         |Keypad busy               |0x11  |V3      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |New program code entered  |0x12  |V3      |                                           |                                         |
        |              |      |       |                      |             |: unique code for lock    |      |        |                                           |                                         |
        |              |      |       |                      |             |configuration             |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Manually enter user       |0x13  |V3      |                                           |                                         |
        |              |      |       |                      |             |access code exceeds code  |      |        |                                           |                                         |
        |              |      |       |                      |             |limit                     |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Unlock by RF with invalid |0x14  |V3      |                                           |                                         |
        |              |      |       |                      |             |user code                 |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Locked by RF with invalid |0x15  |V3      |                                           |                                         |
        |              |      |       |                      |             |user code                 |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Door state            |N/A          |Window/door is open       |0x16  |V3      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Door state            |N/A          |Window/door is closed     |0x17  |V3      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Door handle state     |N/A          |Window/door handle is     |0x18  |V8      |                                           |Doors or more particularly windows       |
        |              |      |       |                      |             |open                      |      |        |                                           |handles can be in fixed Open/Close       |
        |              |      |       |                      |             |                          |      |        |                                           |position (it does not automatically      |
        |              |      |       |                      |             |                          |      |        |                                           |returns to the closed position). This    |
        |              |      |       |                      |             |                          |      |        |                                           |state variable can be used to advertise  |
        |              |      |       |                      |             |                          |      |        |                                           |in which state is a fixed position       |
        |              |      |       |                      |             |                          |      |        |                                           |windows/door handle.                     |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Door handle state     |N/A          |Window/door handle is     |0x19  |V8      |                                           |                                         |
        |              |      |       |                      |             |closed                    |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Messaging User Code       |0x20  |V8      |Event parameter 2 bytes: User Code User    |                                         |
        |              |      |       |                      |             |entered via keypad        |      |        |Identifier (User Code Command Class,       |                                         |
        |              |      |       |                      |             |                          |      |        |version 2)                                 |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Barrier performing    |N/A          |Barrier performing        |0x40  |V4      |Event Parameter 1 byte =                   |                                         |
        |              |      |       |initialization        |             |initialization process    |      |        |    0x00: Process completed                |                                         |
        |              |      |       |process               |             |                          |      |        |    0xFF: Performing process               |                                         |
        |              |      |       |status                |             |                          |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Barrier operation         |0x41  |V4      |                                           |                                         |
        |              |      |       |                      |             |(open/close) force has    |      |        |                                           |                                         |
        |              |      |       |                      |             |been exceeded             |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Barrier motor has         |0x42  |V4      |Event Parameter 1 byte =                   |                                         |
        |              |      |       |                      |             |exceeded manufacturer's   |      |        |    0x00..0x7F: 0..127 seconds             |                                         |
        |              |      |       |                      |             |operational time limit    |      |        |    0x80..0xFE: 1..127 minutes             |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Barrier operation has     |0x43  |V4      |                                           |For example : The barrier has opened     |
        |              |      |       |                      |             |exceeded physical         |      |        |                                           |past the opening limit.                  |
        |              |      |       |                      |             |mechanical limits         |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Barrier unable to perform |0x44  |V4      |                                           |                                         |
        |              |      |       |                      |             |requested operation due   |      |        |                                           |                                         |
        |              |      |       |                      |             |to UL requirements        |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Barrier UL disabling  |Idle         |Barrier unattended        |0x45  |V4      |                                           |                                         |
        |              |      |       |status                |             |operation has been        |      |        |                                           |                                         |
        |              |      |       |                      |             |disabled per UL           |      |        |                                           |                                         |
        |              |      |       |                      |             |requirements              |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Barrier failed to perform |0x46  |V4      |                                           |                                         |
        |              |      |       |                      |             |requested operation,      |      |        |                                           |                                         |
        |              |      |       |                      |             |device malfunction        |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Barrier vacation      |N/A          |Barrier vacation mode     |0x47  |V4      |Event Parameter 1 byte =                   |                                         |
        |              |      |       |mode status           |             |                          |      |        |    0x00: Mode disabled                    |                                         |
        |              |      |       |                      |             |                          |      |        |    0xFF: Mode enabled                     |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Barrier Safety bearm  |N/A          |Barrier safety beam       |0x48  |V4      |Event Parameter 1 byte =                   |                                         |
        |              |      |       |obstacle status       |             |obstacle                  |      |        |    0x00: No obstruction                   |                                         |
        |              |      |       |                      |             |                          |      |        |    0xFF: Obstruction                      |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Barrier sensor status |Idle         |Barrier sensor not        |0x49  |V4      |Event Parameter 1 byte =                   |Note : If the state is cleared, it means |
        |              |      |       |                      |             |detected / supervisory    |      |        |    0x00: Sensor not defined               |that the state is cleared for all issues |
        |              |      |       |                      |             |error                     |      |        |    0x01..0xFF: Sensor ID                  |Sensor IDs in the state change           |
        |              |      |       |                      |             |                          |      |        |                                           |notifications                            |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Barrier Battery       |Idle         |Barrier sensor low        |0x4A  |V4      |Event Parameter 1 byte =                   |Note : If the state is cleared, it means |
        |              |      |       |status                |             |battery warning           |      |        |    0x00: Sensor not defined               |that the state is cleared for all issues |
        |              |      |       |                      |             |                          |      |        |    0x01..0xFF: Sensor ID                  |Sensor IDs in the state change           |
        |              |      |       |                      |             |                          |      |        |                                           |notifications                            |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Barrier short         |Idle         |Barrier detected short in |0x4B  |V4      |                                           |                                         |
        |              |      |       |circuit status        |             |wall station wires        |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Barrier control       |Idle         |Barrier associated with   |0x4C  |V4      |                                           |                                         |
        |              |      |       |status                |             |non Z-Wave remote control |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |N/A    |N/A                   |N/A          |Unknown event/state       |0xFE  |V2      |                                           |                                         |
        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |Home Security |0x07  |State  |(Refer to parameters) |N/A          |State idle                |0x00  |V4      |Notification value for the state variable  |                                         |
        |              |      |       |                      |             |                          |      |        |going to idle. (V5)                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Sensor status         |Idle         |Intrusion (location       |0x01  |V2      |Node Location Report (Node Naming and      |                                         |
        |              |      |       |                      |             |provided)                 |      |        |Location Command Class)                    |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Sensor status         |Idle         |Intrusion                 |0x02  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Cover status          |Idle         |Tampering, product cover  |0x03  |V2      |                                           |                                         |
        |              |      |       |                      |             |removed                   |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Tampering, invalid code   |0x04  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Glass breakage (location  |0x05  |V2      |Node Location Report (Node Naming and      |                                         |
        |              |      |       |                      |             |provided)                 |      |        |Location Command Class)                    |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Glass breakage            |0x06  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Motion sensor status  |Idle         |Motion detection          |0x07  |V2      |Node Location Report (Node Naming and      |                                         |
        |              |      |       |                      |             |(location provided)       |      |        |Location Command Class)                    |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Motion sensor status  |Idle         |Motion detection          |0x08  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Tampering, product moved  |0x09  |V6      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Impact detected           |0x0A  |V8      |                                           |This event indicates that the node has   |
        |              |      |       |                      |             |                          |      |        |                                           |detected an excessive amount of pressure |
        |              |      |       |                      |             |                          |      |        |                                           |or that an impact has occurred on the    |
        |              |      |       |                      |             |                          |      |        |                                           |product itself.                          |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |N/A    |N/A                   |N/A          |Unknown event/state       |0xFE  |V2      |                                           |                                         |
        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |Power         |0x08  |State  |(Refer to parameters) |N/A          |State idle                |0x00  |V4      |Notification value for the state variable  |                                         |
        |Management    |      |       |                      |             |                          |      |        |going to idle. (V5)                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Power status          |Idle         |Power has been applied    |0x01  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Mains status          |N/A          |AC mains disconnected     |0x02  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Mains status          |N/A          |AC mains re-connected     |0x03  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Surge detected            |0x04  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Voltage drop/drift        |0x05  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Over-current status   |Idle         |Over-current detected     |0x06  |V3      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Over-voltage status   |Idle         |Over-voltage detected     |0x07  |V3      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Over-load status      |Idle         |Over-load detected        |0x08  |V3      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Load error status     |Idle         |Load error                |0x09  |V3      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Battery maintenance   |Idle         |Replace battery soon      |0x0A  |V3      |                                           |                                         |
        |              |      |       |status                |             |                          |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Battery maintenance   |Idle         |Replace battery now       |0x0B  |V3      |                                           |                                         |
        |              |      |       |status                |             |                          |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Battery maintenance   |Idle         |Battery fluid is low      |0x11  |V8      |                                           |                                         |
        |              |      |       |status                |             |                          |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Battery load status   |Idle         |Battery is charging       |0x0C  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Battery level status  |Idle         |Battery is fully charged  |0x0D  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Battery level status  |Idle         |Charge battery soon       |0x0E  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Battery level status  |Idle         |Charge battery now        |0x0F  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Backup battery        |Idle         |Back-up battery is low    |0x10  |V8      |                                           |                                         |
        |              |      |       |level status          |             |                          |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Backup battery        |Idle         |Back-up battery           |0x12  |V8      |                                           |                                         |
        |              |      |       |level status          |             |disconnected              |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |N/A    |N/A                   |N/A          |Unknown event/state       |0xFE  |V2      |                                           |                                         |
        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |System        |0x09  |State  |(Refer to parameters) |N/A          |State idle                |0x00  |V4      |Notification value for the state variable  |                                         |
        |              |      |       |                      |             |                          |      |        |going to idle. (V5)                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |HW status             |Idle         |System hardware failure   |0x01  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |HW status             |Idle         |System hardware failure   |0x03  |V3      |Manufacturer proprietary system failure    |                                         |
        |              |      |       |                      |             |(manufacturer proprietary |      |        |codes. Cannot be listed in NIF. Codes MUST |                                         |
        |              |      |       |                      |             |failure code provided)    |      |        |be described in product manual.            |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |SW status             |Idle         |System software failure   |0x02  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |SW status             |Idle         |System software failure   |0x04  |V3      |Manufacturer proprietary system failure    |                                         |
        |              |      |       |                      |             |(manufacturer proprietary |      |        |codes. Cannot be listed in NIF. Codes MUST |                                         |
        |              |      |       |                      |             |failure code provided)    |      |        |be described in product manual.            |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Heartbeat                 |0x05  |V5      |                                           |The Heartbeat event may be issued by a   |
        |              |      |       |                      |             |                          |      |        |                                           |device to advertise that the device is   |
        |              |      |       |                      |             |                          |      |        |                                           |still alive or to notify its presence.   |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Cover status          |Idle         |Tampering, product cover  |0x06  |V5      |                                           |The Product covering removed event may   |
        |              |      |       |                      |             |removed                   |      |        |                                           |be issued by a device to advertise that  |
        |              |      |       |                      |             |                          |      |        |                                           |its physical enclosure has been          |
        |              |      |       |                      |             |                          |      |        |                                           |compromised. This may, for instance,     |
        |              |      |       |                      |             |                          |      |        |                                           |indicate a security threat or that a     |
        |              |      |       |                      |             |                          |      |        |                                           |user is trying to modify a metering      |
        |              |      |       |                      |             |                          |      |        |                                           |device. Note that a similar event is     |
        |              |      |       |                      |             |                          |      |        |                                           |defined for the Home Security            |
        |              |      |       |                      |             |                          |      |        |                                           |Notification Type. If a device           |
        |              |      |       |                      |             |                          |      |        |                                           |implements other events for the Home     |
        |              |      |       |                      |             |                          |      |        |                                           |Security Notification Type, the device   |
        |              |      |       |                      |             |                          |      |        |                                           |should issue the Tampering event defined |
        |              |      |       |                      |             |                          |      |        |                                           |for the Home Security Notification Type. |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Emergency shutoff     |Idle         |Emergency shutoff         |0x07  |V7      |                                           |                                         |
        |              |      |       |status                |             |                          |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |N/A    |N/A                   |N/A          |Unknown event/state       |0xFE  |V2      |                                           |                                         |
        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |Emergency     |0x0A  |State  |(Refer to parameters) |N/A          |State idle                |0x00  |V4      |Notification value for the state variable  |                                         |
        |Alarm         |      |       |                      |             |                          |      |        |going to idle. (V5)                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Contact police            |0x01  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Contact fire service      |0x02  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Contact medical service   |0x03  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Panic alert               |0x04  |V8      |                                           |This event is used to indicate that a    |
        |              |      |       |                      |             |                          |      |        |                                           |panic/emergency situation occured        |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |N/A    |N/A                   |N/A          |Unknown event/state       |0xFE  |V2      |                                           |                                         |
        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |Clock         |0x0B  |State  |(Refer to parameters) |N/A          |State idle                |0x00  |V4      |Notification value for the state variable  |                                         |
        |              |      |       |                      |             |                          |      |        |going to idle. (V5)                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Wake up alert             |0x01  |V2      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Timer ended               |0x02  |V3      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Time remaining            |0x03  |V4      |Event Parameter 3 bytes = Byte 1           |                                         |
        |              |      |       |                      |             |                          |      |        |    0x00..0xFF: 0..255 hours Byte 2        |                                         |
        |              |      |       |                      |             |                          |      |        |    0x00..0xFF: 0..255 minutes Byte 3      |                                         |
        |              |      |       |                      |             |                          |      |        |    0x00..0xFF: 0..255 seconds             |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |N/A    |N/A                   |N/A          |Unknown event/state       |0xFE  |V2      |                                           |                                         |
        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |Appliance     |0x0C  |State  |(Refer to parameters) |N/A          |State idle                |0x00  |V4      |Notification value for the state variable  |                                         |
        |              |      |       |                      |             |                          |      |        |going to idle. (V5)                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Program status        |Idle         |Program started           |0x01  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Program status        |Idle         |Program in progress       |0x02  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Program status        |Idle         |Program completed         |0x03  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Maintenance status    |Idle         |Replace main filter       |0x04  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Appliance status      |Idle         |Supplying water           |0x06  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Appliance status      |Idle         |Boiling                   |0x08  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Appliance status      |Idle         |Washing                   |0x0A  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Appliance status      |Idle         |Rinsing                   |0x0C  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Appliance status      |Idle         |Draining                  |0x0E  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Appliance status      |Idle         |Spinning                  |0x10  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Appliance status      |Idle         |Drying                    |0x12  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Target temperature    |Idle         |Failure to set target     |0x05  |V4      |                                           |                                         |
        |              |      |       |failure status        |             |temperature               |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Water supply          |Idle         |Water supply failure      |0x07  |V4      |                                           |                                         |
        |              |      |       |failure status        |             |                          |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Boiling failure       |Idle         |Boiling failure           |0x09  |V4      |                                           |                                         |
        |              |      |       |status                |             |                          |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Washing failure       |Idle         |Washing failure           |0x0B  |V4      |                                           |                                         |
        |              |      |       |status                |             |                          |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Rinsing failure       |Idle         |Rinsing failure           |0x0D  |V4      |                                           |                                         |
        |              |      |       |status                |             |                          |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Draining failure      |Idle         |Draining failure          |0x0F  |V4      |                                           |                                         |
        |              |      |       |status                |             |                          |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Spinning failure      |Idle         |Spinning failure          |0x11  |V4      |                                           |                                         |
        |              |      |       |status                |             |                          |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Drying failure status |Idle         |Drying failure            |0x13  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Fan failure status    |Idle         |Fan failure               |0x14  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Compressor failure    |Idle         |Compressor failure        |0x15  |V4      |                                           |                                         |
        |              |      |       |status                |             |                          |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |N/A    |N/A                   |N/A          |Unknown event/state       |0xFE  |V4      |                                           |                                         |
        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |Home Health   |0x0D  |State  |(Refer to parameters) |N/A          |State idle                |0x00  |V4      |Notification value for the state variable  |                                         |
        |              |      |       |                      |             |                          |      |        |going to idle. (V5)                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Position status       |Idle         |Leaving bed               |0x01  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Position status       |Idle         |Sitting on bed            |0x02  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Position status       |Idle         |Lying on bed              |0x03  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Position status       |Idle         |Sitting on bed edge       |0x05  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Posture changed           |0x04  |V4      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |VOC level status      |N/A          |Volatile Organic Compound |0x06  |V4      |Event Parameter 1 byte : Pollution level = |                                         |
        |              |      |       |                      |             |level                     |      |        |    0x01: Clean                            |                                         |
        |              |      |       |                      |             |                          |      |        |    0x02: Slightly polluted                |                                         |
        |              |      |       |                      |             |                          |      |        |    0x03: Moderately polluted              |                                         |
        |              |      |       |                      |             |                          |      |        |    0x04: Highly polluted                  |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Sleep apnea status    |Idle         |Sleep apnea detected      |0x07  |V8      |Event Parameter 1 byte : breath level =    |                                         |
        |              |      |       |                      |             |                          |      |        |    0x01: Low breath                       |                                         |
        |              |      |       |                      |             |                          |      |        |    0x02: No breath at all                 |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Sleep stage status    |Idle         |Sleep stage 0 detected    |0x08  |V8      |                                           |The sensors detects that the person is   |
        |              |      |       |                      |             |(Dreaming/REM)            |      |        |                                           |awake when this state variable returns   |
        |              |      |       |                      |             |                          |      |        |                                           |to idle.                                 |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Sleep stage status    |Idle         |Sleep stage 1 detected    |0x09  |V8      |                                           |The sensors detects that the person is   |
        |              |      |       |                      |             |(Light sleep, non-REM 1)  |      |        |                                           |awake when this state variable returns   |
        |              |      |       |                      |             |                          |      |        |                                           |to idle.                                 |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Sleep stage status    |Idle         |Sleep stage 2 detected    |0x0A  |V8      |                                           |The sensors detects that the person is   |
        |              |      |       |                      |             |(Medium sleep, non-REM 2) |      |        |                                           |awake when this state variable returns   |
        |              |      |       |                      |             |                          |      |        |                                           |to idle.                                 |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Sleep stage status    |Idle         |Sleep stage 3 detected    |0x0B  |V8      |                                           |The sensors detects that the person is   |
        |              |      |       |                      |             |(Deep sleep, non-REM 3)   |      |        |                                           |awake when this state variable returns   |
        |              |      |       |                      |             |                          |      |        |                                           |to idle.                                 |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |N/A    |N/A                   |N/A          |Unknown event/state       |0xFE  |V4      |                                           |                                         |
        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |Siren         |0x0E  |State  |(Refer to parameters) |N/A          |State idle                |0x00  |V6      |Notification value for the state variable  |                                         |
        |              |      |       |                      |             |                          |      |        |going to idle. (V5)                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Siren status          |Idle         |Siren active              |0x01  |V6      |                                           |This Event indicates that a siren or     |
        |              |      |       |                      |             |                          |      |        |                                           |sound within a device is active. This    |
        |              |      |       |                      |             |                          |      |        |                                           |may be a Siren within a smoke sensor     |
        |              |      |       |                      |             |                          |      |        |                                           |that goes active when smoke is detected. |
        |              |      |       |                      |             |                          |      |        |                                           |Or a beeping within a power switch to    |
        |              |      |       |                      |             |                          |      |        |                                           |indicate over-current detected. The      |
        |              |      |       |                      |             |                          |      |        |                                           |siren may switch Off automatically or    |
        |              |      |       |                      |             |                          |      |        |                                           |based on user interaction. This can be   |
        |              |      |       |                      |             |                          |      |        |                                           |reported through Notification Type Siren |
        |              |      |       |                      |             |                          |      |        |                                           |and Event 0x00.                          |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |N/A    |N/A                   |N/A          |Unknown event/state       |0xFE  |V6      |                                           |                                         |
        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |Water Valve   |0x0F  |State  |(Refer to parameters) |N/A          |State idle                |0x00  |V7      |Notification value for the state variable  |                                         |
        |              |      |       |                      |             |                          |      |        |going to idle. (V5)                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Valve operation       |N/A          |Valve operation           |0x01  |V7      |Event Parameter 1 byte =                   |                                         |
        |              |      |       |status                |             |                          |      |        |0x00: Off / Closed (valve does not let the |                                         |
        |              |      |       |                      |             |                          |      |        |water run through)                         |                                         |
        |              |      |       |                      |             |                          |      |        |0x01: On / Open (valve lets the water run  |                                         |
        |              |      |       |                      |             |                          |      |        |through)                                   |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Master valve          |N/A          |Master valve operation    |0x02  |V7      |Event Parameter 1 byte =                   |                                         |
        |              |      |       |operation             |             |                          |      |        |0x00: Off / Closed (valve does not let the |                                         |
        |              |      |       |status                |             |                          |      |        |water run through)                         |                                         |
        |              |      |       |                      |             |                          |      |        |0x01: On / Open (valve lets the water run  |                                         |
        |              |      |       |                      |             |                          |      |        |through)                                   |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Valve short circuit   |Idle         |Valve short circuit       |0x03  |V7      |                                           |                                         |
        |              |      |       |status                |             |                          |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Master valve short    |Idle         |Master valve short        |0x04  |V7      |                                           |                                         |
        |              |      |       |circuit status        |             |circuit                   |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Valve current alarm   |Idle         |Valve current alarm       |0x05  |V7      |Event Parameter 1 byte =                   |                                         |
        |              |      |       |status                |             |                          |      |        |    0x01: No data                          |                                         |
        |              |      |       |                      |             |                          |      |        |    0x02: Below low threshold              |                                         |
        |              |      |       |                      |             |                          |      |        |    0x03: Above high threshold             |                                         |
        |              |      |       |                      |             |                          |      |        |    0x04: Max                              |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Master valve current  |Idle         |Master valve current      |0x06  |V7      |Event Parameter 1 byte =                   |                                         |
        |              |      |       |alarm status          |             |alarm                     |      |        |    0x01: No data                          |                                         |
        |              |      |       |                      |             |                          |      |        |    0x02: Below low threshold              |                                         |
        |              |      |       |                      |             |                          |      |        |    0x03: Above high threshold             |                                         |
        |              |      |       |                      |             |                          |      |        |    0x04: Max                              |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |N/A    |N/A                   |N/A          |Unknown event/state       |0xFE  |V7      |                                           |                                         |
        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |Weather Alarm |0x10  |State  |(Refer to parameters) |N/A          |State idle                |0x00  |V7      |Notification value for the state variable  |                                         |
        |              |      |       |                      |             |                          |      |        |going to idle. (V5)                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Rain alarm status     |Idle         |Rain alarm                |0x01  |V7      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Moisture alarm status |Idle         |Moisture alarm            |0x02  |V7      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Freeze alarm status   |Idle         |Freeze alarm              |0x03  |V8      |                                           |The Freeze alarm state is used to        |
        |              |      |       |                      |             |                          |      |        |                                           |indicate that the outside temperature is |
        |              |      |       |                      |             |                          |      |        |                                           |negative and there is an icing risk      |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |N/A    |N/A                   |N/A          |Unknown event/state       |0xFE  |V7      |                                           |                                         |
        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |Irrigation    |0x11  |State  |(Refer to parameters) |N/A          |State idle                |0x00  |V7      |Notification value for the state variable  |                                         |
        |              |      |       |                      |             |                          |      |        |going to idle. (V5)                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Schedule (id) status  |N/A          |Schedule started          |0x01  |V7      |Event Parameter 1 = <Schedule ID>          |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Schedule (id) status  |N/A          |Schedule finished         |0x02  |V7      |Event Parameter 1 = <Schedule ID>          |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Valve run status      |N/A          |Valve table run started   |0x03  |V7      |Event Parameter 1 = <Valve table ID>       |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Valve run status      |N/A          |Valve table run finished  |0x04  |V7      |Event Parameter 1 = <Valve table ID>       |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Device configuration  |Idle         |Device is not configured  |0x05  |V7      |                                           |                                         |
        |              |      |       |status                |             |                          |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |N/A    |N/A                   |N/A          |Unknown event/state       |0xFE  |V7      |                                           |                                         |
        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |Gas alarm     |0x12  |State  |(Refer to parameters) |N/A          |State idle                |0x00  |V7      |Notification value for the state variable  |                                         |
        |              |      |       |                      |             |                          |      |        |going to idle. (V5)                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Combustible gas       |Idle         |Combustible gas detected  |0x01  |V7      |Node Location Report (Node Naming and      |                                         |
        |              |      |       |status                |             |(location provided)       |      |        |Location Command Class)                    |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Combustible gas       |Idle         |Combustible gas detected  |0x02  |V7      |                                           |                                         |
        |              |      |       |status                |             |                          |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Toxic gas status      |Idle         |Toxic gas detected        |0x03  |V7      |Node Location Report (Node Naming and      |                                         |
        |              |      |       |                      |             |(location provided)       |      |        |Location Command Class)                    |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Toxic gas status      |Idle         |Toxic gas detected        |0x04  |V7      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Alarm status          |Idle         |Gas alarm test            |0x05  |V7      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Maintenance status    |Idle         |Replacement required      |0x06  |V7      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |N/A    |N/A                   |N/A          |Unknown event/state       |0xFE  |V7      |                                           |                                         |
        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |Pest Control  |0x13  |State  |(Refer to parameters) |N/A          |State idle                |0x00  |V8      |Notification value for the state variable  |                                         |
        |              |      |       |                      |             |                          |      |        |going to idle. (V5)                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Trap status           |idle         |Trap armed (location      |0x01  |V8      |Node Location Report (Node Naming and      |The state is used to indicate that the   |
        |              |      |       |                      |             |provided)                 |      |        |Location Command Class)                    |trap is armed and potentially dangerous  |
        |              |      |       |                      |             |                          |      |        |                                           |for humans (e.g. risk of electric shock, |
        |              |      |       |                      |             |                          |      |        |                                           |finger being caught)                     |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Trap status           |idle         |Trap armed                |0x02  |V8      |                                           |The state is used to indicate that the   |
        |              |      |       |                      |             |                          |      |        |                                           |trap is armed and potentially dangerous  |
        |              |      |       |                      |             |                          |      |        |                                           |for humans (e.g. risk of electric shock, |
        |              |      |       |                      |             |                          |      |        |                                           |finger being caught)                     |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Trap status           |idle         |Trap re-arm required      |0x03  |V8      |Node Location Report (Node Naming and      |This state is used to indicate that the  |
        |              |      |       |                      |             |(location provided)       |      |        |Location Command Class)                    |trap requires to be re-armed or          |
        |              |      |       |                      |             |                          |      |        |                                           |re-engage before being operational again |
        |              |      |       |                      |             |                          |      |        |                                           |(e.g. remove rodent remains, mechanical  |
        |              |      |       |                      |             |                          |      |        |                                           |re-engagement)                           |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Trap status           |idle         |Trap re-arm required      |0x04  |V8      |                                           |This state is used to indicate that the  |
        |              |      |       |                      |             |                          |      |        |                                           |trap requires to be re-armed or          |
        |              |      |       |                      |             |                          |      |        |                                           |re-engage before being operational again |
        |              |      |       |                      |             |                          |      |        |                                           |(e.g. remove rodent remains, mechanical  |
        |              |      |       |                      |             |                          |      |        |                                           |re-engagement)                           |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Pest detected (location   |0x05  |V8      |Node Location Report (Node Naming and      |This event may be issued by a device to  |
        |              |      |       |                      |             |provided)                 |      |        |Location Command Class)                    |advertise that it detected an            |
        |              |      |       |                      |             |                          |      |        |                                           |undesirable animal, but could not        |
        |              |      |       |                      |             |                          |      |        |                                           |exterminate it                           |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Pest detected             |0x06  |V8      |                                           |This event may be issued by a device to  |
        |              |      |       |                      |             |                          |      |        |                                           |advertise that it detected an            |
        |              |      |       |                      |             |                          |      |        |                                           |undesirable animal, but could not        |
        |              |      |       |                      |             |                          |      |        |                                           |exterminate it                           |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Pest exterminated         |0x07  |V8      |Node Location Report (Node Naming and      |This event may be issued by a device to  |
        |              |      |       |                      |             |(location provided)       |      |        |Location Command Class)                    |advertise that it exterminated an        |
        |              |      |       |                      |             |                          |      |        |                                           |undesirable animal                       |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Pest exterminated         |0x08  |V8      |                                           |This event may be issued by a device to  |
        |              |      |       |                      |             |                          |      |        |                                           |advertise that it exterminated an        |
        |              |      |       |                      |             |                          |      |        |                                           |undesirable animal                       |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |N/A    |N/A                   |N/A          |Unknown event/state       |0xFE  |V8      |                                           |                                         |
        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |Light sensor  |0x14  |State  |(Refer to parameters) |N/A          |State idle                |0x00  |V8      |Notification value for the state variable  |                                         |
        |              |      |       |                      |             |                          |      |        |going to idle. (V5)                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Light detection       |idle         |Light detected            |0x01  |V8      |                                           |                                         |
        |              |      |       |status                |             |                          |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Light color transition    |0x02  |V8      |                                           |                                         |
        |              |      |       |                      |             |detected                  |      |        |                                           |                                         |
        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |Water Quality |0x15  |State  |(Refer to parameters) |N/A          |State idle                |0x00  |V8      |Notification value for the state variable  |                                         |
        |Monitoring    |      |       |                      |             |                          |      |        |going to idle. (V5)                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Chlorine alarm status |Idle         |Chlorine alarm            |0x01  |V8      |Event Parameter 1 byte =                   |                                         |
        |              |      |       |                      |             |                          |      |        |    0x01: Below low threshold              |                                         |
        |              |      |       |                      |             |                          |      |        |    0x02: Above high threshold             |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Acidity (pH) status   |Idle         |Acidity (pH) alarm        |0x02  |V8      |Event Parameter 1 byte =                   |                                         |
        |              |      |       |                      |             |                          |      |        |    0x01: Below low threshold              |                                         |
        |              |      |       |                      |             |                          |      |        |    0x02: Above high threshold             |                                         |
        |              |      |       |                      |             |                          |      |        |    0x03: Decreasing pH                    |                                         |
        |              |      |       |                      |             |                          |      |        |    0x04: Increasing pH                    |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Water Oxidation       |Idle         |Water Oxidation alarm     |0x03  |V8      |Event Parameter 1 byte =                   |                                         |
        |              |      |       |alarm status          |             |                          |      |        |    0x01: Below low threshold              |                                         |
        |              |      |       |                      |             |                          |      |        |    0x02: Above high threshold             |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Chlorine Sensor       |Idle         |Chlorine empty            |0x04  |V8      |                                           |                                         |
        |              |      |       |status                |             |                          |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Acidity (pH)          |Idle         |Acidity (pH) empty        |0x05  |V8      |                                           |                                         |
        |              |      |       |Sensor status         |             |                          |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Waterflow measuring   |Idle         |Waterflow measuring       |0x06  |V8      |                                           |                                         |
        |              |      |       |station sensor        |             |station shortage detected |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Waterflow clear       |Idle         |Waterflow clear water     |0x07  |V8      |                                           |                                         |
        |              |      |       |water sensor          |             |shortage detected         |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Disinfection          |Idle         |Disinfection system error |0x08  |V8      |Event Parameter 1 byte bitmask=            |This state is used to inform that the    |
        |              |      |       |system status         |             |detected                  |      |        |    bits 0..3: represent System            |disinfection system is not functioning   |
        |              |      |       |                      |             |                          |      |        |         1..4 disorder detected            |properly.                                |
        |              |      |       |                      |             |                          |      |        |    bits 4..7: represent System            |                                         |
        |              |      |       |                      |             |                          |      |        |         1..4 salt shortage                |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Filter cleaning       |Idle         |Filter cleaning ongoing   |0x09  |V8      |Event Parameter 1 byte =                   |                                         |
        |              |      |       |status                |             |                          |      |        |    0x01..0xFF: Filter                     |                                         |
        |              |      |       |                      |             |                          |      |        |         1..255 cleaning                   |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Heating status        |Idle         |Heating operation ongoing |0x0A  |V8      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Filter pump status    |Idle         |Filter pump operation     |0x0B  |V8      |                                           |                                         |
        |              |      |       |                      |             |ongoing                   |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Freshwater flow       |Idle         |Freshwater operation      |0x0C  |V8      |                                           |                                         |
        |              |      |       |status                |             |ongoing                   |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Dry protection status |Idle         |Dry protection operation  |0x0D  |V8      |                                           |                                         |
        |              |      |       |                      |             |active                    |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Water tank is empty       |0x0E  |V8      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Water tank level is       |0x0F  |V8      |                                           |                                         |
        |              |      |       |                      |             |unknown                   |      |        |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |Event  |N/A                   |N/A          |Water tank is full        |0x10  |V8      |                                           |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Collective disorder   |Idle         |Collective disorder       |0x11  |V8      |                                           |                                         |
        |              |      |       |status                |             |                          |      |        |                                           |                                         |
        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |Home          |0x16  |State  |(Refer to parameters) |N/A          |State idle                |0x00  |V8      |Notification value for the state variable  |                                         |
        |monitoring    |      |       |                      |             |                          |      |        |going to idle. (V5)                        |                                         |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Home occupancy status |idle         |Home occupied (location   |0x01  |V8      |Node Location Report (Node Naming and      |This state is used to indicate that a    |
        |              |      |       |                      |             |provided)                 |      |        |Location Command Class)                    |sensor detects that the home is          |
        |              |      |       |                      |             |                          |      |        |                                           |currently occupied                       |
        |              |      +-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        |              |      |State  |Home occupancy status |idle         |Home occupied             |0x02  |V8      |                                           |This state is used to indicate that a    |
        |              |      |       |                      |             |                          |      |        |                                           |sensor detects that the home is          |
        |              |      |       |                      |             |                          |      |        |                                           |currently occupied Request pending       |
        |              |      |       |                      |             |                          |      |        |                                           |notification                             |
        +--------------+------+-------+----------------------+-------------+--------------------------+------+--------+-------------------------------------------+-----------------------------------------+
        """

        start = 0
        end = 255
        param_start = 256
        param_end = 511
        type_v1 = 512
        level_v1 = 513
        auto_clear_events = 514
        max_entry = auto_clear_events

    class AssociationCommandConfiguration:
        max_command_length = 0
        commands_are_values = 1
        commands_are_configurable = 2
        num_free_commands = 3
        max_commands = 4
        max_entry = max_commands

    class BarrierOperator:
        command = 0
        label = 1
        supported_signals = 2
        audible = 3
        visual = 4
        max_entry = visual

    class Basic:
        set = 0
        max_entry = set

    class BasicWindowCovering:
        open = 0
        close = 1
        max_entry = close

    class Battery:
        level = 0
        max_entry = level

    class CentralScene:
        start = 1
        end = 255
        scene_count = 256
        clear_scene_timeout = 257
        max_entry = clear_scene_timeout

    class ClimateControlSchedule:
        dow_monday = 1
        dow_tuesday = 2
        dow_wednesday = 3
        dow_thursday = 4
        dow_friday = 5
        dow_saturday = 6
        down_sunday = 7
        override_state = 8
        override_setback = 9
        max_entry = override_setback

    class Clock:
        day = 0
        hour = 1
        minute = 2
        max_entry = minute

    class Color:
        color = 0
        index = 1
        channels_capabilities = 2
        duration = 4
        max_entry = duration

    class Configuration:
        param_start = 0
        param_end = 255
        max_entry = param_end

    class ControllerReplication:
        node_id = 0
        function = 1
        replicate = 2
        max_entry = replicate

    class DoorLock:
        lock = 0
        lock_mode = 1
        system_config_mode = 2
        system_config_minutes = 3
        system_config_seconds = 4
        system_config_outside_handles = 5
        system_config_inside_handles = 6
        max_entry = system_config_inside_handles

    class DoorLockLogging:
        system_config_max_records = 0
        get_record_no = 1
        log_record = 2
        max_entry = log_record

    class EnergyProduction:
        instant = 0
        total = 1
        today = 2
        time = 3
        max_entry = time

    class Indicator:
        indicator = 0
        max_entry = indicator

    class Language:
        language = 0
        country = 1
        max_entry = country

    class Lock:
        locked = 0
        max_entry = locked

    class ManufacturerProprietary:
        fibaro_venetian_blinds_blinds = 0
        fibaro_venetian_blinds_tilt = 1
        max_entry = fibaro_venetian_blinds_tilt

    class ManufacturerSpecific:
        loaded_config = 0
        local_config = 1
        latest_config = 2
        device_id = 3
        serial_number = 4
        max_entry = serial_number

    class Meter:
        start = 1
        end = 31
        exporting = 32
        reset = 33
        max_entry = reset

    class MeterPulse:
        count = 0
        max_entry = count

    class PowerLevel:
        power_level = 0
        timeout = 1
        set = 2
        test_node = 3
        test_power_level = 4
        test_frames = 5
        test = 6
        report = 7
        test_status = 8
        test_ack_frames = 9
        max_entry = test_ack_frames

    class Protection:
        protection = 0
        max_entry = protection

    class SceneActivation:
        scene_id = 0
        duration = 1
        max_entry = duration

    class Security:
        secured = 0
        max_entry = secured

    class SensorAlarm:
        start = 0
        end = 255
        max_entry = end

    class SensorBinary:
        sensor = 0
        start = 1
        end = 255
        max_entry = end

    class SensorMultiLevel:
        start = 1
        end = 255
        max_entry = end

    class SimpleAV:
        command = 0
        max_entry = command

    class SoundSwitch:
        tone_count = 0
        tones = 1
        volume = 2
        default_tone = 3
        max_entry = default_tone

    class SwitchAll:
        switch_all = 0
        max_entry = switch_all

    class SwitchBinary:
        level = 0
        target_state = 1
        duration = 2
        max_entry = duration

    class SwitchMultiLevel:
        level = 0
        bright = 1
        dim = 2
        ignore_start_level = 3
        start_level = 4
        duration = 5
        step = 6
        inc = 7
        dec = 8
        target_value = 9
        max_entry = target_value

    class SwitchToggleBinary:
        toggle_switch = 0
        max_entry = toggle_switch

    class SwitchToggleMultilevel:
        level = 0
        max_entry = level

    class ThermostatFanMode:
        fan_mode = 0
        max_entry = fan_mode

    class ThermostatFanState:
        fan_state = 0
        max_entry = fan_state

    class ThermostatMode:
        mode = 0
        max_entry = mode

    class ThermostatOperatingState:
        operating_state = 0
        max_entry = operating_state

    class ThermostatSetpoint:
        unused0 = 0
        heating = 1
        cooling = 2
        unused3 = 3
        unused4 = 4
        unused5 = 5
        unused6 = 6
        furnace = 7
        dry_air = 8
        moist_air = 9
        auto_changeover = 10
        economy_heating = 11
        economy_cooling = 12
        away_heating = 13
        away_cooling = 14
        full_power = 15
        max_entry = full_power

    class TimeParameters:
        date = 0
        time = 1
        set = 2
        refresh = 3
        max_entry = refresh

    class UserCode:
        start = 1
        end = 254
        refresh = 255
        remove_code = 256
        count = 257
        raw_value = 258
        raw_value_index = 259
        max_entry = raw_value_index

    class Version:
        library = 0
        protocol = 1
        application = 2
        max_entry = application

    class WakeUp:
        interval = 0
        min_interval = 1
        max_interval = 2
        default_interval = 3
        interval_step = 4
        max_entry = interval_step

    class ZWavePlusInfo:
        version = 0
        installer_icon = 1
        user_icon = 2
        max_entry = user_icon


_index_mapping = {
    COMMAND_CLASS_NOTIFICATION: ValueIndexes.Alarm,
    COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION: ValueIndexes.AssociationCommandConfiguration,
    COMMAND_CLASS_BARRIER_OPERATOR: ValueIndexes.BarrierOperator,
    COMMAND_CLASS_BASIC: ValueIndexes.Basic,
    COMMAND_CLASS_BASIC_WINDOW_COVERING: ValueIndexes.BasicWindowCovering,
    COMMAND_CLASS_BATTERY: ValueIndexes.Battery,
    COMMAND_CLASS_CENTRAL_SCENE: ValueIndexes.CentralScene,
    COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE: ValueIndexes.ClimateControlSchedule,
    COMMAND_CLASS_SWITCH_COLOR: ValueIndexes.Color,
    COMMAND_CLASS_CLOCK: ValueIndexes.Clock,
    COMMAND_CLASS_CONFIGURATION: ValueIndexes.Configuration,
    COMMAND_CLASS_CONTROLLER_REPLICATION: ValueIndexes.ControllerReplication,
    COMMAND_CLASS_DOOR_LOCK: ValueIndexes.DoorLock,
    COMMAND_CLASS_DOOR_LOCK_LOGGING: ValueIndexes.DoorLockLogging,
    COMMAND_CLASS_ENERGY_PRODUCTION: ValueIndexes.EnergyProduction,
    COMMAND_CLASS_INDICATOR: ValueIndexes.Indicator,
    COMMAND_CLASS_LANGUAGE: ValueIndexes.Language,
    COMMAND_CLASS_LOCK: ValueIndexes.Lock,
    COMMAND_CLASS_MANUFACTURER_PROPRIETARY: ValueIndexes.ManufacturerProprietary,
    COMMAND_CLASS_MANUFACTURER_SPECIFIC: ValueIndexes.ManufacturerSpecific,
    COMMAND_CLASS_METER: ValueIndexes.Meter,
    COMMAND_CLASS_METER_PULSE: ValueIndexes.MeterPulse,
    COMMAND_CLASS_POWERLEVEL: ValueIndexes.PowerLevel,
    COMMAND_CLASS_PROTECTION: ValueIndexes.Protection,
    COMMAND_CLASS_SCENE_ACTIVATION: ValueIndexes.SceneActivation,
    COMMAND_CLASS_SECURITY: ValueIndexes.Security,
    COMMAND_CLASS_SENSOR_ALARM: ValueIndexes.SensorAlarm,
    COMMAND_CLASS_SENSOR_BINARY: ValueIndexes.SensorBinary,
    COMMAND_CLASS_SENSOR_MULTILEVEL: ValueIndexes.SensorMultiLevel,
    COMMAND_CLASS_SIMPLE_AV_CONTROL: ValueIndexes.SimpleAV,
    COMMAND_CLASS_SOUND_SWITCH: ValueIndexes.SoundSwitch,
    COMMAND_CLASS_SWITCH_ALL: ValueIndexes.SwitchAll,
    COMMAND_CLASS_SWITCH_BINARY: ValueIndexes.SwitchBinary,
    COMMAND_CLASS_SWITCH_MULTILEVEL: ValueIndexes.SwitchMultiLevel,
    COMMAND_CLASS_SWITCH_TOGGLE_BINARY: ValueIndexes.SwitchToggleBinary,
    COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL: ValueIndexes.SwitchToggleMultilevel,
    COMMAND_CLASS_THERMOSTAT_FAN_MODE: ValueIndexes.ThermostatFanMode,
    COMMAND_CLASS_THERMOSTAT_FAN_STATE: ValueIndexes.ThermostatFanState,
    COMMAND_CLASS_THERMOSTAT_MODE: ValueIndexes.ThermostatMode,
    COMMAND_CLASS_THERMOSTAT_OPERATING_STATE: ValueIndexes.ThermostatOperatingState,
    COMMAND_CLASS_THERMOSTAT_SETPOINT: ValueIndexes.ThermostatSetpoint,
    COMMAND_CLASS_TIME_PARAMETERS: ValueIndexes.TimeParameters,
    COMMAND_CLASS_USER_CODE: ValueIndexes.UserCode,
    COMMAND_CLASS_VERSION: ValueIndexes.Version,
    COMMAND_CLASS_WAKE_UP: ValueIndexes.WakeUp,
    COMMAND_CLASS_ZWAVE_PLUS_INFO: ValueIndexes.ZWavePlusInfo
}
