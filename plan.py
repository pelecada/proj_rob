from ctu_bosch_sr450 import RobotBosch
import numpy as np

from line import Line
from ik import ClosestIK

def GetOrientation(q):
    return np.sign(q[1])

def Plan(line:Line, interdist):
    line.Interpolate(interdist)

    model = RobotBosch(tty_dev=None)

    q = [[0,0,0,0]]

    for p in line.points:
        qi = ClosestIK(model, [p[0],p[1],0.5,0],q[-1])
        if p[0] == None:
            print("No IK")
        else:
            q.append(qi)
    return q

if __name__ == "__main__":
    model = RobotBosch(tty_dev=None)
    p = Line([[0.45,0],[0.25,0],[0.35,0.1]])
    for pi in Plan(p,0.01):
        print(pi, GetOrientation(pi), model.fk(pi))