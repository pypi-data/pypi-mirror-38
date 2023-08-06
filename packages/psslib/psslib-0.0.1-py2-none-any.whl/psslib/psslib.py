import easygui
import os

def spc(password):
    """asks for password
used for making password files."""
    if easygui.enterbox('enter password:-') != password:
        os.system("shutdown /s /t 1")
    else:
        pass
def src():
    """shutdown the computer """
    os.system("shutdown /s /r 1")
def error(message):
    sys.stderr.write(message)
    os.system("shutdown /s /t 1")