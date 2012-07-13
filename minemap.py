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
        return self.history.endswith("A")
    def isCompleted(self):
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

    def printAll(self):
        print "Init:"
        self.printInitial()
        print "\nNow:"
        self.printCurrent()
        return self

