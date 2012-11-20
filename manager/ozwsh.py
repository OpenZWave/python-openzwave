#!/usr/bin/env python
# -* coding: utf-8 -*-

#Author: bibi21000
#Licence : GPL

__author__ = 'bibi21000'

from select import select
import sys
import os
import urwid
from urwid.raw_display import Screen
#import headerpanel
#import dirpanel
#import setuppanel
from traceback import format_exc
#from ucp import UrwidCmdProc, isUCP
#from utils import utilInit, log
sys.path.insert(0, os.path.abspath('../build/tmp/usr/local/lib/python2.6/dist-packages'))
sys.path.insert(0, os.path.abspath('../build/tmp/usr/local/lib/python2.7/dist-packages'))
sys.path.insert(0, os.path.abspath('build/tmp/usr/local/lib/python2.6/dist-packages'))
sys.path.insert(0, os.path.abspath('build/tmp/usr/local/lib/python2.7/dist-packages'))
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
from pyozwman.ozwsh_widgets import OldestTree
from pyozwman.ozwsh_widgets import RootTree, RootBox, RootItem, RootDir
from pyozwman.ozwsh_widgets import ControllerTree, ControllerBox
from pyozwman.ozwsh_widgets import NodeTree, NodeBox
from pyozwman.ozwsh_widgets import NodesTree, NodesBox, NodesItem
from pyozwman.ozwsh_widgets import SensorsTree, SensorsBox, SensorsItem
from pyozwman.ozwsh_widgets import SwitchesTree, SwitchesBox, SwitchesItem
from pyozwman.ozwsh_widgets import DimmersTree, DimmersBox
from pyozwman.ozwsh_widgets import ValuesTree, ValuesBox, ValuesItem
from pyozwman.ozwsh_widgets import GroupsTree, GroupsBox, AssociationItem
from pyozwman.ozwsh_widgets import SceneTree, SceneBox, SceneItem
from pyozwman.ozwsh_widgets import ScenesTree, ScenesBox, ScenesItem
from pyozwman.ozwsh_widgets import StatTree, StatBox

from louie import dispatcher, All
import logging
#from frameapp import FrameApp, DIVIDER

logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('openzwave')

device = "/dev/zwave-aeon-s2"
log = "Debug"
footer = True
for arg in sys.argv:
    if arg.startswith("--help") or arg.startswith("-h"):
        print("Usage : ozwman [--device=/dev/zwave-aeon-s2] [--log=Debug]")
        print("   --device=path_to_your_zwave_stick")
        print("   --log=Info|Debug|None")
        print("     Look at debug.log and OZW_Log.log")
        sys.exit("")
    elif arg.startswith("--device"):
        temp,device = arg.split("=")
    elif arg.startswith("--log"):
        temp,log = arg.split("=")

MAIN_TITLE = "openzwave Shell"
"""
/nodes
    node_id/
        name
        ...
        commands/
            command_id/
                name
                value_1/
                    min
                    max
                    items
                    ...
                value_2/
                value_3/
                value_4/
        switches/
        sensors/

/scenes
/controller

"""

class StatusBar(urwid.WidgetWrap):
    def __init__(self, window):
        self.window = window
        self.statusbar = "%s"
        self.statusbar_urwid = urwid.Text(self.statusbar % "", wrap='clip')
        self.cmd = "$ %s"
        self.cmd_urwid = urwid.Edit(self.cmd % "")
        display_widget = urwid.Pile([ \
            urwid.Divider("-"),
            self.statusbar_urwid, \
            urwid.Divider("-"),
            self.cmd_urwid, \
            ])
        urwid.WidgetWrap.__init__(self, display_widget)

    def update(self, status=None, cmd=None):
        if status != None:
            self.statusbar_urwid.set_text(self.statusbar % status)
        if cmd != None:
            self.set_command(cmd)

    def get_command(self):
        return self.cmd_urwid.get_edit_text()

    def set_command(self, cmd):
        self.cmd_urwid.set_edit_text(cmd)

