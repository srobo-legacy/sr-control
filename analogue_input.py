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

from io_widget_base import IOWidgetBase, DEFAULT_LINE_WIDTH

_BORDER_WIDTH = 2  # Excludes line width
_INPUT_OFF_COLOR = gdk.Color(1.0, 1.0, 1.0)  # Must be .0
_INPUT_ON_COLOR = gdk.Color(0.14453125, 0.20703125, 0.44140625)
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

    def _draw(self, cr, w, h):
        if self.value > 0:
            inner_height = h - 2 * _BORDER_WIDTH
            top = (1 - self.value / _MAX_INPUT_VOLTAGE) * inner_height
            line_width = min(DEFAULT_LINE_WIDTH, inner_height - top)
            padding = line_width / 2

            # Draw the background rectangle
            self._draw_rectangle(cr,
                                 _BORDER_WIDTH + padding,
                                 _BORDER_WIDTH + padding,
                                 w - 2*(_BORDER_WIDTH + padding),
                                 h - 2*(_BORDER_WIDTH + padding),
                                 _INPUT_OFF_COLOR)

            # Draw a filled rounded rectangle
            self._draw_rectangle(cr,
                         _BORDER_WIDTH + padding,
                         top + _BORDER_WIDTH + padding,
                         w - 2 * (_BORDER_WIDTH + padding),
                         h - 2 * (_BORDER_WIDTH + padding) - top,
                         _INPUT_ON_COLOR,
                         line_width = line_width)

        else:
            # Just draw the background rectangle
            padding = DEFAULT_LINE_WIDTH / 2

            self._draw_rectangle(cr,
                                 _BORDER_WIDTH + padding,
                                 _BORDER_WIDTH + padding,
                                 w - 2*(_BORDER_WIDTH + padding),
                                 h - 2*(_BORDER_WIDTH + padding),
                                 _INPUT_OFF_COLOR)

gobject.type_register(AnalogueInput)
