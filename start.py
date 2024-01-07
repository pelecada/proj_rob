#Initialize robot and return it home

from ctu_bosch_sr450 import RobotBosch

robot = RobotBosch()
robot.initialize()
robot.close()