import sys
import uuid
import threading
import asyncio
import asyncqt
import time
import traceback
import win32gui
import win32con

from globalvars import globalvars
import auth.avatar
import widgets
import auth

from winenvvars import TEMP, APPDATA

from stdqt import *

app = QApplication(sys.argv)

el = asyncqt.QEventLoop(app)
asyncio.set_event_loop(el)

CLIENT_SECRET = ''
def set_client_secret(_cs:str) -> None:
    global CLIENT_SECRET
    CLIENT_SECRET = _cs
def get_client_Secret() -> str:
    return CLIENT_SECRET

class Fonts():
    @staticmethod
    def initialize():
        fontdb = QtGui.QFontDatabase()
        _hms_ssBB_font_id = fontdb.addApplicationFont('./font/HarmonyOS_SansSC_Black.ttf')
        _hms_ssB_font_id = fontdb.addApplicationFont('./font/HarmonyOS_SansSC_Bold.ttf')

    font_harmony = QFont()
    font_harmony.setFamily("HarmonyOS Sans SC Black")
    font_harmony.setPointSize(12)

    font_harmony_title = QFont()
    font_harmony_title.setFamily("HarmonyOS Sans SC Black")
    font_harmony_title.setPointSize(30)

class Main(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName('MainWindow')
        self.setup_widget_zone()
        self.setup_mainwindow(100, 100, 400, 750)
        self.hwnd = None  # Initialize hwnd to None
        self.setup_background_ui()
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setup_header()
        self.setWindowIcon(QIcon("./resources/forMain/icon/aquawidget_round_square_icon.svg"))
        self.stay_on_top()
    def setup_global_qss(self) -> None:
        try:
            with open('./gui.css', 'r', encoding='utf-8') as f:
                self._global_css = self._global_qss = f.read()
                self.setStyleSheet(self._global_css)
        except Exception as e:
            print('主程序样式表无法载入, 因为:\n' + traceback.print_exception(e))
    def setup_mainwindow(self, x, y, dx, dy):
        self.setWindowTitle("AquaWidget")
        self.move(x, y)
        self.setFixedSize(dx, dy)
    def setup_background_ui(self):
        self.title = QLabel("AquaWidget", self)
        self.title.setFont(Fonts.font_harmony_title)
        self.title.setGeometry(15, 15, 370, 60)
    def setup_widget_zone(self):
        self.wz_scrollarea = QScrollArea(self)
        self.wz_scrollarea.setGeometry(15 - 1, 60 + 15, 370 + 2, 690)
        self.wz_scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.wz_scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.wz_scrollarea.setObjectName(str(uuid.uuid4()))
        self.wz_scrollarea.setFrameStyle(QFrame.NoFrame)
        self.widget_zone = QWidget(self.wz_scrollarea)
        self.widget_zone.setGeometry(0, 0, 370, 0)
        self.wz_scrollarea.setWidget(self.widget_zone)
    def change_wz_size(self, dx, dy):
        self.widget_zone.setGeometry(0, 0, dx, dy)
    # Removed redundant stay_on_top method definition
    def stay_on_top(self):
        self.sot = QCheckBox(parent=self)
        self.sot.setText('窗口置顶')
        self.sot.setChecked(True)
        def _oppo(state):
            if self.hwnd:
                if state == Qt.Checked:
                    win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
                else:
                    win32gui.SetWindowPos(self.hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        self.sot.stateChanged.connect(_oppo)
    def show(self) -> None:
        super().show()
        self.hwnd = win32gui.FindWindow(None, self.windowTitle())
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    def setApp(self, app:QApplication) -> None:
        self.app = app
    def setup_sys_tray(self) -> None:
        self.oTraymenu = QMenu('AquaWidget', parent=self)
        self.oTraymenu.setWindowFlag(Qt.FramelessWindowHint, True)
        self.oTraymenu.setWindowFlag(Qt.NoDropShadowWindowHint, True)
        _ac = QAction('退出', parent=self)
        _ac.triggered.connect(self.app.quit)
        self.oTraymenu.addAction(_ac)

        self.tray = QSystemTrayIcon(self)
        globalvars()['tray'] = self.tray
        self.tray.setIcon(QIcon("./resources/forMain/icon/aquawidget_round_square_icon.svg"))
        self.tray.setToolTip('AquaWidget')
        self.tray.setContextMenu(self.oTraymenu)
        self.tray.activated.connect(self._activate_by_tray)
        self.tray.show()
    def setup_header(self) -> None:
        self.header = auth.MainWindowHeader(self)
        self.header.setGeometry(400 - 15 - 60, 15, 60, 60)
    def _activate_by_tray(self, reason:QSystemTrayIcon.ActivationReason) -> None:
        if reason == 2:  # 只响应双击
            self.show()
    def closeEvent(self, a0) -> None:  # self.close() 以任何形式被调用时, 都只隐藏而不退出
        a0.accept()
        '''self.hide()
        a0.ignore()'''  # 为了方便开发

main_window:Main = None

def main():
    global main_window
    Fonts.initialize()

    main_window = Main()
    globalvars()['main_window'] = main_window

    def _acquire_qw() -> QWidget:
        return QWidget()
    
    widgets.set_qwidget_source(_acquire_qw)
    widgets.set_main_window_widget_zone(main_window.widget_zone)
    widgets.reg_all()
    widgets.auto_lay_widgets()

    main_window.setApp(app)
    main_window.setup_sys_tray()

    main_window.setup_global_qss()
    main_window.show()

    auth.set_client_secret_callback(set_client_secret)

    main_window.header.setup_menu(main_window)

    widgets.set_qwidget_source(_acquire_qw)
    widgets.set_main_window_widget_zone(main_window.widget_zone)
    widgets.reg_all()
    widgets.auto_lay_widgets()

    sys.exit(app.exec())
    #sys.exit(el.run_forever())

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(-1)