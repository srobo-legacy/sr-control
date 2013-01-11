import pygtk
pygtk.require('2.0')
from gtk import *

import pango

from selectable_label import SelectableLabel

NUM_SERVOS = 8

class ServoPanel(Table):
    ## Servo selection and manipulation ##

    selected_servo = 0

    def prev_servo(self):
        if self.selected_servo > 0:
            self.labels[self.selected_servo].set_state(STATE_NORMAL)
            self.selected_servo = self.selected_servo - 1
            self.labels[self.selected_servo].set_state(STATE_SELECTED)

    def next_servo(self):
        if self.selected_servo < NUM_SERVOS - 1:
            self.labels[self.selected_servo].set_state(STATE_NORMAL)
            self.selected_servo = self.selected_servo + 1
            self.labels[self.selected_servo].set_state(STATE_SELECTED)

    def set_servo(self, num, value):
        return None
        #self.servos[num].set_value(value)
        # TODO: Actually set the value

    ## Event handlers ##

    def key_press(self, widget, event):
        if event.keyval == keysyms.Up:
            self.set_servo(self.selected_servo, 1)

        elif event.keyval == keysyms.Down:
            self.set_servo(self.selected_servo, 0)

        elif event.keyval == keysyms.Page_Up:
            self.prev_servo()

        elif event.keyval == keysyms.Page_Down:
            self.next_servo()

    ## Constructor ##

    labels = []
    sliders = []

    def __init__(self, board):
        Table.__init__(self, 3, NUM_SERVOS)

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

        adjustment = None  # TODO

        for i in range(NUM_SERVOS):
            # Heading
            self.labels.append(SelectableLabel(str(i)))
            self.attach(self.labels[i], i, i + 1, 1, 2, yoptions=SHRINK)
            # Slider
            self.sliders.append(VScale(adjustment))
            self.attach(self.sliders[i], i, i + 1, 2, 3)

        self.labels[self.selected_servo].set_state(STATE_SELECTED)

        self.show_all()

        ## Signals ##
        self.connect("key-press-event", self.key_press)
