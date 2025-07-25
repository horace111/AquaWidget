import sys
import threading

from plugins import music_player_plugin
from widgets import AquaWidget
from stdqt import *

acquire_func = None

CLIENT_SECRET = ''
def set_client_secret(_cs:str) -> None:
    global CLIENT_SECRET
    CLIENT_SECRET = _cs

def set_qwidget_source(func) -> None:
    global acquire_func
    """
    该函数在 widgets/__init__.py 中自动调用. 通过调用 acquire_func(), 可以从主程序获取一个 QWidget() 对象.
    """
    acquire_func = func

def acquire() -> QWidget:
    return acquire_func()

def reg() -> AquaWidget:
    global acquire_func
    """
    widgets 入口函数.
    """
    aquaw = AquaWidget(scale=(370, 120))

    button1 = QPushButton('Play/Pause')
    aquaw.bind_child_widget_with_aqua_widget_qwidget(button1)
    button1.setGeometry(30, 30, 140, 50)
    button1.clicked.connect(lambda a0: music_player_plugin.win_med_quick_playing_status_switch())

    return aquaw