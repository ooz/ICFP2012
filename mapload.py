from minemap import Map

class MapLoader:
    def __init__(self):
        pass

    def loadMap(self, path):
        f = open(path, 'r')
        lines = []
        for line in f:
            stripped = line.strip()
            if (stripped != ""):
                lines.append(stripped)
        f.close()
        lines.reverse()
        return Map(lines)


