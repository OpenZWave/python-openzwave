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
from louie import dispatcher, All
import logging
#from frameapp import FrameApp, DIVIDER

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

class OldestTree(urwid.ListWalker):

    def __init__(self, window, parent=None, widget_box=None):
        self.window = window
        self.parent = parent
        self.widget_box = widget_box
        self.usage = ['ls : list directory', 'cd <directory> : change to directory <directory>' ]
        self.childrens = {}
        self.subdirs = []
        self.definition = None
        self.key = None
        self.lines = []
        self.focus, oldfocus = (0, 0)
        self.size = 0

    def add_child(self, child, definition):
        self.window.log.info("Add a child")
        self.subdirs.append(child)
        self.childrens[child] = definition

    def _get_at_pos(self, pos):
        if pos >= 0 and pos < self.size and len(self.lines)>0:
            return self.lines[pos], pos
        else:
            return None, None

    def get_nodeid(self):
        line,pos = self._get_at_pos(self.focus)
        return line.id

    def get_focus(self):
        return self._get_at_pos(self.focus)

    def get_focus_entry(self):
        return self.lines[self.focus]

    def set_focus(self, focus):
        if self.focus != focus:
            self.focus = focus
            #self.parent.update_node(self.get_nodeid())
            self._modified()

    def get_next(self, pos):
        return self._get_at_pos(pos + 1)

    def get_prev(self, pos):
        return self._get_at_pos(pos - 1)

    def go_first(self):
        self.set_focus(0)

    def go_last(self):
        self.set_focus(self.size - 1)

    def read_lines(self):
        self.size = 0
        #self.focus, self.oldfocus = self.oldfocus, self.focus
        self.lines = []

    def show_help(self):
        self.lines.append(urwid.Divider("-"))
        self.size += 1
        self.lines.append(urwid.Text("Help" , align='left'))
        self.size += 1
        for use in self.usage:
            self.lines.append( \
                urwid.Text("%s" % use, align='left'))
            self.size += 1

    def refresh(self):
        self.read_lines()
        self.show_help()

    def get_selected(self):
        ret = []
        for x in self.lines:
            if x.selected == True:
                ret.append(x)
        return ret

    def exist(self, directory):
        """
        Check that the directory exists
        """
        self.window.log.info("OldestTree exist %s" %self.childrens)
        if directory == "..":
            return self.parent != None
        if directory in self.subdirs:
            self.window.log.info("OldestTree exist %s" %directory)
            return True
        #for line in self.lines :
        #    if line.id and line.id == directory:
        #        return True
        return False

    def ls(self, opts):
        """
        List directory content
        """
        self.refresh()

    def cd(self, directory):
        """
        Change to directory and return the widget to display
        """
        if self.exist(directory) :
            if directory == '..':
                return self.parent.widget_box
            else :
                return self.childrens[directory]['widget_box']
        return None

    def fullpath(self):
        """
        Path to this directory
        """
        if self.parent == None:
            return "%s/" % (self.path)
        else:
            return "%s%s/" % (self.parent.fullpath(), self.path)

    @property
    def path(self):
        """
        The path

        :rtype: str

        """
        return self._path

    @path.setter
    def path(self,value):
        """
        Path

        :rtype: str

        """
        self._path = value

class RootTree(OldestTree):

    def __init__(self, window, parent, widget_box):
        OldestTree.__init__(self, window, parent, widget_box)
    #    self._framefocus = framefocus
        self.childrens = { 'controller' : {'id':'ctl',
                                        'name':'Controller',
                                        'help':'Controller management',
                                        'widget_box' : None},
                'scenes' : {'id':'scn',
                            'name':'Scenes',
                            'help':'scenes management',
                            'widget_box' : None},
                }
        self._path = ""
        self.refresh()
        dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)

    def _louie_network_ready(self, network):
        self.read_lines()

    def read_lines(self):
        self.size = 0
        #self.focus, self.oldfocus = self.oldfocus, self.focus
        self.lines = []
        for child in self.subdirs:
            self.lines.append( \
                RootDir( \
                    self.childrens[child]['id'], \
                    self.childrens[child]['name'], \
                    self.childrens[child]['help']))
            self.size += 1
        self.lines.append(urwid.Divider("-"))
        self.size += 1
        if self.window.network != None:
            self.lines.append(urwid.Text("    HomeId = %s" % self.window.network.home_id_str, align='left'))
            self.size += 1
        self._modified()

