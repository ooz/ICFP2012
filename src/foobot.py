import time

from constants import *
import cli
from minemap import Map

class Robot:
    def __init__( self, minemap
                , options = [0.0, False, False]
                ):
        self.mmap    = minemap
        self.sleep = options[0]
        self.displ = options[1]
        self.clear = options[2]

    def getMap(self):
        return self.mmap

    def getCommands(self):
        return self.mmap.cmds

    def wouldGetKilledFor(self, cmds):
        bot = Robot(self.mmap.copy())
        for c in cmds:
            if (not bot.mmap.isTerminated()):
                bot.execute(c)
        return bot.mmap.isDead()

    def execute(self, cmds):
        for c in cmds:
            if (not self.mmap.isTerminated()):
                self.mmap.move(c)
        return self

    def executeVisual(self, cmds):
        for c in cmds:
            if (not self.mmap.isTerminated()):
                self.mmap.move(c)
                time.sleep(self.sleep)
                if self.clear:
                    cli.clear()
                if self.displ:
                    print ""
                    self.mmap.printCurrent()
                    print "Score " + str(self.mmap.getScore())
        return self

    def solve(self):
        while (not self.mmap.isTerminated()):
            self.step(self.execute)
        return self

    def solveVisual(self):
        while (not self.mmap.isTerminated()):
            self.step(self.executeVisual)
        return self

    """ To override """
    def step(self, execute):
        return execute(CMD_ABORT)

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
    def __init__( self, minemap
                , options = [0.0, False, False]
                ):
        Robot.__init__(self, minemap, options)

        self.skip = []
        self.tar = None
        self.path = ""

    def step(self, execute):
        if self.mmap.isLiftOpen():
            self.tar = self.mmap.getLift()
            aStar = AStar(self.mmap.copy(), tar)
            self.path = aStar.process().path()
        else:
            self.tars = []
            for l in self.mmap.getLambdas():
                aStar = AStar(self.mmap.copy(), l)
                self.path = aStar.process().path()
                self.tars.append((l, self.path))
            minmin = reduce(lambda a, b: min(a, b), map(lambda t: len(t[1]), self.tars))
            self.tar, self.path = filter(lambda t: len(t[1]) == minmin, self.tars)[0]

        if (not self.wouldGetKilledFor(self.path) and 
            self.mmap.getLeftCommands() > len(self.path) and
            len(self.path) > 0):
            execute(self.path)
            self.skip = []
        else:
            self.skip.append(self.tar)

        return self




