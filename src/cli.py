import os

def clear():
    """ Plattform independent console clear
    Stolen from:
    http://stackoverflow.com/questions/2084508/clear-terminal-in-python
    """
    os.system("cls" if os.name=="nt" else "clear")

def getChar():
    """ 
    !! DOES NOT WORK, IF STDIN WAS "CLOSED" WITH EOF IN THE SAME PROCESS !!
    Stolen from:
    http://python4fun.blogspot.de/2008/06/get-key-press-in-python.html
    """
    if (os.name == "nt"):
        import msvcrt
        return msvcrt.getch()
    else:
        import termios, sys
        TERMIOS = termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
        new[6][TERMIOS.VMIN] = 1
        new[6][TERMIOS.VTIME] = 0
        termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
        c = None
        try:
            c = os.read(fd, 1)
        finally:
            termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
        return c

