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
from frameapp import FrameApp, DIVIDER

MAIN_TITLE = "openzwave Manager"

class TabManager():
    """
    Manage tabulations between different panels (NodeBox, DetailsWidget, ...)
    """
    _tab_next = None
    _tab_prev = None
    tab_focus = None

    def set_tab_next(self, nexttab):
        """
        Set the next panel of this one. Will also set prev_panel of nexttab as me.
        So you don't need to call set_prev_tab.
        """
        self._tab_next = nexttab
        self._tab_next._tab_prev = self

    def set_tab_prev(self, prevtab):
        """
        Set the prev panel of this one. Will also set next_panel of prevtab as me.
        So you don't need to call set_next_tab.
        """
        self._tab_prev = prevtab
        self._tab_prev._tab_next = self

    def get_tab_next(self):
        """
        Returns the next panel of this one.
        """
        return self._tab_next

    def get_tab_prev(self):
        """
        Returns the prev panel of this one
        """
        return self._tab_prev

    def tab_activate(self):
        """
        Called when a tab will be activated. Must be overwritten by child
        """
        if self.parent.framefocus != self._framefocus:
            self.parent.framefocus = self._framefocus
            self.parent.frame.set_focus(self._framefocus)
            self.parent.status_bar.update('Change frame focus')

    def tab_leave(self):
        """
        Called when a tab will be leaved. Must be overwritten by child
        """
        pass

    def tab_handle_key(self, key):
        """
        Handle the 'tab' and 'shift tab' keys
        Must be called by the master keys manager
        :returns: True if the key is a tab. False otherwise
        :rtype: bool
        """
        handle = False
        if key == 'tab':
            self.tab_leave()
            self._tab_next.tab_activate()
            handle = True
            #self.parent.status_bar.update('tab')
        elif key == 'shift tab':
            self.tab_leave()
            self._tab_prev.tab_activate()
            handle = True
            #self.parent.status_bar.update('shift tab')
        return handle

class LeftHeader(urwid.WidgetWrap):
    def __init__(self):
        self.controller = "%s"
        self.controller_urwid = urwid.Text(self.controller % "")
        self.homeid = "HomeId  %s"
        self.homeid_urwid = urwid.Text(self.homeid % 0)
        self.nodes = "%d node(s) (%d sleeping)"
        self.nodes_urwid = urwid.Text(self.nodes % (0,0))
        display_widget = urwid.Pile([self.controller_urwid, \
            self.homeid_urwid, \
            self.nodes_urwid ])
        urwid.WidgetWrap.__init__(self, display_widget)

    def update_homeid(self, nhomeid):
        self.homeid_urwid.set_text(self.homeid % nhomeid)

    def update_controller(self, ncontroller):
        self.controller_urwid.set_text(self.controller % ncontroller)

    def update_nodes(self, awakes, sleepings):
        self.nodes_urwid.set_text(self.nodes % (awakes, sleepings))

class RightHeader(urwid.WidgetWrap):
    def __init__(self):
        self.zwave = "%s"
        self.zwave_urwid = urwid.Text(self.zwave % "", align='right')
        self.ozwave = "%s"
        self.ozwave_urwid = urwid.Text(self.ozwave % "", align='right')
        self.python = "%s"
        self.python_urwid = urwid.Text(self.python % "", align='right')
        display_widget = urwid.Pile([self.zwave_urwid, \
            self.ozwave_urwid, \
            self.python_urwid ])
        urwid.WidgetWrap.__init__(self, display_widget)

    def update(self, zw, ozw, python):
        self.zwave_urwid.set_text(self.zwave % zw)
        self.ozwave_urwid.set_text(self.ozwave % ozw)
        self.python_urwid.set_text(self.python % python)

