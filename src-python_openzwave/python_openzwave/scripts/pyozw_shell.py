#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: pyozw_shell

This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave API

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

__author__ = 'bibi21000'

import sys, os, optparse, re, shutil, datetime
import logging
import urwid
from pyozwman.ozwsh_main import MainWindow
from libopenzwave import configPath
import signal

def signal_term_handler(signal, frame):
    print('got SIGTERM')
    raise urwid.ExitMainLoop()

signal.signal(signal.SIGTERM, signal_term_handler)
signal.signal(signal.SIGINT, signal_term_handler)

def main():
    parser = optparse.OptionParser(
        usage="pyozw_shell [--device=/dev/ttyUSB0] [--log=Debug] ...")

    parser.add_option(
        '-d', '--device',
        dest='device',
        type="str",
        default="/dev/ttyUSB0",
        help="The path to your ZWave device")

    parser.add_option(
        '-l', '--log',
        dest='log',
        default="Debug",
        type="choice",
        choices=['Debug', 'Info'],
        help="The log level (Debug|Info)")

    def callback_config(option, opt_str, value, parser):
        if value is None :
            value = configPath()
            if value is None :
                raise optparse.OptionValueError("Can't determine the config path automatically.")
        setattr(parser.values, option.dest, value)

    parser.add_option(
        '-c', '--config',
        dest='config',
        action="callback",
        default=None,
        callback=callback_config,
        type="str",
        help="The config path")

    parser.add_option(
        '-u', '--user',
        dest='user',
        default=".",
        type="str",
        help="The user path")

    options, args = parser.parse_args()

    window = None
    window = MainWindow(device=options.device, loglevel=options.log, user_path=options.user, config_path=options.config)
    window.start()
    window.loop.run()
    window.stop()
    window.log.info("="*15 + " exit " + "="*15)

if __name__ == '__main__':
    main()
