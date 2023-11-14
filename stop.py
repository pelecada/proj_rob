from dirimport import DirImportFn
DirImportFn()

import numpy as np
from robotBosch import robotBosch
from CRS_commander import Commander

rob = robotBosch()
c = Commander(rob) 
c.open_comm("/dev/ttyUSB0",speed = 19200)
c.release()
c.reset_motors()
c.rcon.close()
print("Stopped")