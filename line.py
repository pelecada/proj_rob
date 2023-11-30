import numpy as np

class Line():
    def __init__(self) -> None:
        self.points = []

    def SetPoints(self, points:list):
        self.points = points

    def ReadFile(self, name:str):
        f = open(name)
        lines = f.readlines()
        for line in lines:
            coords = line.split(' ')
            self.points.append([float(coords[0]),float(coords[1])])

    def Interpolate(self, dist):
        pointsnew = []
        for i in range(len(self.points)-1):
            this = self.points[i]
            that = self.points[i+1]
            distance = np.linalg.norm(np.array(this)-np.array(that))
            point_number = int(distance//dist)
            #print(point_number)
            for t in range(point_number):
                point = [this[0] + t/point_number*(that[0]-this[0]),this[1] + t/point_number*(that[1]-this[1])]
                pointsnew.append(point)
        pointsnew.append(self.points[-1])
        self.points = pointsnew

