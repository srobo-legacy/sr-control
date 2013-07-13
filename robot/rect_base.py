import pygtk
pygtk.require('2.0')
import gobject
import pango
from gtk import *

if pygtk_version < (2, 8):
    print "PyGtk 2.8 or later required"
    raise SystemExit

import cairo

DEFAULT_LINE_WIDTH = 5.0
BORDER_WIDTH = 5
_SELECTED_COLOR = gdk.Color(0.14453125, 0.20703125, 0.44140625)

class RectBase(Widget):

    ## Constructor ##

    def __init__(self):
        Widget.__init__(self)
        self._layout = self.create_pango_layout('')
        self._layout.set_font_description(pango.FontDescription("sans bold 10"))

    ## GtkWidget methods ##

    def do_realize(self):
        # Method responsible for creating GDK (windowing system) resources. In
        # this example we will create a new gdk.Window which we then draw on

        self.set_flags(REALIZED)

        # Create a new gdk.Window which we can draw on.
        self.window = gdk.Window(
            self.get_parent_window(),
            width=self.allocation.width,
            height=self.allocation.height,
            window_type=gdk.WINDOW_CHILD,
            wclass=gdk.INPUT_OUTPUT,
            event_mask=self.get_events() | gdk.EXPOSURE_MASK)
            # We want exposure events

        # Associate the gdk.Window with ourselves
        self.window.set_user_data(self)

        # Attach the style to the gdk.Window. A style contains colors and
        # GC contexts used for drawing
        self.style.attach(self.window)

        # The default background color should be what the style tells us
        self.style.set_background(self.window, STATE_NORMAL)
        self.window.move_resize(*self.allocation)

    def do_unrealize(self):
        # responsible for freeing the GDK resources
        # De-associate the window we created in do_realize with ourselves
        self.window.set_user_data(None)

    def do_size_request(self, requisition):
        # Request enough space for the text and a border
        width, height = self._layout.get_size()
        requisition.width = width // pango.SCALE + BORDER_WIDTH
        requisition.height = height // pango.SCALE + BORDER_WIDTH*2

    def do_size_allocate(self, allocation):
        # The do_size_allocate is called by when the actual size is known
        # and the widget is told how much space could actually be allocated

        self.allocation = allocation

        if self.flags() & REALIZED:
            self.window.move_resize(*allocation)

    def _draw_rectangle(self, cr, x, y, w, h, color,
            line_width = DEFAULT_LINE_WIDTH):
        cr.set_source_color(color)
        cr.rectangle(x, y, w, h)
        cr.fill_preserve()
        cr.set_line_width(line_width)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()

    def do_expose_event(self, event):
        # The do_expose_event is called when the widget is asked to draw itself

        x, y, w, h = self.allocation
        cr = self.window.cairo_create()

        self._draw(cr, w, h)

        fontw, fonth = self._layout.get_pixel_size()
        cr.move_to((w - fontw)/2, (h - fonth)/2)
        cr.update_layout(self._layout)
        cr.show_layout(self._layout)

gobject.type_register(RectBase)
