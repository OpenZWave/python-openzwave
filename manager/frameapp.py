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

class FrameApp(urwid.BoxWidget):
    def __init__(self, body, command=None, value=None, result=None, \
            header=None, footer=None, log=None, focus_part='body'):
        """
        body -- a box widget for the body of the frame
        command -- a box ? or flow ? widget for the body of the frame
        value -- a box ? or flow ? widget for the body of the frame
        header -- a flow widget for above the body (or None)
        footer -- a flow widget for below the body (or None)
        focus_part -- 'header', 'footer' or 'body'
        """
        self.__super.__init__()

        self._header = header
        self._body = body
        self.log = log
        self._command = command
        self._value = value
        self._result = result
        self._footer = footer
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

        self.focus_part = focus_part

    def get_columns(self):
        cols = []
        if self._command != None:
            cols.append(('weight', 1, urwid.AttrWrap(self._command, 'reverse', 'focus')))
            if self._value != None:
                cols.append(('weight', 1, urwid.AttrWrap(self._value, 'reverse', 'focus')))
            if self._result != None:
                cols.append(('weight', 3, urwid.AttrWrap(self._result, 'reverse', 'focus')))
        if len(cols) == 0:
            return None
        ret = urwid.Pile([
            DIVIDER,
            urwid.Columns(cols, dividechars=2, min_width=8),
            ])
        return ret

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
        self._invalidate()
    command = property(get_command, set_command)

    def get_value(self):
        return self._value
    def set_value(self, value):
        self._value = value
        self._invalidate()
    value = property(get_value, set_value)

    def get_result(self):
        return self._result
    def set_result(self, result):
        self._result = result
        self._invalidate()
    result = property(get_result, set_result)

    def get_footer(self):
        return self._footer
    def set_footer(self, footer):
        self._footer = footer
        self._invalidate()
    footer = property(get_footer, set_footer)

    def set_focus(self, part):
        """Set the part of the frame that is in focus.

        part -- 'header', 'footer' or 'body'
        """
        assert part in ('header', 'footer', 'command', 'result', 'value', 'body')
        self.focus_part = part
        self._invalidate()

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

        if self.command:
            crows = self._columns.rows((maxcol,),
                self.focus_part=='command' and focus)

#        if self.result:
#            crows = self._columns.rows((maxcol,),
#                self.focus_part=='result' and focus)

#        if self.value:
#            crows = self._columns.rows((maxcol,),
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
                columns = urwid.Filler(self._columns, 'columns').render(
                    (maxcol, ftrim),
                    #TODO Changeit it to return command or result
                    focus and self.focus_part == 'value')
                self.log.debug("render in value %s" % (self.focus_part == 'value'))
            elif self.focus_part == 'result' :
                columns = urwid.Filler(self._columns, 'columns').render(
                    (maxcol, ftrim),
                    #TODO Changeit it to return command or result
                    focus and self.focus_part == 'result')
                self.log.debug("render in result %s" % (self.focus_part == 'result'))
            else :
                columns = urwid.Filler(self._columns, 'columns').render(
                    (maxcol, ftrim),
                    #TODO Changeit it to return command or result
                    focus and self.focus_part == 'command')
                self.log.debug("render in command %s" % (self.focus_part == 'command' ))
        elif ctrim:
            if self.focus_part == 'value' :
                columns = self._columns.render((maxcol,),
                    focus and self.focus_part == 'value' )
                self.log.debug("render in value %s" % (self.focus_part == 'value'))
            elif self.focus_part == 'result' :
                columns = self._columns.render((maxcol,),
                    focus and self.focus_part == 'result' )
                self.log.debug("render in result %s" % (self.focus_part == 'result'))
            else :
                columns = self._columns.render((maxcol,),
                    focus and self.focus_part == 'command' )
                self.log.debug("render in command %s" % (self.focus_part == 'command'))
            assert columns.rows() == crows, "rows, render mismatch"
        if columns:
            newfocus="%s" % self.focus_part
            combinelist.append((columns, 'columns',
                self.focus_part == "command" or self.focus_part == "value" \
                    or self.focus_part == "result"))
            depends_on.append(self._columns)

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


    def key_tab(self, key, current_focus):
        """
        Intercept the 'tab' and 'shift tab' keys.
        """
        handle = False
        if key == 'tab':
            if current_focus == 'body' :
                if self._columns == None :
                    #We must setfocus to the column widget
                    self._columns.set_focus()
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

    def keypress(self, size, key):
        """
        Pass keypress to widget in focus.
        """
        (maxcol, maxrow) = size

        if self.focus_part == 'header' and self.header is not None:
            if not self.header.selectable():
                return key
            return self.header.keypress((maxcol,),key)
        if self.focus_part == 'footer' and self.footer is not None:
            if not self.footer.selectable():
                return key
            return self.footer.keypress((maxcol,),key)
        if self.focus_part == 'command' and self.command is not None:
            if not self.command.selectable():
                return key
            return self.command.keypress((maxcol,),key)
        if self.focus_part == 'value' and self.value is not None:
            if not self.value.selectable():
                return key
            return self.value.keypress((maxcol,),key)
        if self.focus_part == 'result' and self.result is not None:
            if not self.result.selectable():
                return key
            return self.result.keypress((maxcol,),key)
        if self.focus_part != 'body':
            return key
        remaining = maxrow
        if self.header is not None:
            remaining -= self.header.rows((maxcol,))
        if self.command is not None:
            remaining -= self._columns.rows((maxcol,))
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
            widths = self._columns.widget_list[1].column_widths((maxcol, maxrow))
            focus = focus and (self.focus_part == 'command' or self.focus_part == 'value' or self.focus_part == 'result')
            if col <= widths[0]  :
                #we are in the command
                if urwid.is_mouse_press(event) and button==1:
                    if self.command.selectable():
                        self.set_focus('command')
                if not hasattr(self.command, 'mouse_event'):
                    return False
                return self.command.mouse_event( (maxcol,), event,
                button, col, row-maxrow+frows+crows-1, focus )
            if len(widths) == 3 :
                last=2
            else :
                last=1
            if col >= maxcol - widths[last]  :
                #we are in the result
                if urwid.is_mouse_press(event) and button==1:
                    if  self.result != None and self.result.selectable():
                        self.set_focus('result')
                if not hasattr(self.result, 'mouse_event'):
                    return False
                return self.result.mouse_event( (maxcol,), event,
                button, col-maxcol+widths[last], row-maxrow+frows+crows-1, focus )
            #we are in the value
            if urwid.is_mouse_press(event) and button==1:
                if self.value != None and self.value.selectable():
                    self.set_focus('value')
            if not hasattr(self.value, 'mouse_event'):
                return False
            return self.value.mouse_event( (maxcol,), event,
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