class RootDir (urwid.WidgetWrap):

    def __init__ (self, id=None, name=None, help=None):
        self.id = id
        #self.content = 'item %s: %s - %s...' % (str(id), name[:20], product_name[:20] )
        self.item = [
            ('fixed', 10,
                urwid.Padding(urwid.AttrWrap(urwid.Text('%s' % id, wrap='clip'), 'body', 'focus'), left=2)),
                urwid.AttrWrap(urwid.Text('%s' % name, wrap='clip'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % help, wrap='clip'), 'body'),
        ]
        w = urwid.Columns(self.item, dividechars=1 )
        self.__super.__init__(w)

    def selectable (self):
        return True

    def keypress(self, size, key):
        return key

class RootItem (urwid.WidgetWrap):

    def __init__ (self, id=0, name=None, location=None, signal=0, battery_level=-1):
        self.id = id
        #self.content = 'item %s: %s - %s...' % (str(id), name[:20], product_name[:20] )
        self.item = [
            ('fixed', 15, urwid.Padding(
                urwid.AttrWrap(urwid.Text('%s' % str(id), wrap='clip'), 'body', 'focus'), left=2)),
                urwid.AttrWrap(urwid.Text('%s' % name, wrap='clip'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % location, wrap='clip'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % signal, wrap='clip'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % battery_level, wrap='clip'), 'body'),
        ]
        w = urwid.Columns(self.item, dividechars=1 )
        self.__super.__init__(w)

    def get_header (self):
        self.item = [
            ('fixed', 15, urwid.Padding(
                urwid.AttrWrap(urwid.Text('%s' % "Id", wrap='clip'), 'node_header'), left=2)),
                urwid.AttrWrap(urwid.Text('%s' % "Name", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Location", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Baud", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Battery", wrap='clip'), 'node_header'),
        ]
        return urwid.Columns(self.item, dividechars=1)

    def selectable (self):
        return True

    def keypress(self, size, key):
        return key

class RootBox(urwid.ListBox):
    """
    RootBox show the walker
    """
    def __init__(self, window, parent, framefocus):
        self.window = window
        self.parent = parent
        self._framefocus = framefocus
        self.walker = RootTree(window, None, self)
        self.__super.__init__(self.walker)


#class NodeTree():
#    nodes

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

class NodesBox(urwid.ListBox):
    """
    NodexBox show the walker
    """
    def __init__(self, window, parent, framefocus):
        self.window = window
        self.parent = parent
        self._framefocus = framefocus
        self.walker = NodesTree(window, parent.walker, self)
        self.__super.__init__(self.walker)


class NodesTree(OldestTree):

    def __init__(self, window, parent, widget_box):
        OldestTree.__init__(self, window, parent, widget_box)
    #    self.window = window
    #    self._framefocus = framefocus
    #    self.read_nodes(None)
        self.subdirs = ['..']
        self.childrens = { '..' : {'id':'..',
                                    'name':'..',
                                    'help':'Go to previous directory',
                                    'widget_box' : None},
                'commands' : {'id':'cmds',
                            'name':'command',
                            'help':'Command classes and values management',
                            'widget_box' : None},
                'groups' : {'id':'grp',
                            'name':'groups',
                            'help':'Association management',
                            'widget_box' : None},
                'switches' : {'id':'swt',
                            'name':'switches',
                            'help':'Switches management',
                            'widget_box' : None},
                'sensors' : {'id':'sns',
                            'name':'sensors',
                            'help':'Sensors management',
                            'widget_box' : None},
                }
        self._path = "nodes"
        self.node_header = NodesItem()
        self.definition = {'id':'nod',
                                'name':'nodes',
                                'help':'Nodes management',
                                'widget_box': self.widget_box
        }
        if parent != None and self.definition != None :
            parent.add_child(self.path, self.definition)
        dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)

    def _louie_network_ready(self, network):
        self.refresh()
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_EVENT)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_ADDED)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_NAMING)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_NEW)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_PROTOCOL_INFO)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_READY)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_REMOVED)

    def _louie_node_update(self, network, node):
        self.refresh()

    def read_lines(self):
        self.size = 0
        #self.focus, self.oldfocus = self.oldfocus, self.focus
        self.lines = []
        if self.window.network == None:
            return
        for child in self.subdirs:
            self.lines.append( \
                RootDir(self.childrens[child]['id'], \
                    self.childrens[child]['name'], \
                    self.childrens[child]['help']))
            self.size += 1
        self.lines.append(urwid.Divider("-"))
        self.size += 1
        self.lines.append(self.node_header.get_header())
        self.size += 1
        for node in self.window.network.nodes:
            self.lines.append(NodesItem(self.window.network.nodes[node].node_id, \
                self.window.network.nodes[node].name, \
                self.window.network.nodes[node].location, \
                self.window.network.nodes[node].max_baud_rate, \
                self.window.network.nodes[node].battery_level, \
                ))
            self.size += 1
        self._modified()

    def exist(self, directory):
        """
        List directory content
        """
        self.window.log.info("exist in NodesTree")
        if OldestTree.exist(self, directory):
            return True
        self.window.log.info("exist in NodesTree")
        if int(directory) in self.window.network.nodes:
            return True
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
            if int(directory) in self.window.network.nodes:
                self.window.log.info("cd a node id %s" %directory)
                self.childrens['node']['widget_box'].walker.key=int(directory)
                return self.childrens['node']['widget_box']
        return None


