import pygtk
pygtk.require('2.0')
from gtk import *

import pango

from selectable_label import SelectableLabel

NUM_SERVOS = 8

_SLIDER_NOTCH = 1

_UNSET_SERVO_COLOR = gdk.Color(1.0, 0.5, 0.0)  # Orange

_SET_SERVO_COLOR = gdk.Color(0.14453125, 0.20703125, 0.44140625)
_SET_SERVO_TEXT_COLOR = gdk.Color(0.0, 0.0, 0.0)

_SET_SERVO_HELP_MESSAGE = "Turn knob to change value."
_UNSET_SERVO_HELP_MESSAGE = "Turn knob to choose value. Press knob to set."

class ServoPanel(Table):
    ## Servo selection and manipulation ##

    def update_help_message(self):
        if self.servo_set[self.selected_servo]:
            self.help_bar.set_text(_SET_SERVO_HELP_MESSAGE)
        else:
            self.help_bar.set_text(_UNSET_SERVO_HELP_MESSAGE)

    selected_servo = 0

    def select(self, offset):
        if 0 <= self.selected_servo + offset < NUM_SERVOS:
            self.labels[self.selected_servo].set_state(STATE_NORMAL)
            self.selected_servo = self.selected_servo + offset
            self.labels[self.selected_servo].set_state(STATE_SELECTED)
            self.update_help_message()

    def set_servo(self, num, value):
        self.sliders[num].set_value(value)
        if self.board != None and self.servo_set[num]:
            self.board[num] = value

    def change_servo(self, num, notches):
        value = self.sliders[num].get_value()
        self.set_servo(num, int(value) + notches * _SLIDER_NOTCH)

    ## Event handlers ##

    def size_allocate(self, widget, allocation):
        # Set the help label's size
        # (stops the columns changing size when the help text changes.)
        self.help_bar.set_size_request(allocation.width, -1)

    def key_press(self, widget, event):
        if event.keyval == keysyms.Up:
            self.change_servo(self.selected_servo, 1)

        elif event.keyval == keysyms.Down:
            self.change_servo(self.selected_servo, -1)

        elif event.keyval == keysyms.Return:
            # Set the servo to the value
            num = self.selected_servo
            self.servo_set[num] = True
            self.set_servo(num, self.sliders[num].get_value())
            # Update the UI
            self.update_help_message()
            self.sliders[num].modify_bg(STATE_NORMAL, _SET_SERVO_COLOR)
            self.sliders[num].modify_fg(STATE_NORMAL, _SET_SERVO_TEXT_COLOR)

        elif event.keyval == keysyms.Page_Up:
            self.select(-1)

        elif event.keyval == keysyms.Page_Down:
            self.select(1)

    def panel_update(self, _):
        for i in range(NUM_SERVOS):
            value = self.board[i]
            if self.servo_set[i]:
                self.sliders[i].set_value(value)

    ## Constructor ##

    labels = []
    sliders = []
    servo_set = []

    def __init__(self, controller, board = None):
        Table.__init__(self, 4, NUM_SERVOS)

        def create_heading(text, font_description):
            """Creates a new label with the given text and font, which is centre aligned."""
            # TODO: Put in common location
            l = Label(text)
            l.set_justify(JUSTIFY_CENTER)
            l.set_alignment(0.5, 0.5)
            l.modify_font(pango.FontDescription(font_description))
            return l

        # Heading
        self.attach(create_heading("Servo Board", "sans bold 12"), 0, NUM_SERVOS + 1, 0, 1,
                    yoptions=SHRINK)

        for i in range(NUM_SERVOS):
            # Heading
            self.labels.append(SelectableLabel(str(i)))
            self.attach(self.labels[i], i, i + 1, 1, 2, yoptions=SHRINK)
            # Slider
            adj = Adjustment(value = 50, lower = 0, upper = 100)
            slider = VScale(adj)
            slider.set_inverted(True)
            slider.set_value_pos(POS_BOTTOM)
            self.attach(slider, i, i + 1, 2, 3)

            slider.modify_fg(STATE_NORMAL, _UNSET_SERVO_COLOR)
            slider.modify_bg(STATE_NORMAL, _UNSET_SERVO_COLOR)
            self.sliders.append(slider)
            self.servo_set.append(False)

        self.labels[self.selected_servo].set_state(STATE_SELECTED)

        self.help_bar = Label()
        self.attach(self.help_bar, 0, NUM_SERVOS + 1, 3, 4, yoptions=SHRINK, xoptions=SHRINK)
        self.update_help_message()

        self.show_all()

        ## Signals ##
        self.connect("size-allocate", self.size_allocate)
        self.connect("key-press-event", self.key_press)

        # Connect to the board
        self.board = board

        if board != None:
            self.panel_update(None)
            self.connect("panel-update", self.panel_update)

