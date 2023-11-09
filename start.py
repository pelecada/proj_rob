import sys
sys.path.append("/bluebot/data/Pyrocon/")
sys.path.append(sys.path[0].replace("proj","pyrocon"))
sys.path.append(sys.path[0].replace("proj","robtoolbox"))

import numpy as np
from robotBosch import robotBosch
from CRS_commander import Commander
#from robotics_toolbox.core import SE2

#a = SE2()
rob = robotBosch()
c = Commander(rob) 
c.open_comm("/dev/ttyUSB0",speed = 19200)
#c.release()
#c.reset_motors()
c.init()
"""
print("home")
c.wait_ready()

resp = c.query('COORDAP')
resp = np.fromiter(map(int, resp.split(',')), int)
print(resp)

tgt = np.array([10,10,-10,10])
deg = np.array([0,0,0,0]) #deg, deg, mm, deg
for i in range(4):
    #c.wait_ready()
    deg[i] = tgt[i]
    irc = c.anglestoirc(deg)
    c.coordmv(irc)
    print("sent", i)

resp = c.query('COORDAP')
resp = np.fromiter(map(int, resp.split(',')), int)
print(resp)
#print(c.irctoangles(resp[]))
#do stuff
"""
c.release()
c.rcon.close()
print("OK")