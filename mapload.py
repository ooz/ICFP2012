import sys

from minemap import Map

class MapLoader:
    def __init__(self):
        pass

    def __padLine(self, line, maxLength):
        if len(line) < maxLength:
            return self.__padLine(line + " ", maxLength)
        return line

    def __mapFromInputLines(self, lines):
        lines.reverse()
        maxLength = max(map(lambda l: len(l), lines))
        lines = map(lambda l: self.__padLine(l, maxLength), lines)
        return Map(lines)

    def mapFromStdin(self):
        lines = sys.stdin.readlines()
        lines = map(lambda l: l.strip(), lines)
        return self.__mapFromInputLines(lines)

    def mapFromFile(self, path):
        f = open(path, 'r')
        lines = []
        for line in f:
            stripped = line.strip()
            if (stripped != ""):
                lines.append(stripped)
        f.close()
        return __mapFromInputLines(lines)