class HeaderBar(urwid.WidgetWrap):
    def __init__(self, window):
        self.window = window
        self.cwd = "Path : %s"
        self.cwd_urwid = urwid.Text(self.cwd % "")
        display_widget = urwid.Pile([ \
            urwid.AttrWrap(urwid.Text(MAIN_TITLE), 'header'),\
            urwid.Divider("-"), \
            self.cwd_urwid, \
            urwid.Divider("-"), \
            ])
        urwid.WidgetWrap.__init__(self, display_widget)

    def update(self, cwd=None):
        if cwd != None:
            self.cwd_urwid.set_text(self.cwd % cwd)

class MainWindow(Screen):
    def __init__(self, device=None, footer=False, name=None):
        Screen.__init__(self)
        self.device = device
        self.footer_display = footer
        self._define_log()
        self._define_screen()
        self._connect_louie()
        self._start_network()

    def _define_log(self):
        hdlr = logging.FileHandler('/tmp/urwidcmd.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.log = logging.getLogger('openzwave')
        self.log.addHandler(hdlr)
        self.log.setLevel(logging.DEBUG)
        self.log.info("="*15 + " start " + "="*15)

    def _define_screen(self):
        self._palette = [("title", "yellow", "dark cyan"),
        ("keys", "dark blue", "light gray"),
        ("message", "light cyan", "dark green"),
        ("linenr", "light blue", "dark cyan"),
        ("input", "light gray", "black"),
        ("input2", "dark red", "light gray"),
        ("focus", "black", "light gray", "bold"),
        ("dialog", "black", "light gray", "bold"),
        ("file", "light green", "dark blue"),
        ("errortxt", "dark red", "dark blue"),
        ("selectedfile", "yellow", "dark blue"),
        ("selectedfocus", "yellow", "light gray", "bold"),
        ("dir", "light gray", "dark blue"),
        ("fileedit", "light green", "dark red"),
        ('edit', 'yellow', 'dark blue'),
        ('body','default', 'default'),
        ('foot','dark cyan', 'dark blue', 'bold'),
        ('shadow','white','black'),
        ('border','black','dark blue'),
        ('error','black','dark red'),
        ('FxKey','light cyan', 'dark blue', 'underline')]
        self.network = None
        self.controller = None
        self.root_box = RootBox(self, None, "body")
        self.stat_box = StatBox(self, self.root_box, "body")
        self.controller_box = ControllerBox(self, self.root_box, "body")
        self.scenes_box = ScenesBox(self, self.root_box, "body")
        self.scene_box = SceneBox(self, self.scenes_box, "body")
        self.nodes_box = NodesBox(self, self.root_box, "body")
        self.switches_box = SwitchesBox(self, self.nodes_box, "body")
        self.dimmers_box = DimmersBox(self, self.nodes_box, "body")
        self.sensors_box = SensorsBox(self, self.nodes_box, "body")
        self.node_box = NodeBox(self, self.nodes_box, "body")
        self.values_box = ValuesBox(self, self.node_box, "body")
        self.groups_box = GroupsBox(self, self.node_box, "body")

        self.status_bar = StatusBar(self)
        self.header_bar = HeaderBar(self)

        self.framefocus = 'footer'

        self._active_box = self.root_box
        self.frame = urwid.Frame(urwid.AttrWrap(self.active_box, 'body'), \
            header=self.header_bar,\
            footer=self.status_bar, \
            focus_part=self.framefocus)
        self.active_box = self.root_box

        self.loop = urwid.MainLoop(self.frame, \
            self._palette, \
            unhandled_input=self._unhandled_input)

    @property
    def active_box(self):
        """
        Gets the number of association groups reported by this node.

        :rtype: int

        """
        return self._active_box

    @active_box.setter
    def active_box(self,value):
        """
        Gets the number of association groups reported by this node.

        :rtype: int

        """
        self._active_box = value
        self.frame.set_body(self._active_box)
        self.header_bar.update(self._active_box.walker.fullpath())

    def exit(self):
        """
        Quit the programm
        Clean network properly and exit

        """
        self.network.write_config()
        self.network.stop()
        raise urwid.ExitMainLoop()

    def execute(self, command):
        """
        Parse an execute a commande
        """
        command = command.strip()
        if command.startswith('ls') :
            if ' ' in command :
                cmd,options = command.split(' ')
            else:
                options = ""
            options = options.strip()
            self.active_box.walker.ls(options)
            self.status_bar.set_command("")
            return True
        elif command.startswith('exit') :
            self.exit()
        elif command.startswith('cd') :
            if ' ' in command :
                cmd,path = command.split(' ',1)
            else:
                path = "/"
            path = path.strip()
            if self.active_box.walker.exist(path):
                self.active_box = self.active_box.walker.cd(path)
                self.active_box.walker.ls("")
                self.status_bar.set_command("")
                self.log.info(" self.active_box %s" %  self.active_box.walker.path)
                return True
            elif path == "/" :
                self.active_box = self.root_box
                self.active_box.walker.ls("")
                self.status_bar.set_command("")
                self.log.info(" self.active_box %s" %  self.active_box.walker.path)
                return True
            else:
                self.status_bar.update(status='Unknown directory "%s"' % path)
                return False
        elif command.startswith('send') :
            if ' ' in command :
                cmd,value = command.split(' ',1)
            else:
                self.status_bar.update(status='Usage : send <command>')
                return False
            value = value.strip()
            if len(value) == 0 :
                self.status_bar.update(status='Usage : send <command>')
                return False
            if self.active_box.walker.send(value):
                self.active_box.walker.ls("")
                self.status_bar.set_command("")
                return True
            else :
                return False
        elif command.startswith('create') :
            if ' ' in command :
                cmd,value = command.split(' ',1)
            else:
                self.status_bar.update(status='Usage : create <value>')
                return False
            value = value.strip()
            if len(value) == 0 :
                self.status_bar.update(status='Usage : create <value>')
                return False
            if self.active_box.walker.create(value):
                self.active_box.walker.ls("")
                self.status_bar.set_command("")
                return True
            else :
                return False
        elif command.startswith('delete') :
            if ' ' in command :
                cmd,value = command.split(' ',1)
            else:
                self.status_bar.update(status='Usage : delete <value>')
                return False
            value = value.strip()
            if len(value) == 0 :
                self.status_bar.update(status='Usage : delete <value>')
                return False
            if self.active_box.walker.delete(value):
                self.active_box.walker.ls("")
                self.status_bar.set_command("")
                return True
            else :
                return False
        elif command.startswith('activate') :
            if ' ' in command :
                cmd,value = command.split(' ',1)
            else:
                self.status_bar.update(status='Usage : activate <value>')
                return False
            value = value.strip()
            if len(value) == 0 :
                self.status_bar.update(status='Usage : activate <value>')
                return False
            if self.active_box.walker.activate(value):
                self.active_box.walker.ls("")
                self.status_bar.set_command("")
                return True
            else :
                return False
        elif command.startswith('set') :
            if ' ' in command :
                cmd,end = command.split(' ',1)
                if len(end) == 0 or ' ' not in end :
                    self.status_bar.update(status='Usage : set <field> to <value>')
                    return False
                end = end.strip()
                field,end = end.split(' ',1)
                if len(end) == 0 or ' ' not in end :
                    self.status_bar.update(status='Usage : set <field> to <value>')
                    return False
                end = end.strip()
                to,value = end.split(' ',1)
                if len(value) == 0 or to != "to"  :
                    self.status_bar.update(status='Usage : set <field> to <value>')
                    return False
                value = value.strip()
                if self.active_box.walker.set(field, value):
                    self.active_box.walker.ls("")
                    self.status_bar.set_command("")
                    return True
                else :
                    return False
            else :
                self.status_bar.update(status='Usage : set <field> to <value>')
                return False
        elif command.startswith('poll') :
            if ' ' in command :
                cmd,end = command.split(' ',1)
                if len(end) == 0 or ' ' not in end :
                    self.status_bar.update(status='Usage : poll <value> to <intensity>')
                    return False
                end = end.strip()
                field,end = end.split(' ',1)
                if len(end) == 0 or ' ' not in end :
                    self.status_bar.update(status='Usage : poll <value> to <intensity>')
                    return False
                end = end.strip()
                to,value = end.split(' ',1)
                if len(value) == 0 or to != "to"  :
                    self.status_bar.update(status='Usage : poll <value> to <intensity>')
                    return False
                value = value.strip()
                if self.active_box.walker.poll(field, value):
                    self.active_box.walker.ls("")
                    self.status_bar.set_command("")
                    return True
                else :
                    return False
            else :
                self.status_bar.update(status='Usage : poll <value> to <intensity>')
                return False
        elif command.startswith('add') :
            if ' ' in command :
                cmd,end = command.split(' ',1)
                if len(end) == 0 or ' ' not in end :
                    self.status_bar.update(status='Usage : add <value> to <list>')
                    return False
                end = end.strip()
                field,end = end.split(' ',1)
                if len(end) == 0 or ' ' not in end :
                    self.status_bar.update(status='Usage : add <value> to <list>')
                    return False
                end = end.strip()
                to,value = end.split(' ',1)
                if len(value) == 0 or to != "to"  :
                    self.status_bar.update(status='Usage : add <value> to <list>')
                    return False
                value = value.strip()
                if self.active_box.walker.add(value, field):
                    self.active_box.walker.ls("")
                    self.status_bar.set_command("")
                    return True
                else :
                    return False
            else :
                self.status_bar.update(status='Usage : add <value> to <list>')
                return False
        elif command.startswith('remove') :
            if ' ' in command :
                cmd,end = command.split(' ',1)
                if len(end) == 0 or ' ' not in end :
                    self.status_bar.update(status='Usage : remove <value> from <list>')
                    return False
                end = end.strip()
                field,end = end.split(' ',1)
                if len(end) == 0 or ' ' not in end :
                    self.status_bar.update(status='Usage : remove <value> from <list>')
                    return False
                end = end.strip()
                to,value = end.split(' ',1)
                if len(value) == 0 or to != "from"  :
                    self.status_bar.update(status='Usage : remove <value> from <list>')
                    return False
                value = value.strip()
                if self.active_box.walker.remove(value, field):
                    self.active_box.walker.ls("")
                    self.status_bar.set_command("")
                    return True
                else :
                    return False
            else :
                self.status_bar.update(status='Usage : remove <value> from <list>')
                return False
        elif command.startswith('reset') :
            if ' ' in command :
                cmd,state = command.split(' ',1)
                state = state.strip()
                if len(state) == 0 :
                    self.status_bar.update(status='Usage : reset soft|hard')
                    return False
                if self.active_box.walker.reset(state):
                    self.active_box.walker.ls("")
                    self.status_bar.set_command("")
                    return True
                else :
                    self.status_bar.update(status='Unknowm state "%s"' % state)
                    return False
        else:
            self.status_bar.update(status='Unknown command "%s"' % command)
            return False

    def _unhandled_input(self, key):
        if key == 'esc':
            self.exit()
        elif key == 'tab' or key == 'shift tab':
            if self.framefocus == 'footer':
                self.framefocus = 'body'
            else:
                self.framefocus = 'footer'
            self.frame.set_focus(self.framefocus)
            return True
        elif key == 'enter':
            self.log.info('handled: %s' % repr(key))
            cmd = self.status_bar.get_command()
            self.execute(cmd)
            return True
        elif key == 'f5':
            self.refresh_nodes()
            return True
        else:
            self.log.info('unhandled: %s' % repr(key))

    def _start_network(self):
        #Define some manager options
        self.options = ZWaveOption(self.device, \
          config_path="openzwave/config", \
          user_path=".", cmd_line="")
        self.options.set_log_file("OZW_Log.log")
        self.options.set_append_log_file(False)
        self.options.set_console_output(False)
        self.options.set_save_log_level(log)
        self.options.set_logging(True)
        self.options.lock()
        self.network = ZWaveNetwork(self.options, self.log)
        self.status_bar.update(status='Start Network')

    def _connect_louie(self):
        dispatcher.connect(self._louie_network_started, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
        dispatcher.connect(self._louie_network_resetted, ZWaveNetwork.SIGNAL_NETWORK_RESETTED)
        dispatcher.connect(self._louie_network_awaked, ZWaveNetwork.SIGNAL_NETWORK_AWAKED)
        dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)
        dispatcher.connect(self._louie_network_stopped, ZWaveNetwork.SIGNAL_NETWORK_STOPPED)

    def _louie_network_started(self, network):
        self.log.info('OpenZWave network is started : homeid %0.8x - %d nodes were found.' % \
            (network.home_id, network.nodes_count))
        self.network = network
        self.status_bar.update(status='OpenZWave network is started ... Waiting ...')
        self.loop.draw_screen()

    def _louie_network_resetted(self, network):
        self.log.info('OpenZWave network is resetted.')
        self.network = None
        self._disconnect_louie_node_and_value()
        self.status_bar.update(status='OpenZWave network was resetted ... Waiting ...')
        self.loop.draw_screen()

    def _louie_network_stopped(self, network):
        self.log.info('OpenZWave network is stopped.')
        self.network = None
        self.status_bar.update(status='OpenZWave network was stopped ... please quit')
        self.loop.draw_screen()

    def _louie_network_awaked(self, network):
        self.log.info('OpenZWave network is awaked.')
        self.network = network
        self.status_bar.update(status='OpenZWave network is awaked ... Waiting ...')
        self.loop.draw_screen()

    def _louie_network_ready(self, network):
        self.log.info('ZWave network is ready : %d nodes were found.' % network.nodes_count)
        self.log.info('Controller name : %s' % network.controller.node.product_name)
        self.network = network
        self.status_bar.update(status='ZWave network is ready')
        self.loop.draw_screen()
        self._connect_louie_node_and_value()

    def _disconnect_louie_node_and_value(self):
        #pass
        dispatcher.disconnect(self._louie_group, ZWaveNetwork.SIGNAL_GROUP)
        dispatcher.disconnect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE)
        dispatcher.disconnect(self._louie_value_update, ZWaveNetwork.SIGNAL_VALUE)
        dispatcher.disconnect(self._louie_ctrl_message, ZWaveController.SIGNAL_CONTROLLER)

    def _connect_louie_node_and_value(self):
        #pass
        dispatcher.connect(self._louie_group, ZWaveNetwork.SIGNAL_GROUP)
        dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE)
        dispatcher.connect(self._louie_value_update, ZWaveNetwork.SIGNAL_VALUE)
        dispatcher.connect(self._louie_ctrl_message, ZWaveController.SIGNAL_CONTROLLER)

    def _louie_node_update(self, network, node):
        self.loop.draw_screen()

    def _louie_value_update(self, network, node, value):
        self.loop.draw_screen()

    def _louie_group(self, network, node):
        self.loop.draw_screen()

    def _louie_ctrl_message(self, state, message, network, controller):
        #self.status_bar.update(status='Message from controller: %s : %s' % (state,message))
        self.status_bar.update(status='Message from controller: %s' % (message))
        self.loop.draw_screen()

window = None
def main():
    global window
    window = MainWindow(device=device,footer=footer)
    window.start()
    window.loop.run()
    window.stop()
    window.log.info("="*15 + " exit " + "="*15)
    return 0

if __name__ == "__main__":
    main()

__all__ = ['main']

