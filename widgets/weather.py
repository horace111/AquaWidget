import json
import requests

from widgets import AquaWidget
from gui import Fonts
from stdqt import *

acquire_func = None
set_blur = QGraphicsBlurEffect()
set_blur.setBlurRadius(20)
set_blur.setBlurType(QGraphicsBlurEffect.GaussianBlur)
set_blur.setBlurHints(QGraphicsBlurEffect.QualityHint)

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

def info():
    global weather, city
    weather = get_weather_by_local_ip()['data']
    city = get_weather_by_local_ip()['cityId']

    return weather, city

def reg() -> AquaWidget:
    global acquire_func
    aquaw = AquaWidget(scale = (370, 370))
    def show_background():
        if weather == "晴朗":
            aquaw.setStyleSheet("background-image: url(./resources/forWeather/background/sunny.jpg);")
        elif weather == "多云":
            aquaw.setStyleSheet("background-image: url(./resources/forWeather/background/cloudy.jpg);")
        elif weather == "雨":
            aquaw.setStyleSheet("background-image: url(./resources/forWeather/background/rain.jpg);")
        elif weather == "小雨":
            aquaw.setStyleSheet("background-image: url(./resources/forWeather/background/little_rain.jpg);")
        elif weather == "阴":
            aquaw.setStyleSheet("background-image: url(./resources/forWeather/background/cloudy.jpg);")
        elif weather == "雷阵雨":
            aquaw.setStyleSheet("background-image: url(./resources/forWeather/background/thunder.jpg);")
        elif weather == "雾":
            aquaw.setStyleSheet("background-image: url(./resources/forWeather/background/fog.jpg);")
        else:
            return None

    show_degree = QLabel()
    show_degree.setText(f"{weather}°C")
    show_degree.setFont(Fonts.font_harmony_title)
    show_degree.setStyleSheet("color: white")
    show_degree.move(15, 20)

    show_city = QLabel()
    show_city.setText(city)
    show_city.setFont(Fonts.font_harmony)
    show_city.setStyleSheet("color: white")
    show_city.move(20, 90)

    '''
    在这里接续一下工作：
    1. set_blur是设置高斯模糊，需要将./resources/forMain/bar.png放置在卡片x = 0，y = 280处，然后应用模糊填充
    2. 天气图标./resources/forWeather/icon是展示未来三小时天气的，暂时不做
    3. 帮我改一下这堆史山
    '''
    aquaw.bind_child_widget_with_aqua_widget_qwidget(show_degree)
    return aquaw