# Authur: MnlSmile
# https://github.com/MnlSmile

import requests
import os
import re
import uuid
import hashlib
import wmi
import functools

from stdqt import *

CLIENT_SECRET = ''

def quickmap(**kwargs) -> dict:
    return kwargs

def cache(account:str, cs:str, expire_at:int) -> None:
    if not os.path.exists('./auth/temp'):
        os.mkdir('./auth/temp')
    with open('./auth/temp/cached', 'w', encoding='utf-8') as f:
        f.write(
            f"{account}\n{cs}\n{expire_at}"
        )

# 账密
def login(account:str, password:str) -> tuple[str, int]:
    data = quickmap(
        clientToken = str(uuid.uuid4()),
        account = account,
        signature = signature(account, password),
        devicedSignature = deviced_signature(account, password)
    )
    try:
        resp = requests.post('http://47.119.20.145:8000/api/v1/auth/login', json=data)
    except Exception:
        return None
    rmap = resp.json()
    if rmap['retcode'] == 10000:
        return rmap['data']['clientSecret'], rmap['data']['expireAt']
    elif rmap['retcode'] >= 40000:
        return 'Incorrect'
    else:
        return '', 0

# 缓存的 cs
def login_via_client_secret(account:str, cs:str) -> str:
    data = quickmap(
        clientToken = str(uuid.uuid4()),
        account = account,
        clientSecret = cs
    )
    try:
        resp = requests.post('http://47.119.20.145:8000/api/v1/auth/login_via_client_secret', json=data)
    except Exception:
        return None
    rmap = resp.json()
    if rmap['retcode'] == 10000:
        return rmap['data']['clientSecret'], rmap['data']['expireAt']
    elif rmap['retcode'] >= 40000:
        return 'Incorrect'
    else:
        return '', 0

# 已有签名
def login_via_signatures(account:str, _signature:str, _deviced_signature:str) -> str:
    data = quickmap(
        clientToken = str(uuid.uuid4()),
        account = account,
        signature = _signature,
        devicedSignature = _deviced_signature
    )
    try:
        resp = requests.post('http://47.119.20.145:8000/api/v1/auth/login', json=data)
    except Exception:
        return None
    rmap = resp.json()
    if rmap['retcode'] == 10000:
        return rmap['data']['clientSecret'], rmap['data']['expireAt']
    elif rmap['retcode'] >= 40000:
        return 'Incorrect'
    else:
        return '', 0

window = None  # 防止垃圾回收删掉 window

def md5(text:str) -> str:
    md5v = hashlib.md5(text.encode('utf-8')).hexdigest()
    return md5v

def neighexchange(text:str) -> str:
    if len(text) >= 2 and len(text) % 2 == 0:
        result = ''
        for i in range(int(len(text)/2)):
            result += text[ 2 * i + 1] + text[2 * i]
        return result
    else:
        return None

def get_device_uid() -> str:
    pc = wmi.WMI()
    id = ''
    atmp = pc.Win32_Processor()
    for cpu in atmp:
        id += cpu.ProcessorId.strip()
    for board in pc.Win32_BaseBoard():
        id += board.SerialNumber.strip()
    return id

def signature(account:str, password:str) -> str:
    if account == 'test@mnlsmile.com':
        return 'testsign========================'
    return md5(account + md5(neighexchange(password)))

def deviced_signature(account:str, password:str) -> str:
    if account == 'test@mnlsmile.com':
        return 'testdsign======================='
    return md5(account + md5(neighexchange(password)) + md5(get_device_uid()))

def user_login_flow() -> None:
    global window
    window = QWidget()
    window.setObjectName('loginwindow')
    window.setWindowTitle('登录')
    with open('./auth/login.css', 'r', encoding='utf-8') as f:
        _css = f.read()
    window.setStyleSheet(_css)
    window.setGeometry(500, 500, 500, 500)
    #window.setWindowOpacity(0.8)

    is_account_legal_label = QLabel(window)
    is_account_legal_label.setGeometry(100, 140, 300, 30)
    is_account_legal_label.setText('请在上框输入邮箱账号')
    account_input = QLineEdit(window)
    account_input.setGeometry(100, 100, 300, 30)
    def _check_account(text:str) -> None:
        if not re.search(r'^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.com$', text):
            is_account_legal_label.setText('账号不符合规范')
        else:
            is_account_legal_label.setText('')
    account_input.textChanged.connect(_check_account)

    is_password_legal_label = QLabel(window)
    is_password_legal_label.setGeometry(100, 240, 300, 30)
    is_password_legal_label.setText('请在上框输入密码')
    password_input = QLineEdit(window)
    password_input.setGeometry(100, 200, 300, 30)
    def _check_password(text:str) -> None:
        if not re.search(r'^[a-zA-Z0-9]{8}[a-zA-Z0-9]*$', text):
            is_password_legal_label.setText('密码不符合规范')
        else:
            is_password_legal_label.setText('')
    password_input.textChanged.connect(_check_password)

    login_button = QPushButton(window)
    login_button.setGeometry(170, 300, 160, 50)
    login_button.setText('登录')
    login_button.setObjectName('lgbtn')
    # 用猴子补丁重写事件处理方法
    def _mousePressEvent(self:QPushButton, e):
        self.setObjectName('QPushButtonPressed')
        self.setStyleSheet(_css)  # 刷新 qss
        return super(type(self), self).mousePressEvent(e)
    def _mouseReleaseEvent(self:QPushButton, e):
        self.setObjectName('lgbtn')
        self.setStyleSheet(_css)  # 刷新 qss
        return super(type(self), self).mouseReleaseEvent(e)
    login_button.mousePressEvent = functools.partial(_mousePressEvent, login_button)
    login_button.mouseReleaseEvent = functools.partial(_mouseReleaseEvent, login_button)

    def _login_action():
        client_secret, expire_at = login(
            account_input.text(),
            password_input.text()
        )
        CLIENT_SECRET = client_secret
        if client_secret:
            if client_secret == 'Incorrect':
                return
            else:
                cache(account_input.text(), client_secret, expire_at)
                window.close()
    login_button.clicked.connect(_login_action)

    window.show()