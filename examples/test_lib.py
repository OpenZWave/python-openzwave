#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave wrapper

.. moduleauthor:: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com>

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
import sys, os
import time
import libopenzwave
from libopenzwave import PyManager

device="/dev/ttyUSB0"
log="Info"
sniff=60.0

for arg in sys.argv:
    if arg.startswith("--device"):
        temp,device = arg.split("=")
    elif arg.startswith("--log"):
        temp,log = arg.split("=")
    elif arg.startswith("--sniff"):
        temp,sniff = arg.split("=")
        sniff = float(sniff)
    if arg.startswith("--help"):
        print("help : ")
        print("  --device=/dev/yourdevice ")
        print("  --log=Info|Debug")
        print("  --sniff=0 : sniff for zwave messages a number of seconds")
        exit(0)

options = libopenzwave.PyOptions(config_path="../openzwave/config", \
  user_path=".", cmd_line="--logging true")

# Specify the open-zwave config path here
options.lock()
manager = libopenzwave.PyManager()
manager.create()

# callback order: (notificationtype, homeid, nodeid, ValueID, groupidx, event)
def callback(args):
    print('\n-------------------------------------------------')
    print('\n[{}]:\n'.format(args['notificationType'])) 
    if args:
        print('homeId: 0x{0:08x}'.format(args['homeId']))
        print('nodeId: {}'.format(args['nodeId']))
        if 'valueId' in args:
            v = args['valueId']
            print('valueID: {}'.format(v['id']))
            if 'groupIndex' in v and v['groupIndex'] != 0xff: print('GroupIndex: {}'.format(v['groupIndex']))
            if 'event' in v and v['event'] != 0xff: print('Event: {}'.format(v['event']))
            if 'value' in v: print('Value: {}'.format(str(v['value'])))
            if 'label' in v: print('Label: {}'.format(v['label']))
            if 'units' in v: print('Units: {}'.format(v['units']))
            if 'readOnly' in v: print('ReadOnly: {}'.format(v['readOnly']))
    print('-------------------------------------------------\n')

print("Add watcher")
manager.addWatcher(callback)
print("Add device")
manager.addDriver(device)
print("Sniff network during {} seconds".format(sniff))
time.sleep(sniff)
print("Remove watcher")
manager.removeWatcher(callback)
print("Remove device")
manager.removeDriver(device)
