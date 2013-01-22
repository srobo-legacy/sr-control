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
    'JointIO': IOPanel,
    'Servo'  : ServoPanel,
    'Motor'  : MotorPanel
}

def create_panel_by_class_name(class_name):
    """Creates and returns a control panel for the given board."""
    if class_name == "IOPanel":
        return IOPanel()
    elif class_name == "ServoPanel":
        return ServoPanel()
    else:
        return MotorPanel()

def create_panel(board):
    return board_to_panel[board.__class__.__name__](board)
