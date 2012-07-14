SCORE_LAMBDA_FOUND = 25
SCORE_ABORT_BONUS  = 25
SCORE_WIN_BONUS    = 50
SCORE_STEP_COST    = 1

class Map:
    def __init__(self, lines, metadata = None):
        self.initialGrid  = map(lambda l: bytearray(b"" + l), lines)
        self.grid         = map(lambda l: bytearray(b"" + l), lines)
        self.__updateGrid = None

        self.m = len(lines)
        if (self.m > 0):
            self.n = len(lines[0])

        self.__lambdas = []
        self.__found   = 0
        self.__robot   = None
        self.cmds = ""
        self.maxCmdCount = self.n * self.m

        if (metadata != None and len(metadata) == 3):
            self.water = metadata[0]
            self.flood = metadata[1]
            self.proof = metadata[2]
        else:
            self.water = 0
            self.flood = 0
            self.proof = 10
        self.drown = self.proof

        self.__win  = False
        self.__dead = False

        if not self.isValid():
            pass
#            raise Exception("Invalid map!")

    """ Map status """
    def isValid(self):
        """ Validation also locates the robot and counts all lambdas """
        lifts  = 0
        robots = 0
        for y in range(0, self.m):
            for x in range(0, self.n):
                c = self.grid[y][x]
                if c == 82:   # 'R'
                    if robots == 0:
                        self.__robot = [x, y]
                    robots += 1
                elif c == 76: # 'L'
                    lifts += 1
                elif c == 79: # 'O'
                    lifts += 2
                elif c == 92: # '\\'
                    self.__lambdas.append((x, y))
        return (robots == 1 and lifts == 1)

    def isAborted(self):
        return self.cmds.endswith("A")

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

    """ Getters and setters """
    def getSize(self):
        return (self.n, self.m)

    def getCommands(self):
        return self.cmds
    def getMaxCommandCount(self):
        return self.maxCmdCount

    def getScore(self):
        lambdaScore = self.__found * SCORE_LAMBDA_FOUND
        if (self.__win):
            lambdaScore += self.__found * SCORE_WIN_BONUS
        elif (self.isAborted()):
            lambdaScore += self.__found * SCORE_ABORT_BONUS
        return lambdaScore - len(self.cmds)

    def getRobot(self):
        return self.__robot

    def getLambdaPositions(self):
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

    def set(self, x, y, b):
        if (x >= 0 and y >= 0 and x < self.n and y < self.m):
            self.grid[y][x] = b
        return self
    def setChar(self, x, y, c):
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
                if (c == 42):                  # '*'
                    cc = self.__updateGet(x, y - 1)
                    if (cc == 32):             # ' '
                        """ Falling rock """
                        self.set(x, y, 32)     # ' '
                        self.set(x, y - 1, 42) # '*'
                        self.checkForRockKill(x, y - 1)
                    elif (cc == 42):           # '*'
                        cc  = self.__updateGet(x + 1, y)
                        ccc = self.__updateGet(x + 1, y - 1)
                        if (cc == 32 and ccc == 32):
                            """ Right sliding rock """
                            self.set(x    , y    , 32) # ' '
                            self.set(x + 1, y - 1, 42) # '*'
                            self.checkForRockKill(x + 1, y - 1)
                        else:
                            cc  = self.__updateGet(x - 1, y)
                            ccc = self.__updateGet(x - 1, y - 1)
                            if (cc == 32 and ccc == 32):
                                """ Left sliding rock """
                                self.set(x    , y    , 32) # ' '
                                self.set(x - 1, y - 1, 42) # '*'
                                self.checkForRockKill(x - 1, y - 1)

                    elif (cc == 92):           # '\\'
                        """ Rock sliding off lambda """
                        cc  = self.__updateGet(x + 1, y)
                        ccc = self.__updateGet(x + 1, y - 1)
                        if (cc == 32 and ccc == 32):
                            """ Right sliding rock """
                            self.set(x    , y    , 32) # ' '
                            self.set(x + 1, y - 1, 42) # '*'
                            self.checkForRockKill(x + 1, y - 1)
                elif (c == 76):            # 'L'
                    if (self.__found == len(self.__lambdas)):
                        self.set(x, y, 79) # 'O'
        self.checkForWin()
        return self

    """ Robot movement """
    def moveLeft(self):
        x = self.__robot[0]
        y = self.__robot[1]
        c = self.get(x - 1, y)
        if (c in [32, 46, 92, 79]): # ' ', '.', '\\', "O"
            self.set(x, y, 32)      # ' '
            self.set(x - 1, y, 82)  # 'R'
            self.__robot[0] = x - 1
            if (c == 92):
                self.__found += 1
            elif (c == 79):
                self.__win = True
            self.cmds += "L"
        elif (c == 42):             # '*'
            cc = self.get(x - 2, y)
            if (cc == 32):          # ' '
                self.set(x, y, 32)      # ' '
                self.set(x - 1, y, 82)  # 'R'
                self.__robot[0] = x - 1
                self.set(x - 2, y, 42)  # '*'
                self.cmds += "L"
            else:
                self.cmds += "W"
        else:
            self.cmds += "W"
        self.update()
        return self

    def moveRight(self):
        x = self.__robot[0]
        y = self.__robot[1]
        c = self.get(x + 1, y)
        if (c in [32, 46, 92, 79]): # ' ', '.', '\\', "O"
            self.set(x, y, 32)      # ' '
            self.set(x + 1, y, 82)  # 'R'
            self.__robot[0] = x + 1
            if (c == 92):
                self.__found += 1
            elif (c == 79):
                self.__win = True
            self.cmds += "R"
        elif (c == 42):             # '*'
            cc = self.get(x + 2, y)
            if (cc == 32):          # ' '
                self.set(x, y, 32)      # ' '
                self.set(x + 1, y, 82)  # 'R'
                self.__robot[0] = x + 1
                self.set(x + 2, y, 42)  # '*'
                self.cmds += "R"
            else:
                self.cmds += "W"
        else:
            self.cmds += "W"
        self.update()
        return self

    def moveUp(self):
        x = self.__robot[0]
        y = self.__robot[1]
        c = self.get(x, y + 1)
        if (c in [32, 46, 92, 79]): # ' ', '.', '\\', "O"
            self.set(x, y, 32)      # ' '
            self.set(x, y + 1, 82)  # 'R'
            self.__robot[1] = y + 1
            if (c == 92):
                self.__found += 1
            elif (c == 79):
                self.__win = True
            self.cmds += "U"
        else:
            self.cmds += "W"
        self.update()
        return self

    def moveDown(self):
        x = self.__robot[0]
        y = self.__robot[1]
        c = self.get(x, y - 1)
        if (c in [32, 46, 92, 79]): # ' ', '.', '\\', "O"
            self.set(x, y, 32)      # ' '
            self.set(x, y - 1, 82)  # 'R'
            self.__robot[1] = y - 1
            if (c == 92):
                self.__found += 1
            elif (c == 79):
                self.__win = True
            self.cmds += "D"
        else:
            self.cmds += "W"
        self.update()
        return self

    def wait(self):
        self.cmds += "W"
        self.update()
        return self

    def abort(self):
        self.cmds += "A"
        return self


    """ Printing """
    def printInitial(self):
        for l in reversed(self.initialGrid):
            print l
        return self
    def printCurrent(self):
        for l in reversed(self.grid):
            print l
        return self
    def printFlooding(self):
        print "Water " + str(self.water)
        print "Flooding " + str(self.flood)
        print "Waterproof " + str(self.proof)

    def printAll(self):
        print "Init:"
        self.printInitial()
        print "\nNow:"
        self.printCurrent()
        print ""
        self.printFlooding()
        return self

