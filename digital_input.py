# Copied from the tutorial at http://git.gnome.org/browse/pygtk/plain/examples/gtk/widget.py

import sys

import pygtk
pygtk.require('2.0')
import gobject
import pango
from gtk import *

if pygtk_version < (2, 8):
    print "PyGtk 2.8 or later required for this example"
    raise SystemExit

try:
    import cairo
except ImportError:
    raise SystemExit("cairo required for this example")

BORDER_WIDTH = 5

# A quite simple gtk.Widget subclass which demonstrates how to subclass
# and do realizing, sizing and drawing.

class DigitalInput(Widget):
    def __init__(self, io_board, input_num):
        Widget.__init__(self)
        self.value = (78 >> input_num) & 1
        self._layout = self.create_pango_layout('')

        if self.value == 1:
            self._layout.set_markup('<span color="white">1</span>')
        else:
            self._layout.set_markup('<span color="black">0</span>')

        self._layout.set_font_description(pango.FontDescription("sans bold 10"))

    # GtkWidget

    def do_realize(self):
        # The do_realize method is responsible for creating GDK (windowing system)
        # resources. In this example we will create a new gdk.Window which we
        # then draw on

        # First set an internal flag telling that we're realized
        self.set_flags(REALIZED)

        # Create a new gdk.Window which we can draw on.
        # Also say that we want to receive exposure events by setting
        # the event_mask
        self.window = gdk.Window(
            self.get_parent_window(),
            width=self.allocation.width,
            height=self.allocation.height,
            window_type=gdk.WINDOW_CHILD,
            wclass=gdk.INPUT_OUTPUT,
            event_mask=self.get_events() | gdk.EXPOSURE_MASK)

        # Associate the gdk.Window with ourselves, Gtk+ needs a reference
        # between the widget and the gdk window
        self.window.set_user_data(self)

        # Attach the style to the gdk.Window, a style contains colors and
        # GC contextes used for drawing
        # TODO: Is this the best place for style info?
        self.style.attach(self.window)

        # The default color of the background should be what
        # the style (theme engine) tells us.
        self.style.set_background(self.window, STATE_NORMAL)
        self.window.move_resize(*self.allocation)

    def do_unrealize(self):
        # The do_unrealized method is responsible for freeing the GDK resources

        # De-associate the window we created in do_realize with ourselves
        self.window.set_user_data(None)

    def do_size_request(self, requisition):
        # The do_size_request method Gtk+ is calling on a widget to ask
        # it the widget how large it wishes to be. It's not guaranteed
        # that gtk+ will actually give this size to the widget

        # In this case, we say that we want to be as big as the
        # text is, plus a little border around it.
        width, height = self._layout.get_size()
        requisition.width = width // pango.SCALE + BORDER_WIDTH*4
        requisition.height = height // pango.SCALE + BORDER_WIDTH*4

    def do_size_allocate(self, allocation):
        # The do_size_allocate is called by when the actual size is known
        # and the widget is told how much space could actually be allocated

        # Save the allocated space
        self.allocation = allocation

        # If we're realized, move and resize the window to the
        # requested coordinates/positions
        if self.flags() & REALIZED:
            self.window.move_resize(*allocation)

    def do_expose_event(self, event):
        # The do_expose_event is called when the widget is asked to draw itself
        # Remember that this will be called a lot of times, so it's usually
        # a good idea to write this code as optimized as it can be, don't
        # Create any resources in here.

        # In this example, draw a rectangle in the foreground color
        x, y, w, h = self.allocation
        cr = self.window.cairo_create()

        # Draw rounded rectangle
        if self.value == 1:
            cr.set_source_color(gdk.Color(0.14453125, 0.20703125, 0.44140625))
            cr.rectangle(BORDER_WIDTH, BORDER_WIDTH,
                         w - 2*BORDER_WIDTH, h - 2*BORDER_WIDTH)
            cr.fill_preserve()
            cr.set_line_width(5.0)
            cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.stroke()

        # And draw the text in the middle of the allocated space
        fontw, fonth = self._layout.get_pixel_size()
        cr.move_to((w - fontw)/2, (h - fonth)/2)
        cr.update_layout(self._layout)
        cr.show_layout(self._layout)

gobject.type_register(DigitalInput)

def _main(args):
    win = Window()
    win.set_border_width(5)
    win.set_title('Widget test')
    win.connect('delete-event', main_quit)

    t = Table(1, 2, True)

    w = DigitalInput(None, 1)
    t.attach(w, 0, 1, 0, 1)
    x = DigitalInput(None, 0)
    t.attach(x, 0, 1, 1, 2)
    win.add(t)

    win.show_all()

    main()

if __name__ == '__main__':
    sys.exit(_main(sys.argv))
