class Line():
    def __init__(self,
        points) -> None:
        self.points = points

    #work with path
    #load from file

    def Interpolate(self, point_number):
        pointsnew = []
        for i in range(len(self.points)-1):
            this = self.points[i]
            that = self.points[i+1]
            for t in range(point_number+1):
                point = [this[0] + t/point_number*(that[0]-this[0]),this[1] + t/point_number*(that[1]-this[1])]
                pointsnew.append(point)
        self.points = pointsnew