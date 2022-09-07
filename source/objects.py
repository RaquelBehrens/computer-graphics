from abc import ABC, abstractmethod
from constants import VIEWPORT_HEIGHT, POINT_SIZE

class Object(ABC):
    @abstractmethod
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
    
    @abstractmethod
    def drawn(self, viewport):
        pass

class Point(Object):
    def __init__(self, name, points): #points = (x1, y1)
        super().__init__()
        self.points = points
        self.name = name
        
    def drawn(self, viewport):
        viewport_y1 = VIEWPORT_HEIGHT - self.points[1]
        self.id = viewport.create_oval(self.points[0], viewport_y1, self.points[0], viewport_y1, width=POINT_SIZE, fill="white")

class Line(Object):
    def __init__(self, name, points): #points=(x1, y1),(x2, y2)
        super().__init__()
        self.name = name
        self.points = points
       
    def drawn(self, viewport):
        viewport_y1 = VIEWPORT_HEIGHT - self.points[1]
        viewport_y2 = VIEWPORT_HEIGHT - self.points[3]
        self.id = viewport.create_line((self.points[0], viewport_y1), (self.points[2], viewport_y2), width=3, fill='white')
        
class Wireframe(Object):  #This is a Polygon
    def __init__(self, name, list_ids, *args):
        super().__init__()
        self.name = name
        self.list_ids = list_ids
        for arg in args:
            self.points.append(arg)
            
    def drawn(self, viewport):
        pass
