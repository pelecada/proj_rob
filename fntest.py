from dirimport import DirImportFn
DirImportFn()

import numpy as np
from robotBosch import robotBosch
from CRS_commander import Commander

from movement import Model
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
x = m.InvKin(SE2([450,9],0.2))[0]
x = [x[0], x[1], 0, x[2]]
m.MoveTo(c,x)
print(m.ForwKin())
