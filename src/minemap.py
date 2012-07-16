from constants import *

class Map:

    """ Constructor """
    def __init__(self, lines, metadata = [], cmds = "", found = 0, win = False, dead = False):
        self.initialGrid  = map(lambda l: bytearray(b"" + str(l)), lines)
        self.grid         = map(lambda l: bytearray(b"" + str(l)), lines)
        self.__updateGrid = None

        self.m = len(lines)
        if (self.m > 0):
            self.n = len(lines[0])

        self.__robot   = None
        self.__lift    = None
        self.__lambdas = []
        self.__found   = found
        self.cmds = cmds
        self.maxCmdCount = self.n * self.m

        if (len(metadata) == 6):
            self.water = metadata[0]
            self.flood = metadata[1]
            self.proof = metadata[2]
            self.growth = metadata[3]
            self.razors = metadata[4]
            self.trampos = metadata[5]
        else:
            self.water   = DEFAULT_WATER 
            self.flood   = DEFAULT_FLOOD 
            self.proof   = DEFAULT_PROOF 
            self.growth  = DEFAULT_GROWTH
            self.razors  = DEFAULT_RAZORS
            self.trampos = DEFAULT_TRAMPOS
        self.drown = self.proof

        self.__win  = win
        self.__dead = dead

        if not self.isValid():
            pass
