from ctu_bosch_sr450 import RobotBosch
import numpy as np

def LimitPi(q): #Limit values of q to [-pi,pi]
    for qi in q:
        for j in [0,1,3]:
            while qi[j] > np.pi:
                qi[j] = qi[j] - 2*np.pi
            while qi[j] < -np.pi:
                qi[j] = qi[j] + 2*np.pi
    return q

def SortIK(robot: RobotBosch ,target, current):
    if len(current) == 0: #If previous is missing, return nothing
        return []
    
    q = LimitPi(robot.ik(target[0],target[1],target[2],target[3])) #Generate all IK, and limit it
    
    def Score(array): #L2 Norm
        num = 0
        for i in range(len(array)):
            num += (array[i] - current[i])**2
        return num
    
    q.sort(key = Score) #Sort by L2 norm
    if len(q) == 0: #No solution
        return []
    return q

def GetOrientation(q): #Get orientation by sign of 2nd joint angle
    return int(-np.sign(q[1]))

def IKinOrientation(model: RobotBosch, c,p,current, height):
    qs = SortIK(model, [p[0],p[1],height,0],current) #Get sorted IK
    if len(qs) == 0: return [] #If no solutions exist, return nothing

    if c == 0: #If configuration doesn't matter, return closest
        return qs[0]
    for q in qs: #Go through configurations
        if GetOrientation(q) == c or GetOrientation(q) == 0: #If right configuration, or ambiguous, return it
            return q
    return []

def ChangeConfig(robot:RobotBosch, config, config_next, q, point, high, low): #Create new points for configuration change

    q_u = IKinOrientation(robot, config,point, q, high) #Lift point
    q_ch = IKinOrientation(robot, config_next,point,q_u, high) #Change configuration
    q_d = IKinOrientation(robot, config_next,point,q_ch, low) #Go down 

    return q_u,q_ch,q_d