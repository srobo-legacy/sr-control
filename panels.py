import pygtk
pygtk.require('2.0')
from gtk import *

from io_panel import IOPanel

BB_PANEL = 0
POWER_PANEL = 1
MOTOR_PANEL = 2
SERVO_PANEL = 3
JIO_PANEL = 4
VISION_PANEL = 5

board_to_panel = {
    'JointIO': IOPanel
}

def create_panel(board):
    """Creates and returns a control panel for the given board."""
    return board_to_panel[board.__class__.__name__](board)
