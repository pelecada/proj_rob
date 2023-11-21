from dirimport import DirImportFn
DirImportFn()

import numpy as np
from robotBosch import robotBosch
from CRS_commander import Commander

from movement import MoveTo, ForwKin

rob = robotBosch()
c = Commander(rob) 
c.open_comm("/dev/ttyUSB0",speed = 19200)
c.wait_ready()

text = input().split()
nums = np.array([0,0,0,0])
for i in range(4): nums[i] = float(text[i])

MoveTo(c, nums)
print(ForwKin(nums))

c.wait_ready()
c.rcon.close()
