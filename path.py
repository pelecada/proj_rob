from dirimport import DirImportFn
DirImportFn()

import numpy as np
from CRS_commander import Commander

from model import Model
from robotics_toolbox.core import SE2

class Path():
    def __init__(self,
        points) -> None:
        self.points = points

    #work with path
    #load from file

    def Interpolate(self):
        pointsnew = []
        for i in range(len(self.points)-1):
            this = self.points[i]
            that = self.points[i+1]
            for t in range(100+1):
                point = [this[0] + t/100*(that[0]-this[0]),this[1] + t/100*(that[1]-this[1])]
                pointsnew.append(point)
        self.points = pointsnew

    #check continuity/validity of path with model
    #create instructions for path, run it