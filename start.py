from ctu_bosch_sr450 import RobotBosch
from path import Path
import numpy as np

def LimitPi(q):
    for qi in q:
        for j in [0,1,3]:
            while qi[j] > np.pi:
                qi[j] = qi[j] - 2*np.pi
            while qi[j] < -np.pi:
                qi[j] = qi[j] + 2*np.pi
    return q

def ClosestIK(robot: RobotBosch ,target, current = None):
    if current.any() == None:
        current = robot.get_q()

    q = LimitPi(robot.ik(target[0],target[1],target[2],target[3]))
    def Score(array):
        num = 0
        for i in range(len(array)): num += (array[i] - current[i])**2
        return num
    q.sort(key = Score)
    if len(q) == 0: #No solution
        return [None,None,None,None]
    return q[0]


robot = RobotBosch(tty_dev=None)  # initialize object without connection to the robot
x, y, z, phi = robot.fk([0, 0, 0, 0])  # compute forward kinematics
#print(x,y,z,phi)
q = robot.ik(x, y, z, phi)  # compute inverse kinematics, get the first solution

p = Path([[0.45,0],[0.2,0],[0.35,0.1]]) #y = 0 : x <0.25,0,45>, h <0.17,0.5>
p.Interpolate(10)

current = LimitPi(q)[0]

for b in p.points:
    #q = LimitPi(robot.ik(b[0],b[1],0.5,0))
    p = ClosestIK(robot, [b[0],b[1],0.2,0],current)
    print(p)
    if p[0] == None:
        print("No IK")
    else:
        current = p