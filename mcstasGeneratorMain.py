from nexus2event import *
from neventarray import *

import sys, os, getopt
import errno
import numpy
import time
import binascii

import zmq

from detector import ToF
from detector import D2

from instrument import Rita2

import ritaHeader as rh

from zmqGenerator import generatorSource

def main(argv,t,surf):

    print argv
    port = argv[0]

    multiplier = 1
    if len(argv) > 2:
        multiplier = argv[2]

    g = generatorSource(port,multiplier)
    detector = Rita2(t[0],surf[0])

    print t[0].n.count
    #    stream = detector.mcstas2stream(np.array([2, 1, 1, 1, 1]))
#    g.run(stream)


    
if __name__ == "__main__":
    try:
        opts,args = getopt.getopt(sys.argv[1:], "t:a:h",["tof","area","help"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
        
#    if len(args) < 4:
#        usage()
#        exit(-1)
        
    for o,arg in opts:
        if o in ("-h","--help"):
            usage()
            sys.exit()
        if o in ("-t","--tof"):
            all_arguments = arg.split(',')
            t = [ToF(s) for s in all_arguments]
        if o in ("-a","--area"):
            all_arguments = arg.split(',')
            surf = [D2(s) for s in all_arguments]

    print t[0].n.size
    main(args,t,surf)

