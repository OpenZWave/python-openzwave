#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import namedtuple

import curses
import curses.panel
import logging
import threading
import time
from louie import dispatcher, All
from openzwave.wrapper.wrapper import ZWaveWrapper

padcoords = namedtuple('padcoords', ['sminrow','smincol','smaxrow','smaxcol'])
colorlevels = namedtuple('colorlevels', ['error','warning'])

class ZWaveCommander:
    def __init__(self, stdscr):
        self._curAlert = False
        self._alertStack = list()
        self._driverInitialized = False
        self._wrapper = None
        self._listMode = True
        self._screen = stdscr
        self._version = '0.1 Beta 1'
        self._listtop = 0
        self._listindex = 0
        self._listcount = 0
        self._selectedNode = None
        self._stop = threading.Event()
        self._keys = {
            'A' : 'Add',
            'B' : 'About',
            'D' : 'Delete',
            'R' : 'Refresh',
            'S' : 'Setup',
            '+' : 'Increase',
            '-' : 'Decrease',
            '1' : 'On',
            '0' : 'Off',
            'Q' : 'Quit'
        }

        self._config = {
            'device': '/dev/keyspan-2',
            'config': '../openzwave/config/',
        }

        # TODO: add log level to config
        # TODO: add log enable/disable to config
        # TODO: logging - can ozw log be redirected to file?  If so, we can add ability to view/tail log
        FORMAT='%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s'
        logging.basicConfig(filename='test.log', level=logging.DEBUG, format=FORMAT)
        self._log = logging.getLogger('ZWaveCommander')
        self._logbar ='\n%s\n' % ('-'*60)

    def main(self):
        '''Main run loop'''
        self._log.info('%sZWaveCommander Version %s Starting%s', self._logbar, self._version, self._logbar)
        self._initCurses(self._screen)
        try:
            self._checkConfig()
            self._checkInterface()
            self._runLoop()
        finally:
            self._shutdown()

    def _delayloop(self, context, duration, callback):
        self._log.debug('thread %s sleeping...', context)
        time.sleep(duration)
        self._log.debug('timer %s expired, executing callback %s', context, callback)
        if context == 'alert':
            self._curAlert = False
            if self._alertStack:
                self._alert(self._alertStack.pop())
        if callback is not None:
            callback()

    def _handleQuit(self):
        # TODO: exit confirmation dialog
        self._log.info('Stop requested')
        self._stop.set()

    def _handleRefresh(self):
        if self._selectedNode:
            self._wrapper.refresh(self._selectedNode)

    def _handleOn(self):
        if self._selectedNode:
            self._wrapper.setNodeOn(self._selectedNode)

    def _handleOff(self):
        if self._selectedNode:
            self._wrapper.setNodeOff(self._selectedNode)

    def _handleIncrease(self):
        if self._selectedNode:
            curLevel = self._selectedNode.level
            newLevel = curLevel + 10
            if newLevel > 99: newLevel = 99
            self._wrapper.setNodeLevel(self._selectedNode, newLevel)

    def _handleDecrease(self):
        if self._selectedNode:
            curLevel = self._selectedNode.level
            newLevel = curLevel - 10
            if newLevel < 0: newLevel = 0
            self._wrapper.setNodeLevel(self._selectedNode, newLevel)
        
    def _setTimer(self, context, duration, callback):
        newTimer = threading.Thread(None, self._delayloop, 'cb-thread-%s' % context, (context, duration, callback), {})
        newTimer.setDaemon(True)
        newTimer.start()

    def _alert(self, text):
        '''perform program alert'''
        if not self._curAlert:
            self._curAlert = True
            curses.flash()
            self._screen.addstr(self._screensize[0] - 1, 0, ' {0:{width}}'.format(text, width=self._screensize[1] - 2),
                            curses.color_pair(self.COLOR_ERROR))
            self._screen.refresh()
            self._setTimer('alert', 1, self._redrawMenu)
        else:
            self._alertStack.append(text)

    def _layoutScreen(self):
        # TODO: handle screen resize on curses.KEY_RESIZE in loop (tear down, re-calculate, and re-build)
        # top 5 lines (fixed): system info (including list header)
        # bottom line (fixed): menu/status
        # remaining top half: item list (scrolling)
        # remaining bottom half: split - left half=static info, right half=detail (scrolling)
        # item list: 8 columns. All column widths here are padded with 1 char space (except col 0, which is always 1 char)
        # c0=1 char fixed (select indicator)
        # c1=4 char fixed (id)
        # c2=10 char min (name)
        # c3=10 char min (location)
        # c4=20 char min (type)
        # c5=9 char fixed (state)
        # c6=7 char fixed (batt)
        # c7=7 char fixed (signal)
        # last three columns: 23 chars: are optional and can fall off if space requires it (min width 45)
        # "min" columns expand evenly to fit remaining space

        self._screen.clear()
        self._log.debug("Laying out screen")
        self._colwidths=[1,4,10,10,15,12,8,8]
        self._colheaders=['','ID','Name','Location','Type','State','Batt','Signal']
        self._detailheaders=['Info','Values','Classes','Groups','Events']
        self._flexcols=[2,3,4]
        self._rowheights=[5,5,10,1]
        self._flexrows=[1,2]
        self._deviceValueColumns=['id','commandClass','instance','index','type','label','value','units']
        self._deviceValueWidths= [10,20,9,6,10,20,10,10]


        self._sortcolumn = self._colheaders[1]
        self._detailview = self._detailheaders[0]

        self._screensize = self._screen.getmaxyx()
        width = self._screensize[1]
        height = self._screensize[0]
        self._log.debug('Screen is %d wide by %d high', width, height)

        # Update dynamic column widths for device list
        self._log.debug('Initial column widths are: %s', self._colwidths)
        cwid = 0
        for i in self._colwidths: cwid += i
        flexwidth = width - cwid
        if flexwidth > 0:
            adder = divmod(flexwidth, len(self._flexcols))
            for i in self._flexcols:
                self._colwidths[i] += adder[0]
            self._colwidths[self._flexcols[-1]] += adder[1]
        self._log.debug('Adjusted column widths are: %s' ,self._colwidths)

        # Update dynamic row heights for screen sections
        self._log.debug('Initial row heights are: %s' , self._rowheights)
        cht = 0
        for i in self._rowheights: cht += i
        flexheight = height - cht
        if flexheight > 0:
            adder = divmod(flexheight, len(self._flexrows))
            for i in self._flexrows:
                self._rowheights[i] += adder[0]
            self._rowheights[self._flexrows[-1]] += adder[1]
        self._log.debug('Adjusted row heights are: %s' , self._rowheights)

        if curses.has_colors():
            self._log.debug('Curses initialized: %d colors and %d color pairs available', curses.COLORS, curses.COLOR_PAIRS)
        else:
            self._log.debug('Curses initialized, but no colors are available')

        self._listpad = curses.newpad(256,256)
        self._detailpads = {
            'Info': curses.newpad(self._rowheights[2], self._screensize[1]),
            'Values': curses.newpad(128, self._screensize[1]),
            'Classes': curses.newpad(128, self._screensize[1]),
            'Groups': curses.newpad(self._rowheights[2], self._screensize[1]),
            'Events': curses.newpad(256, self._screensize[1])
        }
        self._detailpos = dict()
        for k in self._detailpads.iterkeys():
            self._detailpos[k] = 0

        self._detailtop = self._rowheights[0] + self._rowheights[1] + 2
        self._detailbottom = self._detailtop + self._rowheights[2] - 3

        self._updateColumnHeaders()

    def _initCurses(self, stdscr):
        '''Configure ncurses application-specific environment (ncurses has already been initialized)'''
        curses.curs_set(0)

        # Re-define color attributes...
        self.COLOR_NORMAL=1
        self.COLOR_HEADER_NORMAL=2
        self.COLOR_HEADER_HI=3
        self.COLOR_ERROR=4
        self.COLOR_CRITICAL=5
        self.COLOR_WARN=6
        self.COLOR_OK=7

        curses.init_pair(self.COLOR_NORMAL, curses.COLOR_WHITE, curses.COLOR_BLACK) # normal (selected row is inverted, disabled/sleep is dim)
        curses.init_pair(self.COLOR_HEADER_NORMAL, curses.COLOR_BLACK, curses.COLOR_GREEN) # header normal
        curses.init_pair(self.COLOR_HEADER_HI, curses.COLOR_WHITE, curses.COLOR_CYAN) # header hi
        curses.init_pair(self.COLOR_ERROR, curses.COLOR_YELLOW, curses.COLOR_RED) # error text
        curses.init_pair(self.COLOR_CRITICAL, curses.COLOR_RED, curses.COLOR_BLACK) # critical
        curses.init_pair(self.COLOR_WARN, curses.COLOR_YELLOW, curses.COLOR_BLACK) # warn
        curses.init_pair(self.COLOR_OK, curses.COLOR_GREEN, curses.COLOR_BLACK) # ok

        self._layoutScreen()

    def _checkConfig(self):
        # TODO: check if configuration exists and is valid.  If not, then go directly to handleSetup().  Loop until user cancels or enters valid config.
        pass

    def _handleSetup(self):
        self._alert('handleSetup not yet implemented')

    def _checkIfInitialized(self):
        if not self._driverInitialized:
            msg = 'Unable to initialize driver - check configuration'
            self._alert(msg)
            self._log.warning(msg)
            self._handleSetup()
        else:
            self._log.info('OpenZWave initialized successfully.')

    def _notifyDriverReady(self, homeId):
        self._log.info('OpenZWave Driver is Ready; homeid is %0.8x.  %d nodes were found.', homeId, self._wrapper.nodeCount)
        self._driverInitialized = True
        self._addDialogText(2,'Driver initialized with homeid {0}'.format(hex(homeId)))
        self._addDialogText(3,'Node Count is now {0}'.format(self._wrapper.nodeCount))
        self._readyNodeCount = 0

    def _notifyNodeAdded(self, homeId, nodeId):
        self._addDialogText(3,'Node Count is now {0}'.format(self._wrapper.nodeCount))
        self._updateSystemInfo()

    def _redrawAll(self):
        self._clearDialog()
        self._updateSystemInfo()
        self._updateDeviceList()
        self._updateColumnHeaders()
        self._updateDeviceDetail()

    def _notifySystemReady(self):
        self._log.info('OpenZWave Initialization Complete.')
        self._alert('OpenZWave Initialization Complete.')
        self._redrawAll()

    def _notifyNodeReady(self, homeId, nodeId):
        self._readyNodeCount += 1
        self._addDialogText(2, 'OpenZWave is querying associated devices')
        self._addDialogText(3,'Node {0} is now ready'.format(nodeId))
        self._addDialogProgress(5, self._readyNodeCount, self._wrapper.nodeCount)
        self._updateDeviceList()

    def _notifyValueChanged(self, signal, **kw):
        nodeId = kw['nodeId']
        self._log.debug('Got value changed notification for node {0}'.format(nodeId))
        # TODO: this is very heavy handed - just update appropriate elements
        self._updateDeviceList()
        self._updateDeviceDetail()

    def _initDialog(self, height, width, buttons=('OK',), caption=None):
        self._dialogpad = curses.newpad(height, width)
        self._dialogpad.bkgd(0x94, curses.color_pair(self.COLOR_HEADER_HI))
        self._dialogpad.clear()
        self._dialogpad.box()
        if caption:
           lh = (width / 2) - (len(caption) / 2) - 1
           self._dialogpad.addstr(0, lh, ' {0} '.format(caption), curses.color_pair(self.COLOR_NORMAL) | curses.A_STANDOUT)
        if buttons:
            if len(buttons) > 1:
                bwid = 0
                for bcap in buttons:
                    if len(bcap) > bwid: bwid = len(bcap)
                cellwid = (width - 4) / len(buttons)
                lpad = (cellwid - bwid) / 2 - 1
                rpad = cellwid - bwid - lpad - 1
                self._dialogpad.move(height - 2, 1)
            else:
                bwid = len(buttons[0])
                lpad = rpad = 1
                self._dialogpad.move(height - 2, (width / 2) - (bwid / 2) - 2)
            for button in buttons:
                self._dialogpad.addstr('{0:{wlpad}}<{1:^{wbwid}}>{0:{wrpad}}'.format('',button, wlpad=lpad, wbwid=bwid, wrpad=rpad))
        dt = (self._screensize[0] / 2) - (height / 2)
        dl = (self._screensize[1] / 2) - (width / 2)
        dc = padcoords(sminrow=dt,smincol=dl,smaxrow=dt+height - 1, smaxcol=dl+width - 1)
        self._dialogcoords = dc
        self._dialogpad.overlay(self._screen, 0, 0, dc.sminrow, dc.smincol, dc.smaxrow, dc.smaxcol)
        self._screen.refresh()

    def _clearDialog(self):
        del self._dialogpad
        self._dialogpad = None
        self._dialogcoords = None
        self._screen.touchwin()
        self._screen.refresh()

    def _updateDialog(self):
        if self._dialogpad:
            self._screen.refresh()
            dc = self._dialogcoords
            self._dialogpad.refresh(0,0,dc.sminrow, dc.smincol, dc.smaxrow, dc.smaxcol)

    def _addDialogText(self, row, text, align='^'):
        if self._dialogpad:
            self._dialogpad.addstr(row, 1, '{0:{aln}{wid}}'.format(text, aln=align, wid=self._dialogpad.getmaxyx()[1] - 2))
            self._updateDialog()

    def _addDialogProgress(self, row, current, total, showPercent=True, width=None):
        if self._dialogpad:
            dc = self._dialogcoords
            if width is None:
                width = (dc.smaxcol - dc.smincol) * 2 / 3
            pct = float(current) / float(total)
            filled = int(pct * float(width))
            lh = ((dc.smaxcol - dc.smincol) / 2) - (width / 2)
            self._dialogpad.addch(row, lh - 1, '[', curses.color_pair(self.COLOR_NORMAL) | curses.A_BOLD)
            self._dialogpad.addch(row, lh + width, ']', curses.color_pair(self.COLOR_NORMAL) | curses.A_BOLD)
            self._dialogpad.addstr(row, lh, ' '*width, curses.color_pair(self.COLOR_NORMAL))
            self._dialogpad.addstr(row, lh, '|'*filled, curses.color_pair(self.COLOR_OK) | curses.A_BOLD)
            if showPercent:
                pctstr = '{0:4.0%}'.format(pct)
                lh = ((dc.smaxcol - dc.smincol) / 2) - (len(pctstr) / 2)
                self._dialogpad.addstr(row, lh, pctstr, curses.color_pair(self.COLOR_NORMAL) | curses.A_BOLD)
            self._updateDialog()

    def _checkInterface(self):
        dispatcher.connect(self._notifyDriverReady, ZWaveWrapper.SIGNAL_DRIVER_READY)
        dispatcher.connect(self._notifySystemReady, ZWaveWrapper.SIGNAL_SYSTEM_READY)
        dispatcher.connect(self._notifyNodeReady, ZWaveWrapper.SIGNAL_NODE_READY)
        dispatcher.connect(self._notifyValueChanged, ZWaveWrapper.SIGNAL_VALUE_CHANGED)
        dispatcher.connect(self._notifyNodeAdded, ZWaveWrapper.SIGNAL_NODE_ADDED)
        self._initDialog(10,60,['Cancel'],'Progress')
        self._addDialogText(2,'Initializing OpenZWave')
        self._log.info('Initializing OpenZWave via wrapper')
        self._wrapper = ZWaveWrapper.getInstance(device=self._config['device'], config=self._config['config'], log=None)
        self._setTimer('initCheck', 3, self._checkIfInitialized)

        while not self._stop.isSet() and not self._wrapper.initialized:
            time.sleep(0.1)
            # TODO: handle keys here... cancel/etc

    def _runLoop(self):
        while not self._stop.isSet():   
            key = self._screen.getch()
            if key == curses.KEY_DOWN: self._switchItem(1)
            elif key == curses.KEY_UP: self._switchItem(-1)
            elif key == curses.KEY_LEFT: self._switchTab(-1)
            elif key == curses.KEY_RIGHT: self._switchTab(1)
            elif key == 0x09: self._nextMode()
            elif key is not None: self._handleMnemonic(key)

    def _handleMnemonic(self, key):
        for mnemonic, func in self._keys.iteritems():
            if key == ord(mnemonic[0].lower()) or key == ord(mnemonic[0].upper()):
                funcname = '_handle%s' % func
                try:
                    method = getattr(self, funcname)
                    method()
                except AttributeError as ex:
                    msg = 'No method named [%s] defined!' % funcname
                    self._log.warn('handleMnemonic: %s', msg)
                    self._log.warn('handleMnemonic Exception Details: %s', str(ex))
                    self._alert(msg)
                break

    def _resetDetailPos(self):
        for p in self._detailpos.iterkeys():
            self._detailpos[p] = 0

    def _switchItem(self, delta):
        if self._listMode:
            n = self._listindex + delta
            if n in range(0, self._listcount):
                self._listindex = n
                self._updateDeviceList() # TODO: we don't really need to redraw everything when selection changes
                self._resetDetailPos()
                self._updateDeviceDetail()
        else:
            self._detailpos[self._detailview] += delta
            self._updateDeviceDetail()

    def _switchTab(self, delta):
        if self._listMode:
            i = self._colheaders.index(self._sortcolumn)
            i += delta
            if i > len(self._colheaders) - 1: i = 1
            elif i < 1: i = len(self._colheaders) - 1
            self._sortcolumn = self._colheaders[i]
        else:
            i = self._detailheaders.index(self._detailview)
            i += delta
            if i > len(self._detailheaders) - 1: i = 0
            elif i < 0: i = len(self._detailheaders) - 1
            self._detailview = self._detailheaders[i]
        self._updateColumnHeaders()
        self._updateDeviceList()
        self._updateDeviceDetail()

    def _nextMode(self):
        self._listMode = not self._listMode
        self._updateColumnHeaders()

    def _shutdown(self):
        # TODO: handle orderly shutdown
        pass

    def _rightPrint(self, row, data, attrs=None):
        if attrs is None:
            attrs = curses.color_pair(self.COLOR_NORMAL)
        self._screen.addstr(row, self._screensize[1] - len(data), data, attrs)

    def _updateSystemInfo(self):
        self._screen.addstr(0,1,'{0} on {1}'.format(self._wrapper.controllerDescription, self._config['device']), curses.color_pair(self.COLOR_NORMAL))
        self._screen.addstr(1,1,'Home ID 0x%0.8x' % self._wrapper.homeId, curses.color_pair(self.COLOR_NORMAL))
        self._screen.move(2,1)
        self._screen.addstr('{0} Registered Nodes'.format(self._wrapper.nodeCount), curses.color_pair(self.COLOR_NORMAL))
        if self._wrapper.initialized:
            sleepcount = self._wrapper.sleepingNodeCount
            if sleepcount:
                self._screen.addstr(' ({0} Sleeping)'.format(sleepcount),curses.color_pair(self.COLOR_NORMAL) | curses.A_DIM)
        self._rightPrint(0, '{0} Library'.format(self._wrapper.libraryTypeName))
        self._rightPrint(1, 'Version {0}'.format(self._wrapper.libraryVersion))
        self._screen.refresh()

    def _updateColumnHeaders(self):
        self._screen.move(4,0)
        for text, wid in zip(self._colheaders, self._colwidths):
            clr = curses.color_pair(self.COLOR_HEADER_NORMAL) if self._listMode else curses.color_pair(self.COLOR_NORMAL) | curses.A_STANDOUT
            if text == self._sortcolumn:
                clr = curses.color_pair(self.COLOR_HEADER_HI) | curses.A_BOLD
            self._screen.addstr('{0:<{width}}'.format(text, width=wid), clr)

        self._screen.move(self._rowheights[0] + self._rowheights[1] + 1, 0)
        clr = curses.color_pair(self.COLOR_HEADER_NORMAL) if not self._listMode else curses.color_pair(self.COLOR_NORMAL) | curses.A_STANDOUT
        self._screen.addstr('{0:{width}}'.format('', width=self._screensize[1]), clr)
        self._screen.move(self._rowheights[0] + self._rowheights[1] + 1, 0)
        for text in self._detailheaders:
            clr = curses.color_pair(self.COLOR_HEADER_NORMAL) if not self._listMode else curses.color_pair(self.COLOR_NORMAL) | curses.A_STANDOUT
            if text == self._detailview:
                clr = curses.color_pair(self.COLOR_HEADER_HI) | curses.A_BOLD
            wid = len(text)
            self._screen.addstr(' {0:<{width}} '.format(text, width=wid), clr)

    def _fixColumn(self, text, width, align='<'):
        retval = '{0:{aln}{wid}}'.format(text, aln=align, wid=width)
        if len(retval) > width:
            retval = retval[:width]
        return retval
        
    def _getListItemColor(self, drawSelected):
        return curses.color_pair(self.COLOR_NORMAL) | curses.A_STANDOUT if drawSelected \
            else curses.color_pair(self.COLOR_NORMAL)

    def _drawMiniBar(self, value, minValue, maxValue, drawWidth, drawSelected, drawPercent=False, colorLevels=None):
        clr = self._getListItemColor(drawSelected)
        pct = float(value) / float(maxValue)
        dw = drawWidth - 2
        filled = int(pct * float(dw))
        fillcolor = clr
        if not drawSelected:
            fillcolor = curses.color_pair(self.COLOR_OK)
            if colorLevels:
                if pct <= colorLevels.error:
                    fillcolor = curses.color_pair(self.COLOR_CRITICAL)
                elif pct <= colorLevels.warning:
                    fillcolor = curses.color_pair(self.COLOR_WARN)

        self._listpad.addch('[', clr | curses.A_BOLD)
        self._listpad.addstr('|' * filled, fillcolor)
        self._listpad.addstr(' ' * (dw - filled), clr)
        self._listpad.addch(']', clr | curses.A_BOLD)
        # TODO: draw percent text if requested

    def _drawNodeStatus(self, node, drawSelected):
        clr = self._getListItemColor(drawSelected)
        if node.isSleeping:
            self._listpad.addstr(self._fixColumn('(sleeping)', self._colwidths[5]), clr | curses.A_LOW)
        elif node.hasCommandClass(0x76): # lock
            self._listpad.addstr(self._fixColumn('Locked' if node.isLocked else 'Unlocked', self._colwidths[5]), clr)
        elif node.hasCommandClass(0x26): # multi-level switch
            self._drawMiniBar(node.level, 0, 99, self._colwidths[5], drawSelected)
        elif node.hasCommandClass(0x25): # binary switch
            self._listpad.addstr(self._fixColumn('ON' if node.isOn else 'OFF', self._colwidths[5]), clr)
        else:
            self._listpad.addstr(self._fixColumn('OK', self._colwidths[5]), clr)

    def _drawBatteryStatus(self, node, drawSelected):
        clr = self._getListItemColor(drawSelected)
        if node.hasCommandClass(0x80):
            self._drawMiniBar(node.batteryLevel, 0, 100, self._colwidths[6], drawSelected, colorLevels=colorlevels(error=0.10,warning=0.40))
        else:
            self._listpad.addstr(self._fixColumn('', self._colwidths[6]), clr)

    def _drawSignalStrength(self, node, drawSelected):
        clr = self._getListItemColor(drawSelected)
        self._listpad.addstr(self._fixColumn('', self._colwidths[7]), clr)
        
    def _drawDeviceNodeLine(self, node, drawSelected):
        clr = self._getListItemColor(drawSelected)
        self._listpad.addstr(' ', clr)
        self._listpad.addstr(self._fixColumn(node.id, self._colwidths[1]), clr)
        self._listpad.addstr(self._fixColumn(node.name, self._colwidths[2]), clr)
        self._listpad.addstr(self._fixColumn(node.location, self._colwidths[3]), clr)
        self._listpad.addstr(self._fixColumn(node.productType, self._colwidths[4]), clr)
        self._drawNodeStatus(node, drawSelected)
        self._drawBatteryStatus(node, drawSelected)
        self._drawSignalStrength(node, drawSelected)

    def _updateDeviceList(self):
        self._listcount = self._wrapper.nodeCount
        idx = 0
        for node in self._wrapper._nodes.itervalues():
            if idx == self._listindex:
                self._selectedNode = node
            self._listpad.move(idx,0)
            self._drawDeviceNodeLine(node, idx == self._listindex)
            idx += 1

        ctop = self._rowheights[0]
        listheight = self._rowheights[1]
        if self._listindex - self._listtop > listheight:
            self._listtop = self._listindex - listheight
        elif self._listindex < self._listtop:
            self._listtop = self._listindex
        self._screen.refresh()
        self._listpad.refresh(self._listtop, 0, ctop, 0, ctop + listheight, self._screensize[1] - 1)
        self._updateDialog()

    def _redrawDetailTab(self, pad):
        self._screen.refresh()
        pad.refresh(0, 0, self._detailtop, 0, self._detailbottom, self._screensize[1] - 1)

    def _updateDetail_Values(self, pad):
        # Draw column header
        clr = curses.color_pair(self.COLOR_HEADER_HI) | curses.A_BOLD
        pad.addstr(0,0,'{0:<{width}}'.format(' ', width=self._screensize[1]), clr)
        pad.move(0,1)
        for text, wid in zip(self._deviceValueColumns, self._deviceValueWidths):
            pad.addstr('{0:<{width}}'.format(text.title(), width=wid), clr)
        node = self._selectedNode
        if node and node.values:
            # Grab all items except for configuration values (they have their own tab)
            vset = list()
            for value in node.values.itervalues():
                if value.valueData:
                    vset.append(value)
            # Sort the resulting set: (1) command class, (2) instance, (3) index
            s = sorted(sorted(sorted(vset, key=lambda value: value.getValue('index')),
                              key=lambda value: value.getValue('instance')), key=lambda value: value.getValue('commandClass'))

            if self._detailpos[self._detailview] >= len(s): self._detailpos[self._detailview]=len(s)-1
            i = 0
            for value in s:
                vdic = value.valueData
                pad.move(i+1,0)
                # TODO: reset detail position on parent item change
                drawSelected = self._detailpos['Values'] == i
                clr = self._getListItemColor(drawSelected)
                pad.addstr(' ' * self._screensize[1], clr)
                pad.move(i+1,1)
                i += 1
                for key, wid in zip(self._deviceValueColumns, self._deviceValueWidths):
                    clr = self._getListItemColor(drawSelected)
                    text = value.getValue(key)
                    # strip 'COMMAND_CLASS_' prefix to save some space
                    if key == 'commandClass' and text.startswith('COMMAND_CLASS_'):
                        text = text[14:]

                    # TODO: value decorators (checkbox for Booleans, edit box for others)
                    # decimal: format to 2 places
                    # bool as checkbox
                    # byte as minibar if editable
                    # ints need to be directly edited...
                    # buttons... ?

                    # Draw editable items differently
                    if key == 'value' and not vdic['readOnly'] and drawSelected:
                        clr = curses.color_pair(self.COLOR_ERROR)
                    pad.addstr(self._fixColumn(text, wid), clr)

    def _updateDetail_Info(self, pad):
        node = self._selectedNode
        if node:
            #baudRate, basic, generic, specific, version, security
            self._deviceInfoColumns=['id','name','location','capabilities','neighbors','manufacturer','product','productType']
            if self._detailpos[self._detailview] >= len(self._deviceInfoColumns): self._detailpos[self._detailview]=len(self._deviceInfoColumns)-1
            editableColumns=['name','location','manufacturer','product']
            i = maxwid = 0
            for name in self._deviceInfoColumns: maxwid = len(name) if len(name) > maxwid else maxwid
            colwidth = maxwid + 2
            clr = self._getListItemColor(False)
            clr_rw = curses.color_pair(self.COLOR_ERROR)
            clr_ro = self._getListItemColor(True)
            clr_col = curses.color_pair(self.COLOR_OK)
            # TODO: If editable, should be textpad
            for column in self._deviceInfoColumns:
                val = str(getattr(node, column))
                pad.move(i + 1, 1)
                pad.addstr('{0:>{width}}'.format(column.title() + ':', width=colwidth), clr_col)
                selected = i == self._detailpos[self._detailview]
                thisclr = clr
                if selected: thisclr = clr_rw if column in editableColumns else clr_ro
                i += 1
                pad.addstr(' ')
                pad.addstr('{0:<{width}}'.format(val, width=30), thisclr)

    def _updateDetail_Classes(self, pad):
        clr = curses.color_pair(self.COLOR_HEADER_HI) | curses.A_BOLD
        pad.addstr(0,0,'{0:<{width}}'.format(' CommandClass', width=self._screensize[1]), clr)
        node = self._selectedNode
        if node:
            if self._detailpos[self._detailview] >= len(node.commandClasses): self._detailpos[self._detailview]=len(node.commandClasses)-1
            i = 0
            for cc in node.commandClasses:
                pad.addstr(i + 1, 0, ' {0:<{width}}'.format(self._wrapper.getCommandClassName(cc), width=30),
                           self._getListItemColor(i == self._detailpos[self._detailview]))
                i += 1

    def _updateDetail_Groups(self, pad):
        pad.addstr(3,3,'Group view not yet implemented')
        # groups tab:
        # index label               maxMembers members
        # 1     my group            4          1, 2, 4
        # Members column is editable - enter comma-separated list?

    def _updateDetail_Events(self, pad):
        pad.addstr(3,3,'Event view not yet implemented')
        # event detail tab:
        # timestamp  commandClass  notificationType 

    def _updateDeviceDetail(self):
        # TODO: detail needs to be scrollable, but to accomplish that a couple of changes need to be made.  First, the detail header band needs to be moved into a static shared section (above the detail pad); second, a new dict of 'top' positions needs to be created; finally, positioning code needs to be written to correctly offset the pad.
        pad = self._detailpads[self._detailview]
        pad.clear()
        if self._detailpos[self._detailview] < 0: self._detailpos[self._detailview]=0

        funcname = '_updateDetail_{0}'.format(self._detailview)
        try:
            method = getattr(self, funcname)
            method(pad)
        except AttributeError as ex:
            msg = 'No method named [%s] defined!' % funcname
            self._log.warn('_updateDeviceDetail: %s', msg)
            self._log.warn('_updateDeviceDetail Exception Details: %s', str(ex))
            self._alert(msg)

        self._redrawDetailTab(pad)

    def _updateMenu(self):
        menurow = self._screensize[0] - 1
        self._screen.addstr(menurow, 0, ' ' * (self._screensize[1] - 1), curses.color_pair(self.COLOR_HEADER_NORMAL))
        self._screen.move(menurow,4)
        for mnemonic, text in self._keys.iteritems():
            self._screen.addstr(' {0} '.format(mnemonic), curses.color_pair(self.COLOR_NORMAL) | curses.A_BOLD)
            self._screen.addstr('{0}'.format(text), curses.color_pair(self.COLOR_HEADER_NORMAL))

    def _redrawMenu(self):
        self._updateMenu()
        self._screen.refresh()

