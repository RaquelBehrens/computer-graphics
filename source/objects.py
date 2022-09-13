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
    def drawn(self, viewport, color):
        pass


class Point(Object):
    def __init__(self, name, points): #points = (x1, y1)
        super().__init__()
        self.points = points
        self.name = name
        
    def drawn(self, viewport, color):
        viewport_y1 = VIEWPORT_HEIGHT - self.points[1]
        self.id = viewport.create_oval(self.points[0], viewport_y1, self.points[0], viewport_y1, width=POINT_SIZE, fill=color)


class Line(Object):
    def __init__(self, name, points): #points=[(x1, y1),(x2, y2)]
        super().__init__()
        self.name = name
        self.points = points
       
    def drawn(self, viewport, color):
        viewport_y1 = VIEWPORT_HEIGHT - self.points[0][1]
        viewport_y2 = VIEWPORT_HEIGHT - self.points[1][1]
        self.id = viewport.create_line((self.points[0][0], viewport_y1), (self.points[1][0], viewport_y2), width=3, fill=color)


class Wireframe(Object):  #This is a Polygon
    def __init__(self, name, list_points, id=None):
        super().__init__()
        self.name = name
        self.points = list_points
        self.id = id
        self.list_ids = []
            
    def drawn(self, viewport, color):
        x_aux = None
        viewport_aux_y = None

        first_x = None
        first_viewport_y = None

        for i, point in enumerate(self.points):
            x = point[0]
            viewport_y = VIEWPORT_HEIGHT - point[1]

            if i == 0 :
                x_aux = first_x = point[0]
                viewport_aux_y = first_viewport_y = VIEWPORT_HEIGHT - point[1]
            else:
                id = viewport.create_line((x_aux, viewport_aux_y), (x, viewport_y), width=3, fill=color)
                x_aux = x
                viewport_aux_y = viewport_y
                self.list_ids.append(id)

        self.id = viewport.create_line((x_aux, viewport_aux_y), (first_x, first_viewport_y), width=3, fill=color)
        self.list_ids.append(self.id)
