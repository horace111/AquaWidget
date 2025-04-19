import requests

from stdqt import *

qwidget = None

def set_qwidget_source(func) -> None:
    global qwidget
    """
    该函数在 widgets/__init__.py 中自动调用. 通过调用 acquire_func(), 可以从主程序获取一个 QWidget() 对象.
    """
    qwidget = func

def login() -> None:
    pass

def user_login_flow() -> None:
    window:QWidget = qwidget()
    window.setGeometry()