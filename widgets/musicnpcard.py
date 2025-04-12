import sys
import threading
import asyncio
#import pywss

from widgets import AquaWidget
from stdqt import *

acquire_func = None

def set_qwidget_source(func) -> None:
    global acquire_func
    """
    该函数在 widgets/__init__.py 中自动调用. 通过调用 acquire_func(), 可以从主程序获取一个 QWidget() 对象.
    """
    acquire_func = func

def acquire() -> QWidget:
    return acquire_func()

class WsServer(QWebSocketServer):
    clients:list[QWebSocket] = []
    pcp = clients
    clientConnectionChanged = pyqtSignal()
    def __init__(self, serverName, secureMode, parent = ...):
        super().__init__(serverName, secureMode, parent)
        self.newConnection.connect(self._new_connection)
    def _new_connection(self) -> None:
        client = self.nextPendingConnection()
        self.clientConnectionChanged.emit()
        def _lost_connection():
            self.clientConnectionChanged.emit()
            WsServer.pcp.remove(client)
            print('NP: 有一个连接断开了')
            print(f"NP: 连接数: {len(WsServer.pcp)}")
        client.disconnected.connect(_lost_connection)
        WsServer.pcp.append(client)
        print('NP: 收到新连接')
        print(f"NP: 连接数: {len(WsServer.pcp)}")
        client.sendTextMessage("MusicNPCard Accepted Your Connection.")
        

def quick_send(msg:str) -> None:
    for c in WsServer.pcp:
        #if c.state():
            c.sendTextMessage(msg)

def pause_play_music() -> None:
    quick_send('play/pause')

def qwsserver(qws:QWebSocketServer):
    qws.listen(QHostAddress("127.0.0.1"), 6377)
        
def reg() -> AquaWidget:
    global acquire_func
    """
    widgets 入口函数.
    """
    aquaw = AquaWidget(scale=(370, 120))
    qws = WsServer('music_np_card_server', QWebSocketServer.SslMode.NonSecureMode, None)
    aquaw.bind_child_widget_with_aqua_widget_qwidget(qws)

    client_connection_status = QLabel('无客户端连接')
    aquaw.bind_child_widget_with_aqua_widget_qwidget(client_connection_status)
    def _client_changed():
        if len(WsServer.pcp) == 0:
            client_connection_status.setText('无客户端连接')
        else:
            client_connection_status.setText(f'有 {len(WsServer.pcp)} 个客户端连接')
    qws.clientConnectionChanged.connect(_client_changed)

    button1 = QPushButton('Play/Pause NP')
    aquaw.bind_child_widget_with_aqua_widget_qwidget(button1)
    button1.setGeometry(30, 30, 140, 50)
    button1.clicked.connect(pause_play_music)

    qwsserver(qws)

    return aquaw

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = QWidget()
    qws = QWebSocketServer(mw)
    asyncio.run(qwsserver(qws))
    mw.show()
    app.exec()