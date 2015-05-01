#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
.. module:: tests

This file is part of **python-openzwave** project https://github.com/bibi21000/python-openzwave.
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

class TestInit(TestLib):

    def test_000_init(self):
        manager = libopenzwave.PyManager()
        self.assertEqual(manager.getPythonLibraryVersionNumber(), pyozw_version)
        vers=re.findall(r'\d+', manager.getOzwLibraryVersionNumber())
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
        self.assertEqual('ozwlog.log', options.getOptionAsString("LogFileName"))
        self.assertEqual(1, options.getOptionAsInt("SaveLogLevel"))
        self.assertTrue(options.destroy())

class TestOptions(TestLib):
    def setUp(self):
        self._options = libopenzwave.PyOptions()
        self._configpath = self._options.getConfigPath()
        self._options.create(self._configpath, self.userpath, '')

    def tearDown(self):
        self._options.destroy()
        self._configpath = None
        self._options = None

    def test_010_options_string(self):
        self.assertTrue(self._options.addOptionString("LogFileName", 'ozwlog.log', False))
        self.assertEqual('ozwlog.log', self._options.getOptionAsString("LogFileName"))

    def test_020_options_bool(self):
        self.assertTrue(self._options.addOptionBool("Logging", True))
        self.assertEqual(True, self._options.getOptionAsBool("Logging"))

    def test_030_options_int(self):
        self.assertTrue(self._options.addOptionInt("SaveLogLevel", libopenzwave.PyLogLevels['Always']['value']))
        self.assertEqual(libopenzwave.PyLogLevels['Always']['value'], self._options.getOptionAsInt("SaveLogLevel"))

    def test_040_options_generic(self):
        self.assertTrue(self._options.addOption("LogFileName", 'ozwlog.log'))
        self.assertEqual('ozwlog.log', self._options.getOption("LogFileName"))
        self.assertTrue(self._options.addOption("Logging", True))
        self.assertEqual(True, self._options.getOption("Logging"))
        self.assertTrue(self._options.addOption("SaveLogLevel", libopenzwave.PyLogLevels['Always']['value']))
        self.assertEqual(libopenzwave.PyLogLevels['Always']['value'], self._options.getOption("SaveLogLevel"))

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
