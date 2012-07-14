import time

from minemap import Map

class Robot:
    def __init__(self, minemap):
        self.mmap    = minemap

    def getMap(self):
        return self.mmap

    def getCommands(self):
        return self.mmap.cmds

    def moveLeft(self):
        self.mmap.moveLeft()
        return self
    def moveRight(self):
        self.mmap.moveRight()
        return self
    def moveUp(self):
        self.mmap.moveUp()
        return self
    def moveDown(self):
        self.mmap.moveDown()
        return self
    def wait(self):
        self.mmap.wait()
        return self
    def abort(self):
        self.mmap.abort()
        return self

    """ Visual methods, separated to save one condition check :P """
    def executeVisual(self, cmds, sleepSecs = 0.0, 
                      printEmptyLine = False, printScore = False):
        for c in cmds:
            if (not self.mmap.isTerminated()):
                self.execute(c)
                time.sleep(sleepSecs)
                if printEmptyLine:
                    print ""
                self.mmap.printCurrent()
                if printScore:
                    print "Score " + str(self.mmap.getScore())
        return self

    def solveVisual(self):
        self.mmap.printCurrent() 
        self.executeVisual("LDRDDUULLLDDL", 1.0, True, True)
        return self

    """ Normal execute and solve """
    def execute(self, cmds):
        for c in cmds:
            if (not self.mmap.isTerminated()):
                if c == "L":
                    self.moveLeft()
                elif c == "R":
                    self.moveRight()
                elif c == "U":
                    self.moveUp()
                elif c == "D":
                    self.moveDown()
                elif c == "W":
                    self.wait()
                elif c == "A":
                    self.abort()
        return self

    """ To override """
    def solve(self):
        return self


