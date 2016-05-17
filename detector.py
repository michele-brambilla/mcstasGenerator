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
        self.xmin  = int([x for x in h if x[0].strip(':') == 'xlimits'][0][1])
        self.xmax  = int([x for x in h if x[0].strip(':') == 'xlimits'][0][2])
        self.Ncount = int([x for x in h if x[0].strip(':') == 'Ncount'][0][1])
        
    def read(self,str) :
        d,n = np.loadtxt(str,usecols=(0,3),unpack=True)
        return d,n
    
    # Hack
    def randomize(self,val) :
        self.n = np.random.randint(low=self.xmin,high=self.xmax,size=val)


##########################
# 2-D detector    
class D2:
    def __init__ (self,str) :
        self.n = self.read(str)
        self.h = mcstasHeader(str)
        self.Ncount = int([x for x in self.h if x[0].strip(':') == 'Ncount'][0][1])

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
