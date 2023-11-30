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

def SortIK(robot: RobotBosch ,target, current):
    if len(current) == 0:
        return []
    
    q = LimitPi(robot.ik(target[0],target[1],target[2],target[3]))
    
    def Score(array):
        num = 0
        for i in range(len(array)):
            num += (array[i] - current[i])**2
        return num
    
    q.sort(key = Score)
    if len(q) == 0: #No solution
        return []
    return q

def GetOrientation(q):
    return int(-np.sign(q[1]))

def IKinOrientation(model: RobotBosch, c,p,current, height):
    qs = SortIK(model, [p[0],p[1],height,0],current)
    if len(qs) == 0: return []

    if c == 0:
        return qs[0]
    for q in qs:
        if GetOrientation(q) == c or GetOrientation(q) == 0:
            return q
    return []

def ChangeConfig(robot:RobotBosch, config, config_next, q, point, high, low):

    q_u = IKinOrientation(robot, config,point,q[-1], high) #možná takto to bude lepsi?
    q_ch = IKinOrientation(robot, config_next,point,q_u, high)
    q_d = IKinOrientation(robot, config_next,point,q_ch, low)
    #print(q_u)
    #print(q_ch)
    #print(q_d)

    return q_u,q_ch,q_d