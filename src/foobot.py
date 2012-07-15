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

    def wouldGetKilledFor(self, cmds):
        bot = Robot(self.mmap.copy())
        for c in cmds:
            if (not bot.mmap.isTerminated()):
                bot.execute(c)
        return bot.mmap.isDead()

    """
    Only one move left? 
    ABORT if at least 1 lambda, 
     don't abort if no lambda and one lambda gettable with one step!
    """
    def meaningfulLastStep(self):
        if (self.mmap.getFoundLambdaCount() > 0):
            return ""
        reachable = self.mmap.inReach(92) # '\\'
        for move in reachable:
            if (not self.wouldGetKilledFor(move)):
                return move
        return ""

        

    """ Visual methods, separated to save one condition check :P """
    def executeVisual(self, cmds, sleepSecs = 0.0, 
                      printMap = False, printScore = False):
        for c in cmds:
            if (not self.mmap.isTerminated()):
                self.execute(c)
                time.sleep(sleepSecs)
                if printMap:
                    print ""
                    self.mmap.printCurrent()
                if printScore:
                    print "Score " + str(self.mmap.getScore())
        return self

    def solveVisual(self, sleepSecs = 0.0, printMap = False, printScore = False):
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



# TODO: update score formula!
#       even non-aborted runs yields full 50 pts per lambda
#       
"""
General
=======
* Don't die
* Don't block the lift with a rock (
* Never go for a lambda that needs more than 
  (#lambdas + 1) * 25 + 24 steps to get
 
Rocks
=====
* do not block lambdas with rocks
* do not block the lift with rocks
"""

from astar import AStar

class MrScaredGreedy(Robot):
    def solve(self):
        return self.solveVisual()

    def solveVisual(self, sleepSecs = 0.0, printEmptyLine = False, printScore = False):
        maxSteps = self.mmap.getMaxCommandCount()

        skip = []
        tar = None
        path = ""
        while (not self.mmap.isTerminated() and 
                self.mmap.getLeftCommands() > 1 and 
                (self.mmap.isLiftOpen() or 
                    len(skip) < self.mmap.getTotalLambdaCount()) and
                not (tar == self.mmap.getLift() and path == "")):
            if self.mmap.isLiftOpen():
                tar = self.mmap.getLift()
                aStar = AStar(self.mmap.copy(), tar)
                path = aStar.process().path()
            else:
                tars = []
                for l in self.mmap.getLambdas():
                    aStar = AStar(self.mmap.copy(), l)
                    path = aStar.process().path()
                    tars.append((l, path))
                minmin = reduce(lambda a, b: min(a, b), map(lambda t: len(t[1]), tars))
                tar, path = filter(lambda t: len(t[1]) == minmin, tars)[0]

            if (not self.wouldGetKilledFor(path) and 
                self.mmap.getLeftCommands() > len(path) and
                len(path) > 0):
                self.executeVisual(path, sleepSecs, printEmptyLine, printScore)
                skip = []
            else:
                skip.append(tar)

        if (not self.mmap.isTerminated()):
            """ Just """
            last = self.meaningfulLastStep()
            if last != "":
                self.executeVisual(last, sleepSecs, printEmptyLine, printScore)
            else:
                self.abort()
        if printScore:
            print "\nScore " + str(self.mmap.getScore())
        return self




