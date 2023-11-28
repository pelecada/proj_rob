from ctu_bosch_sr450 import RobotBosch

robot = RobotBosch()  # initialize object without connection to the robot
robot.initialize()
robot.close()