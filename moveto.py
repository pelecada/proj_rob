from dirimport import DirImportFn
DirImportFn()

import numpy as np
from robotBosch import robotBosch
from CRS_commander import Commander
from robotics_toolbox.core import SE2

from model import Model

rob = robotBosch()
c = Commander(rob) 
m = Model(False)
c.open_comm("/dev/ttyUSB0",speed = 19200)
c.wait_ready()

text = input().split()
nums = np.array([0,0,0])
for i in range(3): nums[i] = float(text[i])

m.MoveTo(c, m.ClosestInvConfig(SE2([nums[0],nums[1]],nums[2])))
print(m.ForwKin(nums))

c.wait_ready()
c.rcon.close()
