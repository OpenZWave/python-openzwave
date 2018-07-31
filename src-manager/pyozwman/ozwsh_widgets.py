# -* coding: utf-8 -*-

"""
.. module:: pyozwman.ozwsh_widgets

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

from select import select
import sys
import os
from traceback import format_exc
import six
if six.PY3:
    from pydispatch import dispatcher
else:
    from louie import dispatcher
import urwid
from urwid.raw_display import Screen
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption

import logging

class OldestTree(urwid.ListWalker):

    def __init__(self, window, parent=None, widget_box=None):
        self.window = window
        self.parent = parent
        self.widget_box = widget_box
        self.usage = ['ls : list directory', 'cd <directory> : change to directory <directory>', 'exit : quit the program' ]
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
        return self.get_id()

    def get_id(self):
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

    def clean(self):
        """
        Clean properties like key, ..., ...
        """
        pass

    def show_directories(self):
        for child in self.subdirs:
            self.lines.append( \
                RootDir(self.childrens[child]['id'], \
                    self.childrens[child]['name'], \
                    self.childrens[child]['help']))
            self.size += 1
        self.lines.append(urwid.Divider("-"))
        self.size += 1

    def show_help(self):
        self.lines.append(urwid.Divider("-"))
        self.size += 1
        self.lines.append(urwid.Text("Help" , align='left'))
        self.size += 1
        for use in self.usage:
            self.lines.append( \
                urwid.Text("%s" % use, align='left'))
            self.size += 1
        self._modified()

    def refresh(self):
        self.read_lines()
        self.show_help()
        self._modified()

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
        #self.window.log.info("OldestTree exist %s" %self.childrens)
        if directory == "..":
            return self.parent != None
        if directory in self.subdirs:
            #self.window.log.info("OldestTree exist %s" %directory)
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

    def set(self, param, value):
        self.window.status_bar.update(status='Command "set" not supported')
        return False

    def poll(self, param, value):
        self.window.status_bar.update(status='Command "poll" not supported')
        return False

    def add(self, param, value):
        self.window.status_bar.update(status='Command "add" not supported')
        return False

    def remove(self, param, value):
        self.window.status_bar.update(status='Command "remove" not supported')
        return False

    def reset(self, value):
        self.window.status_bar.update(status='Command "reset" not supported')
        return False

    def create(self, value):
        self.window.status_bar.update(status='Command "create" not supported')
        return False

    def delete(self, value):
        self.window.status_bar.update(status='Command "delete" not supported')
        return False

    def activate(self, value):
        self.window.status_bar.update(status='Command "activate" not supported')
        return False

    def send(self, value):
        self.window.status_bar.update(status='Command "send" not supported')
        return False

class StatBox(urwid.ListBox):
    """
    StatBox show the walker
    """
    def __init__(self, window, parent, framefocus):
        self.window = window
        self.parent = parent
        self._framefocus = framefocus
        self.walker =StatTree(window, parent.walker, self)
        self.__super.__init__(self.walker)


class StatTree(OldestTree):

    def __init__(self, window, parent, widget_box):
        OldestTree.__init__(self, window, parent, widget_box)
        self.childrens = { '..' : {'id':'..',
                                'name':'..',
                                'help':'Go to previous directory',
                                'widget_box' : None}
                }
        self._path = "stats"
        self.subdirs = ['..']
        self.definition = {'id':'stats',
                        'name':'stats',
                        'help':'statistics',
                        'widget_box': self.widget_box}
        if parent != None and self.definition != None :
            parent.add_child(self._path,self.definition)

    def read_lines(self):
        self.size = 0
        #self.key = self.window.network.controller.node_id
        #self.focus, self.oldfocus = self.oldfocus, self.focus
        self.lines = []
        if self.window.network == None:
            return
        self.show_directories()
        self.lines.append(urwid.Text(    "    Statistics", align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "  Frames processed: . . . . . . .  . . . . . . . . . . . . %s" % \
            self.window.network.controller.stats['SOFCnt'], align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "  [Device] Messages successfully received: . . . . . . . . %s" % \
            self.window.network.controller.stats['readCnt'], align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "  [Device] Messages successfully sent:  . . . . . . . . . .%s" % \
            self.window.network.controller.stats['writeCnt'], align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "  ACKs received from controller: . . . . . . . . . . . . . %s" % \
            self.window.network.controller.stats['ACKCnt'], align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "  Number of broadcasts read: . . . . . . . . . . . . . . . %s" % \
            self.window.network.controller.stats['broadcastReadCnt'], align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "  Number of broadcasts sent: . . . . . . . . . . . . . . . %s" % \
            self.window.network.controller.stats['broadcastWriteCnt'], align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "    Queue:", align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "  Messages in queue: . . . . . . . . . . . . . . . . . . . %s" % \
            self.window.network.controller.send_queue_count, align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "    Errors:", align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "  Unsolicited messages received while waiting for ACK: . . %s" % \
            self.window.network.controller.stats['ACKWaiting'], align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "  Reads aborted due to timeouts: . . . . . . . . . . . . . %s" % \
            self.window.network.controller.stats['readAborts'], align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "  Bad checksum errors: . . . . . . . . . . . . . . . . . . %s" % \
            self.window.network.controller.stats['badChecksum'], align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "  CANs received from controller: . . . . . . . . . . . . . %s" % \
            self.window.network.controller.stats['CANCnt'], align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "  NAKs received from controller: . . . . . . . . . . . . . %s" % \
            self.window.network.controller.stats['NAKCnt'], align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "  Out of frame data flow errors: . . . . . . . . . . . . . %s" % \
            self.window.network.controller.stats['OOFCnt'], align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "  Messages retransmitted:  . . . . . . . . . . . . . . . . %s" % \
            self.window.network.controller.stats['retries'], align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "  Messages dropped and not delivered:  . . . . . . . . . . %s" % \
            self.window.network.controller.stats['dropped'], align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "  Number of unexpected callbacks: . . . . . . . . .  . . . %s" % \
            self.window.network.controller.stats['callbacks'], align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "  Number of failed messages due to bad route response: . . %s" % \
            self.window.network.controller.stats['badroutes'], align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "  Number of no ACK returned errors: . . . . . . . . .  . . %s" % \
            self.window.network.controller.stats['noack'], align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "  Number of network busy/failure messages: . . . . . . . . %s" % \
            self.window.network.controller.stats['netbusy'], align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "  Number of messages not delivered to network: . . . . . . %s" % \
            self.window.network.controller.stats['nondelivery'], align='left'))
        self.size += 1
        self.lines.append(urwid.Text(    "  Number of messages received with routed busy status: . . %s" % \
            self.window.network.controller.stats['routedbusy'], align='left'))
        self.size += 1
        self._modified()

class GroupsBox(urwid.ListBox):
    """
    GroupsBox show the walker
    """
    def __init__(self, window, parent, framefocus):
        self.window = window
        self.parent = parent
        self._framefocus = framefocus
        self.walker = GroupsTree(window, parent.walker, self)
        self.__super.__init__(self.walker)

class GroupsTree(OldestTree):

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
        self._path = "groups"
        self.node_id = None
        #self.key = 'Groups'
        self.groups_header = AssociationItem()
        self.definition = {'id':'groups',
                                'name':'groups',
                                'help':'Groups/Associations management',
                                'widget_box': self.widget_box
        }
        if parent != None :
            parent.add_child('groups', self.definition)
        self.usage.append("add <nodeid> to <groupindex> : add node <nodeid> to group of index <groupindex>")
        self.usage.append("remove <nodeid> from <groupindex> : remove node <nodeid> from group of index <groupindex>")
        #self.usage.append("set <label> to <data> : change value <label> to data")
        dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)
        dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_AWAKED)
        dispatcher.connect(self._louie_network_resetted, ZWaveNetwork.SIGNAL_NETWORK_RESETTED)

    def _louie_network_resetted(self, network):
        self.window.log.info('GroupsTree _louie_network_resetted.')
        dispatcher.disconnect(self._louie_group_update, ZWaveNetwork.SIGNAL_GROUP)
        self.window.log.info('GroupsTree _louie_network_resetted.')

    def _louie_network_ready(self, network):
        self.window.log.info("GroupsTree _louie_network_ready")
        self.refresh()
        dispatcher.connect(self._louie_group_update, ZWaveNetwork.SIGNAL_GROUP)
        self.window.log.info("GroupsTree _louie_network_ready")

    def _louie_group_update(self, network, node, groupidx):
        self.window.log.info("GroupsTree _louie_node_update")
        self.refresh()
        self.window.log.info("GroupsTree _louie_node_update")

    def read_lines(self):
        self.size = 0
        #self.focus, self.oldfocus = self.oldfocus, self.focus
        self.lines = []
        if self.window.network == None or self.node_id == None:
            return
        self.show_directories()
        self.lines.append(self.groups_header.get_header())
        self.size += 1
        groups = self.window.network.nodes[self.node_id].groups
        self.window.log.info("GroupsTree groups=%s" % groups)
        for group in groups :
            self.window.log.info("GroupsTree group=%s" % group)
            self.lines.append(urwid.Text(    "      %s:%s" % (groups[group].index,groups[group].label), align='left'))
            self.size += 1
            for assoc in groups[group].associations:
                if assoc in self.window.network.nodes:
                    aname = self.window.network.nodes[assoc].name
                else:
                    aname = "[%d missing]" % (assoc)
                self.lines.append(AssociationItem(assoc, aname))
                self.size += 1
        self._modified()

    def exist(self, directory):
        """
        List directory content
        """
        if OldestTree.exist(self, directory):
            return True
        return False

    def cd(self, directory):
        """
        Change to directory and return the widget to display
        """
        if self.exist(directory) :
            if directory == '..':
                self.node_id = None
                return self.parent.widget_box
            if directory in self.childrens:
                self.window.log.info("cd %s" %directory)
                return self.childrens[directory]['widget_box']
        return None

    def add(self, param, value):
        try:
            param = int(param)
            value = int(value)
        except:
            self.window.status_bar.update(status="Invalid index or node ID %s/%s" % (param, value))
            return False
        if param in self.window.network.nodes[self.node_id].groups:
            self.window.network.nodes[self.node_id].groups[param].add_association(value)
            self.window.status_bar.update(status='Group %s updated' % param)
            return True
        else :
            self.window.status_bar.update(status="Group %s don't exist" % param)
            return False

    def remove(self, param, value):
        try:
            param = int(param)
            value = int(value)
        except:
            self.window.status_bar.update(status="Invalid index or node ID %s/%s" % (param, value))
            return False
        if param in self.window.network.nodes[self.node_id].groups:
            if value in self.window.network.nodes[self.node_id].groups[param].associations :
                self.window.network.nodes[self.node_id].groups[param].remove_association(value)
                self.window.status_bar.update(status='Group %s updated' % param)
                return True
            else :
                self.window.status_bar.update(status="Can't find node %s in group %s" % (value,param))
                return False
        else :
            self.window.status_bar.update(status="Can't find group %s" % (param))
            return False

class AssociationItem (urwid.WidgetWrap):

    def __init__ (self, id=0, name=None):
        self.id = id
        #self.content = 'item %s: %s - %s...' % (str(id), name[:20], product_name[:20] )
        self.item = [
            ('fixed', 19, urwid.Padding(
                urwid.AttrWrap(urwid.Text('%s' % id, wrap='space'), 'body', 'focus'), left=2)),
                urwid.AttrWrap(urwid.Text('%s' % name, wrap='space'), 'body'),
        ]
        w = urwid.Columns(self.item, dividechars=1 )
        self.__super.__init__(w)

    def get_header (self):
        self.item = [
            ('fixed', 19, urwid.Padding(
                urwid.AttrWrap(urwid.Text('%s' % "NodeId", wrap='clip'), 'node_header'), left=2)),
                urwid.AttrWrap(urwid.Text('%s' % "Name", wrap='clip'), 'node_header'),
        ]
        return urwid.Columns(self.item, dividechars=1)

    def selectable (self):
        return True

    def keypress(self, size, key):
        return key

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
        dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_AWAKED)
        dispatcher.connect(self._louie_network_resetted, ZWaveNetwork.SIGNAL_NETWORK_RESETTED)

    def _louie_network_ready(self, network):
        self.window.log.info("RootTree _louie_network_ready")
        self.refresh()
        self.window.log.info("RootTree _louie_network_ready")

    def _louie_network_resetted(self, network):
        self.window.log.info('RootTree _louie_network_resetted.')
        self.window.log.info('RootTree _louie_network_resetted.')

    def read_lines(self):
        self.size = 0
        #self.focus, self.oldfocus = self.oldfocus, self.focus
        self.lines = []
        self.show_directories()
        if self.window.network != None:
            self.lines.append(urwid.Text(    "  %s" % \
                self.window.network.controller.library_description, align='left'))
            self.size += 1
            self.lines.append(urwid.Text(    "  %s" % \
                self.window.network.controller.ozw_library_version, align='left'))
            self.size += 1
            self.lines.append(urwid.Text(    "  %s" % \
                self.window.network.controller.python_library_version, align='left'))
            self.size += 1
            self.lines.append(urwid.Divider("-"))
            self.size += 1
            self.lines.append(urwid.Text("  HomeId = %s" % self.window.network.home_id_str, align='left'))
            self.size += 1
        self._modified()

class RootDir (urwid.WidgetWrap):

    def __init__ (self, id=None, name=None, help=None):
        self.id = id
        #self.content = 'item %s: %s - %s...' % (str(id), name[:20], product_name[:20] )
        self.item = [
            ('fixed', 15,
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
            ('fixed', 20, urwid.Padding(
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
            ('fixed', 20, urwid.Padding(
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
                                    'widget_box' : None}
                }
        self._path = "nodes"
        self.node_header = NodesItem()
        self.definition = {'id':'nodes',
                                'name':'nodes',
                                'help':'Nodes management',
                                'widget_box': self.widget_box
        }
        if parent != None and self.definition != None :
            parent.add_child(self.path, self.definition)
        self.usage.append("send switch_all ON|OFF : Send a switch_all command to nodes.")
        dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_AWAKED)
        dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)
        dispatcher.connect(self._louie_network_resetted, ZWaveNetwork.SIGNAL_NETWORK_RESETTED)

    def _louie_network_resetted(self, network):
        self.window.log.info('NodesTree _louie_network_resetted.')
        #dispatcher.disconnect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE)
        self.window.log.info('NodesTree _louie_network_resetted.')

    def _louie_network_ready(self, network):
        self.window.log.info("NodesTree _louie_network_ready")
        self.refresh()
        self.window.log.info("NodesTree _louie_network_ready")
        dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE)
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
        self.show_directories()
        self.lines.append(self.node_header.get_header())
        self.size += 1
        for node in self.window.network.nodes:
            self.lines.append(NodesItem(self.window.network.nodes[node].node_id, \
                self.window.network.nodes[node].name, \
                self.window.network.nodes[node].location, \
                self.window.network.nodes[node].max_baud_rate, \
                self.window.network.nodes[node].get_battery_level(), \
                self.window.network.nodes[node].is_awake, \
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
        try :
            if int(directory) in self.window.network.nodes:
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
                if int(directory) in self.window.network.nodes:
                    self.window.log.info("cd a node id %s" %directory)
                    self.childrens['node']['widget_box'].walker.key=int(directory)
                    return self.childrens['node']['widget_box']
            except :
                pass
        return None

    def send(self, command):
        if command.startswith('switch_all'):
            if ' ' in command :
                cmd,val = command.split(' ',1)
            else:
                self.window.status_bar.update("usage : send switch_all ON|OFF")
                return False
            val = val.strip()
            if val.upper() == "ON" or val.upper() == "TRUE":
                val=True
            else:
                val=False
            self.window.network.switch_all(val)
            self.window.status_bar.update("Command switch_all %s sent" % val)
            return True
        self.window.status_bar.update("usage : send switch_all ON|OFF")
        return False

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

    def __init__ (self, id=0, name=None, location=None, signal=0, battery_level=-1, awaked=False):
        self.id = id
        #self.content = 'item %s: %s - %s...' % (str(id), name[:20], product_name[:20] )
        self.item = [
            ('fixed', 15, urwid.Padding(
                urwid.AttrWrap(urwid.Text('%s' % str(id), wrap='clip'), 'body', 'focus'), left=2)),
                urwid.AttrWrap(urwid.Text('%s' % name, wrap='clip'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % location, wrap='clip'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % signal, wrap='clip'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % battery_level, wrap='clip'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % awaked, wrap='clip'), 'body'),
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
                urwid.AttrWrap(urwid.Text('%s' % "Awaked", wrap='clip'), 'node_header'),
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
                                'widget_box' : None}
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
        self.usage.append("send refresh_info : request info for the node ont the ZWave network")
        self.usage.append("send update_neighbors : update the neighbors.")
        if parent != None and self.definition != None :
            parent.add_child("node",self.definition)
        dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)
        dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_AWAKED)
        dispatcher.connect(self._louie_network_resetted, ZWaveNetwork.SIGNAL_NETWORK_RESETTED)

    def _louie_network_resetted(self, network):
        self.window.log.info('NodeTree _louie_network_resetted.')
        #dispatcher.disconnect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE)
        self.window.log.info('NodeTree _louie_network_resetted.')

    def _louie_network_ready(self, network):
        self.window.log.info("NodeTree _louie_network_ready")
        self.refresh()
        dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE)
        self.window.log.info("NodeTree _louie_network_ready")

    def _louie_node_update(self, network, node):
        self.refresh()

    def set(self, param, value):
        if param in ['name', 'location', 'product_name', 'manufacturer_name' ]:
            self.window.network.nodes[self.key].set_field(param, \
                        value)
            self.window.status_bar.update(status='Field %s updated' % param)
            return True
        return False

    def send(self, command):
        if command == 'refresh_info':
            self.window.network.nodes[self.key].refresh_info()
            self.window.status_bar.update(status='Refresh info requested')
            return True
        elif command.startswith('update_neighbors'):
            self.window.network.controller.request_network_update(self.key)
            self.window.status_bar.update(status='Neighbors nodes requested')
            return True
        return False

    def read_lines(self):
        self.size = 0
        #self.focus, self.oldfocus = self.oldfocus, self.focus
        self.lines = []
        if self.window.network == None or self.key == None:
            return
        self.show_directories()
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
        self.window.log.info("NodeTree num groups = %s" % self.window.network.nodes[self.key].num_groups )
        self._modified()

    @property
    def path(self):
        """
        The path

        :rtype: str

        """
        return "%s" % self.key

    def cd(self, directory):
        """
        Change to directory and return the widget to display
        """
        if self.exist(directory) :
            if directory == '..':
                self.key = None
                return self.parent.widget_box
            if directory in self.childrens:
                self.window.log.info("cd a values list key=%s" %directory)
                self.childrens[directory]['widget_box'].walker.key=directory
                self.childrens[directory]['widget_box'].walker.node_id=self.key
                return self.childrens[directory]['widget_box']
        return None

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
        self.definition = {'id':'controller',
                        'name':'controller',
                        'help':'Controller management',
                        'widget_box': self.widget_box}
        if parent != None and self.definition != None :
            parent.add_child(self._path,self.definition)
        self.usage.append("set <field> to <value> : change the value of a field")
        self.usage.append("reset soft : reset the controller in a soft way. Node association is not required")
        self.usage.append("reset hard : reset the controller. Warning : all nodes must be re-associated with your stick.")
        self.usage.append("send cancel : cancel the current command.")
        self.usage.append("send network_update <node_id> : update the network of <node_id>.")
        self.usage.append("send update_neighbors <node_id> : update the <node_id> neighbors.")
        self.usage.append("send add_device <True|False>: add a device on the network with security support activated or not.")
        self.usage.append("send remove_device : remove a device (not a controller) on the network.")
        #self.usage.append("send add_controller : add a controller on the network.")
        #self.usage.append("send remove_controller : remove a controller on the network.")
        self.usage.append("send has_node_failed <node_id> : Check whether the node <node_id> is in the controller's failed nodes list.")
        self.usage.append("send remove_failed_node <node_id> : move the node <node_id> to the controller's list of failed nodes.")
        self.usage.append("send replace_failed_node <node_id> : Replace the failed <node_id> device with another.")
        dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)
        dispatcher.connect(self._louie_network_resetted, ZWaveNetwork.SIGNAL_NETWORK_RESETTED)
        dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_AWAKED)

    def _louie_network_resetted(self, network):
        self.window.log.info('ControllerTree _louie_network_resetted.')
        #dispatcher.disconnect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE)
        self.window.log.info('ControllerTree _louie_network_resetted.')

    def _louie_network_ready(self, network):
        self.window.log.info("ControllerTree _louie_network_ready")
        self.refresh()
        self.window.log.info("ControllerTree _louie_network_ready")
        dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE)
        #dispatcher.connect(self._louie_ctrl_message, ZWaveNetwork.SIGNAL_CONTROLLER_COMMAND)
        #dispatcher.connect(self._louie_ctrl_message_waiting, ZWaveController.SIGNAL_CTRL_WAITING)

    def _louie_node_update(self, network, node):
        self.refresh()

    #~ def _louie_ctrl_message_waiting(self, network, controller, state_int, state, state_full ):
        #~ self.window.status_bar.update(status='Message from controller: %s : %s' % (state,state_full))
#~
    #~ def _louie_ctrl_message(self, network, controller, node, node_id, state_int, state, state_full, error_int, error, error_full ):
        #~ self.window.status_bar.update(status='Message from controller: %s' % (state_full))

    def set(self, param, value):
        if param in ['name', 'location', 'product_name', 'manufacturer_name' ]:
            self.window.network.controller.node.set_field(param, \
                        value)
            self.window.status_bar.update(status='Field %s updated' % param)
            return True
        return False

    def reset(self, state):
        if state == 'soft':
            self.window.status_bar.update(status='Reset controller softly')
            self.window.network.controller.soft_reset()
            return True
        if state == 'hard':
            self.window.status_bar.update(status='Reset controller hardly')
            self.window.network.controller.hard_reset()
            return True
        return False

    def send(self, command):
        if command == 'network_update':
            if ' ' in command :
                cmd,node = command.split(' ',1)
            else:
                self.window.status_bar.update("usage : send network_update <node_id>")
                return False
            node = node.strip()
            try :
                node = int(node)
            except :
                self.window.status_bar.update("Invalid node_id")
                return False
            self.window.network.controller.request_network_update(node)
            return True
        elif command.startswith('update_neighbors'):
            if ' ' in command :
                cmd,node = command.split(' ',1)
            else:
                self.window.status_bar.update("usage : send update_neighbors <node_id>")
                return False
            node = node.strip()
            try :
                node = int(node)
            except :
                self.window.status_bar.update("Invalid node_id")
                return False
            self.window.network.controller.request_node_neighbor_update(node)
            return True
        elif command.startswith('has_node_failed'):
            if ' ' in command :
                cmd,node = command.split(' ',1)
            else:
                self.window.status_bar.update("usage : send has_node_failed <node_id>")
                return False
            node = node.strip()
            try :
                node = int(node)
            except :
                self.window.status_bar.update("Invalid node_id")
                return False
            self.window.network.controller.has_node_failed(node)
            return True
        elif command.startswith('remove_failed_node'):
            if ' ' in command :
                cmd,node = command.split(' ',1)
            else:
                self.window.status_bar.update("usage : send remove_failed_node <node_id>")
                return False
            node = node.strip()
            try :
                node = int(node)
            except :
                self.window.status_bar.update("Invalid node_id")
                return False
            self.window.network.controller.remove_failed_node(node)
            return True
        elif command.startswith('replace_failed_node'):
            if ' ' in command :
                cmd,node = command.split(' ',1)
            else:
                self.window.status_bar.update("usage : send replace_failed_node <node_id>")
                return False
            node = node.strip()
            try :
                node = int(node)
            except :
                self.window.status_bar.update("Invalid node_id")
                return False
            self.window.network.controller.replace_failed_node(node)
            return True
        elif command.startswith('add_device'):
            if ' ' in command :
                cmd,security = command.split(' ',1)
            else:
                security = False
            try :
                security = bool(security)
            except :
                security = False
            self.window.network.controller.add_node(security)
            return True
        elif command == 'remove_device':
            self.window.network.controller.remove_node()
            return True
        elif command == 'add_controller':
            self.window.network.controller.begin_command_add_controller()
            return True
        elif command == 'remove_controller':
            self.window.network.controller.begin_command_remove_controller()
            return True
        elif command == 'cancel':
            self.window.network.controller.cancel_command()
            return True
        return False

    def read_lines(self):
        self.size = 0
        #self.key = self.window.network.controller.node_id
        #self.focus, self.oldfocus = self.oldfocus, self.focus
        self.lines = []
        if self.window.network == None:
            return
        self.show_directories()
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
                self.window.network.controller.capabilities, align='left'))
            self.size += 1
            self.lines.append(urwid.Divider("-"))
            self.size += 1
            self.lines.append(urwid.Text(    "  Device=%s" % \
                self.window.network.controller.device, align='left'))
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
        self._path = ""
        self.node_id = None
        self.key = 'User'
        self.value_header = ValuesItem()
        self.definition_user = {'id':'User',
                                'name':'User',
                                'help':'User values management',
                                'widget_box': self.widget_box
        }
        self.definition_basic = {'id':'Basic',
                                'name':'Basic',
                                'help':'Basic values management',
                                'widget_box': self.widget_box
        }
        self.definition_config = {'id':'Config',
                                'name':'Config',
                                'help':'Config values management',
                                'widget_box': self.widget_box
        }
        self.definition_system = {'id':'System',
                                'name':'System',
                                'help':'System values management',
                                'widget_box': self.widget_box
        }
        self.definition_all = {'id':'All',
                                'name':'All',
                                'help':'All values management',
                                'widget_box': self.widget_box
        }
        if parent != None :
            parent.add_child('User', self.definition_user)
            parent.add_child('Basic', self.definition_basic)
            parent.add_child('Config', self.definition_config)
            parent.add_child('System', self.definition_system)
            parent.add_child('All', self.definition_all)
        self.usage.append("set <valueid> to <data> : change value <valueid> to data")
        self.usage.append("set <label> to <data> : change value <label> to data")
        self.usage.append("add <label> to <sceneid> : add value <label> to scene od id <sceneid> with current data")
        self.usage.append("poll <label> to <intensity> : poll value <label> with intensity <intensity> : 0 - disable, 1, 2, ...")
        dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_AWAKED)
        dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)
        dispatcher.connect(self._louie_network_resetted, ZWaveNetwork.SIGNAL_NETWORK_RESETTED)

    def _louie_network_ready(self, network):
        self.window.log.info("ValuesTree _louie_network_ready")
        self.refresh()
        dispatcher.connect(self._louie_value_update, ZWaveNetwork.SIGNAL_VALUE)
        self.window.log.info("ValuesTree _louie_network_ready")

    def _louie_network_resetted(self, network):
        self.window.log.info('ValuesTree _louie_network_resetted.')
        #dispatcher.disconnect(self._louie_value_update, ZWaveNetwork.SIGNAL_VALUE)
        self.window.log.info('ValuesTree _louie_network_resetted.')

    def _louie_value_update(self, network, node, value):
        self.window.log.info("ValuesTree _louie_value_update")
        self.refresh()
        self.window.log.info("ValuesTree _louie_value_update")

    def read_lines(self):
        self.size = 0
        #self.focus, self.oldfocus = self.oldfocus, self.focus
        self.lines = []
        if self.window.network == None or self.node_id == None:
            return
        self.show_directories()
        self.lines.append(self.value_header.get_header())
        self.size += 1
        values = self.window.network.nodes[self.node_id].get_values_by_command_classes(genre=self.key)
        for cmd in values :
            self.lines.append(urwid.Text(    "      %s" % (self.window.network.nodes[self.node_id].get_command_class_as_string(cmd)), align='left'))
            self.size += 1
            for val in values[cmd]:
                self.lines.append(ValuesItem(values[cmd][val].value_id, \
                    values[cmd][val].label, \
                    values[cmd][val].help, \
                    values[cmd][val].data, \
                    values[cmd][val].type, \
                    values[cmd][val].data_items, \
                    values[cmd][val].is_read_only, \
                    values[cmd][val].is_polled, \
                    ))
                self.size += 1
        self._modified()

    def exist(self, directory):
        """
        List directory content
        """
        if OldestTree.exist(self, directory):
            return True
        return False

    def cd(self, directory):
        """
        Change to directory and return the widget to display
        """
        if self.exist(directory) :
            if directory == '..':
                self.node_id = None
                return self.parent.widget_box
            if directory in self.childrens:
                self.window.log.info("cd %s" %directory)
                return self.childrens[directory]['widget_box']
        return None

    def add(self, param, value):
        """
        Add a value to scene of id param
        """
        try:
            param = int(param)
        except:
            self.window.status_bar.update(status="Invalid scene id %s" % (param))
            return False
        ok = False
        for val in self.window.network.nodes[self.node_id].values:
            if self.window.network.nodes[self.node_id].values[val].label == value:
                value = val
                ok = True
                exit
        if not ok :
            self.window.status_bar.update(status="Invalid value ID %s" % (param))
            return False
        if self.window.network.scene_exists(param):
            scene = self.window.network.get_scenes()[param]
            ret = scene.add_value(value, \
              self.window.network.nodes[self.node_id].values[value].data)
            if ret :
                self.window.status_bar.update(status='Value %s added to scene %s' % (value,param))
            return ret
        else :
            self.window.status_bar.update(status="Scene %s doesn't exist" % param)
            return False

    def set(self, param, value):
        values = self.window.network.nodes[self.node_id].values
        try:
            param = int(param)
        except:
            ok = False
            for val in values:
                if values[val].label == param:
                    param = val
                    ok = True
                    exit
            if not ok :
                self.window.status_bar.update(status="Invalid value ID %s" % (param))
                return False
        if param in values:
            newval = values[param].check_data(value)
            #self.window.log.info("param %s" %param)
            #self.window.log.info("type param %s" %type(param))
            #self.window.log.info("old_val %s" %value)
            #self.window.log.info("type old_val %s" %type(value))
            #self.window.log.info("newval %s" %newval)
            #self.window.log.info("type newval %s" %type(newval))
            if newval != None :
                values[param].data=newval
                self.window.status_bar.update(status='Value %s updated' % param)
                return True
            else :
                self.window.status_bar.update(status='Invalid data value : "%s"' % value)
            return False
        else :
            self.window.status_bar.update(status="Can't find value Id %s" % (param))
            return False

    def poll(self, param, value):
        values = self.window.network.nodes[self.node_id].values
        try:
            param = int(param)
        except:
            ok = False
            for val in values:
                if values[val].label == param:
                    param = val
                    ok = True
                    exit
            if not ok :
                self.window.status_bar.update(status="Invalid value ID %s" % (param))
                return False
        if param in values:
            try :
                newval = int(value)
            except :
                newval = None
            if newval != None :
                self.window.log.info("poll %s to %s" %(param,newval))
                if newval == 0:
                    values[param].disable_poll()
                else :
                    values[param].enable_poll(newval)
                self.window.status_bar.update(status='Value %s polled to %s' % (param,value))
                return True
            else :
                self.window.status_bar.update(status='Invalid poll value : "%s"' % value)
            return False
        else :
            self.window.status_bar.update(status="Can't find value Id %s" % (param))
            return False

    @property
    def path(self):
        """
        The path

        :rtype: str

        """
        return "%s" % self.key


class ValuesItem (urwid.WidgetWrap):

    def __init__ (self, id=0, name=None, help=None, value=0, type='All', selection='All', read_only=False, polled=False):
        self.id = id
        #self.content = 'item %s: %s - %s...' % (str(id), name[:20], product_name[:20] )
        if read_only :
            value_widget = urwid.AttrWrap(urwid.Text('%s' % value, wrap='clip'), 'body')
        else :
            value_widget = urwid.AttrWrap(urwid.Edit(edit_text='%s' % value, wrap='space'), 'body')
        self.item = [
            ('fixed', 19, urwid.Padding(
                urwid.AttrWrap(urwid.Text('%s' % str(id), wrap='space'), 'body', 'focus'), left=2)),
                urwid.AttrWrap(urwid.Text('%s' % name, wrap='space'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % polled, wrap='space'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % help, wrap='space'), 'body'),
                value_widget,
                urwid.AttrWrap(urwid.Text('%s' % type, wrap='clip'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % selection, wrap='space'), 'body'),
        ]
        w = urwid.Columns(self.item, dividechars=1 )
        self.__super.__init__(w)

    def get_header (self):
        self.item = [
            ('fixed', 19, urwid.Padding(
                urwid.AttrWrap(urwid.Text('%s' % "Id", wrap='clip'), 'node_header'), left=2)),
                urwid.AttrWrap(urwid.Text('%s' % "Label", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Polled", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Help", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Value", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Type", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Items", wrap='clip'), 'node_header'),
        ]
        return urwid.Columns(self.item, dividechars=1)

    def selectable (self):
        return True

    def keypress(self, size, key):
        return key

class SwitchesBox(urwid.ListBox):
    """
    SwitchesBox show the walker
    """
    def __init__(self, window, parent, framefocus):
        self.window = window
        self.parent = parent
        self._framefocus = framefocus
        self.walker = SwitchesTree(window, parent.walker, self)
        self.__super.__init__(self.walker)

class SwitchesTree(OldestTree):

    def __init__(self, window, parent, widget_box):
        OldestTree.__init__(self, window, parent, widget_box)
        self.subdirs = ['..']
        self.childrens = { '..' : {'id':'..',
                                    'name':'..',
                                    'help':'Go to previous directory',
                                    'widget_box' : None},
                }
        self._path = "switches"
        self.switch_header = SwitchesItem()
        self.definition = {'id':'switches',
                                'name':'switches',
                                'help':'All switches on the network',
                                'widget_box': self.widget_box
        }
        if parent != None :
            parent.add_child('switches', self.definition)
        self.usage.append("set <nodeid:Label> to <data> : change value <label> of node <nodeid> to data")
#        self.usage.append("set <label> to <data> : change value <label> to data")
        dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_AWAKED)
        dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)
        dispatcher.connect(self._louie_network_resetted, ZWaveNetwork.SIGNAL_NETWORK_RESETTED)

    def _louie_network_resetted(self, network):
        self.refresh()
        #dispatcher.disconnect(self._louie_value_update, ZWaveNetwork.SIGNAL_VALUE)
        #dispatcher.disconnect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE)

    def _louie_network_ready(self, network):
        dispatcher.connect(self._louie_value_update, ZWaveNetwork.SIGNAL_VALUE)
        dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE)

    def _louie_value_update(self, network, node, value):
        self.refresh()

    def _louie_node_update(self, network, node):
        self.refresh()

    def read_lines(self):
        self.size = 0
        #self.focus, self.oldfocus = self.oldfocus, self.focus
        self.lines = []
        if self.window.network == None:
            return
        self.show_directories()
        self.lines.append(self.switch_header.get_header())
        self.size += 1
        for node in self.window.network.nodes :
            switches = self.window.network.nodes[node].get_switches()
            if len(switches) != 0 :
                self.lines.append(urwid.Text(    "      %s - %s" % (self.window.network.nodes[node].node_id,self.window.network.nodes[node].name), align='left'))
                self.size += 1
                for switch in switches:
                    self.lines.append(SwitchesItem(switches[switch].value_id, \
                        switches[switch].label, \
                        switches[switch].help, \
                        switches[switch].data, \
                        switches[switch].type, \
                        switches[switch].data_items, \
                        ))
                    self.size += 1
        self._modified()

    def exist(self, directory):
        """
        List directory content
        """
        if OldestTree.exist(self, directory):
            return True
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
        return None

    def set(self, param, value):
        try:
            self.window.log.info("SwitchesTree set %s" % param)
            node,switch = param.split(':',1)
            node = int(node)
        except:
            self.window.status_bar.update(status="Invalid node:label %s" % (param))
            return False
        values = self.window.network.nodes[node].values
        ok = False
        for val in values:
            self.window.log.info("SwitchesTree set %s val %s" % (node,val))
            if values[val].label == switch:
                switch = val
                ok = True
                exit
        if not ok :
            self.window.status_bar.update(status="Invalid label %s on node %s" % (switch,node))
            return False
        if node in self.window.network.nodes:
            newval = values[switch].check_data(value)
            if newval != None :
                self.window.network.nodes[node].set_switch(switch, newval)
                #values[switch].data=value
                self.window.status_bar.update(status='Value %s on node %s updated' % (switch,node))
                return True
            else :
                self.window.status_bar.update(status='Invalid data value : "%s"' % value)
            return False
        else :
            self.window.status_bar.update(status="Can't find node %s" % (node))
            return False

class DimmersBox(urwid.ListBox):
    """
    DimmersBox show the walker
    """
    def __init__(self, window, parent, framefocus):
        self.window = window
        self.parent = parent
        self._framefocus = framefocus
        self.walker = DimmersTree(window, parent.walker, self)
        self.__super.__init__(self.walker)

class DimmersTree(OldestTree):

    def __init__(self, window, parent, widget_box):
        OldestTree.__init__(self, window, parent, widget_box)
        self.subdirs = ['..']
        self.childrens = { '..' : {'id':'..',
                                    'name':'..',
                                    'help':'Go to previous directory',
                                    'widget_box' : None},
                }
        self._path = "dimmers"
        self.switch_header = SwitchesItem()
        self.definition = {'id':'dimmers',
                                'name':'dimmers',
                                'help':'All dimmers on the network',
                                'widget_box': self.widget_box
        }
        if parent != None :
            parent.add_child('dimmers', self.definition)
        self.usage.append("set <nodeid:Label> to <data> : change value <label> of node <nodeid> to data")
#        self.usage.append("set <label> to <data> : change value <label> to data")
        dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_AWAKED)
        dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)
        dispatcher.connect(self._louie_network_resetted, ZWaveNetwork.SIGNAL_NETWORK_RESETTED)

    def _louie_network_resetted(self, network):
        #dispatcher.disconnect(self._louie_value_update, ZWaveNetwork.SIGNAL_VALUE)
        #dispatcher.disconnect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE)
        pass

    def _louie_network_ready(self, network):
        self.refresh()
        dispatcher.connect(self._louie_value_update, ZWaveNetwork.SIGNAL_VALUE)
        dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE)

    def _louie_value_update(self, network, node, value):
        self.refresh()

    def _louie_node_update(self, network, node):
        self.refresh()

    def read_lines(self):
        self.size = 0
        #self.focus, self.oldfocus = self.oldfocus, self.focus
        self.lines = []
        if self.window.network == None:
            return
        self.show_directories()
        self.lines.append(self.switch_header.get_header())
        self.size += 1
        for node in self.window.network.nodes :
            switches = self.window.network.nodes[node].get_dimmers()
            if len(switches) != 0 :
                self.lines.append(urwid.Text(    "      %s - %s" % (self.window.network.nodes[node].node_id,self.window.network.nodes[node].name), align='left'))
                self.size += 1
                for switch in switches:
                    self.lines.append(SwitchesItem(switches[switch].value_id, \
                        switches[switch].label, \
                        switches[switch].help, \
                        switches[switch].data, \
                        switches[switch].type, \
                        switches[switch].data_items, \
                        ))
                    self.size += 1
        self._modified()

    def exist(self, directory):
        """
        List directory content
        """
        if OldestTree.exist(self, directory):
            return True
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
        return None

    def set(self, param, value):
        try:
            self.window.log.info("DimmersTree set %s" % param)
            node,switch = param.split(':',1)
            node = int(node)
        except:
            self.window.status_bar.update(status="Invalid node:label %s" % (param))
            return False
        values = self.window.network.nodes[node].values
        ok = False
        for val in values:
            if values[val].label == switch:
                switch = val
                ok = True
                exit
        if not ok :
            self.window.status_bar.update(status="Invalid label %s on node %s" % (switch,node))
            return False
        if node in self.window.network.nodes:
            newval = values[switch].check_data(value)
            if newval != None :
                #values[switch].data=value
                if not values[switch].is_polled :
                    values[switch].enable_poll()
                self.window.network.nodes[node].set_dimmer(switch,newval)
                self.window.status_bar.update(status='Value %s on node %s updated' % (switch,node))
                return True
            else :
                self.window.status_bar.update(status='Invalid data value : "%s"' % value)
            return False
        else :
            self.window.status_bar.update(status="Can't find node %s" % (node))
            return False

class SwitchesItem (urwid.WidgetWrap):

    def __init__ (self, id=0, name=None, help=None, value=0, type='All', selection='All'):
        self.id = id
        #self.content = 'item %s: %s - %s...' % (str(id), name[:20], product_name[:20] )
        value_widget = urwid.AttrWrap(urwid.Edit(edit_text='%s' % value, wrap='space'), 'body')
        self.item = [
            ('fixed', 19, urwid.Padding(
                urwid.AttrWrap(urwid.Text('%s' % str(id), wrap='space'), 'body', 'focus'), left=2)),
                urwid.AttrWrap(urwid.Text('%s' % name, wrap='space'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % help, wrap='space'), 'body'),
                value_widget,
                urwid.AttrWrap(urwid.Text('%s' % type, wrap='clip'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % selection, wrap='space'), 'body'),
        ]
        w = urwid.Columns(self.item, dividechars=1 )
        self.__super.__init__(w)

    def get_header (self):
        self.item = [
            ('fixed', 19, urwid.Padding(
                urwid.AttrWrap(urwid.Text('%s' % "Id", wrap='clip'), 'node_header'), left=2)),
                urwid.AttrWrap(urwid.Text('%s' % "Label", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Help", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Value", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Type", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Items", wrap='clip'), 'node_header'),
        ]
        return urwid.Columns(self.item, dividechars=1)

    def selectable (self):
        return True

    def keypress(self, size, key):
        return key

class SensorsBox(urwid.ListBox):
    """
    SensorsBox show the walker
    """
    def __init__(self, window, parent, framefocus):
        self.window = window
        self.parent = parent
        self._framefocus = framefocus
        self.walker = SensorsTree(window, parent.walker, self)
        self.__super.__init__(self.walker)

class SensorsTree(OldestTree):

    def __init__(self, window, parent, widget_box):
        OldestTree.__init__(self, window, parent, widget_box)
        self.subdirs = ['..']
        self.childrens = { '..' : {'id':'..',
                                    'name':'..',
                                    'help':'Go to previous directory',
                                    'widget_box' : None},
                }
        self._path = "sensors"
        self.sensor_header = SensorsItem()
        self.definition = {'id':'sensors',
                                'name':'sensors',
                                'help':'All sensors on the network',
                                'widget_box': self.widget_box
        }
        if parent != None :
            parent.add_child('sensors', self.definition)
#        self.usage.append("set <nodeid:Label> to <data> : change value <label> of node <nodeid> to data")
#        self.usage.append("set <label> to <data> : change value <label> to data")
        dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_AWAKED)
        dispatcher.connect(self._louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)
        dispatcher.connect(self._louie_network_resetted, ZWaveNetwork.SIGNAL_NETWORK_RESETTED)

    def _louie_network_resetted(self, network):
        #dispatcher.disconnect(self._louie_value_update, ZWaveNetwork.SIGNAL_VALUE)
        #dispatcher.disconnect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE)
        pass

    def _louie_network_ready(self, network):
        self.refresh()
        dispatcher.connect(self._louie_value_update, ZWaveNetwork.SIGNAL_VALUE)
        dispatcher.connect(self._louie_node_update, ZWaveNetwork.SIGNAL_NODE)

    def _louie_value_update(self, network, node, value):
        self.refresh()

    def _louie_node_update(self, network, node):
        self.refresh()

    def read_lines(self):
        self.size = 0
        #self.focus, self.oldfocus = self.oldfocus, self.focus
        self.lines = []
        if self.window.network == None:
            return
        self.show_directories()
        self.lines.append(self.sensor_header.get_header())
        self.size += 1
        for node in self.window.network.nodes :
            sensors = self.window.network.nodes[node].get_sensors()
            if len(sensors) != 0 :
                self.lines.append(urwid.Text(    "      %s - %s" % (self.window.network.nodes[node].node_id,self.window.network.nodes[node].name), align='left'))
                self.size += 1
                for sensor in sensors:
                    self.lines.append(SensorsItem(sensors[sensor].value_id, \
                        sensors[sensor].label, \
                        sensors[sensor].help, \
                        sensors[sensor].data, \
                        sensors[sensor].type, \
                        sensors[sensor].units, \
                        sensors[sensor].is_polled, \
                    ))
                    self.size += 1
        self._modified()

    def exist(self, directory):
        """
        List directory content
        """
        if OldestTree.exist(self, directory):
            return True
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
        return None

class SensorsItem (urwid.WidgetWrap):

    def __init__ (self, id=0, name=None, help=None, value=0, type='All', units="", polled=0):
        self.id = id
        #self.content = 'item %s: %s - %s...' % (str(id), name[:20], product_name[:20] )
        value_widget = urwid.AttrWrap(urwid.Text('%s' % value, wrap='space'), 'body')
        self.item = [
            ('fixed', 19, urwid.Padding(
                urwid.AttrWrap(urwid.Text('%s' % str(id), wrap='space'), 'body', 'focus'), left=2)),
                urwid.AttrWrap(urwid.Text('%s' % name, wrap='space'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % help, wrap='space'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % type, wrap='clip'), 'body'),
                value_widget,
                urwid.AttrWrap(urwid.Text('%s' % units, wrap='space'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % polled, wrap='space'), 'body'),
        ]
        w = urwid.Columns(self.item, dividechars=1 )
        self.__super.__init__(w)

    def get_header (self):
        self.item = [
            ('fixed', 19, urwid.Padding(
                urwid.AttrWrap(urwid.Text('%s' % "Id", wrap='clip'), 'node_header'), left=2)),
                urwid.AttrWrap(urwid.Text('%s' % "Label", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Help", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Type", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Value", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Units", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Polled", wrap='clip'), 'node_header'),
        ]
        return urwid.Columns(self.item, dividechars=1)

    def selectable (self):
        return True

    def keypress(self, size, key):
        return key

class SceneBox(urwid.ListBox):
    """
    SceneBox show the walker
    """
    def __init__(self, window, parent, framefocus):
        self.window = window
        self.parent = parent
        self._framefocus = framefocus
        self.walker = SceneTree(window, parent.walker, self)
        self.__super.__init__(self.walker)


class SceneTree(OldestTree):

    def __init__(self, window, parent, widget_box):
        OldestTree.__init__(self, window, parent, widget_box)
        self.subdirs = ['..']
        self.childrens = { '..' : {'id':'..',
                                    'name':'..',
                                    'help':'Go to previous directory',
                                    'widget_box' : None},
                }
        self._path = ""
        self.node_id = None
        self.value_header = SceneItem()
        self.definition = {'id':'<idx>',
                        'name':'scene',
                        'help':'Scene management',
                        'widget_box': self.widget_box}
        self.usage.append("set <nodeid:label> to <data> : change the data of a value <nodeid:label>")
        self.usage.append("delete <value> : Remove <value> from scene")
        self.usage.append("delete <valueid> : Remove <valueid> from scene")
        if parent != None and self.definition != None :
            parent.add_child("scene",self.definition)

    def read_lines(self):
        self.size = 0
        #self.focus, self.oldfocus = self.oldfocus, self.focus
        self.lines = []
        if self.window.network == None or self.key == None:
            return
        self.show_directories()
        self.lines.append(self.value_header.get_header())
        self.size += 1
        values = self.window.network.get_scenes()[self.key].get_values_by_node()
        for node in values:
            self.lines.append(urwid.Text(    "      %s - %s" % \
              (node, self.window.network.nodes[node].name), align='left'))
            self.size += 1
            for val in values[node]:
                self.lines.append(SceneItem(values[node][val]['value'].value_id, \
                    values[node][val]['value'].label, \
                    values[node][val]['value'].help, \
                    values[node][val]['data'], \
                    values[node][val]['value'].type, \
                    values[node][val]['value'].data_items, \
                    values[node][val]['value'].is_read_only, \
                    ))
                self.size += 1
        self._modified()

    def exist(self, directory):
        """
        List directory content
        """
        if OldestTree.exist(self, directory):
            return True
        return False

    def cd(self, directory):
        """
        Change to directory and return the widget to display
        """
        if self.exist(directory) :
            if directory == '..':
                self.node_id = None
                return self.parent.widget_box
            if directory in self.childrens:
                self.window.log.info("cd %s" %directory)
                return self.childrens[directory]['widget_box']
        return None

    def delete(self, value):
        valueid = None
        try:
            valueid = int(value)
        except:
            ok = False
            try:
                self.window.log.info("SceneTree delete %s" % value)
                node,switch = value.split(':',1)
                node = int(node)
                values = self.window.network.get_scenes()[self.key].get_values_by_node()[node]
                for val in values:
                    if values[val]['value'].label == value:
                        valueid = val
                        ok = True
                        exit
                if not ok :
                    self.window.status_bar.update(status="Can't find %s - Try to use remove <valueid> instead." % (value))
                    return False
            except:
                    self.window.status_bar.update(status="Invalid value ID %s" % (value))
                    return False
        if self.window.network.get_scenes()[self.key].remove_value(valueid) :
            self.window.status_bar.update(status='Value %s deleted' % value)
            return True
        else :
            self.window.status_bar.update(status="Can't delete value %s" % (value))
            return False

    def set(self, param, value):
        try:
            self.window.log.info("SceneTree set %s" % param)
            node,switch = param.split(':',1)
            node = int(node)
        except:
            self.window.status_bar.update(status="Invalid node:label %s" % (param))
            return False
        values = self.window.network.nodes[node].values
        ok = False
        for val in values:
            self.window.log.info("SceneTree set %s val %s" % (node,val))
            if values[val].label == switch:
                switch = val
                ok = True
                exit
        if not ok :
            self.window.status_bar.update(status="Invalid label %s on node %s" % (switch,node))
            return False
        scene = self.window.network.get_scenes()[self.key]
        if switch in scene.get_values() :
            dict_value = scene.get_values()[switch]
            new_val = dict_value['value'].check_data(value)
            self.window.log.info("switch %s" %switch)
            self.window.log.info("type switch %s" %type(switch))
            self.window.log.info("old_val %s" %value)
            self.window.log.info("type old_val %s" %type(value))
            self.window.log.info("new_val %s" %new_val)
            self.window.log.info("type new_val %s" %type(new_val))
            if new_val != None :
                if scene.set_value(switch, new_val) :
                    self.window.status_bar.update(status='Value %s updated' % switch)
                    return True
                else :
                    self.window.status_bar.update(status="Can't update value %s" % switch)
                    return False
            else :
                self.window.status_bar.update(status="Bad data value %s" % (switch))
                return False
        else :
            self.window.status_bar.update(status="Value invalid %s" % (switch))
            return False

    @property
    def path(self):
        """
        The path

        :rtype: str

        """
        return "%s" % self.key

class SceneItem (urwid.WidgetWrap):

    def __init__ (self, id=0, name=None, help=None, value=0, type='All', selection='All', read_only=False):
        self.id = id
        #self.content = 'item %s: %s - %s...' % (str(id), name[:20], product_name[:20] )
        if read_only :
            value_widget = urwid.AttrWrap(urwid.Text('%s' % value, wrap='clip'), 'body')
        else :
            value_widget = urwid.AttrWrap(urwid.Edit(edit_text='%s' % value, wrap='space'), 'body')
        self.item = [
            ('fixed', 19, urwid.Padding(
                urwid.AttrWrap(urwid.Text('%s' % str(id), wrap='space'), 'body', 'focus'), left=2)),
                urwid.AttrWrap(urwid.Text('%s' % name, wrap='space'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % help, wrap='space'), 'body'),
                value_widget,
                urwid.AttrWrap(urwid.Text('%s' % type, wrap='clip'), 'body'),
                urwid.AttrWrap(urwid.Text('%s' % selection, wrap='space'), 'body'),
        ]
        w = urwid.Columns(self.item, dividechars=1 )
        self.__super.__init__(w)

    def get_header (self):
        self.item = [
            ('fixed', 19, urwid.Padding(
                urwid.AttrWrap(urwid.Text('%s' % "Id", wrap='clip'), 'node_header'), left=2)),
                urwid.AttrWrap(urwid.Text('%s' % "Label", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Help", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Value", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Type", wrap='clip'), 'node_header'),
                urwid.AttrWrap(urwid.Text('%s' % "Items", wrap='clip'), 'node_header'),
        ]
        return urwid.Columns(self.item, dividechars=1)

    def selectable (self):
        return True

    def keypress(self, size, key):
        return key


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
            ret = self.window.network.remove_scene(value)
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
            else :
                self.window.status_bar.update(status="Can't activate scene %s" % value)
            return ret
        else :
            self.window.status_bar.update(status="Can't find scene %s" % value)
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
