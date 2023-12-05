from ctu_bosch_sr450 import RobotBosch
import numpy as np

from line import Line
from ik import IKinOrientation, GetOrientation, ChangeConfig
import matplotlib.pyplot as plt

def Plan(line:Line, interdist, high = 0.5, low = 0.4):
    line.Interpolate(interdist) #Interpolate by distance

    model = RobotBosch(tty_dev=None) #Create analog of robot
    
    q = GenerateQ(model, line, low) #Generate a q (a configuration) for every point of a line
    if len(q) == 1: #If failed, give soft home
        return q

    q = InsertExtra(model, q, line, high, low) #Add extra qs for configuration changes
    q = InsertEnds(model, q, line, high) #Add lifted ends of line

    vizualization(model, q, (high+low)/2) #Visualize
    
    return q

def GenerateQ(model: RobotBosch, line:Line, low):
    for c in [-1,1,0]: #Configuration (1st, 2nd, Any)
        c_current = c
        if c == 0:
            c_current = 1
        q = [[0,0,0,0]] #Default (soft home)
        for p in line.points: #For each point on line
            qp = IKinOrientation(model, c_current ,p,q[-1], low) #Try finding q in configuration
            if len(qp) == 0: #If not found
                if c == 0:
                    c_current = -c_current
                    qp = IKinOrientation(model, c_current ,p,q[-1], low)
                    if len(qp) == 0:
                        break
                else:
                    break
            c_current = GetOrientation(qp)
            q.append(qp) #Q valid for the point and configuration

        if len(q) == len(line.points)+1: #If all points have valid q
            return q
        
    print("No IK")
    return [[0,0,0,0]] #No solution

def InsertExtra(model: RobotBosch, q, line:Line, high, low):

    indexes = [] #Indexes where extra qs are needed
    for i in range(len(q)-1):
        c = GetOrientation(q[i])
        c_next = GetOrientation(q[i+1])        
        if c != c_next and not(c == 0 or c_next == 0): #If next point has different configuration
            indexes.append(i)

    for i in range(len(indexes)): #For every index with changing configuration
        indexes[i] += i*3 #Moving index if something was added before it (for i>0 of changes)

        c = GetOrientation(q[indexes[i]])
        c_next = GetOrientation(q[indexes[i]+1])
        up, changed, down = ChangeConfig(model, c, c_next, q, line.points[indexes[i]-1], high, low) #Make needed new qs

        q.insert(indexes[i]+1, up) #Insert in q
        q.insert(indexes[i]+2, changed)
        q.insert(indexes[i]+3, down)
        line.points.insert(indexes[i], line.points[indexes[i]-1]) #Insert in line
        line.points.insert(indexes[i], line.points[indexes[i]-1])
        line.points.insert(indexes[i], line.points[indexes[i]-1])
    return q

def InsertEnds(model: RobotBosch, q, line, high):
    q_first = IKinOrientation(model, GetOrientation(q[1]),line.points[0],q[0], high) #Add lifted point at start
    q.insert(1,q_first)
    q_last = IKinOrientation(model, GetOrientation(q[-1]),line.points[-1],q[-1], high) #Add lifted point at the end
    q.append(q_last)
    return q

def vizualization(model: RobotBosch, q, height_diff):
    if len(q[-1]) != 4: #If q is not valid
        return
    fig: plt.Figure = plt.figure()
    ax_image: plt.Axes = fig.add_subplot(111)
    ax_image.grid(True)
    color = ['tab:blue' , 'tab:green', 'tab:red'] #Colours of configuration
    touching = ['x', '.'] #Shape dependent on height
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
