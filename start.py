from ctu_bosch_sr450 import RobotBosch
import numpy as np

from line import Line
from ik import ClosestIK, LimitPi
from plan import Plan

robot = RobotBosch()  # initialize object without connection to the robot
robot.initialize()

p = Line([[0.45,0],[0.2,0],[0.35,0.1]]) #y = 0 : x <0.25,0,45>, h <0.17,0.5>

configs = Plan(p,0.01)

for q in configs:
    robot.move_to_q(q)

robot.soft_home()
robot.close()