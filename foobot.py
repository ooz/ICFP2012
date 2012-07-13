from minemap import Map

class Robot:
    def __init__(self, minemap):
        self.mmap    = minemap
        self.cmds    = ""
        self.lambdas = 0

    def getStepCount(self):
        return len(self.cmds)
    def getLambdaCount(self):
        return len(self.lambdas)

    def moveLeft(self):
        self.cmds += "L"
        return self
    def moveRight(self):
        self.cmds += "R"
        return self
    def moveUp(self):
        self.cmds += "U"
        return self
    def moveDown(self):
        self.cmds += "D"
        return self
    def wait(self):
        self.cmds += "W"
        return self
    def abort(self):
        self.cmds += "A"
        return self

    def execute(self, cmds):
        for c in cmds:
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

