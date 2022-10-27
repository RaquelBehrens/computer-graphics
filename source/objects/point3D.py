import numpy as np

from constants import VIEWPORT_HEIGHT, POINT_SIZE
from .object import Object


class Point3D(Object):
    def __init__(self, name, points, color): #points = [[x1, y1, z1]]
        super().__init__()
        self.points = points
        self.name = name
        self.color = color
        
    def drawn(self, viewport, normalized_window, new_points=[]):
        if new_points == []:
            new_points = self.points

        normalized_window.point_clipping(self, new_points)
        if not self.clipped:
            viewport_y1 = VIEWPORT_HEIGHT - new_points[0][1]
            viewport.delete(self.id)
            self.id = viewport.create_oval(new_points[0][0], viewport_y1, new_points[0][0], viewport_y1, width=POINT_SIZE, outline=self.color)
        else:
            viewport.delete(self.id)

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
 
    def translate(self, viewport, translation_points, normalized_window):
        translation_points = translation_points.split()
        axis = translation_points[5]
        if axis == 'x':
            rotate_radian = -(np.radians(float(normalized_window.angle_x)))
        elif axis == 'y':
            rotate_radian = -(np.radians(float(normalized_window.angle_y)))
        else:
            rotate_radian = -(np.radians(float(normalized_window.angle_z)))

        rotation_matrix = self.calculate_matrix_operation(axis, rotate_radian)
        
        points_matrix = []
        translation_matrix = [[1, 0, 0, 0],
                              [0, 1, 0, 0],
                              [0, 0, 1, 0],
                              [float(translation_points[0]), float(translation_points[1]), float(translation_points[2]), 1]]
        
        rotate_radian = -rotate_radian
        rotation_matrix_inverse = self.calculate_matrix_operation(axis, rotate_radian)

        for point in self.points:
            points_matrix = [point[0], point[1], point[2], 1]
            result_points = np.matmul(points_matrix, rotation_matrix)
            result_points = np.matmul(result_points, translation_matrix)
            result_points = np.matmul(result_points, rotation_matrix_inverse)

            point[0] = result_points[0]
            point[1] = result_points[1]
            point[2] = result_points[2]

        self.drawn(viewport, normalized_window)
        normalized_window.update_table(self)

    def scale(self, viewport, scalation_points, normalized_window):
        if self.center == None:
            self.calculate_center()

        scalation_points = scalation_points.split()
        points_matrix = []
        first_translation_matrix = [[1, 0, 0, 0],
                                    [0, 1, 0, 0],
                                    [0, 0, 1, 0],
                                    [-(self.center[0]), -(self.center[1]), -(self.center[2]), 1]]

        second_translation_matrix = [[1, 0, 0, 0],
                                     [0, 1, 0, 0],
                                     [0, 0, 1, 0],
                                     [(self.center[0]), (self.center[1]), (self.center[2]), 1]]

        scale_matrix = [[float(scalation_points[0]), 0, 0, 0],
                        [0, float(scalation_points[1]), 0, 0],
                        [0, 0, float(scalation_points[2]), 0],
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

    def rotate_around_world(self, viewport, enter_data, normalized_window):
        enter_data = enter_data.split()
        axis = enter_data[2]
        rotate_radian = -(np.radians(float(enter_data[0])))
        points_matrix = []

        rotation_matrix = self.calculate_matrix_operation(axis, rotate_radian)

        for point in self.points:
            points_matrix = [point[0], point[1], point[2], 1]
            result_points = np.matmul(points_matrix, rotation_matrix)
            point[0] = result_points[0]
            point[1] = result_points[1]
            point[2] = result_points[2]

        self.drawn(viewport, normalized_window)
        normalized_window.update_table(self)

    def rotate_around_object(self, viewport, enter_data, normalized_window):
        self.calculate_center()
        enter_data = enter_data.split()
        axis = enter_data[2]
        rotate_radian = -(np.radians(float(enter_data[0])))

        points_matrix = []
        first_translation_matriz = [[1, 0, 0, 0],
                                    [0, 1, 0, 0],
                                    [0, 0, 1, 0],
                                    [-(self.center[0]), -(self.center[1]), -(self.center[2]), 1]]

        second_translation_matriz = [[1, 0, 0, 0],
                                    [0, 1, 0, 0],
                                    [0, 0, 1, 0],
                                    [(self.center[0]), (self.center[1]), (self.center[2]), 1]]

        rotation_matrix = self.calculate_matrix_operation(axis, rotate_radian)
        
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

    def rotate_around_point(self, viewport, rotate_points, normalized_window):
        rotate_points = rotate_points.split()
        point_x = float(rotate_points[1])
        point_y = float(rotate_points[4])
        point_z = float(rotate_points[7])
        rotate_radian = -(np.radians(float(rotate_points[9])))
        axis = rotate_points[11]

        first_translation_matriz = [[1, 0, 0, 0],
                                    [0, 1, 0, 0],
                                    [0, 0, 1, 0],
                                    [-(point_x), -(point_y), -(point_z), 1]]

        second_translation_matriz = [[1, 0, 0, 0],
                                    [0, 1, 0, 0],
                                    [0, 0, 1, 0],
                                    [(point_x), (point_y), (point_z), 1]]

        rotation_matrix = self.calculate_matrix_operation(axis, rotate_radian)

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

    def calculate_center(self):
        center_x = 0
        center_y = 0
        center_z = 0
        for point in self.points:
            center_x += point[0]
            center_y += point[1]
            center_z += point[2]
        self.center = [center_x/len(self.points), center_y/len(self.points), center_y/len(self.points)]

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

