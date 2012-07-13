class Map:
    def __init__(self, lines, metadata = None):
        self.initialGrid = map(lambda l: bytearray(b"" + l), lines)
        self.grid        = self.initialGrid

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
        pass
    
    def isDead(self):
        """ Either hit by a rock or drowned"""
        pass

    def isTerminated(self):
        return (self.isAborted() 
                or self.isCompleted() 
                or self.isDead() 
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


    def getRobot(self):
        return self.__robot

    def getLambdaPositions(self):
        return self.__lambdas
    def getTotalLambdaCount(self):
        return len(self.__lambdas)
    def getFoundLambdaCount(self):
        return self.__found

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
    def update(self):
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

    """ Robot movement """
    def moveLeft(self):
        self.cmds += "L"
        self.update()
        return self
    def moveRight(self):
        self.cmds += "R"
        self.update()
        return self
    def moveUp(self):
        self.cmds += "U"
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

