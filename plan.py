from ctu_bosch_sr450 import RobotBosch
import numpy as np

from line import Line
from ik import SortIK, LimitPi
import matplotlib.pyplot as plt

def GetOrientation(q):
    return int(-np.sign(q[1]))

def IKinOrientation(model: RobotBosch, c,p,current, high):
    qs = SortIK(model, [p[0],p[1],high,0],current)
    if c == 0:
        return qs[0]
    for q in qs:
        if GetOrientation(q) == c or GetOrientation(q) == 0:
            return q
    return []

def ChangeConfig(robot:RobotBosch, config, config_next, q, line: Line, i):
    size_of = 0.5
    base = 0.2

    q_u = IKinOrientation(robot, config,line.points[i-1],q[-1], size_of) #možná takto to bude lepsi?
    q_ch = IKinOrientation(robot, config_next,line.points[i-1],q_u, size_of)
    q_d = IKinOrientation(robot, config_next,line.points[i-1],q_ch, base)
    #print(q_u)
    #print(q_ch)
    #print(q_d)

    return q_u,q_ch,q_d


def Plan(line:Line, interdist):
    line.Interpolate(interdist)

    model = RobotBosch(tty_dev=None)
    high = 0.2
    size_of = 0.3
    
    for c in [-1,1,0]: #configurations
        q = [[0,0,0,0]]
        for p in line.points: #for each point on line
            qp = IKinOrientation(model, c,p,q[-1], high) #try finding q in configuration
            if len(qp) == 0:
                print("No IK")
                break
            else:
                q.append(qp)

        if len(q) == len(line.points)+1:
            break

    indexes = []
    changes = 0
    #asi by to chtelo nejdřiv detekovat počet zmen a pak je tam teprv konkrétně doplnit?
    for i in range(len(q)-1):
        c = GetOrientation(q[i])
        c_next = GetOrientation(q[i+1])        
        if c != c_next and not(c == 0 or c_next == 0):
            indexes.append(i)
            changes +=1

    for i in range(len(indexes)):
        indexes[i] += i*3

        c = GetOrientation(q[indexes[i]])
        c_next = GetOrientation(q[indexes[i]+1])
        up, changed, down = ChangeConfig(model, c, c_next, q, line, indexes[i])

        q.insert(indexes[i]+1, up)
        q.insert(indexes[i]+2, changed)
        q.insert(indexes[i]+3, down)
        line.points.insert(indexes[i], line.points[indexes[i]-1])
        line.points.insert(indexes[i], line.points[indexes[i]-1])
        line.points.insert(indexes[i], line.points[indexes[i]-1])

    q_first = IKinOrientation(model, GetOrientation(q[1]),line.points[0],q[0], size_of)
    q.insert(1,q_first)
    q_last = IKinOrientation(model, GetOrientation(q[-1]),line.points[-1],q[-1], size_of)
    q.append(q_last)
    vizualization(model, q)
    
    return q

def vizualization(model: RobotBosch, q):
    fig: plt.Figure = plt.figure()
    ax_image: plt.Axes = fig.add_subplot(111)
    ax_image.grid(True)
    color = ['tab:blue' , 'tab:green', 'tab:red']
    touching = ['x', '.']
    h = 0.3
    for qi in q:
        x = model.fk(qi)[0]
        y = model.fk(qi)[1]
        z = model.fk(qi)[2] >= h
        ax_image.plot(x,y,touching[z], color = color[GetOrientation(qi)])

    plt.show() #block = False

if __name__ == "__main__":
    model = RobotBosch(tty_dev=None)
    p = Line([[0, -0.4],[0.3,0],[0,0.4],[0.4,0],[0.1, -0.4]])
    #p = Line([[0.45,0],[0.2,0],[0.35,0.1]])

    #Plan(p, 0.01)
    for pi in Plan(p, 0.1):
        print(pi, GetOrientation(pi), model.fk(pi))
