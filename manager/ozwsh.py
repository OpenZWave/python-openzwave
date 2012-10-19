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
from pyozwman.ozwsh_widgets import ValuesTree, ValuesBox, ValuesItem
from pyozwman.ozwsh_widgets import GroupsTree, GroupsBox, AssociationItem

from louie import dispatcher, All
import logging
#from frameapp import FrameApp, DIVIDER

#logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(level=logging.INFO)

#logger = logging.getLogger('openzwave')

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

class ScenesBox(urwid.ListBox):
    """
    ScenesBox show the walker
    """
    def __init__(self, window, parent, framefocus):
        self.window = window
        self.parent = parent
        self._framefocus = framefocus
        self.walker = ScenesTree(window, parent.walker, self)
        self.__super.__init__(self.walker)

class ScenesTree(OldestTree):

    def __init__(self, window, parent, widget_box):
        OldestTree.__init__(self, window, parent, widget_box)
    #    self.window = window
    #    self._framefocus = framefocus
    #    self.read_scenes(None)
        self.subdirs = ['..']
        self.childrens = { '..' : {'id':'..',
                                    'name':'..',
                                    'help':'Go to previous directory',
                                    'widget_box' : None}
                }
        self._path = "scenes"
        self.scene_header = ScenesItem()
        self.definition = {'id':'scenes',
                                'name':'scenes',
                                'help':'Scenes management',
                                'widget_box': self.widget_box
        }
        if parent != None and self.definition != None :
            parent.add_child(self.path, self.definition)
        self.usage.append("create <scenelabel> : create a scene with label <scenelabel>")
        self.usage.append("delete <scene_id> : delete the scene with id <scene_id>")
        self.usage.append("activate <scene_id> : activate the scene with id <scene_id>")
         #dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)

    def _louie_network_ready(self, network):
        self.window.log.info("ScenesTree _louie_network_ready")
        self.refresh()
        self.window.log.info("ScenesTree _louie_network_ready")
        dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_ADDED)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_NAMING)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_NEW)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_PROTOCOL_INFO)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_READY)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_REMOVED)

    def _louie_node_update(self, network, node_id):
        self.refresh()

    def read_lines(self):
        self.size = 0
        #self.focus, self.oldfocus = self.oldfocus, self.focus
        self.lines = []
        if self.window.network == None:
            return
        self.show_directories()
        self.lines.append(self.scene_header.get_header())
        self.size += 1
        scenes = self.window.network.get_scenes()
        for scene in scenes:
            self.lines.append(ScenesItem(scenes[scene].scene_id, \
                scenes[scene].label, \
                ))
            self.size += 1
        self._modified()

    def exist(self, directory):
        """
        List directory content
        """
        self.window.log.info("exist in ScenesTree")
        if OldestTree.exist(self, directory):
            return True
        self.window.log.info("exist in ScenesTree")
        try :
            if int(directory) in self.window.network.get_scenes():
                return True
        except :
            pass
        self.window.log.info("exist in NodeTrees return false")
        return False

    def cd(self, directory):
        """
        Change to directory and return the widget to display
        """
        if self.exist(directory) :
            if directory == '..':
                return self.parent.widget_box
            if directory in self.childrens:
                self.window.log.info("cd %s" %directory)
                return self.childrens[directory]['widget_box']
            try :
                if int(directory) in self.window.network.get_scenes():
                    self.window.log.info("cd a scene id %s" %directory)
                    self.childrens['scene']['widget_box'].walker.key=int(directory)
                    return self.childrens['scene']['widget_box']
            except :
                pass
        return None

    def create(self, value):
        if self.window.network.create_scene(value)>0:
            self.window.status_bar.update(status='Scene %s created' % value)
            return True
        else :
            self.window.status_bar.update(status="Can't create scene %s" % value)
            return False

    def delete(self, value):
        try :
            value = int(value)
        except:
            self.window.status_bar.update(status='Invalid scene %s' % value)
            return False
        if self.window.network.scene_exists(value):
            ret = self.window.network.get_scenes()[value].delete()
            if ret :
                self.window.status_bar.update(status='Scene %s deleted' % value)
            return ret
        else :
            self.window.status_bar.update(status="Can't delete scene %s" % value)
            return False

    def activate(self, value):
        try :
            value = int(value)
        except:
            self.window.status_bar.update(status='Invalid scene %s' % value)
            return False
        if self.window.network.scene_exists(value):
            ret = self.window.network.get_scenes()[value].activate()
            if ret :
                self.window.status_bar.update(status='Scene %s activated' % value)
            return ret
        else :
            self.window.status_bar.update(status="Can't activate scene %s" % value)
            return False