class DetailsWidget(urwid.WidgetWrap):
    """
    """
    def __init__(self, parent, framefocus):
        self.parent = parent
        self._framefocus = framefocus
        self.nodeid       = "Id           : %s"
        self.nodeid_urwid = urwid.Text(self.nodeid % "", wrap='clip')
        self.name         = "Name         : "
        self.name_urwid = urwid.Edit(self.name, wrap='clip')
        self.location     = "Location     : "
        self.location_urwid = urwid.Edit(self.location, wrap='clip')
        self.manufacturer = "Manufacturer : "
        self.manufacturer_urwid = urwid.Edit(self.manufacturer, wrap='clip')
        self.product      = "Product      : "
        self.product_urwid = urwid.Edit(self.product, wrap='clip')
        self.neighbors    = "Neighbors    : %s"
        self.neighbors_urwid = urwid.Text(self.neighbors % "", wrap='clip')
        self.version      = "Version      : %s"
        self.version_urwid = urwid.Text(self.version % "", wrap='clip')
        self.signal       = "Bauds        : %s"
        self.signal_urwid = urwid.Text(self.signal % "", wrap='clip')
        self.display_widget = urwid.Pile([\
            self.nodeid_urwid, \
            self.name_urwid, \
            self.location_urwid, \
            self.product_urwid, \
            self.manufacturer_urwid, \
            self.neighbors_urwid, \
            self.version_urwid, \
            self.signal_urwid, \
            ])
        urwid.WidgetWrap.__init__(self, self.display_widget)

    def header_widget(self):
        header = urwid.Pile([
            DIVIDER,
            urwid.AttrWrap(urwid.Text("Header"), 'sub_frame_header')
            ])
        return header

    def footer_widget(self):
        footer = urwid.Pile([
            DIVIDER,
            urwid.AttrWrap(urwid.Text("Footer"), 'sub_frame_footer')
            ])
        return footer

    def update( self, nodeid="", name="", location="", manufacturer="", \
            product="", neighbors="", version="", signal="" ):
        #size, = self.nodeid_urwid.pack()
        #print size
        self.nodeid_urwid.set_text(self.nodeid % nodeid)
        self.name_urwid.set_edit_text(name)
        self.location_urwid.set_edit_text(location)
        self.manufacturer_urwid.set_edit_text(manufacturer)
        self.product_urwid.set_edit_text(product)
        self.neighbors_urwid.set_text(self.neighbors % neighbors)
        self.version_urwid.set_text(self.version % version)
        self.signal_urwid.set_text(self.signal % signal)

    def keypress(self, size, key):
        if not self.parent.handle_main_key(key):
            if key == 'enter':
                txtid,attrid = self.nodeid_urwid.get_text()
                snodeid = txtid.split(':')[1]
                nodeid = int(snodeid)
                if self.display_widget.get_focus()==self.name_urwid :
                    self.parent.frame.set_status_bar('Node name update')
                    self.parent.network.nodes[nodeid].name = \
                        self.name_urwid.get_edit_text()
                elif self.display_widget.get_focus()==self.location_urwid :
                    self.parent.frame.set_status_bar('Node location update')
                    self.parent.network.nodes[nodeid].location = \
                        self.location_urwid.get_edit_text()
                elif self.display_widget.get_focus()==self.manufacturer_urwid :
                    self.parent.frame.set_status_bar('Node manufacturer name update')
                    self.parent.network.nodes[nodeid].manufacturer_name = \
                        self.manufacturer_urwid.get_edit_text()
                elif self.display_widget.get_focus()==self.product_urwid :
                    self.parent.frame.set_status_bar('Node product name update')
                    self.parent.network.nodes[nodeid].product_name = \
                        self.product_urwid.get_edit_text()
                else :
                    self.parent.frame.set_status_bar('Warning : unknown update from DetailsWidget')
                return
            else :
                rc = self.__super.keypress(size, key)
                return rc
        return

class MenuItem (urwid.WidgetWrap):

    def __init__ (self, name=None, view=None):
        self.name = name
        self.view = view
        self.item = [
            ('fixed', 15, urwid.Padding(
                urwid.AttrWrap(urwid.Text('%s' % name, wrap='clip'), 'body', 'focus'), left=2)),
        ]
        w = urwid.BoxAdapter(self.item, height=1 )
        self.__super.__init__(w)

    def selectable (self):
        return True

    def keypress(self, size, key):
        return key

