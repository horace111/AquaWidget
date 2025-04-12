import sys

from widgets import AquaWidget
from stdqt import *

acquire_func = None

def set_qwidget_source(func) -> None:
    global acquire_func
    """
    该函数在 widgets/__init__.py 中自动调用. 通过调用 acquire_func(), 可以从主程序获取一个 QWidget() 对象.
    """
    acquire_func = func

def reg() -> AquaWidget:
    global acquire_func
    """
    widgets 入口函数.
    """
    aquaw = AquaWidget(scale=(370, 120))
    text1 = QLabel('我要玩原神！')
    aquaw.bind_child_widget_with_aqua_widget_qwidget(text1)

    return aquaw