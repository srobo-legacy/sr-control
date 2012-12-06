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

_BORDER_WIDTH = 5
_INPUT_ON_COLOR = gdk.Color(0.14453125, 0.20703125, 0.44140625)
# TODO: Put the on color in some common location

_MAX_INPUT_VOLTAGE = 3.3

class AnalogueInput(Widget):

    def set_value(self, value):
        """Set the value displayed by the AnalogueInput widget."""
        self.value = value

        if self.value > _MAX_INPUT_VOLTAGE / 2:
            markup = str.format('<span color="white">{:.1f}V</span>', self.value)
        else:
            markup = str.format('<span color="black">{:.1f}V</span>', self.value)

        self._layout.set_markup(markup)

    ## Constructor ##

    def __init__(self, value):
        Widget.__init__(self)
        self._layout = self.create_pango_layout('')
        self._layout.set_font_description(pango.FontDescription("sans bold 10"))
        self.set_value(value)

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
        # The do_size_request method Gtk+ is calling on a widget to ask
        # it the widget how large it wishes to be. It's not guaranteed
        # that gtk+ will actually give this size to the widget

        # In this case, we say that we want to be as big as the
        # text is, plus a little border around it.
        width, height = self._layout.get_size()
        requisition.width = width // pango.SCALE + _BORDER_WIDTH*3
        requisition.height = height // pango.SCALE + _BORDER_WIDTH*2

    def do_size_allocate(self, allocation):
        # The do_size_allocate is called by when the actual size is known
        # and the widget is told how much space could actually be allocated

        self.allocation = allocation

        if self.flags() & REALIZED:
            self.window.move_resize(*allocation)

    def do_expose_event(self, event):
        # The do_expose_event is called when the widget is asked to draw itself

        x, y, w, h = self.allocation
        cr = self.window.cairo_create()

        if self.value > 0:
            # Draw a filled rounded rectangle
            # TODO: take the line width into account
            top = (1 - self.value / _MAX_INPUT_VOLTAGE) * (h - 2*_BORDER_WIDTH) + _BORDER_WIDTH
            cr.set_source_color(_INPUT_ON_COLOR)
            cr.rectangle(_BORDER_WIDTH, top,
                         w - 2*_BORDER_WIDTH, h - _BORDER_WIDTH - top)
            cr.fill_preserve()
            cr.set_line_width(5.0)
            cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.stroke()

        # draw the value in the centre of the control
        fontw, fonth = self._layout.get_pixel_size()
        cr.move_to((w - fontw)/2, (h - fonth)/2)
        cr.update_layout(self._layout)
        cr.show_layout(self._layout)

gobject.type_register(AnalogueInput)

def _main(args):
    win = Window()
    win.set_border_width(5)
    win.set_title('Widget test')
    win.connect('delete-event', main_quit)

    t = Table(1, 2, True)

    w = AnalogueInput(2.4578)
    t.attach(w, 0, 1, 0, 1)
    x = AnalogueInput(0.0001)
    t.attach(x, 1, 2, 0, 1)
    win.add(t)

    win.show_all()

    main()

if __name__ == '__main__':
    sys.exit(_main(sys.argv))
