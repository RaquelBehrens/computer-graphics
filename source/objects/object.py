from abc import ABC, abstractmethod
import numpy as np

class Object(ABC):
    @abstractmethod
    def __init__(self):
        self.id = None
        self.name = None
        self.points = []
        self.color = None
        self.center = None
        self.clipped = None

    def get_points(self):
        return self.points

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_color(self):
        return self.color
    
    @abstractmethod
    def drawn(self, viewport, normalized_window):
        pass

    @abstractmethod
    def translate(self, viewport, translation_points, normalized_window):
        pass

    @abstractmethod
    def scale(self, viewport, translation_points, normalized_window):
        pass

    @abstractmethod
    def rotate_around_world(self, viewport, rotate_angle, normalized_window):
        pass

    @abstractmethod
    def rotate_around_object(self, viewport, rotate_angle, normalized_window):
        pass

    @abstractmethod
    def rotate_around_point(self, viewport, rotate_points, normalized_window):
        pass

    @abstractmethod
    def obj_string(self, counter):
        pass

    def calculate_center(self):
        center_x = 0
        center_y = 0
        for point in self.points:
            center_x += point[0]
            center_y += point[1]
        self.center = [center_x/len(self.points), center_y/len(self.points)]
