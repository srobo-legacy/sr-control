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

    def _draw_rectangle(self, cr, w, h):
        if self.value == 1:
            # Draw a filled rounded rectangle
            cr.set_source_color(_INPUT_ON_COLOR)
            cr.rectangle(_BORDER_WIDTH, _BORDER_WIDTH,
                         w - 2*_BORDER_WIDTH, h - 2*_BORDER_WIDTH)
            cr.fill_preserve()
            cr.set_line_width(5.0)
            cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.stroke()

gobject.type_register(DigitalInput)

def _main(args):
    win = Window()
    win.set_border_width(5)
    win.set_title('Widget test')
    win.connect('delete-event', main_quit)

    t = Table(1, 2, True)

    w = DigitalInput(1)
    t.attach(w, 0, 1, 0, 1)
    x = DigitalInput(0)
    t.attach(x, 0, 1, 1, 2)
    win.add(t)

    win.show_all()

    main()

if __name__ == '__main__':
    sys.exit(_main(sys.argv))