def main(stdscr):
    # TODO: prune log file
    commander = ZWaveCommander(stdscr)
    commander.main()
    
curses.wrapper(main)

class DeleteMe:
    '''
              1         2         3         4         5         6         7         8
     12345678901234567890123456789012345678901234567890123456789012345678901234567890
    +--------------------------------------------------------------------------------+
    | HomeSeer Z-Troller on /dev/keyspan-2                         Installer Library | 1
    | Home ID 0x003d8522                                         Version Z-Wave 2.78 | 2
    | 7 Registered Nodes (2 Sleeping)                                                | 3
    |                                                                                | 4
    | ID  Name          Location      Type                    State    Batt   Signal | 5
    | 1   Controller                  Remote Controller       OK                     | 6    |
    | 2   Sconce 1      Living Room   Multilevel Switch       [||||  ]        [||||] | 7    |
    |>3   TV            Living Room   Binary Power Switch     on              [||| ] | 8    |
    | 4   Liv Rm Motion Living Room   Motion Sensor           sleeping [||||] [||||] | 9    |
    | 5   Sliding Door  Family Room   Door/Window Sensor      ALARM    [||| ] [||  ] | 10   +- Scrollable box, lists nodes
    | 6   Sconce 2      Living Room   Multilevel Switch       [||||  ]        [||||] | 11   |
    | 7   Bedroom Lamp  Master Bed    Multilevel Scene Switch on                     | 12   |
    |                                                                                | 13   |
    |                                                                                | 14   |
    | Name:         TV                      | Command Classes                        | 15
    | Location:     Living Room             | COMMAND_CLASS_BASIC                    | 16   |
    | Manufacturer: Aeon Labs               | COMMAND_CLASS_HAIL                     | 17   |
    | Product:      Smart Energy Switch     | COMMAND_CLASS_ASSOCIATION              | 18   |
    | Neighbors:    2,4,5,6,7               | COMMAND_CLASS_VERSION                  | 19   |
    | Version:      3                       | COMMAND_CLASS_SWITCH_ALL               | 20   |
    | State:        On                      | COMMAND_CLASS_MANUFACTURER_SPECIFIC    | 21   +- Scrollable box, toggles:
    | Signal:       3dbA (good)             | COMMAND_CLASS_CONFIGURATION            | 22   |  1) command classes
    |                                       | COMMAND_CLASS_SENSOR_MULTILEVEL        | 23   |  2) values
    |                                       | COMMAND_CLASS_METER                    | 24   |  3) groups
    |        Add Del Edit Refresh + - oN oFf Values Groups Classes Setup Quit        | 25   |  4) config params
    +---------------------------------------+----------------------------------------+

    [a]add          - associate new node
    [b]about        - show about dialog
    [c]classes      - view command classes
    [d]delete       - remove association
    [e]edit         (COMMAND_CLASS_CONFIGURATION or has editable values)
    [f]off          (command_class_switch_binary,command_class_switch_multilevel,COMMAND_CLASS_SWITCH_TOGGLE_BINARY,COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL)
    [g]groups       (COMMAND_CLASS_ASSOCIATION)
    [n]on           (command_class_switch_binary,command_class_switch_multilevel,COMMAND_CLASS_SWITCH_TOGGLE_BINARY,COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL)
    [r]refresh      - refresh specified node
    [s]setup
    [+]increase     (COMMAND_CLASS_SWITCH_MULTILEVEL)
    [-]decrease     (COMMAND_CLASS_SWITCH_MULTILEVEL)


    '''
