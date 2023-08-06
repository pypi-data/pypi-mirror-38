import sys

def myinput(desc):
    if sys.version_info > (2, 7):
        return input(desc)
    else:
        return raw_input(desc)
