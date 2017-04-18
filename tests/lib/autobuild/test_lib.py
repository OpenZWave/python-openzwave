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
from tests.common import pyozw_version
import six

class TestInit(TestLib):

    def test_000_init(self):
        manager = libopenzwave.PyManager()
        self.assertEqual(manager.getPythonLibraryVersionNumber(), pyozw_version)
        vers=re.findall(u'\d+', manager.getOzwLibraryVersionNumber())
        self.assertEqual(len(vers),3)

    def test_010_options_exceptions(self):
        fake_config_dir = os.path.join(self.userpath,'fake_config_dir')
        fake_user_dir = os.path.join(self.userpath,'fake_user_dir')
        with self.assertRaises(libopenzwave.LibZWaveException):
            options = libopenzwave.PyOptions(config_path="non_exisitng_dir", user_path=None, cmd_line=None)
        try:
            shutil.rmtree(self.userpath)
        except:
            pass
        os.makedirs(self.userpath)
        os.makedirs(fake_config_dir)
        os.chmod(fake_config_dir, stat.S_IREAD|stat.S_IRUSR|stat.S_IRGRP|stat.S_IROTH)
        with self.assertRaises(libopenzwave.LibZWaveException):
            options = libopenzwave.PyOptions(config_path=fake_config_dir, user_path=None, cmd_line=None)

        try:
            shutil.rmtree(self.userpath)
        except:
            pass
        os.makedirs(self.userpath)
        os.makedirs(fake_config_dir)
        os.chmod(fake_config_dir, stat.S_IREAD|stat.S_IRUSR|stat.S_IRGRP|stat.S_IROTH|stat.S_IWRITE|stat.S_IWUSR|stat.S_IWGRP|stat.S_IWOTH)
        with self.assertRaises(libopenzwave.LibZWaveException):
            options = libopenzwave.PyOptions(config_path=fake_config_dir, user_path=None, cmd_line=None)

        options = libopenzwave.PyOptions(config_path=None, user_path=None, cmd_line="")

    def test_020_options_without_command_line(self):
        options = libopenzwave.PyOptions()
        configpath = options.getConfigPath()
        self.assertNotEqual(configpath, None)
        self.assertTrue(os.path.exists(os.path.join(configpath, "zwcfg.xsd")))
        self.assertTrue(options.destroy())

    def test_030_options_with_command_line(self):
        options = libopenzwave.PyOptions(cmd_line='--LogFileName ozwlog.log --Logging --SaveLogLevel 1')
        self.assertTrue(options.lock())
        self.assertTrue(options.areLocked())
        self.assertEqual(True, options.getOptionAsBool("Logging"))
        self.assertEqual(six.u('ozwlog.log'), six.u(options.getOptionAsString("LogFileName")))
        self.assertEqual(1, options.getOptionAsInt("SaveLogLevel"))
        self.assertTrue(options.destroy())

    def test_050_version(self):
        time.sleep(1.0)
        from pyozw_version import pyozw_version
        manager = libopenzwave.PyManager()
        version = manager.getPythonLibraryVersion()
        self.assertEqual(version.find("None"), -1)

class TestOptions(TestLib):

    def test_010_options_string(self):
        _options = libopenzwave.PyOptions()
        _configpath = _options.getConfigPath()
        _options.create(_configpath, self.userpath, '')
        self.assertTrue(_options.addOptionString("LogFileName", 'ozwlog.log', False))
        self.assertEqual('ozwlog.log', _options.getOptionAsString("LogFileName"))
        _options.destroy()
        _configpath = None
        _options = None

    def test_020_options_bool(self):
        _options = libopenzwave.PyOptions()
        _configpath = _options.getConfigPath()
        _options.create(_configpath, self.userpath, '')
        self.assertTrue(_options.addOptionBool("Logging", True))
        self.assertEqual(True, _options.getOptionAsBool("Logging"))
        _options.destroy()
        _configpath = None
        _options = None

    def test_030_options_int(self):
        _options = libopenzwave.PyOptions()
        _configpath = _options.getConfigPath()
        _options.create(_configpath, self.userpath, '')
        self.assertTrue(_options.addOptionInt("SaveLogLevel", libopenzwave.PyLogLevels['Always']['value']))
        self.assertEqual(libopenzwave.PyLogLevels['Always']['value'], _options.getOptionAsInt("SaveLogLevel"))
        _options.destroy()
        _configpath = None
        _options = None

    def test_040_options_generic(self):
        _options = libopenzwave.PyOptions()
        _configpath = _options.getConfigPath()
        _options.create(_configpath, self.userpath, '')
        self.assertTrue(_options.addOption("LogFileName", 'ozwlog.log'))
        self.assertEqual('ozwlog.log', _options.getOption("LogFileName"))
        self.assertTrue(_options.addOption("Logging", True))
        self.assertEqual(True, _options.getOption("Logging"))
        self.assertTrue(_options.addOption("SaveLogLevel", libopenzwave.PyLogLevels['Always']['value']))
        self.assertEqual(libopenzwave.PyLogLevels['Always']['value'], _options.getOption("SaveLogLevel"))
        _options.destroy()
        _configpath = None
        _options = None

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