class MenuWalker(urwid.ListWalker):
    focus, oldfocus = (0, 0)
    size = 0

    def __init__(self, parent):
        self.parent = parent
        self.load_menus()

    def _get_at_pos(self, pos):
        if pos >= 0 and pos < self.size and len(self.menus)>0:
            return self.menus[pos], pos
        else:
            return None, None

    def get_focus(self):
        return self._get_at_pos(self.focus)

    def get_focus_entry(self):
        return self.menus[self.focus]

#    def set_focus(self, focus):
#        if self.focus != focus:
#            self.focus = focus
#            self.parent.update_node(self.get_nodeid())
#            self._modified()

    def get_next(self, pos):
        return self._get_at_pos(pos + 1)

    def get_prev(self, pos):
        return self._get_at_pos(pos - 1)

    def go_first(self):
        self.set_focus(0)

    def go_last(self):
        self.set_focus(self.size - 1)

    def load_menus(self):
        self.size = 0
        self.menus = []
        self.menus.append(MenuItem("Details", \
                None ))
        self.size += 1
        self.menus.append(MenuItem("Commands", \
                None ))
        self.size += 1

class MenuBox(urwid.ListBox):
    """
    NodexBox show the walker
    """

    def __init__(self, parent, framefocus):
        self.parent = parent
        self._framefocus = framefocus
        self.walker = MenuWalker(self.parent)
        self.__super.__init__(self.walker)

#    def rows(self):
#        return 8

class MenuBox3(urwid.Pile, TabManager):
    """
    NodexBox show the walker
    """

    def __init__(self, parent, framefocus):
        self.parent = parent
        self._framefocus = framefocus
        self.size = 0
        self.menu_details = MenuItem("Details", \
                None )
        self.size += 1
        self.menu_commands = MenuItem("Commands", \
                None )
        self.size += 1
        self.__super.__init__([\
            self.menu_details, \
            self.menu_commands, \
            ])

    def tab_activate(self):
        """
        Called when a tab will be activated. Must be overwritten by child
        """
        TabManager.tab_activate(self)
        #if self.tab_focus != None :
        #    self.set_focus(self.tab_focus)

    def tab_leave(self):
        """
        Called when a tab will be leaved. Must be overwritten by child
        """
        #self.tab_focus = self.get_focus()
        pass

    def keypress(self,(maxcol,maxrow), key):
        if not self.parent.handle_main_key(key) and \
                not self.tab_handle_key(key):
            rc = self.__super.keypress((maxcol, maxrow), key)
            return rc
        return

class MenuWidget2(urwid.WidgetWrap, TabManager):
    def __init__(self, parent, framefocus):
        self.parent = parent
        self._framefocus = framefocus
        self.size = 0
        self.menu_details = MenuItem("Details", \
                None )
        self.size += 1
        self.menu_commands = MenuItem("Commands", \
                None )
        self.size += 1
        self.__super.__init__([\
            self.menu_details, \
            self.menu_commands, \
            ])
        self.display_widget = urwid.Pile([\
            self.menu_details, \
            self.menu_commands, \
            ])
        urwid.WidgetWrap.__init__(self, self.display_widget)

class MenuWidget(urwid.WidgetWrap):
    def __init__(self, parent, framefocus):
        self.parent = parent
        self._framefocus = framefocus
        self.details = "Details"
        self.details_urwid = urwid.Button(self.details)
        self.commands = "Commands"
        self.commands_urwid = urwid.Button(self.commands)
        self.neighbors = "Neighbors"
        self.neighbors_urwid = urwid.Button(self.neighbors)
        self.display_widget = urwid.Pile([ \
            urwid.AttrWrap(self.details_urwid, 'menu', 'focus'), \
            urwid.AttrWrap(self.commands_urwid, 'menu', 'focus'), \
            urwid.AttrWrap(self.neighbors_urwid, 'menu', 'focus'), \
            ])
        urwid.WidgetWrap.__init__(self, self.display_widget)

    def keypress(self, size, key):
        if not self.parent.handle_main_key(key):
            if key == 'enter':
                pass
                return
            else :
                rc = self.__super.keypress(size, key)
                return rc
        return