#class NodesDir (urwid.WidgetWrap):
#
#    def __init__ (self, id=None, help=None):
#        self.id = id
#        #self.content = 'item %s: %s - %s...' % (str(id), name[:20], product_name[:20] )
#        self.item = [
#            ('fixed', 15, urwid.Padding(
#                urwid.AttrWrap(urwid.Text('%s' % id, wrap='clip'), 'body', 'focus'), left=2)),
#        ]
#        w = urwid.Columns(self.item, dividechars=1 )
#        self.__super.__init__(w)
#
#    def selectable (self):
#        return True
#
#    def keypress(self, size, key):
#        return key

class NodesItem (urwid.WidgetWrap):

    def __init__ (self, id=0, name=None, location=None, signal=0, battery_level=-1):
        self.id = id
        #self.content = 'item %s: %s - %s...' % (str(id), name[:20], product_name[:20] )
        self.item = [
            ('fixed', 15, urwid.Padding(
                urwid.AttrWrap(urwid.Text('%s' % str(id), wrap='clip'), 'body', 'focus'), left=2)),
                urwid.AttrWrap(urwid.Text('%s' % name, wrap='clip'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % location, wrap='clip'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % signal, wrap='clip'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % battery_level, wrap='clip'), 'body'),
        ]
        w = urwid.Columns(self.item, dividechars=1 )
        self.__super.__init__(w)

    def get_header (self):
        self.item = [
            ('fixed', 15, urwid.Padding(
                urwid.AttrWrap(urwid.Text('%s' % "Id", wrap='clip'), 'node_header'), left=2)),
                urwid.AttrWrap(urwid.Text('%s' % "Name", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Location", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Baud", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Battery", wrap='clip'), 'node_header'),
        ]
        return urwid.Columns(self.item, dividechars=1)

    def selectable (self):
        return True

    def keypress(self, size, key):
        return key

class NodeBox(urwid.ListBox):
    """
    NodeBox show the walker
    """
    def __init__(self, window, parent, framefocus):
        self.window = window
        self.parent = parent
        self._framefocus = framefocus
        self.walker = NodeTree(window, parent.walker, self)
        self.__super.__init__(self.walker)


class NodeTree(OldestTree):

    def __init__(self, window, parent, widget_box):
        OldestTree.__init__(self, window, parent, widget_box)
        self.childrens = { '..' : {'id':'..',
                                'name':'..',
                                'help':'Go to previous directory',
                                'widget_box' : None},
                'commands' : {'id':'cmds',
                            'name':'command',
                            'help':'Command classes and values management',
                            'widget_box' : None},
                'groups' : {'id':'grp',
                            'name':'groups',
                            'help':'Association management',
                            'widget_box' : None},
                'switches' : {'id':'swt',
                            'name':'switches',
                            'help':'Switches management',
                            'widget_box' : None},
                'sensors' : {'id':'sns',
                            'name':'sensors',
                            'help':'Sensors management',
                            'widget_box' : None},
                }
        self._path = ""
        self.subdirs = ['..']
    #    self.window = window
    #    self._framefocus = framefocus
    #    self.read_nodes(None)
        self.definition = {'id':'<idx>',
                        'name':'node',
                        'help':'Node management',
                        'widget_box': self.widget_box}
        self.usage.append("set <field> to <value> : change the value of a field")
        if parent != None and self.definition != None :
            parent.add_child("node",self.definition)
        #dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)

    def _louie_network_ready(self, network):
        self.read_lines()
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_EVENT)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_ADDED)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_NAMING)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_NEW)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_PROTOCOL_INFO)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_READY)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_REMOVED)

    def _louie_node_update(self, network, node):
        self.read_lines()

    def set(self, param, value):
        if param in ['name', 'location', 'product_name', 'manufacturer_name' ]:
            self.window.network.nodes[self.key].set_field(param, \
                        value)
            self.window.status_bar.update(status='Field %s updated' % param)
            return True
        return False

    def read_lines(self):
        self.size = 0
        #self.focus, self.oldfocus = self.oldfocus, self.focus
        self.lines = []
        if self.window.network == None:
            return
        for child in self.subdirs:
            self.lines.append( \
                RootDir(self.childrens[child]['id'], \
                    self.childrens[child]['name'], \
                    self.childrens[child]['help']))
            self.size += 1
        self.lines.append(urwid.Divider("-"))
        self.size += 1
        self.edit_fields = {
            'name' :              urwid.Edit("  Name <name>                      = ", \
                self.window.network.nodes[self.key].name, align='left'),
            'location' :          urwid.Edit("  Location <location>              = ", \
                self.window.network.nodes[self.key].location, align='left'),
            'product_name' :      urwid.Edit("  Product <product_name>           = ", \
                self.window.network.nodes[self.key].product_name, align='left'),
            'manufacturer_name' : urwid.Edit("  Manufacturer <manufacturer_name> = ", \
                self.window.network.nodes[self.key].manufacturer_name, align='left'),
        }
        if self.window.network != None:
            self.lines.append(self.edit_fields['name'])
            self.size += 1
            self.lines.append(self.edit_fields['location'])
            self.size += 1
            self.lines.append(self.edit_fields['product_name'])
            self.size += 1
            self.lines.append(self.edit_fields['manufacturer_name'])
            self.size += 1
            self.lines.append(urwid.Text(    "  Baud rate                        = %s" % \
                self.window.network.nodes[self.key].max_baud_rate, align='left'))
            self.size += 1
            self.lines.append(urwid.Text(    "  Capabilities                     = %s" % \
                self.window.network.nodes[self.key].capabilities, align='left'))
            self.size += 1
            self.lines.append(urwid.Text(    "  Neighbors                        = %s" % \
                self.window.network.nodes[self.key].neighbors, align='left'))
            self.size += 1
            self.lines.append(urwid.Text(    "  Groups                           = %s" % \
                self.window.network.nodes[self.key].groups, align='left'))
            self.size += 1
        self._modified()

    @property
    def path(self):
        """
        The path

        :rtype: str

        """
        return "%s" % self.key

