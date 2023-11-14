from dirimport import DirImportFn
DirImportFn()

import numpy as np
from robotBosch import robotBosch
from CRS_commander import Commander
from robotics_toolbox.core import SE2
from robotics_toolbox.robots import PlanarManipulator

model = PlanarManipulator([250,200,10],'RRR')

def MoveTo(c : Commander,target):
    irc = c.anglestoirc(c.radtodeg(target))
    c.coordmv(irc)
    print("Moving to:", target)

def ForwKin(config) -> SE2:
    model.q = [config[0],config[1],config[3]]
    return model.flange_pose()