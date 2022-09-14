from abc import ABC, abstractmethod
from constants import VIEWPORT_HEIGHT, POINT_SIZE
import numpy as np

class Object(ABC):
    @abstractmethod
    def __init__(self):
        self.id = None
        self.name = None
        self.points = []
        self.center = None

    def getPoints(self):
        return self.points

    def getName(self):
        return self.name

    def getId(self):
        return self.id
    
    @abstractmethod
    def drawn(self, viewport):
        pass

    @abstractmethod
    def translate(self, viewport, translation_points):
        pass

    #@abstractmethod
    def escalonate(self, viewport, translation_points):
        pass

    #@abstractmethod
    def rotate_around_world(self, viewport, translation_points):
        pass

    #@abstractmethod
    def rotate_around_object(self, viewport, translation_points):
        pass

    #@abstractmethod
    def rotate_around_point(self, viewport, translation_points):
        pass

    def calculate_center(self):
        center_x = None
        center_y = None
        for point in self.points:
            center_x += point[0]
            center_y += point[1]
        self.center = (center_x/len(self.points), center_y/len(self.points))
        

class Point(Object):
    def __init__(self, name, points, color): #points = [[x1, y1]]
        super().__init__()
        self.points = points
        self.name = name
        self.color = color
        
    def drawn(self, viewport):
        viewport_y1 = VIEWPORT_HEIGHT - self.points[0][1]
        self.id = viewport.create_oval(self.points[0][0], viewport_y1, self.points[0][0], viewport_y1, width=POINT_SIZE, outline=self.color)

    def translate(self, viewport, translation_points):
        translation_points = translation_points.split()
        points_matrix = []
        translation_matrix = [[1, 0, 0],
                              [0, 1, 0],
                              [float(translation_points[0]), float(translation_points[1]), 1]]

        for point in self.points:
            points_matrix = [point[0], point[1], 1]
            result_points = np.matmul(points_matrix, translation_matrix)
            point[0] = result_points[0]
            point[1] = result_points[1]

        #parte de ponto e linha
        viewport_y1 = VIEWPORT_HEIGHT - self.points[0][1]
        viewport.coords(self.id, self.points[0][0], viewport_y1, self.points[0][0], viewport_y1)

class Line(Object):
    def __init__(self, name, points, color): #points=[[x1, y1],[x2, y2]]
        super().__init__()
        self.name = name
        self.points = points
        self.color = color
       
    def drawn(self, viewport):
        viewport_y1 = VIEWPORT_HEIGHT - self.points[0][1]
        viewport_y2 = VIEWPORT_HEIGHT - self.points[1][1]
        self.id = viewport.create_line((self.points[0][0], viewport_y1), (self.points[1][0], viewport_y2), width=3, fill=self.color)

    def translate(self, viewport, translation_points):
        translation_points = translation_points.split()
        points_matrix = []
        translation_matrix = [[1, 0, 0],
                              [0, 1, 0],
                              [float(translation_points[0]), float(translation_points[1]), 1]]

        for point in self.points:
            points_matrix = [point[0], point[1], 1]
            result_points = np.matmul(points_matrix, translation_matrix)
            point[0] = result_points[0]
            point[1] = result_points[1]

        #parte de ponto e linha
        viewport_y1 = VIEWPORT_HEIGHT - self.points[0][1]
        viewport_y2 = VIEWPORT_HEIGHT - self.points[1][1]
        viewport.coords(self.id, self.points[0][0], viewport_y1, self.points[1][0], viewport_y2)

class Wireframe(Object):  #This is a Polygon
    def __init__(self, name, list_points, color, id=None):
        super().__init__()
        self.name = name
        self.points = list_points #[[x1,y1], [x2,y2], [x3,y3]]
        self.id = id
        self.list_ids = []
        self.color = color
            
    def drawn(self, viewport):
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
                id = viewport.create_line((x_aux, viewport_aux_y), (x, viewport_y), width=3, fill=self.color)
                x_aux = x
                viewport_aux_y = viewport_y
                self.list_ids.append(id)

        self.id = viewport.create_line((x_aux, viewport_aux_y), (first_x, first_viewport_y), width=3, fill=self.color)
        self.list_ids.append(self.id)

    def translate(self, viewport, translation_points):
        translation_points = translation_points.split()
        points_matrix = []
        translation_matrix = [[1, 0, 0],
                              [0, 1, 0],
                              [float(translation_points[0]), float(translation_points[1]), 1]]

        x_aux = None
        y_aux = None
        first_x = None
        first_y = None
        for i, point in enumerate(self.points):
            points_matrix = [point[0], point[1], 1]
            result_points = np.matmul(points_matrix, translation_matrix)
            point[0] = result_points[0]
            point[1] = result_points[1]

            if not (i == 0):
                viewport_y1 = VIEWPORT_HEIGHT - y_aux
                viewport_y2 = VIEWPORT_HEIGHT - point[1]
                viewport.coords(self.list_ids[i], x_aux, viewport_y1, point[0], viewport_y2)
            else:
                first_x = point[0]
                first_y = point[1]

            x_aux = point[0]
            y_aux = point[1]

        viewport_y1 = VIEWPORT_HEIGHT - y_aux
        viewport_y2 = VIEWPORT_HEIGHT - first_y
        viewport.coords(self.list_ids[0], x_aux, viewport_y1, first_x, viewport_y2)
