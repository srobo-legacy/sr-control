import pygtk
pygtk.require('2.0')
from gtk import *

BB_PANEL = 0
POWER_PANEL = 1
MOTOR_PANEL = 2
SERVO_PANEL = 3
JIO_PANEL = 4
VISION_PANEL = 5

def create_panel(board):
    return Button("Panel " + str(board))