class ScenesItem (urwid.WidgetWrap):

    def __init__ (self, id=0, name=None):
        self.id = id
        #self.content = 'item %s: %s - %s...' % (str(id), name[:20], product_name[:20] )
        self.item = [
            ('fixed', 15, urwid.Padding(
                urwid.AttrWrap(urwid.Text('%s' % str(id), wrap='clip'), 'body', 'focus'), left=2)),
                urwid.AttrWrap(urwid.Text('%s' % name, wrap='clip'), 'body'),
        ]
        w = urwid.Columns(self.item, dividechars=1 )
        self.__super.__init__(w)

    def get_header (self):
        self.item = [
            ('fixed', 15, urwid.Padding(
                urwid.AttrWrap(urwid.Text('%s' % "Id", wrap='clip'), 'scene_header'), left=2)),
                urwid.AttrWrap(urwid.Text('%s' % "Name", wrap='clip'), 'scene_header'),
        ]
        return urwid.Columns(self.item, dividechars=1)

    def selectable (self):
        return True

    def keypress(self, size, key):
        return key


class StatusBar(urwid.WidgetWrap):
    def __init__(self, window):
        self.window = window
        self.statusbar = "%s"
        self.statusbar_urwid = urwid.Text(self.statusbar % "")
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
        self.controller_box = ControllerBox(self, self.root_box, "body")
        self.scenes_box = ScenesBox(self, self.root_box, "body")
        self.nodes_box = NodesBox(self, self.root_box, "body")
        self.switches_box = SwitchesBox(self, self.nodes_box, "body")
        self.sensors_box = SensorsBox(self, self.nodes_box, "body")
        self.node_box = NodeBox(self, self.nodes_box, "body")
        self.values_box = ValuesBox(self, self.node_box, "body")
        self.groups_box = GroupsBox(self, self.node_box, "body")
        #self.menu = MenuWidget(self, "value")


        #self.nodes = []
        self.status_bar = StatusBar(self)
        self.header_bar = HeaderBar(self)
        #self.header = urwid.Pile([
        #    #self.divider,
        #    urwid.Columns([
        #        ('weight', 2, urwid.AttrWrap(self.left_header, 'reverse')),
        #        #('fixed', 1, urwid.Divider("|")),
        #        ('weight', 2, urwid.AttrWrap(self.right_header, 'reverse'))
        #    ], dividechars=2, min_width=8),
        #    DIVIDER,
        #    self.listbox_header.get_header()
        #    ])

#        self.footer_columns = urwid.Columns([
#                ('weight', 1, urwid.AttrWrap(self.menu, 'reverse')),
#                #('fixed', 1, urwid.Divider("|")),
#                ('weight', 3,urwid.AttrWrap(self.details, 'reverse'))
#            ], dividechars=2, min_width=8)

        #self.sub_frame = urwid.Filler(urwid.Frame( \
        #    urwid.AttrWrap(
        #    self.details, 'sub_frame_body'), \
        #        header=self.details.header_widget(),\
        #        footer=self.details.footer_widget(), \
        #        focus_part="body"),  height=9)

        #self.footer_columns = urwid.Columns([
        #        ('weight', 1, urwid.AttrWrap(self.menu, 'reverse')),
                #('fixed', 1, urwid.Divider("|")),
        #        ('weight', 3,urwid.AttrWrap(self.details, 'reverse'))
        #    ], dividechars=2, min_width=8)
