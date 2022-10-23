import numpy as np

from constants import VIEWPORT_HEIGHT, POINT_SIZE
from .object import Object


class Point(Object):
    def __init__(self, name, points, color): #points = [[x1, y1]]
        super().__init__()
        self.points = points
        self.name = name
        self.color = color
        
    def drawn(self, viewport, normalized_window, new_points=None):
        if new_points == None:
            new_points = self.points

        normalized_window.point_clipping(self, new_points)
        if not self.clipped:
            viewport_y1 = VIEWPORT_HEIGHT - new_points[0][1]
            viewport.delete(self.id)
            self.id = viewport.create_oval(new_points[0][0], viewport_y1, new_points[0][0], viewport_y1, width=POINT_SIZE, outline=self.color)
        else:
            viewport.delete(self.id)
                
    def translate(self, viewport, translation_points, normalized_window):
        translation_points = translation_points.split()
        
        rotate_radian = -(np.radians(float(normalized_window.angle)))
        rotation_matrix = [[np.cos(rotate_radian), -(np.sin(rotate_radian)), 0],
                           [np.sin(rotate_radian), np.cos(rotate_radian), 0],
                           [0, 0, 1]]
    
        points_matrix = []
        translation_matrix = [[1, 0, 0],
                              [0, 1, 0],
                              [float(translation_points[0]), float(translation_points[1]), 1]]
        
        rotate_radian = (np.radians(float(normalized_window.angle)))
        rotation_matrix_inverse = [[np.cos(rotate_radian), -(np.sin(rotate_radian)), 0],
                                   [np.sin(rotate_radian), np.cos(rotate_radian), 0],
                                   [0, 0, 1]]

        for point in self.points:
            points_matrix = [point[0], point[1], 1]
            result_points = np.matmul(points_matrix, rotation_matrix)
            result_points = np.matmul(result_points, translation_matrix)
            result_points = np.matmul(result_points, rotation_matrix_inverse)
            point[0] = result_points[0]
            point[1] = result_points[1]

        #parte de ponto e linha
        if self.id != None:
            normalized_window.point_clipping(self)
            if not self.clipped:
                viewport_y1 = VIEWPORT_HEIGHT - self.points[0][1]
                viewport.coords(self.id, self.points[0][0], viewport_y1, self.points[0][0], viewport_y1)
        else:
            self.drawn(viewport, normalized_window)
            normalized_window.update_table(self)

    def scale(self, viewport, translation_points, normalized_window):
        if self.center == None:
            self.calculate_center()

        translation_points = translation_points.split()
        points_matrix = []
        first_translation_matrix = [[1, 0, 0],
                                    [0, 1, 0],
                                    [-(self.center[0]), -(self.center[1]), 1]]

        second_translation_matrix = [[1, 0, 0],
                                     [0, 1, 0],
                                     [(self.center[0]), (self.center[1]), 1]]

        scale_matrix = [[float(translation_points[0]), 0, 0],
                        [0, float(translation_points[1]), 0],
                        [0, 0, 1]]

        for point in self.points:
            points_matrix = [point[0], point[1], 1]
            result_points = np.matmul(points_matrix, first_translation_matrix)
            result_points = np.matmul(result_points, scale_matrix)
            result_points = np.matmul(result_points, second_translation_matrix)
            point[0] = result_points[0]
            point[1] = result_points[1]

        #parte de ponto e linha
        if self.id != None:
            normalized_window.point_clipping(self)
            if not self.clipped:
                viewport_y1 = VIEWPORT_HEIGHT - self.points[0][1]
                viewport.coords(self.id, self.points[0][0], viewport_y1, self.points[0][0], viewport_y1)
        else:
            self.drawn(viewport, normalized_window)
            normalized_window.update_table(self)

    def rotate_around_world(self, viewport, rotate_angle, normalized_window):
        rotate_radian = -(np.radians(float(rotate_angle)))
        points_matrix = []
        rotation_matrix = [[np.cos(rotate_radian), -(np.sin(rotate_radian)), 0],
                            [np.sin(rotate_radian), np.cos(rotate_radian), 0],
                            [0, 0, 1]]

        for point in self.points:
            points_matrix = [point[0], point[1], 1]
            result_points = np.matmul(points_matrix, rotation_matrix)
            point[0] = result_points[0]
            point[1] = result_points[1]

        if self.id != None:
            normalized_window.point_clipping(self)
            if not self.clipped:
                viewport_y1 = VIEWPORT_HEIGHT - self.points[0][1]
                viewport.coords(self.id, self.points[0][0], viewport_y1, self.points[0][0], viewport_y1)
        else:
            self.drawn(viewport, normalized_window)
            normalized_window.update_table(self)

    def rotate_around_object(self, viewport, rotate_angle, normalized_window):
        if self.center == None:
            self.calculate_center()
        
        rotate_radian = -(np.radians(float(rotate_angle)))
        points_matrix = []
        first_translation_matriz = [[1, 0, 0],
                                    [0, 1, 0],
                                    [-(self.center[0]), -(self.center[1]), 1]]
        second_translation_matriz = [[1, 0, 0],
                                     [0, 1, 0],
                                     [self.center[0], self.center[1], 1]]
        rotation_matrix = [[np.cos(rotate_radian), -(np.sin(rotate_radian)), 0],
                            [np.sin(rotate_radian), np.cos(rotate_radian), 0],
                            [0, 0, 1]]

        for point in self.points:
            points_matrix = [point[0], point[1], 1]
            result_points = np.matmul(points_matrix, first_translation_matriz)
            result_points = np.matmul(result_points, rotation_matrix)
            result_points = np.matmul(result_points, second_translation_matriz)
            point[0] = result_points[0]
            point[1] = result_points[1]

        if self.id != None:
            normalized_window.point_clipping(self)
            if not self.clipped:
                viewport_y1 = VIEWPORT_HEIGHT - self.points[0][1]
                viewport.coords(self.id, self.points[0][0], viewport_y1, self.points[0][0], viewport_y1)
        else:
            self.drawn(viewport, normalized_window)
            normalized_window.update_table(self)

    def rotate_around_point(self, viewport, rotate_points, normalized_window):
        rotate_points = rotate_points.split()
        point_x = float(rotate_points[1])
        point_y = float(rotate_points[4])
        rotate_radian = -(np.radians(float(rotate_points[6])))

        points_matrix = []
        first_translation_matriz = [[1, 0, 0],
                                    [0, 1, 0],
                                    [-(point_x), -(point_y), 1]]
        second_translation_matriz = [[1, 0, 0],
                                     [0, 1, 0],
                                     [point_x, point_y, 1]]
        rotation_matrix = [[np.cos(rotate_radian), -(np.sin(rotate_radian)), 0],
                            [np.sin(rotate_radian), np.cos(rotate_radian), 0],
                            [0, 0, 1]]

        for point in self.points:
            points_matrix = [point[0], point[1], 1]
            result_points = np.matmul(points_matrix, first_translation_matriz)
            result_points = np.matmul(result_points, rotation_matrix)
            result_points = np.matmul(result_points, second_translation_matriz)
            point[0] = result_points[0]
            point[1] = result_points[1]

        if self.id != None:
            normalized_window.point_clipping(self)
            if not self.clipped:
                viewport_y1 = VIEWPORT_HEIGHT - self.points[0][1]
                viewport.coords(self.id, self.points[0][0], viewport_y1, self.points[0][0], viewport_y1)
        else:
            self.drawn(viewport, normalized_window)
            normalized_window.update_table(self)

    def obj_string(self, list_of_points, list_of_colors):
        points = []

        name = f"o {self.name}\n"
        color = f"usemtl {list_of_colors.get(self.color)}\n"

        for point in self.points:
            point_index = list(list_of_points.keys())[list(list_of_points.values()).index(point)]
            points.append(point_index)

        points = " ".join(map(str,points))
        points = f"p {points}\n"

        return name, color, points
