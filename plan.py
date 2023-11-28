import array
from pyexpat.errors import XML_ERROR_ABORTED
from turtle import mode
from ctu_bosch_sr450 import RobotBosch
import numpy as np

from line import Line
from ik import SortIK
import matplotlib.pyplot as plt

def GetOrientation(q):
    return np.sign(q[1])

def IKinOrientation(model: RobotBosch, c,p,current):
    qs = SortIK(model, [p[0],p[1],0.5,0],current)
    if c == 0:
        return qs[0]
    for q in qs:
        if GetOrientation(q) == c or GetOrientation(q) == 0:
            return q
    return [None,None,None,None]


def Plan(line:Line, interdist):
    line.Interpolate(interdist)

    model = RobotBosch(tty_dev=None)

    
    for c in [-1,1,0]: #configurations
        q = [[0,0,0,0]]
        for p in line.points: #for each point on line
            qp = IKinOrientation(model, c,p,q[-1]) #try finding q in configuration
            if p[0] == None:
                print("No IK")
                break
            else:
                q.append(qp)
        vizualization(model, q)
        return q
    
    
    return None

def vizualization(model: RobotBosch, q):
    fig: plt.Figure = plt.figure()
    ax_image: plt.Axes = fig.add_subplot(111)
    ax_image.grid(True)
    x,y = [],[]
    for qi in q:
        x.append(model.fk(qi)[0])
        y.append(model.fk(qi)[1])
    ax_image.plot(x[:],y[:],'x', color = 'tab:red')

    x_arr, y_arr = [],[]
    for point in p.points:
        x_arr.append(point[0])
        y_arr.append(point[1])
    
    ax_image.plot(x_arr[:],y_arr[:],'o', color = 'tab:green')
    plt.show()

if __name__ == "__main__":
    model = RobotBosch(tty_dev=None)
    p = Line([[0.45,0],[0.25,0],[0.35,0.1]])
    
    #fig: plt.Figure = plt.figure()
    #ax_image: plt.Axes = fig.add_subplot(111)
    #ax_image.grid(True)

    #x,y = [],[]
    for pi in Plan(p, 0.01):
        print(pi, GetOrientation(pi), model.fk(pi))
        #x.append(model.fk(pi)[0])
        #y.append(model.fk(pi)[1])
    #ax_image.plot(x[:],y[:],'x', color = 'tab:red')

    #x_arr, y_arr = [],[]
    #for point in p.points:
     #   x_arr.append(point[0])
      #  y_arr.append(point[1])
    
    #ax_image.plot(x_arr[:],y_arr[:],'o', color = 'tab:green')
    #plt.show()