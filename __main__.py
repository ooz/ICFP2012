#!/usr/bin/python
# coding: utf-8

__author__  = "Oliver Zscheyge"
__email__   = "oliverzscheyge@gmail.com"
__version__ = "0.1.0"



import sys
from   optparse import OptionParser

usage  = "Usage: %prog [options] file(s)" 
parser = OptionParser(usage = usage)

parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="Display the solving process live on stdout (each step is delayed to be easier followed by a human).")

parser.add_option("-p", "--print",
                  action="store_true", dest="print", default=False,
                  help="Print the solving history to stdout.")



""" MAIN """
if __name__ == "__main__":
    (options, args) = parser.parse_args()

    from minemap import Map
    from mapload import MapLoader

    ml = MapLoader()
    m  = ml.loadMap("maps/contest1.map")
    m.printAll()
