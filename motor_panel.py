import pygtk
pygtk.require('2.0')
from gtk import *

import pango

from dial import Dial

_MOTOR_STEP = 5

class MotorPanel(Table):

    ## Event handlers ##

    def key_press(self, widget, event):
        if event.keyval == keysyms.Up:
            value = self.dial.get_value() + _MOTOR_STEP
            if value <= 100:
                self.dial.set_value(value)

        elif event.keyval == keysyms.Down:
            value = self.dial.get_value() - _MOTOR_STEP
            if value >= -100:
                self.dial.set_value(value)

        elif event.keyval == keysyms.Page_Up:
            print "Motor page up"

        elif event.keyval == keysyms.Page_Down:
            print "Motor page down"

    ## Constructor ##

    def __init__(self, board = None):
        Table.__init__(self, 1, 1)

        self.dial = Dial(Adjustment(lower=-100, value=0, upper=100))
        self.attach(self.dial, 0, 1, 0, 1)

        self.show_all()

        ## Signals ##
        self.connect("key-press-event", self.key_press)
        #self.connect("panel-update", self.panel_update)
