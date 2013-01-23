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

import math


_NEEDLE_COLOR = gdk.Color(0.0, 0.0, 0.0)

_background_pixbuf = gdk.pixbuf_new_from_file('dial-background-trimmed.png')
_MIN_WIDTH = 272
_MIN_HEIGHT = 272
_ANGLE_MIN = math.pi / 4
_ANGLE_MAX = 7 * math.pi / 4

class Dial(Widget):

    ## Data ##

    adjustment = None
    angle = _ANGLE_MIN

    def recalculate_angle(self):
        adj = self.adjustment
        scale = (_ANGLE_MAX - _ANGLE_MIN) / (adj.upper - adj.lower)
        self.angle = _ANGLE_MIN + (adj.value - adj.lower) * scale
        self.queue_draw()

    def set_adjustment(self, adj):
        self.adjustment = adj
        self.recalculate_angle()

    def get_adjustment(self):
        return self.adjustment

    def set_value(self, value):
        self.adjustment.value = value

        # Change the label
        self._layout.set_markup(str.format('{0:.1f}', value))

        self.recalculate_angle()

    def get_value(self):
        return self.adjustment.value

    ## Constructor ##

    def __init__(self, adj):
        Widget.__init__(self)

        self._layout = self.create_pango_layout('')
        self._layout.set_font_description(pango.FontDescription("sans bold 10"))
        self._layout.set_markup(str.format('{0:.1f}', adj.value))

        self.adjustment = adj
        self.recalculate_angle()

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
        #width, height = self._layout.get_size()
        requisition.width = _MIN_WIDTH
        requisition.height = _MIN_HEIGHT

    def do_size_allocate(self, allocation):
        # The do_size_allocate is called by when the actual size is known
        # and the widget is told how much space could actually be allocated

        self.allocation = allocation

        if self.flags() & REALIZED:
            self.window.move_resize(*allocation)

    gc = None

    def do_expose_event(self, event):
        # The do_expose_event is called when the widget is asked to draw itself

        x, y, w, h = self.allocation

        # Draw the background image
        if self.gc == None:
            self.gc = self.window.new_gc()

        self.window.draw_pixbuf(self.gc, _background_pixbuf,
                                0, 0,    # Source
                                w / 2 - _MIN_WIDTH / 2,
                                h / 2 - _MIN_HEIGHT / 2,
                                -1, -1)  # Dimensions

        fontw, fonth = self._layout.get_pixel_size()
        cr = self.window.cairo_create()

        cr.move_to((w - fontw)/2, 0.75 * h - fonth / 2)
        cr.update_layout(self._layout)
        cr.show_layout(self._layout)

        points = [(0.0, 0.4), (0.07, 0.0), (0.0, -0.07), (-0.07, 0.0)]

        m = cairo.Matrix()
        m.translate(w / 2, h / 2)  # Centre the coordinates
        m.rotate(self.angle)
        cr.set_matrix(m)
        cr.set_source_color(_NEEDLE_COLOR)

        # Draw the points
        pX, pY = points[0]
        cr.move_to(pX * _MIN_WIDTH, pY * _MIN_HEIGHT)
        for i in range(1, len(points)):
            pX, pY = points[i]
            cr.line_to(pX * _MIN_WIDTH, pY * _MIN_HEIGHT)

        cr.close_path()
        cr.fill()


gobject.type_register(Dial)
