import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

app = QtWidgets.QApplication(sys.argv)
from widgets import genshin

def main():
    window = QWidget()
    window.setGeometry(760, 120, 300, 600)
    genshin.reg(window)
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()