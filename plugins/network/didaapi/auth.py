import requests

import plugins

from plugins import plugintools
from plugintools import *

BASE_URL = 'mnlsmile.xyz'

# refer(f"./{__name__}/")

def auth() -> str:
    
    return

def login() -> None:
    r = requests.get(...)
    with refer(f"./{__name__}/user_token.txt", 'wb') as f:
        f.write(r.content)
    return

