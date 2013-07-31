import pygtk
pygtk.require('2.0')
from gtk import *

import pango

from output_switch import OutputSwitch
from analogue_input import AnalogueInput

_HELP_MESSAGE = "Press right knob to toggle motor rail."
# TODO: Try using \u2460 and \u2461 (with u"...") on a power board

_MAX_VOLTAGE = 14
_DUMMY_VOLTAGE = 12.6

_MAX_CURRENT = 15
_DUMMY_CURRENT = 7.5

class PowerPanel(Table):
    ## Output selection and manipulation ##
    motor_rail = True

    ## Event handlers ##
    def toggle_motor_rail(self):
        self.motor_rail = not self.motor_rail
        if self.board != None:
            self.board._set_motor_rail(self.motor_rail)
        self.motor_rail_control.set_value(self.motor_rail)
        self.motor_rail_control.queue_draw()

    def key_press(self, widget, event):
        if event.keyval == keysyms.Return:
            self.toggle_motor_rail()

    def panel_update(self, _):
        voltage = self.board.battery.voltage
        current = self.board.battery.current

        self.voltage.set_value(voltage)
        self.current.set_value(current)
        self.voltage.queue_draw()
        self.current.queue_draw()


    ## Constructor ##

    def __init__(self, controller, board = None):
        Table.__init__(self, 4, 2)

        def create_heading(text, font_description):
            """Creates a new label with the given text and font, which is centre aligned."""
            l = Label(text)
            l.set_justify(JUSTIFY_CENTER)
            l.set_alignment(0.5, 0.5)
            l.modify_font(pango.FontDescription(font_description))
            return l

        # Battery Voltage
        self.attach(create_heading("Battery Voltage", "sans 10"), 0, 1, 0, 1)

        # Battery Current
        self.attach(create_heading("Battery Current", "sans 10"), 0, 1, 1, 2)

        # Motor Rail
        self.attach(create_heading("Power Rail", "sans 10"), 0, 1, 2, 3)

        # Battery Voltage control
        self.voltage = AnalogueInput(_DUMMY_VOLTAGE, _MAX_VOLTAGE)
        self.attach(self.voltage, 1, 2, 0, 1)

        # Battery Current control
        self.current = AnalogueInput(_DUMMY_CURRENT, _MAX_CURRENT)
        self.attach(self.current, 1, 2, 1, 2)

        # Motor rail control
        self.motor_rail_control = OutputSwitch(True)
        self.attach(self.motor_rail_control, 1, 2, 2, 3)
        self.motor_rail_control.set_state(STATE_SELECTED)

        # Help bar
        self.help_bar = Label(_HELP_MESSAGE)
        self.attach(self.help_bar, 0, 2, 3, 4, yoptions=SHRINK)

        self.show_all()

        ## Signals ##
        self.connect("key-press-event", self.key_press)

        # Connect to the board
        self.board = board

        if board != None:
            self.panel_update(None)
            self.connect("panel-update", self.panel_update)