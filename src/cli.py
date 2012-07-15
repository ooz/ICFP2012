import os

def clear():
    """ Plattform independent console clear
    Stolen from:
    http://stackoverflow.com/questions/2084508/clear-terminal-in-python
    """
    os.system("cls" if os.name=="nt" else "clear")