#            raise Exception("Invalid map!")

    """ Copy """
    def copy(self):
        return Map(self.grid, 
                   [self.water, self.flood, self.proof], 
                   self.cmds, self.__found, self.__win, self.__dead)
    def copyInitial(self):
        return Map(self.initialGrid, 
                   [self.water, self.flood, self.proof])

    """ Map status """
    def isValid(self):
        """ Validation also locates the robot and counts all lambdas """
        lifts  = 0
        robots = 0
        for y in range(0, self.m):
            for x in range(0, self.n):
                c = self.grid[y][x]
                if c == ORD_ROBOT:
                    if robots == 0:
                        self.__robot = [x, y]
                    robots += 1
                elif c == ORD_CLOSED_LIFT:
                    self.__lift = (x, y)
                    lifts += 1
                elif c == ORD_OPEN_LIFT:
                    self.__lift = (x, y)
                    lifts += 2
                elif c == ORD_LAMBDA:
                    self.__lambdas.append((x, y))
        return (robots == 1 and lifts == 1)

    def isAborted(self):
        return self.cmds.endswith(CMD_ABORT)

    def isLiftOpen(self):
        return len(self.__lambdas) == 0

    def isCompleted(self):
        return self.__win
    
    def isDead(self):
        """ Either hit by a rock or drowned"""
        return self.__dead

    def isTerminated(self):
        return (self.isAborted() 
                or self.__win 
                or self.__dead
                    or (not self.hasCommandsLeft()))

    def hasCommandsLeft(self):
        return len(self.cmds) < self.maxCmdCount

    """ # Getters and setters """
    def getSize(self):
        return (self.n, self.m)

    def getCommands(self):
        return self.cmds
    def getLeftCommands(self):
        return self.maxCmdCount - len(self.cmds)
    def getCommandCount(self):
        return len(self.cmds)
    def getMaxCommandCount(self):
        return self.maxCmdCount

    def getScore(self):
        lambdaScore = self.__found * SCORE_LAMBDA_FOUND
        if (self.__win):
            lambdaScore += self.__found * SCORE_WIN_BONUS
        elif (not self.isDead()):
            lambdaScore += self.__found * SCORE_ABORT_BONUS
        return lambdaScore - len(self.cmds.replace(CMD_ABORT, ""))

    """ ## Robot stuff """
    def getRobot(self):
        return self.__robot
    def getLift(self):
        return self.__lift

    def getLambdas(self):
        return self.__lambdas
    def getTotalLambdaCount(self):
        return len(self.__lambdas)
    def getFoundLambdaCount(self):
        return self.__found

    def __updateGet(self, x, y):
        if (x >= 0 and y >= 0 and x < self.n and y < self.m):
            return self.__updateGrid[y][x]
        return None
    def get(self, x, y):
        if (x >= 0 and y >= 0 and x < self.n and y < self.m):
            return self.grid[y][x]
        return None
    def getChar(self, x, y):
        if (x >= 0 and y >= 0 and x < self.n and y < self.m):
            return chr(self.grid[y][x])
        return None

    """ Checks whether object (code) is in direct reach of the robot """
    def inReach(self, c):
        x = self.__robot[0]
        y = self.__robot[1]
        reach = []
        if self.get(x + 1, y) == c:
            reach.append(CMD_RIGHT)
        elif self.get(x - 1, y) == c:
            reach.append(CMD_LEFT)
        elif self.get(x, y + 1) == c:
            reach.append(CMD_UP)
        elif self.get(x, y - 1) == c:
            reach.append(CMD_DOWN)
        return reach

    # FIXME: Method doesnt make sense, therefore made private
    def __isStoppingRock(self, x, y):
        return (self.get(x, y) == ORD_EMPTY and self.get(x, y + 1) == ORD_ROCK)

    def __set(self, x, y, b):
        if (x >= 0 and y >= 0 and x < self.n and y < self.m):
            self.grid[y][x] = b
        return self
    def __setChar(self, x, y, c):
        if (x >= 0 and y >= 0 and x < self.n and y < self.m):
            self.grid[y][x] = ord(c)
        return self

    """ Update """
    def checkForRockKill(self, rockX, rockY):
        x = self.__robot[0]
        y = self.__robot[1]
        if (x == rockX and y + 1 == rockY):
            self.__dead = True

    def checkForWin(self):
        if (self.__win):
            self.__dead = False
        return self

    def update(self):
        self.__updateGrid = map(lambda l: bytearray(l), self.grid)

        for y in range(0, self.m):
            for x in range(0, self.n):
                c = self.__updateGet(x, y)
                if (c in [ORD_ROCK, ORD_HOROCK]): 
                    cc = self.__updateGet(x, y - 1)
                    if (cc == ORD_EMPTY):
                        """ Falling rock """
                        self.__set(x, y, ORD_EMPTY)
                        self.__set(x, y - 1, c)
                        self.checkForRockKill(x, y - 1)
                    elif (cc in [ORD_ROCK, ORD_HOROCK]):
                        cc  = self.__updateGet(x + 1, y)
                        ccc = self.__updateGet(x + 1, y - 1)
                        if (cc == ORD_EMPTY and ccc == ORD_EMPTY):
                            """ Right sliding rock """
                            self.__set(x    , y    , ORD_EMPTY)
                            self.__set(x + 1, y - 1, c)
                            self.checkForRockKill(x + 1, y - 1)
                        else:
                            cc  = self.__updateGet(x - 1, y)
                            ccc = self.__updateGet(x - 1, y - 1)
                            if (cc == ORD_EMPTY and ccc == ORD_EMPTY):
                                """ Left sliding rock """
                                self.__set(x    , y    , ORD_EMPTY)
                                self.__set(x - 1, y - 1, c)
                                self.checkForRockKill(x - 1, y - 1)

                    elif (cc == ORD_LAMBDA):
                        """ Rock sliding off lambda """
                        cc  = self.__updateGet(x + 1, y)
                        ccc = self.__updateGet(x + 1, y - 1)
                        if (cc == ORD_EMPTY and ccc == ORD_EMPTY):
                            """ Right sliding rock """
                            self.__set(x    , y    , ORD_EMPTY)
                            self.__set(x + 1, y - 1, c)
                            self.checkForRockKill(x + 1, y - 1)
                elif (c == ORD_CLOSED_LIFT):
                    if (0 == len(self.__lambdas)):
                        self.__set(x, y, ORD_OPEN_LIFT)
        self.checkForWin()
        return self

    """ Robot movement """
    def move(self, cmd):
        moved = False
        if cmd == CMD_LEFT:
            moved = self.__moveLR(-1)
        elif cmd == CMD_RIGHT:
            moved = self.__moveLR(1)
        elif cmd == CMD_DOWN:
            moved = self.__moveDU(-1)
        elif cmd == CMD_UP:
            moved = self.__moveDU(1)
        elif cmd == CMD_ABORT:
            self.cmds += CMD_ABORT
            return self
        if moved:
            self.cmds += cmd
        else:
            self.cmds += CMD_WAIT
        self.update()
        return self

    def __moveLR(self, xOffset):
        x = self.__robot[0]
        y = self.__robot[1]
        c = self.get(x + xOffset, y)
        if (c in [ORD_EMPTY, ORD_EARTH, ORD_LAMBDA, ORD_OPEN_LIFT]):
            self.__set(x, y, ORD_EMPTY)
            self.__set(x + xOffset, y, ORD_ROBOT)
            self.__robot[0] = x + xOffset
            if (c == ORD_LAMBDA):
                self.__collectLambda(x + xOffset, y)
            elif (c == ORD_OPEN_LIFT):
                self.__win = True
            return True
        elif (c in [ORD_ROCK, ORD_HOROCK]):
            cc = self.get(x + (xOffset * 2), y)
            if (cc == ORD_EMPTY):
                self.__set(x, y, ORD_EMPTY)
                self.__set(x + xOffset, y, ORD_ROBOT)
                self.__robot[0] = x + xOffset
                self.__set(x + (xOffset * 2), y, c)
                return True
        return False

    def __moveDU(self, yOffset):
        x = self.__robot[0]
        y = self.__robot[1]
        c = self.get(x, y + yOffset)
        if (c in [ORD_EMPTY, ORD_EARTH, ORD_LAMBDA, ORD_OPEN_LIFT]):
            self.__set(x, y, ORD_EMPTY)
            self.__set(x, y + yOffset, ORD_ROBOT)
            self.__robot[1] = y + yOffset
            if (c == ORD_LAMBDA):
                self.__collectLambda(x, y + yOffset)
            elif (c == ORD_OPEN_LIFT):
                self.__win = True
            return True
        return False

    def __collectLambda(self, x, y):
        self.__found += LAMBDA_FOUND_INCREMENT
        if (x, y) in self.__lambdas:
            self.__lambdas.remove((x, y))


    """ Printing """
    def printInitial(self):
        for l in reversed(self.initialGrid):
            print l
    def printCurrent(self):
        for l in reversed(self.grid):
            print l
    def printFlooding(self):
        print "Water " + str(self.water)
        print "Flooding " + str(self.flood)
        print "Waterproof " + str(self.proof)
    
    def printBeard(self):
        print "Growth " + str(self.growth)
        print "Razors " + str(self.razors)

    def printAll(self):
        print "Init:"
        self.printInitial()
        print "\nNow:"
        self.printCurrent()
        print ""
        self.printFlooding()
        print ""
        self.printBeard()
        return self

