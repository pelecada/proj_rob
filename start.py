from ctu_bosch_sr450 import RobotBosch
import numpy as np

from line import Line
from ik import ClosestIK, LimitPi

robot = RobotBosch(tty_dev=None)  # initialize object without connection to the robot
x, y, z, phi = robot.fk([0, 0, 0, 0])  # compute forward kinematics
#print(x,y,z,phi)
q = robot.ik(x, y, z, phi)  # compute inverse kinematics, get the first solution

p = Line([[0.45,0],[0.2,0],[0.35,0.1]]) #y = 0 : x <0.25,0,45>, h <0.17,0.5>
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