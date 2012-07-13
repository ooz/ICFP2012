#!/usr/bin/python
# coding: utf-8

__author__  = "Oliver Zscheyge"
__email__   = "oliverzscheyge@gmail.com"
__version__ = "0.1.0"

import sys
import signal
# from   optparse import OptionParser
# 
# usage  = "Usage: %prog [options] file(s)" 
# parser = OptionParser(usage = usage)
# 
# parser.add_option("-v", "--verbose",
#                   action="store_true", dest="verbose", default=False,
#                   help="Display the solving process live on stdout (each step is delayed to be easier followed by a human). Last line printed is the command sequence.")

BOT = None
def sigintHandler(signal, frame):
    if (BOT != None):
        sys.stdout.flush()
        print BOT.getCommands()
        sys.exit(0)

""" MAIN """
if __name__ == "__main__":
#    (options, args) = parser.parse_args()

    signal.signal(signal.SIGINT, sigintHandler)

    from minemap import Map
    from mapload import MapLoader

    ml = MapLoader()
    m  = ml.mapFromFile("maps/contest1.map")

    if (m != None):
        m.printAll()

        from foobot import Robot
        BOT = Robot(m)
        BOT.solveVisual()
        print BOT.getCommands()
