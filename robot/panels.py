import pygtk
pygtk.require('2.0')
from gtk import *

from io_panel import IOPanel
from servo_panel import ServoPanel
from motor_panel import MotorPanel
from power_panel import PowerPanel

BB_PANEL = 0
POWER_PANEL = 1
MOTOR_PANEL = 2
SERVO_PANEL = 3
JIO_PANEL = 4
VISION_PANEL = 5

board_to_panel = {
    'JointIO': IOPanel,
    'Servo'  : ServoPanel,
    'Motor'  : MotorPanel,
    'Power'  : PowerPanel
}

def create_panel_by_class_name(controller, class_name):
    """Creates and returns a control panel for the given board."""
    if class_name == "IOPanel":
        return IOPanel(controller)
    elif class_name == "ServoPanel":
        return ServoPanel(controller)
    elif class_name == "PowerPanel":
        return PowerPanel(controller)
    else:
        return MotorPanel(controller)

def create_panel(controller, board):
    return board_to_panel[board.__class__.__name__](controller, board)
