from ctu_bosch_sr450 import RobotBosch
import numpy as np

from line import Line
from plan import Plan

robot = RobotBosch()  # initialize object without connection to the robot
robot.initialize(home=False)
robot.soft_home()

p = Line() #y = 0 : x <0.25,0,45>, h <0.17,0.5>
p.SetPoints([[0.45,0],[0.2,0],[0.35,0.1]])

configs = Plan(p,0.01,0.5,0.4)

for q in configs:
    #robot.wait_for_motion_stop()
    robot.move_to_q(q)

robot.soft_home()
robot.close()