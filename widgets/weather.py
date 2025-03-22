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

def get_weather_by_local_ip():
    r = requests.get('http://47.119.20.145:82/v1/weather/ip_based_quick_query')
    '''
    weather -- request from server
    '''
    return r.json()

def reg() -> AquaWidget:
    global acquire_func
    aquaw = AquaWidget(scale = (370, 370))
    show_degree = QLabel(parent = aquaw.get_aqua_widget())
    weather = get_weather_by_local_ip()['data']
    show_degree.setText(f"{weather['cityId']} {weather['temperature']}℃")
    show_degree.move(15, 15)
    return aquaw