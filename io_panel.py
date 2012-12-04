import pygtk
pygtk.require('2.0')
from gtk import *

import pango

NUM_IO_PINS = 8

class IOPanel(Table):
    def __init__(self, board):
        Table.__init__(self, 11, NUM_IO_PINS , False)

        def create_heading(text, font_description):
            """Creates a new label with the given text and font, which is centre aligned."""
            l = Label(text)
            l.set_justify(JUSTIFY_CENTER)
            l.set_alignment(0.5, 0.5)
            l.modify_font(pango.FontDescription(font_description))
            return l

        def create_analogue_input(num):
            # TODO: implement properly
            # analogue inputs will have a vertical bar behind them
            # (height indicating value)
            return Label(str(num * 0.33) + "V")

        def create_digital_input(num):
            # TODO: implement properly
            # digital inputs will be highlighted by a rounded rectangle when on
            return Label(str((78 >> num) & 1))

        def create_output(num):
            # TODO: implement properly
            # outputs will display as the value above a switch icon
            l = Label(str((82 >> num) & 1))
            b = Label("[ ]")
            t = Table(2, 1, True)
            t.attach(l, 0, 1, 0, 1)
            t.attach(b, 0, 1, 1, 2)
            return t

        ## Inputs ##
        self.attach(create_heading("Inputs", "sans bold 12"), 0, NUM_IO_PINS, 0, 1)#, yoptions=FILL)

        # Analogue inputs
        self.attach(create_heading("Analogue", "sans 10"), 0, NUM_IO_PINS, 1, 2)#, yoptions=FILL)
        self.inputs_a = []
        for i in range(NUM_IO_PINS):
            self.inputs_a.append(create_analogue_input(i))
            self.attach(self.inputs_a[i], i, i + 1, 2, 3)

        # Digital inputs
        self.attach(create_heading("Digital", "sans 10"), 0, NUM_IO_PINS, 3, 4)
        self.inputs_d = []
        for i in range(NUM_IO_PINS):
            self.inputs_d.append(create_digital_input(i))
            self.attach(self.inputs_d[i], i, i + 1, 4, 5)

        ## Outputs ##
        self.attach(create_heading("Outputs", "sans bold 12"), 0, NUM_IO_PINS, 5, 6)
        self.outputs = []
        for i in range(NUM_IO_PINS):
            self.outputs.append(create_output(i))
            self.attach(self.outputs[i], i, i + 1, 6, 7)

        self.show_all()
