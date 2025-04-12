import json
import requests

from widgets import AquaWidget
from gui import Fonts
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

acquire_func = None
def set_qwidget_source(func) -> None:
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
    show_degree = QLabel()
    weather = get_weather_by_local_ip()['data']
    show_degree.setText(f"{weather['temperature']}℃")
    show_degree.setFont(Fonts.font_harmony_title)
    show_degree.setObjectName('weather_show_degree')
    show_degree.setStyleSheet("QLabel#weather_show_degree{color:rgba(255, 255, 255, 0.7)}")
    show_degree.move(15, 15)

    show_city = QLabel()
    show_city.setText(weather['cityId'])
    show_city.setFont(Fonts.font_harmony)
    show_degree.setObjectName('weather_show_city')
    show_degree.setStyleSheet("QLabel#weather_show_city{color:rgba(255, 255, 255, 0.7)}")
    show_city.move(15, 45)

    aquaw.bind_child_widget_with_aqua_widget_qwidget(show_degree)
    aquaw.bind_child_widget_with_aqua_widget_qwidget(show_city)
    return aquaw