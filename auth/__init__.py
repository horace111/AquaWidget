import os
import traceback
import threading

import auth.avatar
import auth.login

from stdqt import *

CLIENT_SECRET = ''
client_secret_callback = None

def set_client_secret_callback(func) -> None:
    global client_secret_callback
    client_secret_callback = func

def quick_css_statement(selector:str, statements:dict) -> str:
    result = ''
    result += selector + ' {\n'
    for k,v in statements.items():
        result += f"    {k}: {v};\n"
    return result + '}'

def user_login_flow() -> str:
    return auth.login.user_login_flow()

class MainWindowHeader(QPushButton):
    static_unique_main_window_header_instance = None  # 这类的实例全局且唯一
    client_secret = ''

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.clicked.connect(auth.login.user_login_flow)
        self.headerImage = ''  # 和 Qt 命名格式一样
        self.setObjectName('MainWindowHeader')
        self.setMouseTracking(True)  # 否则 Qt 为了节省资源, 会仅在鼠标按下的时候跟踪
        self.setStyleSheet(
            f"""QPushButton#MainWindowHeader {'{'}
                border-image: url({self.headerImage});
                border: 1px solid black;
                border-radius: 30px
                {'}'}"""
        )  # 在 self.headerImage 有值前, 显示默认样式
        MainWindowHeader.static_unique_main_window_header_instance = self
        self._thread_onstart_auto_login()
    def setHeaderImageUrl(self, url:str) -> None:
        self.headerImage = url
        _s1 = quick_css_statement(
            'QPushButton#MainWindowHeader', {
                    'border-image': f'url({self.headerImage})',
                    'border': '1px solid black',
                    'border-radius': '30px'
                }
            )
        _s2 = quick_css_statement(
            'QPushButton#MainWindowHeader:hover', {
                    'border-image': f'url({self.headerImage})',
                    'border': '1px solid black',
                    'border-radius': '30px',
                }
            )
        self.default_css = f"{_s1}\n{_s2}"
        self.setStyleSheet(self.default_css)
        self.show()
    def mousePressEvent(self, e):
        self.setStyleSheet(
            """QPushButton#MainWindowHeader {
            background-color: black;
            border: 1px solid black;
            border-radius: 30px
            }"""
        )
        return super().mousePressEvent(e)
    def mouseReleaseEvent(self, e):
        self.setStyleSheet(
            self.default_css
        )
        return super().mouseReleaseEvent(e)
    def onstart_auto_login(self):
        try:
            if os.path.exists('./auth/temp/cached'):
                with open('./auth/temp/cached', 'r', encoding='utf-8') as f:
                    account, _cs, expire_at = f.read().split('\n')
                _cs, expire_at = auth.login.login_via_client_secret(account, _cs)
                if _cs and _cs != 'Incorrect':
                    CLIENT_SECRET = _cs
                    MainWindowHeader.client_secret = _cs
                    auth.login.cache(account, _cs, expire_at)
                    self.setHeaderImageUrl(auth.avatar.query(account))
        except Exception as e:
            traceback.print_exception(e)
            self.setHeaderImageUrl('')
            #auth.user_login_flow()
    def _thread_onstart_auto_login(self):
        threading.Thread(target=self.onstart_auto_login, daemon=True).start()