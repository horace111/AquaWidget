import json
import requests

from widgets import AquaWidget
from PyQt5.QtWidgets import *

acquire_func = None
def set_acquire_func(func) -> None:
    global acquire_func
    acquire_func = func

def acquire() -> QWidget:
    return acquire_func()

def get_weather():
    pass
'''
weather -- request from server
'''

def reg() -> AquaWidget:
    global acquire_func
    aquaw = AquaWidget(scale = (370, 370))
    degree = 15
    show_degree = QLabel('{degree}°C'.format(degree = degree), parent = aquaw.get_aqua_widget())
    show_degree.move(15, 15)
    return aquaw