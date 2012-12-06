"""
Displays a window showing three InputWidgets (two digital and two analogue).
"""

import sys
import pygtk
pygtk.require('2.0')
import gobject
import pango
from gtk import *

if pygtk_version < (2, 8):
    raise SystemExit("PyGtk 2.8 or later required")

try:
    import cairo
except ImportError:
    raise SystemExit("cairo required")

from analogue_input import AnalogueInput
from digital_input import DigitalInput

def _main(args):
    win = Window()
    win.set_border_width(5)
    win.set_title('Widget test')
    win.connect('delete-event', main_quit)

    t = Table(2, 2, True)

    w = DigitalInput(1)
    t.attach(w, 0, 1, 0, 1)
    x = DigitalInput(0)
    t.attach(x, 0, 1, 1, 2)
    y = AnalogueInput(2.4578)
    t.attach(y, 1, 2, 0, 1)
    z = AnalogueInput(0.0001)
    t.attach(z, 1, 2, 1, 2)
    win.add(t)

    win.show_all()

    main()

if __name__ == '__main__':
    sys.exit(_main(sys.argv))

