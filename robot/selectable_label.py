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

from rect_base import RectBase, BORDER_WIDTH

_SELECTED_COLOR = gdk.Color(0.14453125, 0.20703125, 0.44140625)

class SelectableLabel(RectBase):

    last_state = None

    def _update_markup(self):
        if self.state == STATE_SELECTED:
            self._layout.set_markup('<span color="white">%s</span>'
                                    % self.text)
        else:
            self._layout.set_markup('<span color="black">%s</span>'
                                    % self.text)

        self.last_state = self.state

    def set_text(self, text):
        self.text = text
        self._update_markup()
        self.queue_draw()

    def __init__(self, text):
        RectBase.__init__(self)
        self.set_text(text)

    def _draw(self, cr, w, h):
        if self.state == STATE_SELECTED:
            # Draw a background rectangle
            self._draw_rectangle(cr, BORDER_WIDTH, BORDER_WIDTH,
                                 w - 2*BORDER_WIDTH, h - 2*BORDER_WIDTH,
                                 _SELECTED_COLOR)

        # draw the value in the centre of the control
        if self.state <> self.last_state:
            self._update_markup()
            self.last_state = self.state


gobject.type_register(SelectableLabel)
