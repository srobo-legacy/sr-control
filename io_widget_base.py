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

from rect_base import RectBase, BORDER_WIDTH

class IOWidgetBase(RectBase):

    def _get_markup(self, value):
        return '<span color="red">Dummy</span>'

    def set_value(self, value):
        """Set the value displayed by the IOWidgetBase."""
        self.value = value
        self._layout.set_markup(self._get_markup(value))

    def __init__(self, value):
        RectBase.__init__(self)
        self.set_value(value)

gobject.type_register(IOWidgetBase)
