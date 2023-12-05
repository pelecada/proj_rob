from ctu_bosch_sr450 import RobotBosch
import numpy as np

from line import Line
from plan import Plan

robot = RobotBosch() 
robot.initialize(home=False) #Quickstart
robot.soft_home()

p = Line() #y = 0 : x <0.25,0,45>, h <0.17,0.5>
#p.SetPoints([[0.45,0],[0.2,0],[0.35,0.1]])
p.ReadFile("points.txt")

configs = Plan(p,0.01,0.25,0.18) #Plan configuration

for q in configs: #Execute
    #robot.wait_for_motion_stop()
    robot.move_to_q(q)

robot.soft_home() #Return home
robot.close() #Bye