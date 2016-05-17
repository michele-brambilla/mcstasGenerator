import numpy as np
import csv
import re
import json

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

    def mcstas2stream(self,flags):
        sz = self.area.n.shape
        count = 0
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
                    self.d[count]["ts"]     =    self.tof.n[count]
                    count = count+1
        return self.d
