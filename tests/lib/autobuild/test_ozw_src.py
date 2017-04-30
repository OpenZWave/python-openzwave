#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
.. module:: tests

This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave Library

.. moduleauthor: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com>

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

import sys, os, shutil, stat
import time
import unittest
from pprint import pprint
import datetime
import random
import socket
import libopenzwave
from tests.lib.common import TestLib
import re
import glob
from tests.common import pyozw_version
import six

OZWDIR = "openzwave"

class TestOzwSrc(TestLib):

    def test_010_command_classes(self):
        manager = libopenzwave.PyManager()
        CLASSID = re.compile(r"StaticGetCommandClassId\(\)\{ return (.*);")
        CLASSST = re.compile(r'StaticGetCommandClassName\(\)\{ return "(.*)";')
        headers = glob.glob(os.path.join (OZWDIR, 'cpp', 'src', 'command_classes', '*.h'))
        for header in headers:
            classid = None
            classst = None
            if not (header.endswith('CommandClass.h') or header.endswith('CommandClasses.h')):
                with open(header, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        match = CLASSID.search(line)
                        if match:
                            classid = match.group(1)
                        else:
                            match = CLASSST.search(line)
                            if match:
                                classst = match.group(1)
                    print(header)
                    print(classid, ':', classst)
                    self.assertEqual(classst, manager.COMMAND_CLASS_DESC[int(classid,16)])

    def test_020_notification_types(self):
        with open(os.path.join (OZWDIR, 'cpp', 'src', 'Notification.h'), 'r') as f:
            lines = ''.join(f.readlines())
            #~ print(lines)
            types = re.search(r"enum NotificationType.*\{(.*)\}.*enum NotificationCode", lines, re.MULTILINE|re.DOTALL).group(1)
            #~ print(types)
            alls = re.findall(r"Type_(\w*)", types, re.MULTILINE)
            #~ print(alls)
            for i,j in zip(range(len(alls)),alls):
                print(libopenzwave.PyNotifications[i], j)
                self.assertEqual(libopenzwave.PyNotifications[i], j)

    def test_030_notification_codes(self):
        with open(os.path.join (OZWDIR, 'cpp', 'src', 'Notification.h'), 'r') as f:
            lines = ''.join(f.readlines())
            #~ print(lines)
            types = re.search(r"enum NotificationCode.*\{(.*)\}.*NotificationType GetType", lines, re.MULTILINE|re.DOTALL).group(1)
            #~ print(types)
            alls = re.findall(r"Code_(\w*)", types, re.MULTILINE)
            #~ print(alls)
            for i,j in zip(range(len(alls)),alls):
                print(libopenzwave.PyNotificationCodes[i], j)
                self.assertEqual(libopenzwave.PyNotificationCodes[i], j)

    def test_040_value_genres(self):
        with open(os.path.join (OZWDIR, 'cpp', 'src', 'value_classes', 'ValueID.h'), 'r') as f:
            lines = ''.join(f.readlines())
            #~ print(lines)
            values = re.search(r"enum ValueGenre.*\{(.*)\}.*enum ValueType", lines, re.MULTILINE|re.DOTALL).group(1)
            #~ print(values)
            alls = re.findall(r"ValueGenre_(\w*)", values, re.MULTILINE)
            print(alls)
            for i,j in zip(range(len(alls)-1),alls):
                print(libopenzwave.PyGenres[i], j)
                self.assertEqual(libopenzwave.PyGenres[i], j)

    def test_050_value_types(self):
        with open(os.path.join (OZWDIR, 'cpp', 'src', 'value_classes', 'ValueID.h'), 'r') as f:
            lines = ''.join(f.readlines())
            #~ print(lines)
            values = re.search(r"enum ValueType.*\{(.*)\}.*uint32 GetHomeId", lines, re.MULTILINE|re.DOTALL).group(1)
            #~ print(values)
            alls = re.findall(r"ValueType_(\w*)", values, re.MULTILINE)
            print(alls)
            for i,j in zip(range(len(alls)-2),alls):
                print(libopenzwave.PyValueTypes[i], j)
                self.assertEqual(libopenzwave.PyValueTypes[i], j)

    def test_060_controller_command(self):
        with open(os.path.join (OZWDIR, 'cpp', 'src', 'Driver.h'), 'r') as f:
            lines = ''.join(f.readlines())
            #~ print(lines)
            values = re.search(r"enum ControllerCommand.*\{(.*)\}.*enum ControllerState", lines, re.MULTILINE|re.DOTALL).group(1)
            #~ print(values)
            alls = re.findall(r"ControllerCommand_(\w*)", values, re.MULTILINE)
            print(alls)
            for i,j in zip(range(len(alls)),alls):
                print(libopenzwave.PyControllerCommand[i], j)
                self.assertEqual(libopenzwave.PyControllerCommand[i], j)

    def test_070_controller_state(self):
        with open(os.path.join (OZWDIR, 'cpp', 'src', 'Driver.h'), 'r') as f:
            lines = ''.join(f.readlines())
            #~ print(lines)
            values = re.search(r"enum ControllerState.*\{(.*)\}.*enum ControllerError", lines, re.MULTILINE|re.DOTALL).group(1)
            #~ print(values)
            alls = re.findall(r"ControllerState_(\w*)", values, re.MULTILINE)
            print(alls)
            for i,j in zip(range(len(alls)),alls):
                print(libopenzwave.PyControllerState[i], j)
                self.assertEqual(libopenzwave.PyControllerState[i], j)

    def test_080_controller_error(self):
        with open(os.path.join (OZWDIR, 'cpp', 'src', 'Driver.h'), 'r') as f:
            lines = ''.join(f.readlines())
            #~ print(lines)
            values = re.search(r"enum ControllerError.*\{(.*)\}.*typedef void", lines, re.MULTILINE|re.DOTALL).group(1)
            #~ print(values)
            alls = re.findall(r"ControllerError_(\w*)", values, re.MULTILINE)
            print(alls)
            for i,j in zip(range(len(alls)),alls):
                print(libopenzwave.PyControllerError[i], j)
                self.assertEqual(libopenzwave.PyControllerError[i], j)

    def test_090_controller_interface(self):
        with open(os.path.join (OZWDIR, 'cpp', 'src', 'Driver.h'), 'r') as f:
            lines = ''.join(f.readlines())
            #~ print(lines)
            values = re.search(r"enum ControllerInterface.*\{(.*)\}.*private:", lines, re.MULTILINE|re.DOTALL).group(1)
            #~ print(values)
            alls = re.findall(r"ControllerInterface_(\w*)", values, re.MULTILINE)
            print(alls)
            for i,j in zip(range(len(alls)),alls):
                print(libopenzwave.PyControllerInterface[i], j)
                self.assertEqual(libopenzwave.PyControllerInterface[i], j)

    def test_100_option_types(self):
        with open(os.path.join (OZWDIR, 'cpp', 'src', 'Options.h'), 'r') as f:
            lines = ''.join(f.readlines())
            #~ print(lines)
            values = re.search(r"enum OptionType.*\{(.*)\}.*static Options", lines, re.MULTILINE|re.DOTALL).group(1)
            #~ print(values)
            alls = re.findall(r"OptionType_(\w*)", values, re.MULTILINE)
            print(alls)
            for i,j in zip(range(len(alls)),alls):
                print(libopenzwave.PyOptionType[i], j)
                self.assertEqual(libopenzwave.PyOptionType[i], j)

    def test_110_option_names(self):
        with open(os.path.join (OZWDIR, 'cpp', 'src', 'Options.cpp'), 'r') as f:
            lines = ''.join(f.readlines())
            #~ print(lines)
            values = re.search(r"s_instance = new Options(.*)return s_instance", lines, re.MULTILINE|re.DOTALL).group(1)
            #~ print(values)
            alls = re.findall(r's_instance->AddOption(\w*).*\([\t]*"(\w*)",[\t]*(.*);(.*)$', values, re.MULTILINE)
            #~ alls = re.findall(r's_instance->AddOption(\w*).*\(\t"(\w*).*\t(.*) \);(.*)$', values, re.MULTILINE)
            print(alls)
            for i in alls:
                print(i)
                self.assertTrue(i[1] in libopenzwave.PyOptionList)
                self.assertEqual(libopenzwave.PyOptionList[i[1]]['type'], i[0])

    def test_120_log_level(self):
        with open(os.path.join (OZWDIR, 'cpp', 'src', 'platform', 'Log.h'), 'r') as f:
            lines = ''.join(f.readlines())
            #~ print(lines)
            values = re.search(r"enum LogLevel.*\{(.*)\}.*class i_LogImpl", lines, re.MULTILINE|re.DOTALL).group(1)
            #~ print(values)
            alls = re.findall(r"LogLevel_(\w*)", values, re.MULTILINE)
            print(alls)
            for i,j in zip(range(len(alls)),alls):
                print(libopenzwave.PyLogLevels[j])
                self.assertTrue(j in libopenzwave.PyLogLevels)
                self.assertEqual(libopenzwave.PyLogLevels[j]['value'], i)

    def test_130_manager_functions(self):
        PRIVATES = ['SetDriverReady', 'NotifyWatchers']
        RENAMES = [('SoftReset', ['SoftResetController']), 
                    ('GetValueListSelection', ['GetValueListSelectionStr','GetValueListSelectionNum']),
                    ('SetValueListSelection', ['SetValue']),
                    ('AddSceneValueListSelection', ['AddSceneValue','AddSceneValue']),
                    ('SceneGetValueAsBool', ['SceneGetValues']),
                    ('SceneGetValueAsByte', ['SceneGetValues']),
                    ('SceneGetValueAsFloat', ['SceneGetValues']),
                    ('SceneGetValueAsInt', ['SceneGetValues']),
                    ('SceneGetValueAsShort', ['SceneGetValues']),
                    ('SceneGetValueAsString', ['SceneGetValues']),
                    ('SceneGetValueListSelection', ['SceneGetValues']),
                    ('SetSceneValueListSelection', ['setSceneValue']),
                ]
        with open(os.path.join (OZWDIR, 'cpp', 'src', 'Manager.h'), 'r') as f:
            lines = ''.join(f.readlines())
            #~ print(lines)
            code = re.search(r"namespace OpenZWave(.*)\} // namespace OpenZWave", lines, re.MULTILINE|re.DOTALL).group(1)
            #~ print(code)
            funcvoids = re.findall(r"void (\w*)\( ", code, re.MULTILINE)
            print(funcvoids)
            funcbools = re.findall(r"bool (\w*)\( ", code, re.MULTILINE)
            print(funcbools)
            funcuint8s = re.findall(r"uint8 (\w*)\( ", code, re.MULTILINE)
            print(funcuint8s)
            funcstrings = re.findall(r"string (\w*)\( ", code, re.MULTILINE)
            print(funcstrings)
            funcint32s = re.findall(r"int32 (\w*)\( ", code, re.MULTILINE)
            print(funcint32s)
            funcuint32s = re.findall(r"uint32 (\w*)\( ", code, re.MULTILINE)
            print(funcuint32s)
            funcuint16s = re.findall(r"uint16 (\w*)\( ", code, re.MULTILINE)
            print(funcuint16s)
            funcs = funcvoids + funcbools + funcuint8s + funcstrings + funcint32s + funcuint32s + funcuint16s
            funcs2 = funcs[:]
            for f in funcs2:
                if f in PRIVATES:
                    funcs.remove(f)
                for g in RENAMES:
                    #~ print g
                    if g[0] == f:
                        funcs.remove(g[0])
                        funcs += g[1]
            print(funcs)
            for i in funcs:
                py = i[0].lower() + i[1:]
                print("Check %s (%s)"%(i, py))
                self.assertTrue(hasattr(libopenzwave.PyManager,py))

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