class ControllerBox(urwid.ListBox):
    """
    NodeBox show the walker
    """
    def __init__(self, window, parent, framefocus):
        self.window = window
        self.parent = parent
        self._framefocus = framefocus
        self.walker = ControllerTree(window, parent.walker, self)
        self.__super.__init__(self.walker)


class ControllerTree(OldestTree):

    def __init__(self, window, parent, widget_box):
        OldestTree.__init__(self, window, parent, widget_box)
        self.childrens = { '..' : {'id':'..',
                                'name':'..',
                                'help':'Go to previous directory',
                                'widget_box' : None}
                }
        self._path = "controller"
        self.subdirs = ['..']
    #    self.window = window
    #    self._framefocus = framefocus
    #    self.read_nodes(None)
        self.definition = {'id':'ctrl',
                        'name':'controller',
                        'help':'Controller management',
                        'widget_box': self.widget_box}
        if parent != None and self.definition != None :
            parent.add_child(self._path,self.definition)
        self.usage.append("reset soft : reset the controller in a soft way. Node association is not required")
        self.usage.append("reset hard : reset the controller. Warning : all nodes must be re-associated with your stick.")
        #dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)

    def _louie_network_ready(self, network):
        self.read_lines()
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_EVENT)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_ADDED)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_NAMING)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_NEW)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_PROTOCOL_INFO)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_READY)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_REMOVED)

    def _louie_node_update(self, network, node):
        self.read_lines()

    def set(self, param, value):
        if param in ['name', 'location', 'product_name', 'manufacturer_name' ]:
            self.window.network.controller.node.set_field(param, \
                        value)
            self.window.status_bar.update(status='Field %s updated' % param)
            return True
        return False

    def reset(self, state):
        if state == 'soft':
            self.window.network.controller.soft_reset()
            self.window.status_bar.update(status='Reset controller softly')
            return True
        if state == 'hard':
            self.window.network.controller.hard_reset()
            self.window.status_bar.update(status='Reset controller hardly')
            return True
        return False

    def read_lines(self):
        self.size = 0
        #self.key = self.window.network.controller.node_id
        #self.focus, self.oldfocus = self.oldfocus, self.focus
        self.lines = []
        if self.window.network == None:
            return
        for child in self.subdirs:
            self.lines.append( \
                RootDir(self.childrens[child]['id'], \
                    self.childrens[child]['name'], \
                    self.childrens[child]['help']))
            self.size += 1
        self.lines.append(urwid.Divider("-"))
        self.size += 1
        self.edit_fields = {
            'name' :              urwid.Edit("  Name <name>                      = ", \
                self.window.network.controller.node.name, align='left'),
            'location' :          urwid.Edit("  Location <location>              = ", \
                self.window.network.controller.node.location, align='left'),
            'product_name' :      urwid.Edit("  Product <product_name>           = ", \
                self.window.network.controller.node.product_name, align='left'),
            'manufacturer_name' : urwid.Edit("  Manufacturer <manufacturer_name> = ", \
                self.window.network.controller.node.manufacturer_name, align='left'),
        }
        if self.window.network != None:
            self.lines.append(self.edit_fields['name'])
            self.size += 1
            self.lines.append(self.edit_fields['location'])
            self.size += 1
            self.lines.append(self.edit_fields['product_name'])
            self.size += 1
            self.lines.append(self.edit_fields['manufacturer_name'])
            self.size += 1
            self.lines.append(urwid.Divider("-"))
            self.size += 1
            self.lines.append(urwid.Text(    "  Capabilities = %s" % \
                self.window.network.controller.node.capabilities, align='left'))
            self.size += 1
            self.lines.append(urwid.Text(    "  Neighbors    = %s" % \
                self.window.network.controller.node.neighbors, align='left'))
            self.size += 1
            self.lines.append(urwid.Text(    "  Baud rate    = %s" % \
                self.window.network.controller.node.max_baud_rate, align='left'))
            self.size += 1
            self.lines.append(urwid.Divider("-"))
            self.size += 1
            self.lines.append(urwid.Text(    "  Statistics   = %s" % \
                self.window.network.controller.stats, align='left'))
            self.size += 1
            self.lines.append(urwid.Divider("-"))
            self.size += 1
            self.lines.append(urwid.Text(    "  Device=%s" % \
                self.window.network.controller.device, align='left'))
            self.size += 1
            self.lines.append(urwid.Text(    "  %s" % \
                self.window.network.controller.library_description, align='left'))
            self.size += 1
            self.lines.append(urwid.Text(    "  %s" % \
                self.window.network.controller.ozw_library_version, align='left'))
            self.size += 1
            self.lines.append(urwid.Text(    "  %s" % \
                self.window.network.controller.python_library_version, align='left'))
            self.size += 1
        self._modified()

