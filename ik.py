from ctu_bosch_sr450 import RobotBosch
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