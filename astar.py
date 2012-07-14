"""
Heavily inspired by and mostly stolen from:

http://www.laurentluce.com/posts/solving-mazes-using-python-simple-recursivity-and-a-search/
"""

import heapq

class Cell(object):
    def __init__(self, x, y, code = 32, parent = None, g = 0, h = 0):
        self.x = x
        self.y = y
        self.code = code
        self.parent = parent
        self.g = g
        self.h = h
        self.f = 0

    def reachable(self):
        """                   ' ' '\\''O' 'R' """
        return (self.code in [32, 92, 79, 82])
# with '.' (earth)
#        """                   ' ' '.' '\\''O' 'R' """
#        return (self.code in [32, 46, 92, 79, 82])

    def moveFromParent(self):
        """ What move to do from parent to get to self """
        if self.parent == None:
            return ""
        elif self.parent.x == self.x + 1:
            return "L"
        elif self.parent.x == self.x - 1:
            return "R"
        elif self.parent.y == self.y + 1:
            return "D"
        elif self.parent.y == self.y - 1:
            return "U"
        return ""

    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+","+chr(self.code)+")"

class AStar:
    def __init__(self, mmap, tarPos):
        self.mmap = mmap
        
        robot = mmap.getRobot()

        self.ol = []
        heapq.heapify(self.ol)
        self.cl = set()
        mSize = mmap.getSize()
        self.gridWidth  = mSize[0]
        self.gridHeight = mSize[1]

        self.cells = []
        for y in range(0, self.gridHeight):
            for x in range(0, self.gridWidth):
                self.cells.append(Cell(x, y, mmap.grid[y][x]))

        self.start = self.getCell(robot[0], robot[1])
        if (tarPos != None and len(tarPos) == 2):
            self.end = self.getCell(tarPos[0], tarPos[1])
        else:
            self.end = self.getCell(robot[0], robot[1])
        self.__path = ""


    def heuristic(self, cell):
        return (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def getCell(self, x, y):
        return self.cells[y * self.gridWidth + x]
    def getAdjacents(self, cell):
        cells = []
        if cell.x < self.gridWidth - 1:
          cells.append(self.getCell(cell.x + 1, cell.y))
        if cell.y > 0:
          cells.append(self.getCell(cell.x, cell.y - 1))
        if cell.x > 0:
          cells.append(self.getCell(cell.x - 1, cell.y))
        if cell.y < self.gridHeight - 1:
          cells.append(self.getCell(cell.x, cell.y + 1))
        return cells

    def path(self):
        if (self.__path == ""):
            cell = self.end
            while cell.parent is not None:
                self.__path = cell.moveFromParent() + self.__path
                cell = cell.parent
        return self.__path

    def updateCell(self, adj, cell):
        adj.g = cell.g + 1
        adj.h = self.heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def process(self):
        heapq.heappush(self.ol, (self.start.f, self.start))
        while len(self.ol):
            h, cell = heapq.heappop(self.ol)
            self.cl.add(cell)

            if cell is self.end:
                return self

            adjs = self.getAdjacents(cell)
            for c in adjs:
                if c.reachable() and c not in self.cl:
                    if c in self.ol:
                        if c.g > cell.g + 1:
                            self.updateCell(c, cell)
                    else:
                        self.updateCell(c, cell)
                        heapq.heappush(self.ol, (c.f, c))
        return self
