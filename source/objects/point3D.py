import numpy as np

from constants import VIEWPORT_HEIGHT, POINT_SIZE
from .object import Object


class Point3D(Object):
    def __init__(self, name, points, color): #points = [[x1, y1, z1]]
        super().__init__()
        self.points = points
        self.name = name
        self.color = color
        
    def drawn(self, viewport, normalized_window):
        normalized_window.point_clipping(self)
        if not self.clipped:
            viewport_y1 = VIEWPORT_HEIGHT - self.points[0][1]
            self.id = viewport.create_oval(self.points[0][0], viewport_y1, self.points[0][0], viewport_y1, width=POINT_SIZE, outline=self.color)

    def calculate_matrix_operation(self, axis, angle):
        if axis == 'x':
            return [[1, 0, 0, 0],
                    [0, (np.cos(angle)), (np.sin(angle)), 0],
                    [0, -(np.sin(angle)), (np.cos(angle)), 0],
                    [0, 0, 0, 1]]
        elif axis == 'y':
            return [[(np.cos(angle)), 0, -(np.sin(angle)), 0],
                    [0, 1, 0, 0],
                    [(np.sin(angle)), 0, (np.cos(angle)), 0],
                    [0, 0, 0, 1]]
        elif axis == 'z':
            return [[(np.cos(angle)), (np.sin(angle)), 0, 0],
                    [-(np.sin(angle)), (np.cos(angle)), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]]
 
    def translate(self, viewport, translation_points, axis, normalized_window):
        translation_points = translation_points.split()
        
        rotate_radian = -(np.radians(float(normalized_window.angle)))
        rotation_matrix = self.calculate_matrix_operation(self, axis, rotate_radian)
        
        points_matrix = []
        translation_matrix = [[1, 0, 0, 0],
                              [0, 1, 0, 0],
                              [0, 0, 1, 0],
                              [float(translation_points[0]), float(translation_points[1]), float(translation_points[2]), 1]]
        
        rotation_matrix_inverse = -(np.radians(float(normalized_window.angle)))
        rotation_matrix = self.calculate_matrix_operation(self, axis, rotate_radian)
        
        for point in self.points:
            points_matrix = [point[0], point[1], point[2], 1]
            result_points = np.matmul(points_matrix, rotation_matrix)
            result_points = np.matmul(result_points, translation_matrix)
            result_points = np.matmul(result_points, rotation_matrix_inverse)
            point[0] = result_points[0]
            point[1] = result_points[1]
            point[3] = result_points[3]

        self.drawn(viewport, normalized_window)
        normalized_window.update_table(self)

    def scale(self, viewport, translation_points, normalized_window):
        if self.center == None:
            self.calculate_center()

        translation_points = translation_points.split()
        points_matrix = []
        first_translation_matrix = [[1, 0, 0, 0],
                                    [0, 1, 0, 0],
                                    [0, 0, 1, 0]
                                    [-(self.center[0]), -(self.center[1]), -(self.center[2]), 1]]

        second_translation_matrix = [[1, 0, 0, 0],
                                     [0, 1, 0, 0],
                                     [0, 0, 1, 0]
                                     [(self.center[0]), (self.center[1]), (self.center[2]), 1]]

        scale_matrix = [[float(translation_points[0]), 0, 0, 0],
                        [0, float(translation_points[1]), 0, 0],
                        [0, 0, float(translation_points[2]), 0],
                        [0, 0, 0, 1]]
        
        for point in self.points:
            points_matrix = [point[0], point[1], point[2], 1]
            result_points = np.matmul(points_matrix, first_translation_matrix)
            result_points = np.matmul(result_points, scale_matrix)
            result_points = np.matmul(result_points, second_translation_matrix)
            point[0] = result_points[0]
            point[1] = result_points[1]
            point[2] = result_points[2]

        self.drawn(viewport, normalized_window)
        normalized_window.update_table(self)

    def rotate_around_world(self, viewport, rotate_angle, axis, normalized_window):
        rotate_radian = -(np.radians(float(rotate_angle)))
        points_matrix = []

        rotation_matrix = self.calculate_matrix_operation(self, axis, rotate_radian)

        for point in self.points:
            points_matrix = [point[0], point[1], point[2], 1]
            result_points = np.matmul(points_matrix, rotation_matrix)
            point[0] = result_points[0]
            point[1] = result_points[1]
            point[2] = result_points[2]

        self.drawn(viewport, normalized_window)
        normalized_window.update_table(self)

    def rotate_around_object(self, viewport, rotate_angle, axis, normalized_window):
        self.calculate_center()
        rotate_radian = -(np.radians(float(rotate_angle)))
        points_matrix = []
        first_translation_matriz = [[1, 0, 0, 0],
                                    [0, 1, 0, 0],
                                    [0, 0, 1, 0]
                                    [-(self.center[0]), -(self.center[1]), -(self.center[2]), 1]]

        second_translation_matriz = [[1, 0, 0, 0],
                                    [0, 1, 0, 0],
                                    [0, 0, 1, 0]
                                    [(self.center[0]), (self.center[1]), (self.center[2]), 1]]

        rotation_matrix = self.calculate_matrix_operation(self, axis, rotate_radian)
        
        for point in self.points:
            points_matrix = [point[0], point[1], point[2], 1]
            result_points = np.matmul(points_matrix, first_translation_matriz)
            result_points = np.matmul(result_points, rotation_matrix)
            result_points = np.matmul(result_points, second_translation_matriz)
            point[0] = result_points[0]
            point[1] = result_points[1]
            point[2] = result_points[2]

        self.drawn(viewport, normalized_window)
        normalized_window.update_table(self)

    def rotate_around_point(self, viewport, rotate_points, axis, normalized_window):
        rotate_points = rotate_points.split()
        point_x = float(rotate_points[1])
        point_y = float(rotate_points[4])
        point_z = float(rotate_points[7])
        rotate_radian = -(np.radians(float(rotate_points[9])))

        first_translation_matriz = [[1, 0, 0, 0],
                                    [0, 1, 0, 0],
                                    [0, 0, 1, 0]
                                    [-(point_x), -(point_y), -(point_z), 1]]

        second_translation_matriz = [[1, 0, 0, 0],
                                    [0, 1, 0, 0],
                                    [0, 0, 1, 0]
                                    [(point_x), (point_y), (point_z), 1]]

        rotation_matrix = self.calculate_matrix_operation(self, axis, rotate_radian)

        for point in self.points:
            points_matrix = [point[0], point[1], point[2], 1]
            result_points = np.matmul(points_matrix, first_translation_matriz)
            result_points = np.matmul(result_points, rotation_matrix)
            result_points = np.matmul(result_points, second_translation_matriz)
            point[0] = result_points[0]
            point[1] = result_points[1]
            point[2] = result_points[2]

        self.drawn(viewport, normalized_window)
        normalized_window.update_table(self)

    def obj_string(self, list_of_points, list_of_colors):
        pass
