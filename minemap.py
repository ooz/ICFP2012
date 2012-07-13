class Map:
    def __init__(self, lines, metadata = None):
        self.initialLines = lines
        self.lines        = lines

        self.m = len(lines)
        if (self.m > 0):
            self.n = len(lines[0])

        # TODO: count lambdas on map
        self.__lambdas = 0
        # TODO: find robot on map
        self.__robot = (0, 0)

        if (metadata != None and len(metadata) == 3):
            self.water = metadata[0]
            self.flood = metadata[1]
            self.proof = metadata[2]
        else:
            self.water = 0
            self.flood = 0
            self.proof = 10

    def isAborted(self):
        return self.history.endswith("A")
    def isCompleted(self):
        pass
    def isDrowned(self):
        pass

    def isValid(self):
        lifts  = 0
        robots = 0
        for l in lines:
            for c in l:
                if c == 'R':
                    robots += 1
                elif c == 'L':
                    lifts += 1
                elif c == 'O':
                    lifts += 2
        return (robots == 1 and lifts == 1)

    def getRobot(self):
        return self.__robot

    def get(self, x, y):
        if (x >= 0 and y >= 0 and x < self.n and y < self.m):
            return self.lines[y][x]
        return None

    def set(self, x, y, c):
        if (x >= 0 and y >= 0 and x < self.n and y < self.m):
            self.lines[y][x] = c
        return self

    def getSize(self):
        return (self.n, self.m)

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

