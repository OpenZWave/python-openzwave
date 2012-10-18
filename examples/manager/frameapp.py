# -* coding: utf-8 -*-

#Author: bibi21000
#Licence : GPL

__author__ = 'bibi21000'

from select import select
import sys
import os
import urwid
from urwid.raw_display import Screen
from traceback import format_exc
sys.path.insert(0, os.path.abspath('../build/tmp/usr/local/lib/python2.6/dist-packages'))
sys.path.insert(0, os.path.abspath('../build/tmp/usr/local/lib/python2.7/dist-packages'))
sys.path.insert(0, os.path.abspath('build/tmp/usr/local/lib/python2.6/dist-packages'))
sys.path.insert(0, os.path.abspath('build/tmp/usr/local/lib/python2.7/dist-packages'))
import logging

DIVIDER = urwid.Divider("-")

class TabManager(list):
    """
    Provide a circular list
    """

    def __init__(self, sequence):
        list.__init__(self, sequence)
        self.i = 0

    def set_index(self, i):
        """
        """
        if i not in range(len(self)):
            raise IndexError, 'Can\'t set index out of range'
        else:
            self.i = i

    def set_current(self, val):
        """
        """
        if val not in (self):
            raise IndexError, 'Can\'t set current out of range'
        else:
            self.i = self.index(val)

    def next(self, n=1):
        """
        """
        if self == []:
            return None
        if n < 0:
            return self.prev(abs(n))
        if self.i not in range(len(self)):
            self.i = len(self) - 1
        if self.i + n >= len(self):
            i = self.i
            self.set_index(0)
            return self.next(n - len(self) + i)
        else:
            self.set_index(self.i + n)
            return self[self.i]

    def prev(self, n=1):
        """
        """
        if self == []:
            return None
        if n < 0:
            return self.next(abs(n))
        if self.i not in range(len(self)):
            self.i = len(self) - 1
        if self.i - n < 0:
            i = self.i
            self.set_index(len(self) - 1)
            return self.prev(n - i - 1)
        else:
            self.i -= n
            return self[self.i]

class FrameApp(urwid.BoxWidget):
    def __init__(self, body, command=(None,0), value=(None,0), result=(None,0), \
            header=None, footer=None, log=None,
            status_bar=False, menu_f=False, focus_part='body'):
        """
        body -- a box widget for the body of the frame
        command,cols -- a box ? or flow ? widget for the body of the frame
        value,cols -- a box ? or flow ? widget for the body of the frame
        result,cols -- a box ? or flow ? widget for the body of the frame
        header -- a flow widget for above the body (or None)
        footer -- a flow widget for below the body (or None)
        log -- a log factory or None
        status_bar : A status bar to display messages
        menu_f : Function keys menu
        focus_part -- 'header', 'footer' or 'body'
        """
        self.__super.__init__()

        self.tabs = TabManager(['header', 'body', 'command', 'value', 'result', 'footer'])
        self._header = header
        self._body = body
        self.log = log
        self._status_bar_enable = status_bar
        self._status_bar = None
        self._status_bar_msg = "> %s"
        self._menu_f_enable = menu_f
        self._menu_f = None
        self._command, self._command_width = command
        self._value, self._value_width = value
        self._result, self._result_width = result
        self._footer = self.create_footer(footer)
        self._columns_invalid = True
        self._columns_pile = None
        self._columns = self.get_columns()
