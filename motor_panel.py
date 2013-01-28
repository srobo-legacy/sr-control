import pygtk
pygtk.require('2.0')
from gtk import *

import pango

from dial import Dial

_MOTOR_STEP = 5

_HELP_MESSAGE = "Turn right knob to change speed."

class MotorPanel(Table):

    ## Event handlers ##

    def key_press(self, widget, event):
        if event.keyval == keysyms.Up:
            value = self.dial.get_value() + _MOTOR_STEP
            if value <= 100:
                self.dial.set_value(value)

                if self.board <> None:
                    self.board.target = value

        elif event.keyval == keysyms.Down:
            value = self.dial.get_value() - _MOTOR_STEP
            if value >= -100:
                self.dial.set_value(value)

                if self.board <> None:
                    self.board.target = value

        elif event.keyval == keysyms.Page_Up:
            print "Motor page up"

        elif event.keyval == keysyms.Page_Down:
            print "Motor page down"

    def panel_update(self, _):
        self.dial.set_value(self.board.target)

    ## Constructor ##

    def __init__(self, board = None):
        Table.__init__(self, 2, 1)

        self.dial = Dial(Adjustment(lower=-100, value=0, upper=100))
        self.attach(self.dial, 0, 1, 0, 1)

        self.help_bar = Label(_HELP_MESSAGE)
        self.attach(self.help_bar, 0, 1, 1, 2)

        self.show_all()

        ## Signals ##
        self.connect("key-press-event", self.key_press)

        self.board = board

        if board <> None:
            self.panel_update(None)
            self.connect("panel-update", self.panel_update)

