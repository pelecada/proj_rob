import sys
sys.path.append("/bluebot/data/Pyrocon/")
sys.path.append(sys.path[0].replace("proj","pyrocon"))
sys.path.append(sys.path[0].replace("proj","robtoolbox"))

import numpy as np
from robotBosch import robotBosch
from CRS_commander import Commander
from robotics_toolbox.core import SE2

a = SE2()
rob = robotBosch()
c = Commander(rob) 
c.open_comm("/dev/ttyUSB0")
c.init()

#do stuff

print("OK")