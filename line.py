import numpy as np

class Line():
    def __init__(self) -> None: #Create Object
        self.points = []

    def SetPoints(self, points:list): #Change points
        self.points = points

    def ReadFile(self, name:str): #Add points from file (line with floats "x y")
        f = open(name)
        lines = f.readlines()
        if(lines[0].split(' ')[0] == "poly"):
            words = lines[0].split(' ')
            n = int(words[1])
            x = float(words[2])
            y = float(words[3])
            r = float(words[4])
            a = float(words[5])
            for i in range(n):
                self.points.append([np.cos(i*2*np.pi/n + a)*r+x,np.sin(i*2*np.pi/n + a)*r+y])
            self.points.append([np.cos(a)*r+x,np.sin(a)*r+y])
        else:
            for line in lines:
                coords = line.split(' ')
                self.points.append([float(coords[0]),float(coords[1])])

    def Interpolate(self, dist): # Add points so their distance is less than required
        pointsnew = []
        for i in range(len(self.points)-1): #For every original point
            this = self.points[i]
            that = self.points[i+1]
            distance = np.linalg.norm(np.array(this)-np.array(that)) #Get distance
            point_number = int(distance//dist) #Count how many points are needed for the distance
            #print(point_number)
            for t in range(point_number): #Interpolate (from a to b-1)
                point = [this[0] + t/point_number*(that[0]-this[0]),this[1] + t/point_number*(that[1]-this[1])]
                pointsnew.append(point)
        pointsnew.append(self.points[-1]) #Add last point at the end
        self.points = pointsnew #Overwrite

