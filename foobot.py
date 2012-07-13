from minemap import Map

class Robot:
    def __init__(self, minemap):
        self.mmap    = minemap
        self.lambdas = 0

    def getLambdaCount(self):
        return len(self.lambdas)

    def getCommands(self):
        return self.mmap.cmds

    def moveLeft(self):
        mmap.moveLeft()
        return self
    def moveRight(self):
        mmap.moveRight()
        return self
    def moveUp(self):
        mmap.moveUp()
        return self
    def moveDown(self):
        mmap.moveDown()
        return self
    def wait(self):
        mmap.wait()
        return self
    def abort(self):
        mmap.abort()
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

    def solve(self):
        return self

    def solve(self, tvmode)
        if (tvmode):
            return self.solve()
        pass
        

