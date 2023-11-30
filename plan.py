from ctu_bosch_sr450 import RobotBosch
import numpy as np

from line import Line
from ik import IKinOrientation, GetOrientation, ChangeConfig
import matplotlib.pyplot as plt

def Plan(line:Line, interdist, high = 0.5, low = 0.4):
    line.Interpolate(interdist)

    model = RobotBosch(tty_dev=None)
    
    q = GenerateQ(model, line, low)
    if len(q) == 1:
        return q

    q = InsertExtra(model, q, line, high, low)
    q = InsertEnds(q,line,high)

    vizualization(model, q, (high+low)/2)
    
    return q

def GenerateQ(model: RobotBosch, line:Line, low):
    for c in [-1,1,0]: #configurations
        q = [[0,0,0,0]]
        for p in line.points: #for each point on line
            qp = IKinOrientation(model, c,p,q[-1], low) #try finding q in configuration
            if len(qp) == 0:
                break
            else:
                q.append(qp)

        if len(q) == len(line.points)+1:
            return q
        
    print("No IK")
    return [[0,0,0,0]] #No solution

def InsertExtra(model: RobotBosch, q, line:Line, high, low):
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
        up, changed, down = ChangeConfig(model, c, c_next, q, line.points[indexes[i]-1], high, low)

        q.insert(indexes[i]+1, up)
        q.insert(indexes[i]+2, changed)
        q.insert(indexes[i]+3, down)
        line.points.insert(indexes[i], line.points[indexes[i]-1])
        line.points.insert(indexes[i], line.points[indexes[i]-1])
        line.points.insert(indexes[i], line.points[indexes[i]-1])
    return q

def InsertEnds(q, line, high):
    q_first = IKinOrientation(model, GetOrientation(q[1]),line.points[0],q[0], high)
    q.insert(1,q_first)
    q_last = IKinOrientation(model, GetOrientation(q[-1]),line.points[-1],q[-1], high)
    q.append(q_last)
    return q

def vizualization(model: RobotBosch, q, height_diff):
    if len(q[-1]) != 4:
        return
    fig: plt.Figure = plt.figure()
    ax_image: plt.Axes = fig.add_subplot(111)
    ax_image.grid(True)
    color = ['tab:blue' , 'tab:green', 'tab:red']
    touching = ['x', '.']
    size = [5,7]
    for qi in q:
        x = model.fk(qi)[0]
        y = model.fk(qi)[1]
        z = model.fk(qi)[2] >= height_diff
        ax_image.plot(x,y,touching[z],ms = size[z], color = color[GetOrientation(qi)])

    plt.show() #block = False

if __name__ == "__main__":
    model = RobotBosch(tty_dev=None)
    p = Line()
    p.ReadFile('points.txt')
    #p.SetPoints([[0, -0.4],[0.3,0],[0,0.4],[0.4,0],[0.1, -0.4]])
    #p = Line([[0.45,0],[0.2,0],[0.35,0.1]])

    Plan(p, 0.01)
    #for pi in Plan(p, 0.1):
        #print(pi, GetOrientation(pi), model.fk(pi))