class StatusBar(urwid.WidgetWrap):
    def __init__(self):
        self.statusbar = "%s"
        self.statusbar_urwid = urwid.Text(self.statusbar % "")
        self.menu_urwid = urwid.Columns([
                #urwid.AttrWrap(urwid.Text('F:', wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('1%s' % "Help", wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('2%s' % "", wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('3%s' % "", wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('4%s' % "", wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('5%s' % "Refresh", wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('6%s' % "", wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('7%s' % "", wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('8%s' % "", wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('9%s' % "", wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('10%s' % "", wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('11%s' % "", wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('12%s' % "", wrap='clip'), 'menu'),
        ], dividechars=1)
        display_widget = urwid.Pile([ \
            self.menu_urwid, \
            DIVIDER,
            self.statusbar_urwid, \
            ])
        urwid.WidgetWrap.__init__(self, display_widget)

    def update(self, status):
        self.statusbar_urwid.set_text(self.statusbar % status)

class NodeItem (urwid.WidgetWrap):

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

class NodesWalker(urwid.ListWalker):
    nodes = []
    focus, oldfocus = (0, 0)
    size = 0

    def __init__(self, parent):
        self.parent = parent
    #    self._framefocus = framefocus
    #    self.read_nodes(None)

    def _get_at_pos(self, pos):
        if pos >= 0 and pos < self.size and len(self.nodes)>0:
            return self.nodes[pos], pos
        else:
            return None, None

    def get_nodeid(self):
        node,pos = self._get_at_pos(self.focus)
        return node.id

    def get_focus(self):
        return self._get_at_pos(self.focus)

    def get_focus_entry(self):
        return self.nodes[self.focus]

    def set_focus(self, focus):
        if self.focus != focus:
            self.focus = focus
            self.parent.update_node(self.get_nodeid())
            self._modified()

    def get_next(self, pos):
        return self._get_at_pos(pos + 1)

    def get_prev(self, pos):
        return self._get_at_pos(pos - 1)

    def go_first(self):
        self.set_focus(0)

    def go_last(self):
        self.set_focus(self.size - 1)

    def reread_nodes(self, network):
        #self.oldfocus = self.focus
        self.read_nodes(network)

    def read_nodes(self, network):
        self.size = 0
        #self.focus, self.oldfocus = self.oldfocus, self.focus
        self.nodes = []
        if network == None:
            return
        for node in network.nodes:
            self.nodes.append(NodeItem(network.nodes[node].node_id, \
                network.nodes[node].name, \
                network.nodes[node].location, \
                network.nodes[node].max_baud_rate, \
                network.nodes[node].battery_level, \
                ))
            self.size += 1
        self._modified()

    def get_selected(self):
        ret = []
        for x in self.nodes:
            if x.selected == True:
                ret.append(x)
        return ret

class NodesBox(urwid.ListBox):
    """
    NodexBox show the walker
    """

    def __init__(self, parent, framefocus):
        self.parent = parent
        self._framefocus = framefocus
        self.walker = NodesWalker(self.parent)
        self.__super.__init__(self.walker)

    def keypress(self,(maxcol,maxrow), key):
        if not self.parent.handle_main_key(key):
            rc = self.__super.keypress((maxcol, maxrow), key)
            return rc
        return

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
        self.left_header = LeftHeader()
        self.right_header = RightHeader()
        self.details = DetailsWidget(self, "result")
        #self.menu = MenuWidget(self, "footer")
        self.network = None
        #self.nodes_walker = NodesWalker(self, self.network)
        self.listbox_header = NodeItem()
        self.listbox = NodesBox(self, "body")
        self.menu = MenuWidget(self, "value")


        self.nodes = []
        self.status_bar = StatusBar()
        self.header = urwid.Pile([
            #self.divider,
            urwid.Columns([
                ('weight', 2, urwid.AttrWrap(self.left_header, 'reverse')),
                #('fixed', 1, urwid.Divider("|")),
                ('weight', 2, urwid.AttrWrap(self.right_header, 'reverse'))
            ], dividechars=2, min_width=8),
            DIVIDER,
            self.listbox_header.get_header()
            ])

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
        self.footer = urwid.Pile([
            DIVIDER,
            urwid.AttrWrap(self.status_bar, 'reverse'),
            #self.divider,
            #urwid.AttrWrap(urwid.Text(" > "), 'footer')
            ])
        self.framefocus = 'body'

