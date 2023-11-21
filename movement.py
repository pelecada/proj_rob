from dirimport import DirImportFn
DirImportFn()

import numpy as np
from robotBosch import robotBosch
from CRS_commander import Commander
from robotics_toolbox.core import SE2
from robotics_toolbox.robots import PlanarManipulator

class Model():
    def __init__(self,
        fict
        ) -> None:
        self.model = PlanarManipulator([250,200,10],'RRR')
        self.fict = fict

    def MoveTo(self,c : Commander,target):
        self.model.q = [target[0],target[1],target[3]]
        if not self.fict:
            target = [c.radtodeg(target[0]), c.radtodeg(target[1]), target[2] ,c.radtodeg(target[3])]
            irc = c.anglestoirc(target)
            c.coordmv(irc)
        print("Moving to:", target)

    def ForwKin(self) -> SE2:
        return self.model.flange_pose()

    def InvKin(self,target): #doesn't work for edge cases
        return self.model.ik_analytical(target)