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

import cairo

from analogue_input import AnalogueInput
from digital_input import DigitalInput
from selectable_label import SelectableLabel
from dial import Dial

def _main(args):
    win = Window()
    win.set_border_width(5)
    win.set_title('Widget test')
    win.connect('delete-event', main_quit)

    t = Table(5, 2, True)

    l1 = SelectableLabel("1")
    l1.set_state(STATE_SELECTED)
    t.attach(l1, 0, 1, 0, 1)
    l2 = SelectableLabel("2")
    t.attach(l2, 1, 2, 0, 1)

    w = DigitalInput(1)
    t.attach(w, 0, 1, 1, 2)
    x = DigitalInput(0)
    t.attach(x, 0, 1, 2, 3)
    y = AnalogueInput(2.4578)
    t.attach(y, 1, 2, 1, 2)
    z = AnalogueInput(0.0001)
    t.attach(z, 1, 2, 2, 3)

    d = Dial(Adjustment(value=53, lower=-100, upper=100))
    t.attach(d, 0, 3, 3, 5)
    win.add(t)

    win.show_all()

    main()

if __name__ == '__main__':
    sys.exit(_main(sys.argv))

