from dirimport import DirImportFn
DirImportFn()

import numpy as np
from robotBosch import robotBosch
from CRS_commander import Commander

from proj_rob.model import Model
from robotics_toolbox.core import SE2

rob = robotBosch()
c = Commander(rob) 
m = Model(True)

m.MoveTo(c,[0,0,0,0])
print(m.ForwKin())
m.MoveTo(c,[0,0,0,np.pi/2])
print(m.ForwKin())

m.MoveTo(c,[0,0,0,0])
print(m.InvKin(SE2([450,9],0.2)))
m.MoveTo(c,m.ClosestInvConfig(SE2([450,9],0.2)))
print(m.ForwKin())
