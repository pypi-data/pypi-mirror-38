import os

def mkdirs(path):
    path = path.strip()
    path = path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    else:
        return False