class ValuesBox(urwid.ListBox):
    """
    ValuesBox show the walker
    """
    def __init__(self, window, parent, framefocus):
        self.window = window
        self.parent = parent
        self._framefocus = framefocus
        self.walker = ValuesTree(window, parent.walker, self)
        self.__super.__init__(self.walker)


class ValuesTree(OldestTree):

    def __init__(self, window, parent, widget_box):
        OldestTree.__init__(self, window, parent, widget_box)
    #    self.window = window
    #    self._framefocus = framefocus
    #    self.read_nodes(None)
        self.subdirs = ['..']
        self.childrens = { '..' : {'id':'..',
                                    'name':'..',
                                    'help':'Go to previous directory',
                                    'widget_box' : None},
                }
        self._path = "values"
        self.node_header = NodesItem()
        self.definition = {'id':'val',
                                'name':'values',
                                'help':'Values management',
                                'widget_box': self.widget_box
        }
        if parent != None and self.definition != None :
            parent.add_child(self.path, self.definition)
        dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)

    def _louie_network_ready(self, network):
        self.refresh()
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_EVENT)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_ADDED)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_NAMING)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_NEW)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_PROTOCOL_INFO)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_READY)
        #dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_REMOVED)

    def _louie_node_update(self, network, node):
        self.read_lines()

    def read_lines(self):
        self.size = 0
        #self.focus, self.oldfocus = self.oldfocus, self.focus
        self.lines = []
        if self.window.network == None:
            return
        for child in self.subdirs:
            self.lines.append( \
                RootDir(self.childrens[child]['id'], \
                    self.childrens[child]['name'], \
                    self.childrens[child]['help']))
            self.size += 1
        self.lines.append(urwid.Divider("-"))
        self.size += 1
        self.lines.append(self.node_header.get_header())
        self.size += 1
        for node in self.window.network.nodes:
            self.lines.append(NodesItem(self.window.network.nodes[node].node_id, \
                self.window.network.nodes[node].name, \
                self.window.network.nodes[node].location, \
                self.window.network.nodes[node].max_baud_rate, \
                self.window.network.nodes[node].battery_level, \
                ))
            self.size += 1
        self._modified()

    def exist(self, directory):
        """
        List directory content
        """
        self.window.log.info("exist in NodesTree")
        if OldestTree.exist(self, directory):
            return True
        self.window.log.info("exist in NodesTree")
        if int(directory) in self.window.network.nodes:
            return True
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
            if int(directory) in self.window.network.nodes:
                self.window.log.info("cd a node id %s" %directory)
                self.childrens['node']['widget_box'].walker.key=int(directory)
                return self.childrens['node']['widget_box']
        return None


