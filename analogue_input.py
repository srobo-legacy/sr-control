# Copied from the tutorial at http://git.gnome.org/browse/pygtk/plain/examples/gtk/widget.py

import sys

import pygtk
pygtk.require('2.0')
import gobject
import pango
from gtk import *

if pygtk_version < (2, 8):
    print "PyGtk 2.8 or later required"
    raise SystemExit

try:
    import cairo
except ImportError:
    raise SystemExit("cairo required")

from io_widget_base import IOWidgetBase

_BORDER_WIDTH = 2  # Excludes line width
_INPUT_OFF_COLOR = gdk.Color(1.0, 1.0, 1.0)  # Must be .0
_INPUT_ON_COLOR = gdk.Color(0.14453125, 0.20703125, 0.44140625)
_DEFAULT_LINE_WIDTH = 5.0
# TODO: Put color in some common location

_MAX_INPUT_VOLTAGE = 3.3

class AnalogueInput(IOWidgetBase):

    def __init__(self, value):
        IOWidgetBase.__init__(self, value)

    ## Internal Methods ##

    def _get_markup(self, value):
        if value > _MAX_INPUT_VOLTAGE / 2:
            return str.format('<span color="white">{:.1f}</span>', self.value)
        else:
            return str.format('<span color="black">{:.1f}</span>', self.value)

    def _draw_rectangle(self, cr, w, h):
        if self.value > 0:
            inner_height = h - 2 * _BORDER_WIDTH
            top = (1 - self.value / _MAX_INPUT_VOLTAGE) * inner_height
            line_width = min(_DEFAULT_LINE_WIDTH, inner_height - top)
            padding = line_width / 2

            # Draw the background rectangle
            cr.set_source_color(_INPUT_OFF_COLOR)
            cr.rectangle(_BORDER_WIDTH + padding,
                         _BORDER_WIDTH + padding,
                         w - 2*(_BORDER_WIDTH + padding),
                         h - 2*(_BORDER_WIDTH + padding))
            cr.fill_preserve()
            cr.set_line_width(_DEFAULT_LINE_WIDTH)
            cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.stroke()

            # Draw a filled rounded rectangle
            cr.rectangle(_BORDER_WIDTH + padding,
                         top + _BORDER_WIDTH + padding,
                         w - 2 * (_BORDER_WIDTH + padding),
                         h - 2 * (_BORDER_WIDTH + padding) - top)

            cr.set_source_color(_INPUT_ON_COLOR)
            cr.fill_preserve()
            cr.set_line_width(line_width)
            #cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.stroke()

        else:
            # Just draw the background rectangle
            padding = _DEFAULT_LINE_WIDTH / 2

            cr.set_source_color(_INPUT_OFF_COLOR)
            cr.rectangle(_BORDER_WIDTH + padding,
                         _BORDER_WIDTH + padding,
                         w - 2*(_BORDER_WIDTH + padding),
                         h - 2*(_BORDER_WIDTH + padding))
            cr.fill_preserve()
            cr.set_line_width(_DEFAULT_LINE_WIDTH)
            cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.stroke()

gobject.type_register(AnalogueInput)
