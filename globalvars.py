class GlobalVars:
    def __init__(self):
        self.globalvars = {}

_global_instance = GlobalVars()

def globalvars():
    return _global_instance.globalvars