#class NodesDir (urwid.WidgetWrap):
#
#    def __init__ (self, id=None, help=None):
#        self.id = id
#        #self.content = 'item %s: %s - %s...' % (str(id), name[:20], product_name[:20] )
#        self.item = [
#            ('fixed', 15, urwid.Padding(
#                urwid.AttrWrap(urwid.Text('%s' % id, wrap='clip'), 'body', 'focus'), left=2)),
#        ]
#        w = urwid.Columns(self.item, dividechars=1 )
#        self.__super.__init__(w)
#
#    def selectable (self):
#        return True
#
#    def keypress(self, size, key):
#        return key

class ValuesItem (urwid.WidgetWrap):

    def __init__ (self, id=0, name=None, help=None, value=0, type='All', genre='All'):
        self.id = id
        #self.content = 'item %s: %s - %s...' % (str(id), name[:20], product_name[:20] )
        self.item = [
            ('fixed', 15, urwid.Padding(
                urwid.AttrWrap(urwid.Text('%s' % str(id), wrap='clip'), 'body', 'focus'), left=2)),
                urwid.AttrWrap(urwid.Text('%s' % name, wrap='clip'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % help, wrap='clip'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % value, wrap='clip'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % type, wrap='clip'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % genre, wrap='clip'), 'body'),
        ]
        w = urwid.Columns(self.item, dividechars=1 )
        self.__super.__init__(w)

    def get_header (self):
        self.item = [
            ('fixed', 15, urwid.Padding(
                urwid.AttrWrap(urwid.Text('%s' % "Id", wrap='clip'), 'node_header'), left=2)),
                urwid.AttrWrap(urwid.Text('%s' % "Name", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Help", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Value", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Type", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Genre", wrap='clip'), 'node_header'),
        ]
        return urwid.Columns(self.item, dividechars=1)

    def selectable (self):
        return True

    def keypress(self, size, key):
        return key

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
        self.log = logging.getLogger('ozwman')
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
        #self.divider = urwid.Divider("-")
        #self.left_header = LeftHeader()
        #self.right_header = RightHeader()
        #self.details = DetailsWidget(self, "result")
        #self.menu = MenuWidget(self, "footer")
        self.network = None
        self.controller = None
        #self.nodes_walker = NodesWalker(self, self.network)
        #self.listbox_header = NodeItem()
        self.root_box = RootBox(self, None, "body")
        self.controller_box = ControllerBox(self, self.root_box, "body")
        self.nodes_box = NodesBox(self, self.root_box, "body")
        self.node_box = NodeBox(self, self.nodes_box, "body")
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
        #command = command.rtrim()
        #command = command.ltrim()
        if command.startswith('ls') :
            if ' ' in command :
                cmd,options = command.split(' ')
            else:
                options = ""
            self.active_box.walker.ls(options)
            self.status_bar.set_command("")
            return True
        elif command.startswith('cd') :
            if ' ' in command :
                cmd,path = command.split(' ',1)
            else:
                path = "/"
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
        elif command.startswith('set') :
            if ' ' in command :
                cmd,end = command.split(' ',1)
                if len(end) == 0 or ' ' not in end :
                    self.status_bar.update(status='Usage : set <field> to <value>')
                    return False
                field,end = end.split(' ',1)
                if len(end) == 0 or ' ' not in end :
                    self.status_bar.update(status='Usage : set <field> to <value>')
                    return False
                to,value = end.split(' ',1)
                if len(value) == 0 or to != "to"  :
                    self.status_bar.update(status='Usage : set <field> to <value>')
                    return False
                if self.active_box.walker.set(field, value):
                    self.active_box.walker.ls("")
                    self.status_bar.set_command("")
                    return True
                else :
                    self.status_bar.update(status='Unknowm field "%s"' % field)
                    return False
            else :
                self.status_bar.update(status='Usage : set %s to <value>' % field)
                return False
        elif command.startswith('reset') :
            if ' ' in command :
                cmd,state = command.split(' ',1)
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
        self.nodes_box.body.read_lines()
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
        #dispatcher.connect(self._notifyNetworkFailed, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
        #dispatcher.connect(self._notifyNodeReady, ZWaveNetwork.SIGNAL_NODE_READY)
        #dispatcher.connect(self._notifyValueChanged, ZWaveNetwork.SIGNAL_VALUE_CHANGED)
        #dispatcher.connect(self._notifyNodeAdded, ZWaveNetwork.SIGNAL_NODE_ADDED)

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
        self._connect_louie_node()

    def _connect_louie_node(self):
        dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_EVENT)
        dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_ADDED)
        dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_NAMING)
        dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_NEW)
        dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_PROTOCOL_INFO)
        dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_READY)
        dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE_REMOVED)

    def _louie_node_update(self, network, node):
        self.log.info('Node event %s' % node)
        self.network = network
        #self.set_nodes()
        self.status_bar.update(status='Node event')
        self.refresh_nodes()
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

