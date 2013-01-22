import pygtk
pygtk.require('2.0')
from gtk import *

from io_panel import IOPanel
from servo_panel import ServoPanel
from motor_panel import MotorPanel

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
    if board == "IOPanel":
        return IOPanel()
    elif board == "ServoPanel":
        return ServoPanel()
    else:
        return MotorPanel()
