from ctu_bosch_sr450 import RobotBosch
import numpy as np

from line import Line
from ik import SortIK

def GetOrientation(q):
    return np.sign(q[1])

def IKinOrientation(c,p,current):
    qs = SortIK(model, [p[0],p[1],0.5,0],current)
    if c == 0:
        return qs[0]
    for q in qs:
        if GetOrientation(q) == c or GetOrientation(q) == 0:
            return q
    return [None,None,None,None]


def Plan(line:Line, interdist):
    line.Interpolate(interdist)

    model = RobotBosch(tty_dev=None)

    
    for c in [-1,1,0]: #configurations
        q = [[0,0,0,0]]
        for p in line.points: #for each point on line
            qp = IKinOrientation(c,p,q[-1]) #try finding q in configuration
            if p[0] == None:
                print("No IK")
                break
            else:
                q.append(qp)
        return q
    return None

if __name__ == "__main__":
    model = RobotBosch(tty_dev=None)
    p = Line([[0.45,0],[0.25,0],[0.35,0.1]])
    for pi in Plan(p,0.01):
        print(pi, GetOrientation(pi), model.fk(pi))