#        self._columns = urwid.Pile([
#            DIVIDER,
#            urwid.Columns([
#                ('weight', 1, urwid.AttrWrap(self._command, 'reverse')),
#                #('fixed', 1, urwid.Divider("|")),
#                ('weight', 4, urwid.AttrWrap(self._result, 'reverse'))
#            ], dividechars=2, min_width=8),
#            ])
#        self._columns = urwid.Columns([
#                ('weight', 1, self._command),
#                #('weight', 1, urwid.AttrWrap(self._command, 'reverse')),
#                #('fixed', 1, urwid.Divider("|")),
#                #('weight', 4,urwid.AttrWrap(self._result, 'reverse'))
#                ('weight', 4, self._result)
#            ], dividechars=2, min_width=8)

        #part = self.tabs.next()
        #while (not self.is_tab_selectable(focus_part)) :
        #    focus_part = self.tabs.next()
        #self.set_focus(part)
        self.tabs.set_current(focus_part)
        self.focus_part = focus_part

    def get_columns(self):
        if not self._columns_invalid :
            return self._columns
        cols = []
        if self._command != None:
            cols.append(('weight', self._command_width, urwid.AttrWrap(self._command, 'reverse', 'focus')))
            if self._value != None:
                cols.append(('weight', self._value_width, urwid.AttrWrap(self._value, 'reverse', 'focus')))
            if self._result != None:
                cols.append(('weight', self._result_width, urwid.AttrWrap(self._result, 'reverse')))
            self._columns_invalid = False
        if len(cols) == 0:
            self._columns = None
            return self._columns
        self._columns = urwid.Columns(cols, dividechars=2, min_width=8)
        return self._columns
    columns = property(get_columns)

    def get_columns_pile(self):
        cols = self.columns
        self._columns_pile = urwid.Pile([
            DIVIDER,
            cols,
            ])
        return self._columns_pile
    columns_pile = property(get_columns_pile)

    def get_header(self):
        return self._header
    def set_header(self, header):
        self._header = header
        self._invalidate()
    header = property(get_header, set_header)

    def get_body(self):
        return self._body
    def set_body(self, body):
        self._body = body
        self._invalidate()
    body = property(get_body, set_body)

    def get_command(self):
        return self._command
    def set_command(self, command):
        self._command = command
        self._columns_invalid = True
        self._invalidate()
    command = property(get_command, set_command)

    def get_value(self):
        return self._value
    def set_value(self, value):
        self._value = value
        self._columns_invalid = True
        self._invalidate()
    value = property(get_value, set_value)

    def get_result(self):
        return self._result
    def set_result(self, result):
        self._result = result
        self._columns_invalid = True
        self._invalidate()
    result = property(get_result, set_result)

    def set_menu_f(self, f1=None, f2=None, f3=None, f4=None, f5=None, f6=None,
            f7=None, f8=None, f9=None, f10=None, f11=None, f12=None):
        if self._menu_f_enable :
            if f1 != None :
                self._menu_f.widget_list[0].set_text('1%s' % f1)
            if f2 != None :
                self._menu_f.widget_list[1].set_text('2%s' % f2)
            if f3 != None :
                self._menu_f.widget_list[2].set_text('3%s' % f3)
            if f4 != None :
                self._menu_f.widget_list[3].set_text('4%s' % f4)
            if f5 != None :
                self._menu_f.widget_list[4].set_text('5%s' % f5)
            if f6 != None :
                self._menu_f.widget_list[5].set_text('6%s' % f6)
            if f7 != None :
                self._menu_f.widget_list[6].set_text('7%s' % f7)
            if f8 != None :
                self._menu_f.widget_list[7].set_text('8%s' % f8)
            if f9 != None :
                self._menu_f.widget_list[8].set_text('9%s' % f9)
            if f10 != None :
                self._menu_f.widget_list[9].set_text('10%s' % f10)
            if f11 != None :
                self._menu_f.widget_list[10].set_text('11%s' % f11)
            if f12 != None :
                self._menu_f.widget_list[11].set_text('12%s' % f12)

    def set_status_bar(self, msg=None):
        if self._status_bar_enable :
            if msg != None :
                self._status_bar.set_text('> %s' % msg)

    def create_footer(self, footer):
        newfooter = []
        if self._menu_f_enable :
            self._menu_f = urwid.Columns([
                #urwid.AttrWrap(urwid.Text('F:', wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('1%s' % "", wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('2%s' % "", wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('3%s' % "", wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('4%s' % "", wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('5%s' % "", wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('6%s' % "", wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('7%s' % "", wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('8%s' % "", wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('9%s' % "", wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('10%s' % "", wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('11%s' % "", wrap='clip'), 'menu'),
                urwid.AttrWrap(urwid.Text('12%s' % "", wrap='clip'), 'menu'),
            ], dividechars=1)
            newfooter.append(DIVIDER)
            newfooter.append(self._menu_f)
        if self._status_bar_enable :
            self._status_bar = urwid.Text(self._status_bar_msg % "")
            newfooter.append(DIVIDER)
            newfooter.append(self._status_bar)
        if footer != None :
            newfooter.append(footer)
        if len(newfooter) == 0:
            return None
        return urwid.Pile(newfooter)

    def get_footer(self):
        return self._footer
    def set_footer(self, footer):
        self._footer = self.create_footer(footer)
        self._invalidate()
    footer = property(get_footer, set_footer)

    def set_columns_focus(self, part):
        """Set the part of the frame that is in focus.

        part -- 'header', 'footer' or 'body'
        """
        if part == 'command':
            self.columns.set_focus_column(0)
        elif part == 'result':
            self.columns.set_focus_column(len(self.columns.widget_list)-1)
        else:
            self.columns.set_focus_column(1)

    def set_focus(self, part):
        """Set the part of the frame that is in focus.

        part -- 'header', 'footer' or 'body'
        """
        assert part in ('header', 'footer', 'command', 'result', 'value', 'body')
        if part in ('command', 'result', 'value'):
            self.set_columns_focus(part)
        self.focus_part = part
        self.tabs.set_current(part)
        self._invalidate()

    def is_tab_selectable(self, part):
        """
        Test if the focus exists and is selectable

        part -- 'header', 'footer' or 'body'
        """
        assert part in ('header', 'footer', 'command', 'result', 'value', 'body')
        if part == 'body':
            #Body is allways selectable
            return True
        elif part == 'header' and self.header != None and self.header.selectable():
            return True
        elif part == 'footer' and self.footer != None and self.footer.selectable():
            return True
        elif part == 'command' and self._command != None and self._command.selectable():
            return True
        elif part == 'value' and self._value != None and self._value.selectable():
            return True
        elif part == 'result' and self._result != None and self._result.selectable():
            return True
        return False

    def get_focus (self):
        """Return the part of the frame that is in focus.

        Will be one of 'header', 'footer' or 'body'.
        """
        return self.focus_part

    def frame_top_bottom(self, size, focus):
        """Calculate the number of rows for the header and footer.

        Returns (head rows, command rows, foot rows),(orig head, orig command, orig foot).
        orig head/command/foot are from rows() calls.
        """
        (maxcol, maxrow) = size
        frows = hrows = crows = 0

        if self.header:
            hrows = self.header.rows((maxcol,),
                self.focus_part=='header' and focus)

        if self.footer:
            frows = self.footer.rows((maxcol,),
                self.focus_part=='footer' and focus)

        if self._command:
            crows = self.columns_pile.rows((maxcol,),
                self.focus_part=='command' and focus)

