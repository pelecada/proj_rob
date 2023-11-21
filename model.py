from dirimport import DirImportFn
DirImportFn()

import numpy as np
from robotBosch import robotBosch
from CRS_commander import Commander

from robotics_toolbox.core import SE2
from robotics_toolbox.robots import PlanarManipulator
from copy import deepcopy

class Model():
    def __init__(self,
        fict
        ) -> None:
        self.model = PlanarManipulator([250,200,10],'RRR')
        self.height = 0
        self.fict = fict

    def Pretend(self):
        x = deepcopy(self)
        x.fict = True
        return x

    def MoveTo(self,c : Commander,target):
        self.height = target[2]
        self.model.q = [target[0],target[1],target[3]]
        if not self.fict:
            target = [c.radtodeg(target[0]), c.radtodeg(target[1]), target[2] ,c.radtodeg(target[3])]
            irc = c.anglestoirc(target)
            c.coordmv(irc)
        print("Moving to:", target)

    def ForwKin(self) -> SE2:
        return self.model.flange_pose()
    
    def InvKin(self,target): #doesn't work for edge cases!
        return self.model.ik_analytical(target)
    
    def ClosestInvKin(self,target):
        kins = self.InvKin(target)
        def Score(array):
            num = 0
            for i in range(len(array)): num += (array[i] - self.model.q[i])**2
            print(num)
            return num
        kins.sort(key = Score)
        return kins[0]
    
    def GetConfig(self, kin = None):
        if kin == None:
            return [self.model.q[0],self.model.q[1],self.height,self.model.q[2]]
        else:
            return [kin[0],kin[1],self.height,kin[2]]
        
    def ClosestInvConfig(self, target):
        return self.GetConfig(self.ClosestInvKin(target))