import numpy as np

class Line():
    def __init__(self,
        points) -> None:
        self.points = points

    #work with path
    #load from file

    def Interpolate(self, dist):
        pointsnew = []
        for i in range(len(self.points)-1):
            this = self.points[i]
            that = self.points[i+1]
            distance = np.linalg.norm(np.array(this)-np.array(that))
            point_number = int(distance//dist)
            print(point_number)
            for t in range(point_number):
                point = [this[0] + t/point_number*(that[0]-this[0]),this[1] + t/point_number*(that[1]-this[1])]
                pointsnew.append(point)
        pointsnew.append(self.points[-1])
        self.points = pointsnew