import numpy as np
import csv
import re

def mcstasHeader(str):
    reader = csv.reader(open(str,"r"), delimiter=' ')
    return [row[1:] for row in reader if re.match('#', row[0], re.IGNORECASE)]
    

##########################
# ToF detector    
class ToF:
    def __init__ (self,str) :
        self.t,self.n = self.read(str)
        h = mcstasHeader(str)
        self.Ncount = int(float([x for x in h if x[0].strip(':') == 'Ncount'][0][1]))
        self.xmin  = float([x for x in h if x[0].strip(':') == 'xlimits'][0][1])
        self.xmax  = float([x for x in h if x[0].strip(':') == 'xlimits'][0][2])
        
    def read(self,str) :
        d,n = np.loadtxt(str,usecols=(0,3),unpack=True)
        return d,n
    
    # Hack
    def randomize(self,val) :
        self.n = np.random.random(size=val)*(self.xmax-self.xmin)+self.xmin


##########################
# 2-D detector    
class D2:
    def __init__ (self,str) :
        self.n = self.read(str)
        self.h = mcstasHeader(str)
        self.Ncount = int(float([x for x in self.h if x[0].strip(':') == 'Ncount'][0][1]))

    def read(self,str) :
        d = np.loadtxt(str,unpack=True)
        x,y = d.shape
#        return d[:x,:y/3]
        return d[:x,2*y/3:]

    def count(self):
        return sum(sum(self.n))



##########################
# N-D detector (TODO)
#class ND:
#    def __init__(self):
