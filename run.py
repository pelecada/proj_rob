from dirimport import DirImportFn
DirImportFn()

import numpy as np
from robotBosch import robotBosch
from CRS_commander import Commander
from robotics_toolbox.core import SE2

from proj_rob.model import Model

rob = robotBosch()
c = Commander(rob) 
m = Model(False)
c.open_comm("/dev/ttyUSB0",speed = 19200)
c.wait_ready()

"""
resp = c.query('COORDAP')
resp = np.fromiter(map(int, resp.split(',')), int)
print(resp)
"""

tgt = np.array([10,10,-10,10])
deg = np.array([0,0,0,0]) #deg, deg, mm, deg
for i in range(4):
    #c.wait_ready()
    deg[i] = tgt[i]
    m.MoveTo(deg)

"""
resp = c.query('COORDAP')
resp = np.fromiter(map(int, resp.split(',')), int)
print(resp)
"""

#do stuff

c.rcon.close()