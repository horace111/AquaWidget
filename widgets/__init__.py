"""
"""

import traceback
import os
import importlib
import uuid
import asyncio
import typing

from stdqt import *

acquire_qwidget_from_func = lambda : None
main_window_widget_zone = None

def set_main_window_widget_zone(mw:QWidget) -> None:
    """
    主程序通过这个函数, 来设置 plugins 包应用的全局组件区对象.
    全局组件区对象是一个 QWidget, 所有 AquaWidget 对应的 QWidget 都是全局组件区的子组件.
    """
    global main_window_widget_zone
    main_window_widget_zone = mw

def set_qwidget_source(qw:callable) -> None:
    global acquire_qwidget_from_func
    """
    主程序通过这个函数, 来告知 widgets 各个组件应该通过何种函数来从主程序获取一个 QWidget 对象.
    """
    acquire_qwidget_from_func = qw
    
class AquaWidget():
    def __init__(self, scale:tuple=(200, 200)):
        self.width, self.height  = self.dx, self.dy = scale
        self._qw:QWidget = acquire_qwidget_from_func()  # 这个组件在主程序注册的 QWidget. 之后所有其他属于这个 AquaWidget 的子 Qt 组件都绑这个 QWidget.
        self._qw.setFixedSize(self.dx, self.dy)
        _qwon = str(uuid.uuid4())
        self._qw.setObjectName(_qwon)
        self._qw.setStyleSheet(f"QWidget#{_qwon}{'{'}border: 1px solid black;border-radius: 30px{'}'}")
        self._qw.setParent(main_window_widget_zone)
    def bind_child_widget_with_aqua_widget_qwidget(self, w:QWidget) -> None:  # 不允许子组件获取 self._qw, 否则其可以实现解绑主程序这种疯狂的举动
        """
        AquaWidget 通过这个方法, 来把自己需要用到的子组件绑到 AquaWidget 对应的 QWidget 上.
        """
        w.setParent(self._qw)
    def get_aqua_widget_qwidget(self) -> QWidget:  # 如果子组件执意要获取, 在此处通知用户
        return
    def move_aqua_widget_qwidget(self, ax:int, ay:int) -> None:
        """
        AquaWidget 通过这个方法, 来把自己对应的 QWidget 移动到某个位置上.
        """
        self._qw.move(ax, ay)

def scan() -> list[str]:
    """
    扫描所有组件并返回组件路径组成的列表.
    组件以 widgets 包的子库或子包的形式存在.
    """
    fl = os.listdir('./widgets')
    if fl != []:
        for fn in ['doc.md', '.git', '.gitignore', '.vscode', 'plugintools.py', 'README.md', '__pycache__', '__init__.py', 'temp', 'disabled']:
            if fn in fl: fl.remove(fn)
        widget_pymodule_names = []
        try:
            for p in fl:
                try:
                    widget_pymodule_names.append(f"widgets.{p.split('.')[0]}")
                except Exception:
                    pass
        except Exception:
            pass
        return widget_pymodule_names
    else:
        return []

def load_widgets() -> list:
    """
    加载所有组件.
    组件以 widgets 包的子库或子包的形式存在.
    """
    pl = scan()
    widget_pymodules = []
    for p in pl:
        try:
            widget_pymodules.append(importlib.import_module(p))
        except Exception as e:
            print(f"AquaWidget {p} failed to load({e}).")
    return widget_pymodules

async def a_load_widgets() -> list:
    """
    async
    加载所有组件.
    组件以 widgets 包的子库或子包的形式存在.
    """
    pl = scan()
    widget_pymodules = []
    for p in pl:
        try:
            _module = importlib.import_module(p)
            widget_pymodules.append(_module)
        except Exception as e:
            print(f"AquaWidget {p} failed to load({e}).")
    return widget_pymodules

widget_modules = load_widgets()
aqua_widgets:list[AquaWidget] = []

# Define acquire_func as a placeholder function
def _ac_func() -> QWidget:
    return acquire_qwidget_from_func()

def reg_all() -> None:
    """
    注册所有组件.
    组件以 widgets 包的子库或子包的形式存在.
    """
    for p in widget_modules:
        try:
            p.set_qwidget_source(_ac_func)
            aqua_widgets.append(p.reg())
        except Exception:
            print(f"组件 {p.__name__} 注册失败, 因为:")
            traceback.print_exc()
            print('\n')

async def a_reg_all() -> None:
    """
    async
    注册所有组件.
    组件以 widgets 包的子库或子包的形式存在.
    """
    for p in widget_modules:
        try:
            p.set_qwidget_source(_ac_func)
            _r = p.reg()
            if type(_r) == typing.Coroutine:
                pass
            aqua_widgets.append(_r)
        except Exception:
            print(f"组件 {p.__name__} 注册失败, 因为:")
            traceback.print_exc()
            print('\n')

def set_client_secret(_cs:str) -> None:
    """
    为所有组件设置 clientSecret.
    组件以 widgets 包的子库或子包的形式存在.
    """
    for p in widget_modules:
        try:
            p.set_client_secret(_cs)
        except Exception:
            print(f"组件 {p.__name__} 注册失败, 因为:")
            traceback.print_exc()
            print('\n')

def auto_lay_widgets() -> None:
    # 暂时无脑竖着排列
    deltaY = 15
    current_y = -15
    for aw in aqua_widgets:
        # aw.get_aqua_widget_qwidget().setParent(_w)  # 从初始化的时候就已经应该绑全局变量 main_window_widget_zone 了
        aw.move_aqua_widget_qwidget(0, current_y + deltaY)
        current_y += (aw.height + deltaY)
    main_window_widget_zone.setFixedSize(370, current_y + 15 + 15)  # 这样滚动到最底下的时候, 会留出 15px 的高度而非与底边相切, 同时消除初 current_y 设为 15 带来的影响

if __name__ == '__main__':
    print(scan())