#        self.footer = urwid.Pile([
#            DIVIDER,
#            self.footer_columns,
#            DIVIDER,
#            urwid.AttrWrap(self.status_bar, 'reverse'),
#            #self.divider,
#            #urwid.AttrWrap(urwid.Text(" > "), 'footer')
#            ])
#        self.footer = urwid.Pile([
#            DIVIDER,
#            urwid.AttrWrap(self.status_bar, 'reverse'),
#            #self.divider,
#            #urwid.AttrWrap(urwid.Text(" > "), 'footer')
#            ])
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

    def refresh_nodes(self):
        self.nodes_box.body.refresh()
        #self.update_node(self.nodes_box.walker.get_nodeid())

    def update_node(self, nodeid):
        if nodeid != None :
            self.details.update( \
                nodeid=nodeid, \
                name=self.network.nodes[nodeid].name, \
                location=self.network.nodes[nodeid].location, \
                manufacturer=self.network.nodes[nodeid].manufacturer_name, \
                product=self.network.nodes[nodeid].product_name, \
                neighbors=self.network.nodes[nodeid].neighbors, \
                version=self.network.nodes[nodeid].version, \
                signal=self.network.nodes[nodeid].max_baud_rate, \
                )
            self.log.info('Update node id=%d, product name=%s.' % \
                (nodeid, self.network.nodes[nodeid].product_name))

    def _unhandled_input(self, key):
        if key == 'esc':
            self.network.write_config()
            raise urwid.ExitMainLoop()
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
        self.options.set_save_log_level('Debug')
        self.options.set_logging(True)
        self.options.lock()
        self.network = ZWaveNetwork(self.options, self.log)
        self.status_bar.update(status='Start Network')

    def _connect_louie(self):
        dispatcher.connect(self._louie_driver_ready, ZWaveNetwork.SIGNAL_DRIVER_READY)
        dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)

    def _louie_driver_ready(self, network, controller):
        self.log.info('OpenZWave driver is ready : homeid %0.8x - %d nodes were found.' % \
            (network.home_id, network.nodes_count))
        self.network = network
        self.controller = controller
        #self.left_header.update_controller("%s on %s" % \
        #    (network.controller.node.product_name, self.device))
        #self.left_header.update_homeid(network.home_id_str)
        #self.left_header.update_nodes(network.nodes_count,0)
        #self.right_header.update(network.controller.library_description, \
        #    network.controller.ozw_library_version, \
        #    network.controller.python_library_version)
        self.status_bar.update(status='OpenZWave driver is ready')
        self.loop.draw_screen()

    def _louie_network_ready(self, network):
        self.log.info('ZWave network is ready : %d nodes were found.' % network.nodes_count)
        self.log.info('Controller name : %s' % network.controller.node.product_name)
        self.network = network
        #self.left_header.update_controller("%s on %s" % \
        #    (network.controller.node.product_name, self.device))
        #self.left_header.update_nodes(network.nodes_count,0)
        #self.set_nodes()
        self.status_bar.update(status='ZWave network is ready')
        self.loop.draw_screen()
        self._connect_louie_node_and_value()

    def _connect_louie_node_and_value(self):
        #pass
        dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE)
        dispatcher.connect(self._louie_value_update, ZWaveNetwork.SIGNAL_VALUE)

    def _louie_node_update(self, network, node_id):
        self.loop.draw_screen()

    def _louie_value_update(self, network, node, value_id):
        self.loop.draw_screen()

window = None
def main():
    device = "/dev/zwave-aeon-s2"
    footer = True
    for arg in sys.argv:
        if arg.startswith("--help") or arg.startswith("-h"):
            print("Usage : ozwman [--device=/dev/zwave-aeon-s2]")
            print("   --device=path_to_your_zwave_stick")
            sys.exit("")

        if arg.startswith("--device"):
            temp,device = arg.split("=")
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

