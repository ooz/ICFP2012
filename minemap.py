class Map:
    def __init__(self, lines, metadata = None):
        self.initialLines = lines
        self.lines        = lines

        self.m = len(lines)
        if (self.m > 0):
            self.n = len(lines[0])

        self.__lambdas = 0
        self.__found   = 0
        self.__robot   = None

        if (metadata != None and len(metadata) == 3):
            self.water = metadata[0]
            self.flood = metadata[1]
            self.proof = metadata[2]
        else:
            self.water = 0
            self.flood = 0
            self.proof = 10

#        if not self.isValid():
#            raise Exception("Invalid map!")

    """ Map status """
    def isValid(self):
        """ Validation also locates the robot and counts all lambdas """
        lifts  = 0
        robots = 0
        for y in range(0, self.m):
            for x in range(0, self.n):
                c = self.lines[y][x]
                if c == 'R':
                    if robots == 0:
                        self.__robot = (x, y)
                    robots += 1
                elif c == 'L':
                    lifts += 1
                elif c == 'O':
                    lifts += 2
                elif c == '\\':
                    self.__lambdas += 1
        return (robots == 1 and lifts == 1)

    def isAborted(self):
        return self.cmds.endswith("A")

    def isCompleted(self):
        pass
    
    def isDead(self):
        """ Either hit by a rock or drowned"""
        pass


    """ Getters and setters """
    def getSize(self):
        return (self.n, self.m)

    def getRobot(self):
        return self.__robot

    def getTotalLambdas(self):
        return self.__lambdas
    def getFoundLambdas(self):
        return self.__found

    def get(self, x, y):
        if (x >= 0 and y >= 0 and x < self.n and y < self.m):
            return self.lines[y][x]
        return None

    def set(self, x, y, c):
        if (x >= 0 and y >= 0 and x < self.n and y < self.m):
            self.lines[y][x] = c
        return self

    """ Update """
    def update(self):
        return self

    """ Printing """
    def printInitial(self):
        for l in reversed(self.initialLines):
            print l
        return self
    def printCurrent(self):
        for l in reversed(self.lines):
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
        if (c in [' ', '.', '\\', "O"]):
            self.set(x, y, ' ')
            self.set(x, y - 1, 'R')
            if (c == '\\'):
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

