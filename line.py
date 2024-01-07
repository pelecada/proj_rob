#Contains the Line class and it's functions

import numpy as np

class Line():
    def __init__(self) -> None: #Create Object
        self.points = []

    def SetPoints(self, points:list): #Change points
        self.points = points

    def ReadFile(self, name:str): #Add points from file (line with floats "x y")
        f = open(name)
        lines = f.readlines()
        if(lines[0].split(' ')[0] == "poly"): #If first line starts with "poly" create polygon
            words = lines[0].split(' ')
            n = int(words[1])
            x = float(words[2])
            y = float(words[3])
            r = float(words[4])
            a = float(words[5])
            for i in range(n): #Create edge points
                self.points.append([np.cos(i*2*np.pi/n + a)*r+x,np.sin(i*2*np.pi/n + a)*r+y])
            self.points.append([np.cos(a)*r+x,np.sin(a)*r+y]) #Connect last and first
        else: #Else read points
            for line in lines:
                coords = line.split(' ')
                self.points.append([float(coords[0]),float(coords[1])])

    def Interpolate(self, dist): # Add points so their distance is less than required
        pointsnew = []
        for i in range(len(self.points)-1): #For every original point
            p1 = self.points[i]
            p2 = self.points[i+1]
            distance = np.linalg.norm(np.array(p1)-np.array(p2)) #Get distance
            point_number = int(distance//dist) #Count how many points are needed for the distance
            if (point_number == 0): #If there is no points needed, keep the first one
                pointsnew.append(p1)
            else:
                for t in range(point_number): #Interpolate (from a to b-1)
                    point = [p1[0] + t/point_number*(p2[0]-p1[0]),p1[1] + t/point_number*(p2[1]-p1[1])]
                    pointsnew.append(point)
        pointsnew.append(self.points[-1]) #Add last point at the end
        self.points = pointsnew #Overwrite

