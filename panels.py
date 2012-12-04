import pygtk
pygtk.require('2.0')
from gtk import *

BB_PANEL = 0
POWER_PANEL = 1
MOTOR_PANEL = 2
SERVO_PANEL = 3
JIO_PANEL = 4
VISION_PANEL = 5

def test(widget):
    print "panel \"",widget.foo,"\" updated"

def create_panel(board):
    """Creates and returns a control panel for the given board."""
    b = Button("Panel " + str(board))
    b.foo = board
    b.connect("panel-update", test)
    return b
