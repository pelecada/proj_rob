from dirimport import DirImportFn
DirImportFn()

import numpy as np
from robotBosch import robotBosch
from CRS_commander import Commander

rob = robotBosch()
c = Commander(rob) 
c.open_comm("/dev/ttyUSB0",speed = 19200)
c.init()
c.wait_ready()
c.rcon.close()
print("Home")
