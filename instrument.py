import numpy as np
import csv
import re
import json
import numpy.random as random

event_t = np.dtype([("ts",np.uint32),
                    ("data",np.uint32)])

class Rita2:
    def __init__ (self,tof,area):
        self.tof = tof
        self.area = area
        self.d = np.empty(area.count(),dtype=event_t)

    def dataHeader(str) :
        with open(str) as data_file:
            self.h = json.dumps(json.load(data_file))
        return self.h

    #Hack
    def arrangeToF(self):
        # if the number of elements in the two monitor is different
        # rescale tof.n
        if self.area.count() != self.tof.count():
            factor = self.area.count()/self.tof.count()
            self.tof.n = map(round,self.tof.n*factor)
        # if not yet equal (because of rounding), randomly subtract
        # od add some counting
        diff = self.area.count() - self.tof.count()
        if diff > 0:
            for n in np.random.randint(self.tof.n.size,size=diff):
                self.tof.n[n] = self.tof.n[n] + 1
        if diff < 0:
            for n in np.random.randint(self.tof.n.size,size=-diff):
                self.tof.n[n] = self.tof.n[n] - 1

    def mcstas2stream(self,flags):
        self.arrangeToF()
        sz = self.area.n.shape
        count = 0
        n_t=0
        t=0
        for x in range(sz[0]):
            for y in range(sz[1]):
                for n in range(int(self.area.n[x][y])):
                    self.d[count]["data"]   =    np.uint32(x)
                    self.d[count]["data"]  |=    np.uint32(y) << 12
                    self.d[count]["data"]  |=    flags[0] << 24
                    self.d[count]["data"]  |=    flags[1] << 28
                    self.d[count]["data"]  |=    flags[2] << 29
                    self.d[count]["data"]  |=    flags[3] << 30
                    self.d[count]["data"]  |=    flags[4] << 31
                    self.d[count]["ts"]     =    -self.tof.t[t]
                    count = count+1
                    n_t   = n_t+1
                    if n_t >= self.tof.n[t]:
                        t = t+1
                        n_t = 0
        return self.d
