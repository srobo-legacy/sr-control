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

_BORDER_WIDTH = 5
_INPUT_OFF_COLOR = gdk.Color(1.0, 1.0, 1.0)  # Must be .0
_INPUT_ON_COLOR = gdk.Color(0.14453125, 0.20703125, 0.44140625)

class DigitalInput(IOWidgetBase):

    def __init__(self, value):
        IOWidgetBase.__init__(self, value)

    ## Internal Methods ##

    def _get_markup(self, value):
        if value == 1:
            return '<span color="white">1</span>'
        else:
            return '<span color="black">0</span>'

    def _draw(self, cr, w, h):
        # Draw a filled rounded rectangle
        if self.value == 1:
            color = _INPUT_ON_COLOR
        else:
            color = _INPUT_OFF_COLOR

        self._draw_rectangle(cr, _BORDER_WIDTH, _BORDER_WIDTH,
                     w - 2*_BORDER_WIDTH, h - 2*_BORDER_WIDTH, color)

gobject.type_register(DigitalInput)
