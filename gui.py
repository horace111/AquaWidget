import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget,  QLabel, QVBoxLayout, QPlainTextEdit
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtGui import QFont


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
    def set_mainwindow(self):
        self.setWindowTitle("AquaWidget")
        self.setGeometry(100, 100, 400, 750)
    def background_ui(self):
        self.title = QLabel("AquaWidget", self)
        self.title.setFont(Fonts.font_harmony_title)
        self.title.move(15, 15)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Fonts.initialize()

    main_window = Main()
    main_window.show()

    sys.exit(app.exec_())