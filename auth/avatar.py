import requests
from winenvvars import TEMP

def query(em:str) -> str:
    """
    Return value is the avatar path.
    """
    r = requests.get('http://47.119.20.145:82/v1/auth/avatar', params={"account": em})
    with open(f"{TEMP}/AquaWidget/user_avatar.png", 'wb') as f:
        f.write(r.content)
    # return f"{TEMP}/AquaWidget/{em}.png"
    return f"{TEMP}/AquaWidget/user_avatar.png"

# https://q.qlogo.cn/headimg_dl?dst_uin=986561577&spec=100&img_type=png