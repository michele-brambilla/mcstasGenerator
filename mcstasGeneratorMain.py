#from neventarray import *

import sys, os, getopt
import errno
import numpy as np

from detector import ToF
from detector import D2

from instrument import Rita2

from ritaHeader import control

from zmqGenerator import generatorSource

def usage() :
    print '\nUsage:'
    print '\tpython mcstasGeneratorMain.py -a <area detector file(s)> -t <tof detector file(s)> port [multiplier]\n'
    print '\tpython mcstasGeneratorMain.py -h'
    print ''
    print '-a,--area :\tfile (or list of,comma separated) containing area detector mcstas output'
    print '-t,--tof :\tfile (or list of,comma separated) containing tof mcstas output'
    print 'port :\tTCP port on which 0MQ will stream data'
    print 'multiplier :\tincrease data size using <multiplier> identical copies in the same blob (optional, default = 1)'
    print '-h,--help :\tthis help'



def main(argv,t,surf):

    if len(argv) < 1:
        usage()
        exit(-1)
        
    port = argv[0]

    multiplier = 1
    if len(argv) > 2:
        multiplier = argv[2]

    g = generatorSource(port,multiplier)
    detector = Rita2(t[0],surf[0])

    ctl = control('control.in')
    flags = np.array([ctl['evt'],ctl['bsy'],ctl['cnt'],ctl['rok'],ctl['gat']])

    stream = detector.mcstas2stream(flags)
    print stream.shape
    g.run(stream,'control.in')


    
if __name__ == "__main__":
    try:
        opts,args = getopt.getopt(sys.argv[1:], "t:a:h",["tof","area","help"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
        
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
    
    t[0].randomize(surf[0].count())


    main(args,t,surf)



