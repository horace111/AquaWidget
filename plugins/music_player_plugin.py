from PyQt5.QtMultimedia import *
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication

def quick_play(fp:str, parent:QApplication) -> QMediaPlayer:
    qmp = QMediaPlayer(parent=parent)
    qmp.setMedia(QMediaContent(QUrl.fromLocalFile(fp)))
    qmp.setVolume(30)
    qmp.play()
    return qmp

if __name__ == '__main__':
    quick_play('D:\\python_works\\obs\\大喜.flac')