#        self.frame = urwid.Frame(urwid.AttrWrap(self.listbox, 'body'), \
#            header=self.header,\
#            footer=self.footer, \
#            focus_part=self.framefocus)

        self.frame = FrameApp(urwid.AttrWrap(self.listbox, 'body'), \
            header=self.header,\
            command=(self.menu,1),\
            result=(self.details,5),\
#            value=self.menu,\
#            footer=self.footer, \
            log = self.log, \
            focus_part=self.framefocus,
            status_bar=self.footer_display,
            menu_f=self.footer_display,
            )

        self.frame.set_menu_f(f1="Help",f5="Refresh")

        self.loop = urwid.MainLoop(self.frame, \
            self._palette, \
            unhandled_input=self._unhandled_input)


    def refresh_nodes(self):
        self.listbox.body.read_nodes(self.network)
        self.update_node(self.listbox.walker.get_nodeid())

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

    def handle_main_key(self, key):
        if key == 'f5':
            self.refresh_nodes()
        else:
            self.log.info('unhandled: %s' % repr(key))

    def _unhandled_input(self, key):
        if key == 'esc':
            self.network.write_config()
            raise urwid.ExitMainLoop()
        else:
            self.log.info('unhandled: %s' % repr(key))

    def _start_network(self):
        #Define some manager options
        self.options = ZWaveOption(self.device, \
          config_path="../openzwave/config", \
          user_path=".", cmd_line="")
        self.options.set_log_file("OZW_Log.log")
        self.options.set_append_log_file(False)
        self.options.set_console_output(False)
        self.options.set_save_log_level('Debug')
        self.options.set_logging(True)
        self.options.lock()
        self.network = ZWaveNetwork(self.options, self.log)
        self.frame.set_status_bar('Start Network')

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
        self.left_header.update_controller("%s on %s" % \
            (network.controller.node.product_name, self.device))
        self.left_header.update_homeid(network.home_id_str)
        self.left_header.update_nodes(network.nodes_count,0)
        self.right_header.update(network.controller.library_description, \
            network.controller.ozw_library_version, \
            network.controller.python_library_version)
        self.frame.set_status_bar('OpenZWave driver is ready')
        self.loop.draw_screen()

    def _louie_network_ready(self, network):
        self.log.info('ZWave network is ready : %d nodes were found.' % network.nodes_count)
        self.log.info('Controller name : %s' % network.controller.node.product_name)
        self.network = network
        self.left_header.update_controller("%s on %s" % \
            (network.controller.node.product_name, self.device))
        self.left_header.update_nodes(network.nodes_count,0)
        #self.set_nodes()
        self.frame.set_status_bar('ZWave network is ready')
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
        self.frame.set_status_bar('Node event')
        self.refresh_nodes()
        self.loop.draw_screen()

    def _wrap(self, widget, attr_map):
        return urwid.AttrMap(widget, attr_map)

    def rawWrite(self, text):
        """ Add a line of text to our listbox. """
        self.walker.append(urwid.Text(text))
        self.walker.set_focus(len(self.walker.contents))

    def update_screen(self, size):
        canvas = self.frame.render(size, focus=True)
        self.draw_screen(size, canvas)

window = None
def main():
    device = "/dev/zwave-aeon-s2"
    footer = True
    for arg in sys.argv:
        if arg.startswith("--help") or arg.startswith("-h"):
            print("Usage : ozwman [--device=/dev/zwave-aeon-s2] [--nofooter]")
            print("   --device=path_to_your_zwave_stick")
            print("   --nofooter : Don't display footer")
            sys.exit("")

        if arg.startswith("--device"):
            temp,device = arg.split("=")
        if arg.startswith("--nofooter"):
            footer = False
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

