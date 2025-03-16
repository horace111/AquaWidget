import sys

import tray
import widgets

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtGui import QFont

import widgets.music_player


class Fonts():
    @staticmethod
    def initialize():
        fontdb = QtGui.QFontDatabase()
        _hms_ss_font_id = fontdb.addApplicationFont('./font/HarmonyOS_SansSC_Black.ttf')
        _hms_ssB_font_id = fontdb.addApplicationFont('./font/HarmonyOS_SansSC_Bold.ttf')

    font_harmony = QFont()
    font_harmony.setFamily("HarmonyOS Sans SC")
    font_harmony.setPointSize(12)
    font_harmony.setWeight(75)

    font_harmony_title = QFont()
    font_harmony_title.setFamily("HarmonyOS Sans SC")
    font_harmony_title.setPointSize(30)
    font_harmony_title.setWeight(200)

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.set_mainwindow()
        self.background_ui()
        self.stay_on_top()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    def set_mainwindow(self):
        self.setWindowTitle("AquaWidget")
        self.setGeometry(100, 100, 400, 750)
    def background_ui(self):
        self.title = QLabel("AquaWidget", self)
        self.title.setFont(Fonts.font_harmony_title)
        self.title.move(15, 15)
    def stay_on_top(self):
        self.sot = QCheckBox(parent=self)
        self.sot.setText('窗口置顶')
        self.sot.setChecked(True)
        def _oppo():
            self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, self.sot.isChecked())
            self.show()
            """
DeepSeek Reasoner 的解决方案:
            
            6. 替代方案：系统级置顶 API
通过调用操作系统 API 直接修改窗口属性（无需重建窗口），但需跨平台适配：

# Windows 示例(需 pywin32)
if sys.platform == "win32":
    import win32gui
    import win32con

    def toggle_stay_on_top_win(state):
        hwnd = self.winId().__int__()
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        if state:
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, 
                win32con.SWP_NOMOVE | win32
            """
        self.sot.stateChanged.connect(_oppo)
    def closeEvent(self, a0) -> None:  # self.close() 以任何形式被调用时, 都只隐藏而不退出
        self.hide()
        a0.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Fonts.initialize()

    main_window = Main()

    def _acquire_qw() -> QWidget:
        return QWidget()
    
    widgets.set_main_window(main_window)
    widgets.set_acquire_func(_acquire_qw)
    widgets.reg_all()
    widgets.auto_lay_widgets()

    def _ra(): main_window.stay_on_top(); main_window.show()
    def _qu(): app.quit()
    mo = tray.bind_menu_option(
        {
            '主程序': _ra,
            '音乐示例': lambda:widgets.music_player.music_player_plugin.quick_play('D:\\python_works\\obs\\大喜.flac'),
            '退出': _qu
        }
    )
    tray.apply(mo)
    
    main_window.show()

    sys.exit(app.exec_())