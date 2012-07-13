class Map:
    def __init__(self, lines):
        self.initialLines = lines
        self.lines        = lines

        self.n = len(lines)
        if (self.n > 0):
            self.m = len(lines[0])

        # TODO: count lambdas on map
        self.__lambdas = 0
        self.__foundLambdas = 0

        self.history = ""
        

    def isAborted(self):
        return self.__aborted

    def get(self, x, y):
        if (x > 0 and y > 0 and x <= self.n and y <= self.m):
            return self.lines[x - 1][y - 1]
        return None

    def getSize(self):
        return (self.n, self.m)

    def getStepCount(self):
        return len(self.history)
    def getLambdaCount(self):
        return self.__lambdas
    def getFoundLambdaCount(self):
        return self.__foundLambdas

    def executeCommands(self, cmds):
        for c in cmds:
            pass

    def moveLeft(self):
        self.history += "L"
        return self
    def moveRight(self):
        self.history += "R"
        return self
    def moveUp(self):
        self.history += "U"
        return self
    def moveDown(self):
        self.history += "D"
        return self
    def wait(self):
        self.history += "W"
        return self
    def abort(self):
        self.history += "A"
        self.__aborted = True
        return self

    def update(self):
        return self

    def printInitial(self):
        for l in reversed(self.initialLines):
            print l
        return self
    def printCurrent(self):
        for l in reversed(self.lines):
            print l
        return self
    def printHistory(self):
        print self.history
        return self



    def printAll(self):
        """ Prints the initial and current map as well as the history """
        print "Init:"
        self.printInitial()
        print "\nNow:"
        self.printCurrent()
        print "\nHistory:"
        self.printHistory()
        return self

