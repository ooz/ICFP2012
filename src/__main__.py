#!/usr/bin/python
# coding: utf-8

__author__  = "Oliver Zscheyge"
__email__   = "oliverzscheyge@gmail.com"
__version__ = "0.1.0"

import sys
import signal
from   optparse import OptionParser

usage  = "Usage: %prog [options] file(s)" 
parser = OptionParser(usage = usage)

#parser.add_option("-i", "--interactive",
#                  action="store_true", dest="interactive", default=False,
#                  help="""Control the Robot manually:
#                          W, A, S, D ... Up, Left, Down, Right
#                          [Space]    ... Shave
#                          ESC, q, e  ... any of those key exists the game""")
parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="""Display the solving process live on stdout 
                          (each step is delayed to be easier followed by a human). 
                          Last line printed is the command sequence.
                          You can alter the sleep duration with the --sleep option.""")
parser.add_option("-t", "--tv",
                  action="store_true", dest="tv", default=False,
                  help="""Like -v except it clears the screen before printing every new
                          frame. Use -v for debugging/getting a trace. 
                          Use -t for just enjoying the show!""")
parser.add_option("-s", "--sleep", type="float", dest="sleep", default=1.0,
                  help="""Time to sleep after one step was executed.
                          Only has an effect in combination with the -v or -t flag.""")

BOT = None
def sigintHandler(signal, frame):
    if (BOT != None):
        sys.stdout.flush()
        print BOT.getCommands()
        sys.exit(0)

""" MAIN """
if __name__ == "__main__":
    (options, args) = parser.parse_args()

    signal.signal(signal.SIGINT, sigintHandler)

    from minemap import Map
    from mapload import MapLoader

    ml = MapLoader()
    m  = ml.mapFromStdin()
    
    if (m != None):
        from foobot import *
        BOT = MrScaredGreedy(m, [options.sleep, (options.verbose or options.tv), options.tv])
#        if (options.interactive):
#            BOT.interactive()
#        el
        if (options.verbose or options.tv):
            BOT.solveVisual()
        else:
            BOT.solve()
        print BOT.getCommands()

