import pygtk
pygtk.require('2.0')
from gtk import *

import pango

import digital_input
import analogue_input

NUM_IO_PINS = 8

class IOPanel(Table):
    ## Output selection and manipulation ##

    def select_output(self, num):
        self.outputs[num].set_state(STATE_SELECTED)

    def deselect_output(self, num):
        self.outputs[num].set_state(STATE_NORMAL)

    selected_output = 0

    def prev_output(self):
        if self.selected_output > 0:
            self.deselect_output(self.selected_output)
            self.selected_output = self.selected_output - 1
            self.select_output(self.selected_output)

        print self.selected_output

    def next_output(self):
        if self.selected_output < NUM_IO_PINS - 1:
            self.deselect_output(self.selected_output)
            self.selected_output = self.selected_output + 1
            self.select_output(self.selected_output)

        print self.selected_output

    ## Event handlers ##

    def key_press(self, widget, event):
        if event.keyval == keysyms.Up:
            print "Up"

        elif event.keyval == keysyms.Down:
            print "Down"

        elif event.keyval == keysyms.Page_Up:
            self.prev_output()

        elif event.keyval == keysyms.Page_Down:
            self.next_output()

    ## Constructor ##

    def __init__(self, board):
        Table.__init__(self, 11, NUM_IO_PINS)

        def create_heading(text, font_description):
            """Creates a new label with the given text and font, which is centre aligned."""
            l = Label(text)
            l.set_justify(JUSTIFY_CENTER)
            l.set_alignment(0.5, 0.5)
            l.modify_font(pango.FontDescription(font_description))
            return l

        def create_column_label(num):
            return Label(str(num))

        def create_output(num):
            # TODO: implement properly
            # outputs will display as the value above a switch icon
            l = Label(str((82 >> num) & 1))
            b = Label("[ ]")
            t = Table(2, 1, True)
            t.attach(l, 0, 1, 0, 1)
            t.attach(b, 0, 1, 1, 2)
            t.modify_bg(STATE_SELECTED, gdk.Color(blue=0.8))
            return t

        ## Inputs ##
        self.attach(create_heading("Inputs", "sans bold 12"), 0, NUM_IO_PINS, 0, 1)#, yoptions=FILL)

        # Column labels
        for i in range(NUM_IO_PINS):
            self.attach(create_column_label(i), i, i + 1, 1, 2)

        # Analogue inputs
        self.attach(create_heading("Analogue", "sans 10"), 0, NUM_IO_PINS, 2, 3)#, yoptions=FILL)
        self.inputs_a = []
        for i in range(NUM_IO_PINS):
            self.inputs_a.append(analogue_input.AnalogueInput(i * 3.3 / 8))
            self.attach(self.inputs_a[i], i, i + 1, 3, 4)

        # Digital inputs
        self.attach(create_heading("Digital", "sans 10"), 0, NUM_IO_PINS, 4, 5)
        self.inputs_d = []
        for i in range(NUM_IO_PINS):
            self.inputs_d.append(digital_input.DigitalInput((78 >> i) & 1))
            self.attach(self.inputs_d[i], i, i + 1, 5, 6)

        ## Outputs ##
        self.attach(create_heading("Outputs", "sans bold 12"), 0, NUM_IO_PINS, 6, 7)
        self.outputs = []
        for i in range(NUM_IO_PINS):
            self.outputs.append(create_output(i))
            self.attach(self.outputs[i], i, i + 1, 7, 8)

        self.show_all()

        ## Signals ##
        self.connect("key-press-event", self.key_press)
