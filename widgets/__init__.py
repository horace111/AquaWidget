"""
"""

import threading
import os
import importlib
import uuid

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget

acquire_func = lambda x: None
main_window = None

def set_main_window(mw:QWidget) -> None:
    global main_window
    main_window = mw

def set_acquire_func(qw) -> None:
    global acquire_func
    """
    主程序通过这个函数, 来告知 widgets 各个组件应该通过何种函数来从主程序获取一个 QWidget 对象.
    """
    acquire_func = qw

class AquaWidget():
    def __init__(self, scale:tuple=(200, 200)):
        self.width, self.height  = self.dx, self.dy = scale
        self.qw:QtWidgets.QWidget = acquire_func()  # 这个组件在主程序注册的 QWidget. 之后所有其他 Qt 组件都绑这个 QWidget.
        self.qw.setFixedSize(self.dx, self.dy)
        qwon = str(uuid.uuid4())
        self.qw.setObjectName(qwon)
        self.qw.setStyleSheet(f"QWidget#{qwon}{'{'}border: 1px solid black;border-radius: 30px{'}'}")
    def aqua_set_parent(self, parent=QtWidgets.QWidget) -> None:
        self.aqua_parent = parent
    def get_aqua_widget(self) -> QtWidgets.QWidget:
        return self.qw
    def move(self, ax:int, ay:int) -> None:
        self.qw.move(ax, ay)

def scan() -> list:
    fl = os.listdir('./widgets')
    for fn in ['doc.md', '.git', '.gitignore', '.vscode', 'plugintools.py', 'README.md', '__pycache__', '__init__.py', 'temp', 'disabled']:
        if fn in fl: fl.remove(fn)
    widgets = [f"widgets.{p.split('.')[0]}" for p in fl]
    return widgets

def load_widgets() -> None:
    pl = scan()
    return [importlib.import_module(p) for p in pl]

widget_modules = load_widgets()
aqua_widgets:list[AquaWidget] = []

def reg_all() -> None:
    for p in widget_modules:
        p.set_acquire_func(acquire_func)
        aqua_widgets.append(p.reg())

def auto_lay_widgets(_w:QWidget) -> None:
    # 暂时无脑竖着排列
    deltaY = 15
    current_y = -15
    for aw in aqua_widgets:
        aw.get_aqua_widget().setParent(_w)
        aw.move(0, current_y + deltaY)
        current_y += (aw.height + deltaY)
    _w.setFixedSize(370, current_y + 15 + 15)  # 这样滚动到最底下的时候, 会留出 15px 的高度而非与底边相切, 同时消除初 current_y 设为 15 带来的影响

if __name__ == '__main__':
    print(scan())