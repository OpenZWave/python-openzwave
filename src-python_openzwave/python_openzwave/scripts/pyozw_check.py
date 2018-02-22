#!python
# -*- coding: utf-8 -*-
"""
This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X

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
import logging
h = logging.NullHandler()
logger = logging.getLogger(__name__).addHandler(h)
import time
import argparse

network_state = None
home_id = None
args = None

def imports(args):
    if args.timeout is None:
        args.timeout = 2
    if args.output == 'txt':
        print("-------------------------------------------------------------------------------")
        print("Import libs")
        print("Try to import libopenzwave")
        import libopenzwave
        print("Try to import libopenzwave.PyLogLevels")
        from libopenzwave import PyLogLevels
        print("Try to get options")
        options = libopenzwave.PyOptions(user_path=".", cmd_line="--logging false")
        options.lock()
        time.sleep(0.5)
        print("Try to get manager")
        manager = libopenzwave.PyManager()
        manager.create()
        print("Try to get python_openzwave version")
        print(manager.getPythonLibraryVersionNumber())
        print("Try to get python_openzwave full version")
        print(manager.getPythonLibraryVersion())
        print("Try to get openzwave version")
        print(manager.getPythonLibraryVersion())
        print("Try to get openzwave version")
        print(manager.getOzwLibraryVersion())
        print("Try to get default config path")
        print(libopenzwave.configPath())
        print("Try to destroy manager")
        manager.destroy()
        print("Try to destroy options")
        options.destroy()
        time.sleep(0.5)
        print("Try to import openzwave (API)")
        import openzwave
        
    elif args.output == 'raw':
        import libopenzwave
        from libopenzwave import PyLogLevels
        options = libopenzwave.PyOptions(user_path=".", cmd_line="--logging false")
        options.lock()
        time.sleep(0.5)
        manager = libopenzwave.PyManager()
        manager.create()
        print("{0}|{1}|{2}|{3}".format(
                manager.getOzwLibraryVersion(),
                manager.getPythonLibraryVersionNumber(),
                manager.getPythonLibraryVersion(),
                libopenzwave.configPath()
                ))
        manager.destroy()
        options.destroy()
        time.sleep(0.5)
        import openzwave

def zwcallback(zwargs):
    import libopenzwave
    global args
    if args.output == 'txt':
        print('--------------------------------- zwcallback with args=[%s]' % zwargs)
    notify_type = zwargs['notificationType']
    global network_state
    network_state = notify_type
    if notify_type == "DriverReady":
        global home_id
        home_id = zwargs['homeId']
    
    #~ print("Received {0} : {1}".format(notify_type,libopenzwave.PyNotifications[notify_type].doc))
    if args.output == 'txt':
        print("Received {0}".format(notify_type))

def init_device(args):
    global home_id
    if args.timeout is None:
        args.timeout = 15
    if args.output == 'txt':
        print("-------------------------------------------------------------------------------")
        print("Intialize device {0}".format(args.device))
        import libopenzwave
        print("Try to get options")
        options = libopenzwave.PyOptions(config_path=args.config_path, user_path=args.user_path, cmd_line="--logging true")
        options.lock()
        time.sleep(1.0)
        print("Try to get manager")
        manager = libopenzwave.PyManager()
        manager.create()
        print("Try to get python_openzwave version")
        print(manager.getPythonLibraryVersionNumber())
        print("Try to get python_openzwave full version")
        print(manager.getPythonLibraryVersion())
        print("Try to get openzwave version")
        print(manager.getOzwLibraryVersion())
        print("Try to get default config path")
        print(libopenzwave.configPath())
        print("Try to add watcher")
        manager.addWatcher(zwcallback)
        time.sleep(1.0)
        manager.addDriver(args.device)
        print("Wait for notifications ({0}s)".format(args.timeout))
        next_print = args.timeout/10
        delta = 0.1
        for i in range(0, int(args.timeout/delta)):
            time.sleep(delta)
            next_print -= delta
            if next_print < 0:
                next_print = args.timeout/10
                print('.')
        print("Try to remove driver")
        manager.removeDriver(args.device)
        time.sleep(3.0)
        print("Try to remove watcher")
        manager.removeWatcher(zwcallback)
        print("Try to destroy manager")
        manager.destroy()
        time.sleep(0.2)
        print("Try to destroy options")
        options.destroy()
        time.sleep(1.0)
        print("Retrieve HomeID")
        print("{0:08x}".format(home_id))
    elif args.output == 'raw':
        import libopenzwave
        options = libopenzwave.PyOptions(config_path=args.config_path, user_path=args.user_path, cmd_line="--logging false")
        options.lock()
        time.sleep(1.0)
        manager = libopenzwave.PyManager()
        manager.create()
        manager.addWatcher(zwcallback)
        time.sleep(1.0)
        manager.addDriver(args.device)
        next_print = args.timeout/10
        delta = 0.1
        for i in range(0, int(args.timeout/delta)):
            time.sleep(delta)
        print("{0}|{1}|{2}|{3}|{4:08x}".format(
                manager.getOzwLibraryVersion(),
                manager.getPythonLibraryVersionNumber(),
                manager.getPythonLibraryVersion(),
                libopenzwave.configPath(),
                home_id,
                ))
        manager.removeDriver(args.device)
        time.sleep(0.5)
        manager.removeWatcher(zwcallback)
        manager.destroy()
        time.sleep(0.2)
        options.destroy()

def list_nodes(args):
    global home_id
    if args.timeout is None:
        args.timeout = 60*60*4+1
    import openzwave
    from openzwave.node import ZWaveNode
    from openzwave.value import ZWaveValue
    from openzwave.scene import ZWaveScene
    from openzwave.controller import ZWaveController
    from openzwave.network import ZWaveNetwork
    from openzwave.option import ZWaveOption

    #Define some manager options
    print("-------------------------------------------------------------------------------")
    print("Define options for device {0}".format(args.device))
    options = ZWaveOption(device=args.device, config_path=args.config_path, user_path=args.user_path)
    options.set_log_file("OZW_Log.log")
    options.set_append_log_file(False)
    options.set_console_output(False)
    options.set_save_log_level("Debug")
    options.set_logging(True)
    options.lock()

    print("Start network")
    network = ZWaveNetwork(options, log=None)

    delta = 0.5
    for i in range(0, int(args.timeout/delta)):
        time.sleep(delta)
        if network.state >= network.STATE_AWAKED:
            break

    print("-------------------------------------------------------------------------------")
    print("Network is awaked. Talk to controller.")
    print("Get python_openzwave version : {}".format(network.controller.python_library_version))
    print("Get python_openzwave config version : {}".format(network.controller.python_library_config_version))
    print("Get python_openzwave flavor : {}".format(network.controller.python_library_flavor))
    print("Get openzwave version : {}".format(network.controller.ozw_library_version))
    print("Get config path : {}".format(network.controller.library_config_path))
    print("Controller capabilities : {}".format(network.controller.capabilities))
    print("Controller node capabilities : {}".format(network.controller.node.capabilities))
    print("Nodes in network : {}".format(network.nodes_count))

    print("-------------------------------------------------------------------------------")
    if args.timeout > 1800:
        print("You defined a really long timneout. Please use --help to change this feature.")
    print("Wait for network ready ({0}s)".format(args.timeout))
    for i in range(0, int(args.timeout/delta)):
        time.sleep(delta)
        if network.state == network.STATE_READY:
            break
    print("-------------------------------------------------------------------------------")
    if network.state == network.STATE_READY:
        print("Network is ready. Get nodes")
    elif network.state == network.STATE_AWAKED:
        print("Network is awake. Some sleeping devices may miss. You can increase timeout to get them. But will continue.")
    else:
        print("Network is still starting. You MUST increase timeout. But will continue.")

    for node in network.nodes:

        print("------------------------------------------------------------")
        print("{} - Name : {} ( Location : {} )".format(network.nodes[node].node_id, network.nodes[node].name, network.nodes[node].location))
        print(" {} - Ready : {} / Awake : {} / Failed : {}".format(network.nodes[node].node_id, network.nodes[node].is_ready, network.nodes[node].is_awake, network.nodes[node].is_failed))
        print(" {} - Manufacturer : {}  ( id : {} )".format(network.nodes[node].node_id, network.nodes[node].manufacturer_name, network.nodes[node].manufacturer_id))
        print(" {} - Product : {} ( id  : {} / type : {} / Version : {})".format(network.nodes[node].node_id, network.nodes[node].product_name, network.nodes[node].product_id, network.nodes[node].product_type, network.nodes[node].version))
        print(" {} - Command classes : {}".format(network.nodes[node].node_id, network.nodes[node].command_classes_as_string))
        print(" {} - Capabilities : {}".format(network.nodes[node].node_id, network.nodes[node].capabilities))
        print(" {} - Neighbors : {} / Power level : {}".format(network.nodes[node].node_id, network.nodes[node].neighbors, network.nodes[node].get_power_level()))
        print(" {} - Is sleeping : {} / Can wake-up : {} / Battery level : {}".format(network.nodes[node].node_id, network.nodes[node].is_sleeping, network.nodes[node].can_wake_up(), network.nodes[node].get_battery_level()))

    print("------------------------------------------------------------")
    print("Driver statistics : {}".format(network.controller.stats))
    print("------------------------------------------------------------")
    print("Stop network")
    network.stop()
    print("Exit")
                
def pyozw_parser():
    parser = argparse.ArgumentParser(description='Run python_openzwave basics checks.')
    parser.add_argument('-o', '--output', action='store', help='The format (txt, raw, ...)', choices=['txt', 'raw'], default='txt')
    parser.add_argument('-d', '--device', action='store', help='The device port', default='/dev/ttyUSB0')
    parser.add_argument('-m', '--imports', action='store_true', help='Import all libs', default=True)
    parser.add_argument('-i', '--init_device', action='store_true', help='Intialize the device', default=False)
    parser.add_argument('-l', '--list_nodes', action='store_true', help='List the nodes on zwave network', default=False)
    parser.add_argument('-t', '--timeout', action='store',type=int, help='The default timeout for zwave network sniffing', default=None)
    parser.add_argument('--config_path', action='store', help='The config_path for openzwave', default=None)
    parser.add_argument('--user_path', action='store', help='The user_path for openzwave', default=".")
    return parser

def main():
    parser = pyozw_parser()
    global args
    args = parser.parse_args()
    if args.init_device:
        init_device(args)
    elif args.list_nodes:
        list_nodes(args)
    elif args.imports:
        imports(args)
        
if __name__ == '__main__':
    main()

