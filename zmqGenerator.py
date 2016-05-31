#from neventarray import *

import errno
import numpy as np
import time
import binascii

import zmq

import ritaHeader as rh

class generatorSource:

    def __init__ (self,port,multiplier):
        self.port = port
        self.context = zmq.Context()
        self.socket = self.connect()
        self.multiplier = multiplier
        self.count = 0

    def connect(self):
        zmq_socket = self.context.socket(zmq.PUSH)
        zmq_socket.bind("tcp://*:"+self.port)
        zmq_socket.setsockopt(zmq.SNDHWM, 100)
        return zmq_socket

    def mutation(self,ctl,d):
        o = d
        if (ctl['mutation'] == 'nev') or (ctl['mutation'] == 'all'):
            if  np.random.rand() > .99 :
                o = np.delete(o,np.random.rand(o.size))
                print "Error: missing value"

        if (ctl['mutation'] == 'ts') or (ctl['mutation'] == 'all'):
            if  np.random.rand() > .99 :
                o[1]['ts'] = -1
                print "Error: wrong timestamp"

        if (ctl['mutation'] == 'pos') or (ctl['mutation'] == 'all'):
            if  np.random.rand() > .99 :
                x=np.random.randint(o.size,size=np.random.randint(5)) 
                o[1]["data"] = o[1]["data"] & 0xff000fff | 16773120
                print "Error: wrong position"
            if  np.random.rand() > .99 :
                x=np.random.randint(o.size,size=np.random.randint(5)) 
                o[2]["data"] = o[2]["data"] & 0xfffff000 | 4095
                print "Error: wrong position"

        return o

    
    def run(self,data,control_str):

        if self.multiplier > 1:
            data = np.tile(data,float(self.multiplier))

        ctl = rh.control(control_str)
        ctime=time.time()
        pulseID=0

        s = 1e-6*(data.nbytes+len(rh.header(pulseID,ctime,12345678,data.shape[0])))
        print "size = ",s, "MB; expected bw = ",s * ctl["rate"], "MB/s"

        while(ctl["run"] != "stop"):

            stream_frequency = 1./ctl["rate"]

            itime = time.time()
            if ctl["run"] != "pause":
                dataHeader = rh.header(pulseID,itime,12345678,data.shape[0])
            else:
                dataHeader = rh.header(pulseID,itime,12345678,0)

            def send_data(socket,head):
                if ctl["run"] == "run": 
                    socket.send(head,zmq.SNDMORE)
                    socket.send(self.mutation(ctl,data))
#                    socket.send(data)
                    self.count += 1
                else:
                    socket.send(head)
                    self.count += 1

            send_data(self.socket,dataHeader)

            elapsed = time.time() - itime
            remaining = stream_frequency-elapsed

            if remaining > 0:
                time.sleep (remaining)

            pulseID += 1
            ctl = rh.control(control_str)
            if time.time()-ctime > 10 :
                size = (data.nbytes+len(dataHeader))

                print "Sent ",self.count," events @ ",size*self.count/(10.*1e6)," MB/s"
                self.count = 0
                ctime = time.time()

                
