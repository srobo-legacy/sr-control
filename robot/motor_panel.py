import pygtk
pygtk.require('2.0')
from gtk import *

import pango

from dial import Dial
from selectable_label import SelectableLabel

NUM_MOTORS = 2

_MOTOR_STEP = 5

_HELP_MESSAGE = "(1) or (2) to choose motor. Turn knob to change."

class MotorPanel(Table):

    ## Motor selection and manipulation ##

    def select(self, offset):
        if 0 <= self.selected_motor + offset < NUM_MOTORS:
            self.labels[self.selected_motor].set_state(STATE_NORMAL)
            self.selected_motor = self.selected_motor + offset
            self.labels[self.selected_motor].set_state(STATE_SELECTED)
            if self.board != None:
                self.panel_update(None)

    def set_motor_speed(self, value):
        self.dial.set_value(value)
        if self.board != None:
            if self.selected_motor == 0:
                self.board.m0.power = value
            else:
                self.board.m1.power = value

    ## Event handlers ##

    def key_press(self, widget, event):
        if event.keyval == keysyms.Up:
            value = self.dial.get_value() + _MOTOR_STEP
            if value <= 100:
                self.set_motor_speed(value)

        elif event.keyval == keysyms.Down:
            value = self.dial.get_value() - _MOTOR_STEP
            if value >= -100:
                self.set_motor_speed(value)

        elif event.keyval == keysyms.Page_Up:
            self.select(-1)

        elif event.keyval == keysyms.Page_Down:
            self.select(1)

    def panel_update(self, _):
        if self.selected_motor == 0:
            self.dial.set_value(self.board.m0.power)
        else:
            self.dial.set_value(self.board.m1.power)

    ## Constructor ##

    def __init__(self, controller, board = None):
        Table.__init__(self, 2, 2)

        self.dial = Dial(Adjustment(lower=-100, value=0, upper=100))
        self.attach(self.dial, 0, 1, 0, 1)

        right_box = VBox()
        right_box.add(Label("Motor"))

        self.selected_motor = 0
        self.labels = [SelectableLabel(str(num)) for num in range(2)]
        self.labels[self.selected_motor].set_state(STATE_SELECTED)
        for label in self.labels:
            right_box.add(label)

        self.attach(right_box, 1, 2, 0, 1)

        self.help_bar = Label(_HELP_MESSAGE)
        self.attach(self.help_bar, 0, 2, 1, 2)

        self.show_all()

        ## Signals ##
        self.connect("key-press-event", self.key_press)

        self.board = board
        self.controller = controller

        if board <> None:
            self.panel_update(None)
            self.connect("panel-update", self.panel_update)
