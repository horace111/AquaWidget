"""
其实 Qt 有现成的托盘类, 但不想用
"""

import PIL.Image
import pystray
import threading

import PIL

def bind_menu_option(_d:dict) -> pystray.Menu:
    """
    将菜单选项和目标函数进行绑定.
    :param _d: dict
    键应为 str, 字段值应为函数引用.
    """
    return pystray.Menu(*(pystray.MenuItem(*item) for item in _d.items()))

def apply(_m:pystray.Menu) -> None:
    def _thread():
        tray_ico = PIL.Image.open('./resources/python-logo-only.png')
        tray = pystray.Icon('Aqua Widget', tray_ico, 'Aqua Widget\nNothing to show here', _m)
        tray.run()
    t = threading.Thread(target=_thread)
    t.daemon = True
    t.start()