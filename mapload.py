import sys

from minemap import Map

class MapLoader:
    def __init__(self):
        pass

    def __mapFromInputLines(self, lines):
        lines.reverse()
        return Map(lines)

    def mapFromStdin(self):
        lines = sys.stdin.readlines()
        lines = map(lambda l: l.strip(), lines)
        print lines
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