#        if self._result:
#            crows = self.columns_pile.rows((maxcol,),
#                self.focus_part=='result' and focus)

#        if self._value:
#            crows = self.columns_pile.rows((maxcol,),
#                self.focus_part=='value' and focus)

        remaining = maxrow

        if self.focus_part == 'footer':
            if frows >= maxrow:
                return (0, 0, remaining),(hrows, crows, frows)

            remaining -= frows
            if hrows >= remaining:
                return (remaining, 0, frows),(hrows, crows, frows)

            remaining -= hrows
            if crows >= remaining:
                return (hrows, remaining, frows),(hrows, crows, frows)

        elif self.focus_part == 'header':
            if hrows >= maxrow:
                return (remaining, 0, 0),(hrows, crows, frows)

            remaining -= hrows
            if frows >= remaining:
                return (hrows, 0, remaining),(hrows, crows, frows)

            remaining -= frows
            if crows >= remaining:
                return (hrows, remaining, frows),(hrows, crows, frows)

        elif self.focus_part == 'command' \
                or self.focus_part == 'value' \
                or self.focus_part == 'result' :
            if crows >= maxrow:
                return (0, remaining, 0),(hrows, crows, frows)

            remaining -= crows
            if frows >= remaining:
                return (0, crows, remaining),(hrows, crows, frows)

            remaining -= frows
            if hrows >= remaining:
                return (remaining, crows, frows),(hrows, crows, frows)

        elif hrows + frows + crows >= remaining:
            # self.focus_part == 'body'
            rless1 = max(0, remaining-1)
            if frows >= remaining-1:
                return (0, 0, rless1),(hrows, crows, frows)

            remaining -= frows
            if hrows >= remaining-1:
                rless1 = max(0, remaining-1)
                return (rless1, 0, frows),(hrows, crows, frows)

            remaining -= hrows
            rless1 = max(0, remaining-1)
            return (hrows, rless1, frows),(hrows, crows, frows)

        return (hrows, crows, frows),(hrows, crows, frows)


    def render(self, size, focus=False):
        """
        Render frame and return it.
        """
        (maxcol, maxrow) = size
        (htrim, ctrim, ftrim),(hrows, crows, frows) = self.frame_top_bottom(
            (maxcol, maxrow), focus)

        combinelist = []
        depends_on = []

        head = None
        if htrim and htrim < hrows:
            head = urwid.Filler(self.header, 'top').render(
                (maxcol, htrim),
                focus and self.focus_part == 'header')
        elif htrim:
            head = self.header.render((maxcol,),
                focus and self.focus_part == 'header')
            assert head.rows() == hrows, "rows, render mismatch"
        if head:
            combinelist.append((head, 'header',
                self.focus_part == 'header'))
            depends_on.append(self.header)

        if ftrim+htrim+ctrim < maxrow:
            body = self.body.render((maxcol, maxrow-ftrim-htrim-ctrim),
                focus and self.focus_part == 'body')
            combinelist.append((body, 'body',
                self.focus_part == 'body'))
            depends_on.append(self.body)

        columns = None
        if ctrim and ctrim < crows:
            if self.focus_part == 'value' :
                columns = urwid.Filler(self.columns_pile, 'columns').render(
                    (maxcol, ftrim),
                    #TODO Changeit it to return command or result
                    focus and self.focus_part == 'value')
                self.log.debug("render in value %s" % (self.focus_part == 'value'))
            elif self.focus_part == 'result' :
                columns = urwid.Filler(self.columns_pile, 'columns').render(
                    (maxcol, ftrim),
                    #TODO Changeit it to return command or result
                    focus and self.focus_part == 'result')
                self.log.debug("render in result %s" % (self.focus_part == 'result'))
            else :
                columns = urwid.Filler(self.columns_pile, 'columns').render(
                    (maxcol, ftrim),
                    #TODO Changeit it to return command or result
                    focus and self.focus_part == 'command')
                self.log.debug("render in command %s" % (self.focus_part == 'command' ))
        elif ctrim:
            if self.focus_part == 'value' :
                columns = self.columns_pile.render((maxcol,),
                    focus and self.focus_part == 'value' )
                self.log.debug("render in value %s" % (self.focus_part == 'value'))
            elif self.focus_part == 'result' :
                columns = self.columns_pile.render((maxcol,),
                    focus and self.focus_part == 'result' )
                self.log.debug("render in result %s" % (self.focus_part == 'result'))
            else :
                columns = self.columns_pile.render((maxcol,),
                    focus and self.focus_part == 'command' )
                self.log.debug("render in command %s" % (self.focus_part == 'command'))
            assert columns.rows() == crows, "rows, render mismatch"
        if columns:
            newfocus="%s" % self.focus_part
            combinelist.append((columns, 'columns',
                self.focus_part == "command" or self.focus_part == "value" \
                    or self.focus_part == "result"))
            depends_on.append(self.columns_pile)

        foot = None
        if ftrim and ftrim < frows:
            foot = urwid.Filler(self.footer, 'bottom').render(
                (maxcol, ftrim),
                focus and self.focus_part == 'footer')
        elif ftrim:
            foot = self.footer.render((maxcol,),
                focus and self.focus_part == 'footer')
            assert foot.rows() == frows, "rows, render mismatch"
        if foot:
            combinelist.append((foot, 'footer',
                self.focus_part == 'footer'))
            depends_on.append(self.footer)

        return urwid.CanvasCombine(combinelist)


    def key_tab(self, key):
        """
        Intercept the 'tab' and 'shift tab' keys.
        """
        handle = False
        if key == 'tab':
            part = self.tabs.next()
            while (not self.is_tab_selectable(part)) :
                part = self.tabs.next()
            self.set_focus(part)
            handle = True
            #self.parent.status_bar.update('tab')
        elif key == 'shift tab':
            part = self.tabs.prev()
            while (not self.is_tab_selectable(part)) :
                part = self.tabs.prev()
            self.set_focus(part)
            handle = True
            #self.parent.status_bar.update('shift tab')
        return handle

    def keypress(self, size, key):
        """
        Pass keypress to widget in focus.
        """
        if self.key_tab(key):
            return

        (maxcol, maxrow) = size

        if self.focus_part == 'header' and self.header is not None:
            if not self.header.selectable():
                return key
            return self.header.keypress((maxcol,),key)
        if self.focus_part == 'footer' and self.footer is not None:
            if not self.footer.selectable():
                return key
            return self.footer.keypress((maxcol,),key)
        if self.focus_part == 'command' and self._command is not None:
            if not self._command.selectable():
                return key
            return self._command.keypress((maxcol,),key)
        if self.focus_part == 'value' and self._value is not None:
            if not self._value.selectable():
                return key
            return self._value.keypress((maxcol,),key)
        if self.focus_part == 'result' and self._result is not None:
            if not self._result.selectable():
                return key
            return self._result.keypress((maxcol,),key)
        if self.focus_part != 'body':
            return key
        remaining = maxrow
        if self.header is not None:
            remaining -= self.header.rows((maxcol,))
        if self._command is not None:
            remaining -= self.columns_pile.rows((maxcol,))
        if self.footer is not None:
            remaining -= self.footer.rows((maxcol,))
        if remaining <= 0: return key

        if not self.body.selectable():
            return key
        return self.body.keypress( (maxcol, remaining), key )

    def mouse_event(self, size, event, button, col, row, focus):
        """
        Pass mouse event to appropriate part of frame.
        Focus may be changed on button 1 press.
        """
        (maxcol, maxrow) = size
        (htrim, ctrim, ftrim),(hrows, crows, frows) = self.frame_top_bottom(
            (maxcol, maxrow), focus)

        if row < htrim: # within header
            focus = focus and self.focus_part == 'header'
            if urwid.is_mouse_press(event) and button==1:
                if self.header.selectable():
                    self.set_focus('header')
            if not hasattr(self.header, 'mouse_event'):
                return False
            return self.header.mouse_event( (maxcol,), event,
                button, col, row, focus )

        if row >= maxrow-ftrim: # within footer
            focus = focus and self.focus_part == 'footer'
            if urwid.is_mouse_press(event) and button==1:
                if self.footer.selectable():
                    self.set_focus('footer')
            if not hasattr(self.footer, 'mouse_event'):
                return False
            return self.footer.mouse_event( (maxcol,), event,
                button, col, row-maxrow+frows, focus )

        if row >= maxrow-ftrim-ctrim: # within columns
        #TODO mangae values / result
            widths = self.columns.column_widths((maxcol, maxrow))
            focus = focus and (self.focus_part == 'command' or self.focus_part == 'value' or self.focus_part == 'result')
            if col <= widths[0]  :
                #we are in the command
                if urwid.is_mouse_press(event) and button==1:
                    if self._command.selectable():
                        self.set_focus('command')
                if not hasattr(self._command, 'mouse_event'):
                    return False
                return self._command.mouse_event( (maxcol,), event,
                button, col, row-maxrow+frows+crows-1, focus )
            if len(widths) == 3 :
                last=2
            else :
                last=1
            if col >= maxcol - widths[last]  :
                #we are in the result
                if urwid.is_mouse_press(event) and button==1:
                    if  self._result != None and self._result.selectable():
                        self.set_focus('result')
                if not hasattr(self._result, 'mouse_event'):
                    return False
                return self._result.mouse_event( (maxcol,), event,
                button, col-maxcol+widths[last], row-maxrow+frows+crows-1, focus )
            #we are in the value
            if urwid.is_mouse_press(event) and button==1:
                if self._value != None and self._value.selectable():
                    self.set_focus('value')
            if not hasattr(self._value, 'mouse_event'):
                return False
            return self._value.mouse_event( (maxcol,), event,
            button, col-maxcol+widths[1]+widths[2], row-maxrow+frows+crows-1, focus )

        # within body
        focus = focus and self.focus_part == 'body'
        if urwid.is_mouse_press(event) and button==1:
            if self.body.selectable():
                self.set_focus('body')

        if not hasattr(self.body, 'mouse_event'):
            return False
        return self.body.mouse_event( (maxcol, maxrow-htrim-ftrim),
            event, button, col, row-htrim, focus )

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
