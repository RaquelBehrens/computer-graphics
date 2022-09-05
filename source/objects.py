class Object:
    def __init__(self):
        self.id = None
        self.name = None
        self.points = []

    def getPoints(self):
        return self.points

    def getName(self):
        return self.name

    def getId(self):
        return self.id

class Point(Object):
    def __init__(self, name, id, point): #point = (x1, y1)
        super().__init__()
        self.points.append(point)
        self.name = name
        self.id = id

class Line(Object):
    def __init__(self, id, name, point1, point2): #point1=(x1, y1), point2=(x2, y2)
        super().__init__()
        self.id = id
        self.name = name
        self.points.append(point1)
        self.points.append(point2)
        
class Wireframe(Object):  #This is a Polygon
    def __init__(self, id, name, *args):
        super().__init__()
        self.id = id
        self.name = name
        for arg in args:
            self.points.append(arg)
