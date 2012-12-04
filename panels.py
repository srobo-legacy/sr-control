import pygtk
pygtk.require('2.0')
from gtk import *

import io_panel

BB_PANEL = 0
POWER_PANEL = 1
MOTOR_PANEL = 2
SERVO_PANEL = 3
JIO_PANEL = 4
VISION_PANEL = 5

def create_panel(board):
    """Creates and returns a control panel for the given board."""
    return io_panel.IOPanel(board)
