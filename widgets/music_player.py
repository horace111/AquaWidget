import sys
import threading

from plugins import music_player_plugin
from widgets import AquaWidget
from stdqt import *

acquire_func = None

def set_acquire_func(func) -> None:
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


    '''
    app = QApplication(sys.argv)

    sub_window = QWidget()
    sub_window.setFixedSize(400, 400)
    
    def _sub_window_exec() -> None:
        sub_window.show()
        t = threading.Thread(target=app.exec)
        t.start()
    '''

    fp = './resources/大喜.flac'
    def _quick_play() -> None:
        player = music_player_plugin.quick_play(fp, parent=aquaw.get_aqua_widget())
    
    # 一个播放按钮
    button1 = QPushButton('Play', parent=aquaw.get_aqua_widget())
    button1.setGeometry(30, 30, 140, 50)
    button1.clicked.connect(_quick_play)

    return aquaw