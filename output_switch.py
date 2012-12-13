import sys

import pygtk
#pygtk.require('2,0')
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
_ARROW_HEIGHT = 6
_ARROW_BORDER = 5
_INPUT_ON_COLOR = gdk.Color(0.14453125, 0.20703125, 0.44140625)
_INPUT_OFF_COLOR = gdk.Color(1.0, 1.0, 1.0)

class OutputSwitch(IOWidgetBase):

    def __init__(self, value):
        IOWidgetBase.__init__(self, value)

    def _get_markup(self, value):
        if value == 1:
            return '<span color="white">1</span>'
        else:
            return '<span color="black">0</span>'

    def _draw_rectangle(self, cr, w, h):
        if self.state == STATE_SELECTED:
            # Draw the arrows
            cr.set_source_rgb(0, 0, 0)
            cr.move_to(w / 2, 0)
            cr.line_to(w / 2 + _ARROW_HEIGHT, _ARROW_HEIGHT)
            cr.line_to(w / 2 - _ARROW_HEIGHT, _ARROW_HEIGHT)
            cr.close_path()
            cr.fill()

            cr.move_to(w / 2, h)
            cr.line_to(w / 2 + _ARROW_HEIGHT, h - _ARROW_HEIGHT)
            cr.line_to(w / 2 - _ARROW_HEIGHT, h - _ARROW_HEIGHT)
            cr.close_path()
            cr.fill()

        # Set the rectangle color
        if self.value == 1:
            cr.set_source_color(_INPUT_ON_COLOR)
        else:
            cr.set_source_color(_INPUT_OFF_COLOR)

        # Draw the rectangle
        cr.rectangle(_BORDER_WIDTH, _BORDER_WIDTH + _ARROW_BORDER,
                     w - 2*_BORDER_WIDTH, h - 2*(_BORDER_WIDTH + _ARROW_BORDER))
        cr.fill_preserve()
        cr.set_line_width(5.0)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()

gobject.type_register(IOWidgetBase)
