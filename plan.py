from ctu_bosch_sr450 import RobotBosch
import numpy as np

from line import Line
from ik import SortIK
import matplotlib.pyplot as plt

def GetOrientation(q):
    return -np.sign(q[1])

def IKinOrientation(model: RobotBosch, c,p,current):
    qs = SortIK(model, [p[0],p[1],0.5,0],current)
    if c == 0:
        return qs[0]
    for q in qs:
        if GetOrientation(q) == c or GetOrientation(q) == 0:
            return q
    return []

def ChangeConfig():
    ...

def Plan(line:Line, interdist):
    line.Interpolate(interdist)

    model = RobotBosch(tty_dev=None)

    
    for c in [-1,1,0]: #configurations
        q = [[0,0,0,0]]
        for p in line.points: #for each point on line
            qp = IKinOrientation(model, c,p,q[-1]) #try finding q in configuration
            if len(qp) == 0:
                print("No IK")
                break
            else:
                q.append(qp)

        if len(q) == len(line.points)+1:
            break

    vizualization(model, q)

    for i in range(len(q)-1):
        c = GetOrientation(q[i])
        c_next = GetOrientation(q[i+1])        
        if c != c_next and not(c == 0 or c_next == 0):
            ...
            #v pode c chcem najit konfig c_nect pomoci pristupu v přímce o 1 menší a poté přidat do přimky nové body (aby se rovnaly délky)
    return q

def vizualization(model: RobotBosch, q):
    fig: plt.Figure = plt.figure()
    ax_image: plt.Axes = fig.add_subplot(111)
    ax_image.grid(True)
    color = ['tab:blue' , 'tab:green', 'tab:red']

    for qi in q:
        x = model.fk(qi)[0]
        y = model.fk(qi)[1]
        ax_image.plot(x,y,'x', color = color[int(GetOrientation(qi))])

    plt.show() #block = False

if __name__ == "__main__":
    model = RobotBosch(tty_dev=None)
    p = Line([[0, -0.4],[0.4,0],[0,0.4]])
    
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