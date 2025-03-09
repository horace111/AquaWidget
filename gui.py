import sys
from PyQt5.QtWidgets import QApplication, QWidget,  QLabel, QVBoxLayout, QPlainTextEdit
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtGui import QFont

class Fonts(QFont):
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
        
    def set_mainwindow(self):

        self.setWindowTitle("AquaWidget")
        self.setGeometry(100, 100, 400, 750)
    def background_ui(self):
        self.title = QLabel("AquaWidget", self)
        self.title.setFont(Fonts.font_harmony_title)
        self.title.move(15, 15)

app = QApplication(sys.argv)

main_window = Main()
main_window.set_mainwindow()
main_window.background_ui()
main_window.show()

sys.exit(app.exec_())