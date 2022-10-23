import numpy as np

from constants import VIEWPORT_HEIGHT
from .object import Object
from utils import angle_between


class Object3D(Object):
    def __init__(self, name, list_points, list_vectors, color, id=None):
        super().__init__()
        self.name = name
        self.points = list_points #[[x1,y1,z1], [x2,y2,z2], [x3,y3,z3]]
        self.vectors = list_vectors
        self.id = id
        self.list_ids = []
        self.color = color
            
    def drawn(self, viewport, normalized_window, new_points=None):
        pass

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

    def rotate_around_axis(self, viewport, rotate_points, normalized_window):
        rotate_points = rotate_points.split()
        point_x = float(rotate_points[1])
        point_y = float(rotate_points[4])
        rotate_radian = -(np.radians(float(rotate_points[6])))
        
        axis, axis_center = self.find_axis()
        translation_matrix = [[1, 0, 0, 0],
                              [0, 1, 0, 0],
                              [0, 0, 1, 0],
                              [-axis_center[0], -axis_center[1], -axis_center[0], 1]]

        rotate_radian_x = (np.radians(float(angle_between(axis, [1, 0, 0]))))
        rotation_matrix_x = [[1, 0, 0, 0],
                             [0, (np.cos(rotate_radian_x)), (np.sin(rotate_radian_x)), 0],
                             [0, -(np.sin(rotate_radian_x)), (np.cos(rotate_radian_x)), 0],
                             [0, 0, 0, 1]]

        #translation_matrix * rotation_matrix_x 
        #resultado = [[1, 0, 0, 0],
        #             [0, (np.cos(rotate_radian_x)), (np.sin(rotate_radian_x)), 0],
        #             [0, -(np.sin(rotate_radian_x)),  (np.cos(rotate_radian_x)), 0],
        #             [-axis_center[0], 
        #              ((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x)))), 
        #              ((-axis_center[1])*(np.sin(rotate_radian_x)))+((-axis_center[0])*(np.cos(rotate_radian_x))),
        #              1
        #             ]]

        rotate_radian_z = (np.radians(float(angle_between(axis, [0, 0, 1]))))
        rotation_matrix_z = [[(np.cos(rotate_radian_z)), (np.sin(rotate_radian_z)), 0, 0],
                             [-(np.sin(rotate_radian_z)), (np.cos(rotate_radian_z)), 0, 0],
                             [0, 0, 1, 0],
                             [0, 0, 0, 1]]

        #translation_matrix * rotation_matrix_x * rotation_matrix_z
        #resultado2 = [[(np.cos(rotate_radian_z)), 
        #               (np.sin(rotate_radian_z)), 
        #               0, 
        #               0],
        #              [(np.cos(rotate_radian_x))*(-(np.sin(rotate_radian_z)))
        #               (np.cos(rotate_radian_x))*(np.cos(rotate_radian_z)),
        #               (np.sin(rotate_radian_x)),
        #               0],
        #              [((-(np.sin(rotate_radian_x)))*(-(np.sin(rotate_radian_z)))),
        #               ((-(np.sin(rotate_radian_x)))*(np.cos(rotate_radian_z)))
        #               (np.cos(rotate_radian_x)),
        #               0],
        #              [((-axis_center[0])*(np.cos(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))*(-(np.sin(rotate_radian_z)))),
        #               ((-axis_center[0])*(np.sin(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))* (np.cos(rotate_radian_z))),
        #               ((-axis_center[1])*(np.sin(rotate_radian_x)))+((-axis_center[0])*(np.cos(rotate_radian_x))),
        #               1
        #              ]]

        rotate_radian_y = rotate_radian
        rotation_matrix_y = [[(np.cos(rotate_radian_y)), 0, -(np.sin(rotate_radian_y)), 0],
                             [0, 1, 0, 0],
                             [(np.sin(rotate_radian_y)), 0, (np.cos(rotate_radian_y)), 0],
                             [0, 0, 0, 1]]

        #translation_matrix * rotation_matrix_x * rotation_matrix_z * rotation_matrix_y
        #resultado3 = [[(np.cos(rotate_radian_z))*(np.cos(rotate_radian_y)),
        #                ((np.sin(rotate_radian_z))),
        #                ((np.cos(rotate_radian_z))*(-(np.sin(rotate_radian_y)))),
        #                (0)],
        #               [((np.cos(rotate_radian_x))*(-(np.sin(rotate_radian_z)))*(np.cos(rotate_radian_y)))+(np.sin(rotate_radian_x)*(np.sin(rotate_radian_y))),
        #                ((np.cos(rotate_radian_x))*(np.cos(rotate_radian_z))),
        #                ((np.cos(rotate_radian_x))*(-(np.sin(rotate_radian_z)))*(-(np.sin(rotate_radian_y))))+((np.sin(rotate_radian_x))*(np.cos(rotate_radian_y))),
        #                (0)],
        #               [(((-(np.sin(rotate_radian_x)))*(-(np.sin(rotate_radian_z))))*(np.cos(rotate_radian_y)))+(np.cos(rotate_radian_x)*(np.sin(rotate_radian_y))),
        #                (((-(np.sin(rotate_radian_x)))*(np.cos(rotate_radian_z)))),
        #                (((-(np.sin(rotate_radian_x)))*(-(np.sin(rotate_radian_z))))*(-(np.sin(rotate_radian_y))))+((np.cos(rotate_radian_x))*((np.cos(rotate_radian_y)))),
        #                (0)],
        #               [(((-axis_center[0])*(np.cos(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))*(-(np.sin(rotate_radian_z))))*(np.cos(rotate_radian_y)))+(((-axis_center[1])*(np.sin(rotate_radian_x)))+((-axis_center[0])*(np.cos(rotate_radian_x)))*(np.sin(rotate_radian_y))),
        #                ((-axis_center[0])*(np.sin(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))* (np.cos(rotate_radian_z))),
        #                (((-axis_center[0])*(np.cos(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))*(-(np.sin(rotate_radian_z))))*(-(np.sin(rotate_radian_y))))+(((-axis_center[1])*(np.sin(rotate_radian_x)))+((-axis_center[0])*(np.cos(rotate_radian_x)))*(np.cos(rotate_radian_y))),
        #                (1)]]

        undo_rotate_radian_z = -rotate_radian_z
        undo_rotation_matrix_z = [[(np.cos(undo_rotate_radian_z)), (np.sin(undo_rotate_radian_z)), 0, 0],
                                  [-(np.sin(undo_rotate_radian_z)), (np.cos(undo_rotate_radian_z)), 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1]]
        
        #translation_matrix * rotation_matrix_x * rotation_matrix_z * rotation_matrix_y * undo_rotation_matrix_z
        #resultado4 = [[(((np.cos(rotate_radian_z))*(np.cos(rotate_radian_y))*(np.cos(undo_rotate_radian_z)))+(((np.sin(rotate_radian_z)))*(-(np.sin(undo_rotate_radian_z))))),
        #               ((np.cos(rotate_radian_z))*(np.cos(rotate_radian_y))*(np.sin(undo_rotate_radian_z)))+(((np.sin(rotate_radian_z)))* (np.cos(undo_rotate_radian_z))),
        #               ((np.cos(rotate_radian_z))*(-(np.sin(rotate_radian_y)))),
        #               (0)],
        #              [(((np.cos(rotate_radian_x))*(-(np.sin(rotate_radian_z)))*(np.cos(rotate_radian_y)))+(np.sin(rotate_radian_x)*(np.sin(rotate_radian_y)))*(np.cos(undo_rotate_radian_z)))+(((np.cos(rotate_radian_x))*(np.cos(rotate_radian_z)))*(-(np.sin(undo_rotate_radian_z)))),
        #               (((np.cos(rotate_radian_x))*(-(np.sin(rotate_radian_z)))*(np.cos(rotate_radian_y)))+(np.sin(rotate_radian_x)*(np.sin(rotate_radian_y)))*(np.sin(undo_rotate_radian_z)))+(((np.cos(rotate_radian_x))*(np.cos(rotate_radian_z)))*(np.cos(undo_rotate_radian_z))),
        #               (((np.cos(rotate_radian_x))*(-(np.sin(rotate_radian_z)))*(-(np.sin(rotate_radian_y))))+((np.sin(rotate_radian_x))*(np.cos(rotate_radian_y)))),
        #               (0)],
        #              [((((-(np.sin(rotate_radian_x)))*(-(np.sin(rotate_radian_z))))*(np.cos(rotate_radian_y)))+(np.cos(rotate_radian_x)*(np.sin(rotate_radian_y)))*(np.cos(undo_rotate_radian_z)))+((((-(np.sin(rotate_radian_x)))*(np.cos(rotate_radian_z))))*(-(np.sin(undo_rotate_radian_z)))),
        #               ((((-(np.sin(rotate_radian_x)))*(-(np.sin(rotate_radian_z))))*(np.cos(rotate_radian_y)))+(np.cos(rotate_radian_x)*(np.sin(rotate_radian_y)))*(np.sin(undo_rotate_radian_z)))+((((-(np.sin(rotate_radian_x)))*(np.cos(rotate_radian_z))))*(np.cos(undo_rotate_radian_z))),
        #               (((-(np.sin(rotate_radian_x)))*(-(np.sin(rotate_radian_z))))*(-(np.sin(rotate_radian_y))))+((np.cos(rotate_radian_x))*((np.cos(rotate_radian_y)))),
        #               (0)],
        #              [((((-axis_center[0])*(np.cos(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))*(-(np.sin(rotate_radian_z))))*(np.cos(rotate_radian_y)))+(((-axis_center[1])*(np.sin(rotate_radian_x)))+((-axis_center[0])*(np.cos(rotate_radian_x)))*(np.sin(rotate_radian_y)))*(np.cos(undo_rotate_radian_z)))+(((-axis_center[0])*(np.sin(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))* (np.cos(rotate_radian_z)))*(-(np.sin(undo_rotate_radian_z)))),
        #               ((((-axis_center[0])*(np.cos(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))*(-(np.sin(rotate_radian_z))))*(np.cos(rotate_radian_y)))+(((-axis_center[1])*(np.sin(rotate_radian_x)))+((-axis_center[0])*(np.cos(rotate_radian_x)))*(np.sin(rotate_radian_y)))*((np.sin(undo_rotate_radian_z))))+(((-axis_center[0])*(np.sin(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))* (np.cos(rotate_radian_z)))*(np.cos(undo_rotate_radian_z))),
        #               (((-axis_center[0])*(np.cos(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))*(-(np.sin(rotate_radian_z))))*(-(np.sin(rotate_radian_y))))+(((-axis_center[1])*(np.sin(rotate_radian_x)))+((-axis_center[0])*(np.cos(rotate_radian_x)))*(np.cos(rotate_radian_y))),
        #               (1)]]

        undo_rotate_radian_x = -rotate_radian_x
        undo_rotation_matrix_x = [[1, 0, 0, 0],
                             [0, (np.cos(undo_rotate_radian_x)), (np.sin(undo_rotate_radian_x)), 0],
                             [0, -(np.sin(undo_rotate_radian_x)), (np.cos(undo_rotate_radian_x)), 0],
                             [0, 0, 0, 1]]

        #translation_matrix * rotation_matrix_x * rotation_matrix_z * rotation_matrix_y * undo_rotation_matrix_z * undo_rotation_matrix_x
        #resultado5 = [[(((np.cos(rotate_radian_z))*(np.cos(rotate_radian_y))*(np.cos(undo_rotate_radian_z)))+(((np.sin(rotate_radian_z)))*(-(np.sin(undo_rotate_radian_z))))),
        #               ((((np.cos(rotate_radian_z))*(np.cos(rotate_radian_y))*(np.sin(undo_rotate_radian_z)))+(((np.sin(rotate_radian_z)))* (np.cos(undo_rotate_radian_z))))*(np.cos(undo_rotate_radian_x)))+((((np.cos(rotate_radian_z))*(-(np.sin(rotate_radian_y)))))*(-(np.sin(undo_rotate_radian_x)))),
        #               ((((np.cos(rotate_radian_z))*(np.cos(rotate_radian_y))*(np.sin(undo_rotate_radian_z)))+(((np.sin(rotate_radian_z)))* (np.cos(undo_rotate_radian_z))))*(np.sin(undo_rotate_radian_x)))+((((np.cos(rotate_radian_z))*(-(np.sin(rotate_radian_y)))))*((np.cos(undo_rotate_radian_x)))),
        #               (0)],
        #              [(((np.cos(rotate_radian_x))*(-(np.sin(rotate_radian_z)))*(np.cos(rotate_radian_y)))+(np.sin(rotate_radian_x)*(np.sin(rotate_radian_y)))*(np.cos(undo_rotate_radian_z)))+(((np.cos(rotate_radian_x))*(np.cos(rotate_radian_z)))*(-(np.sin(undo_rotate_radian_z)))),
        #               (((((np.cos(rotate_radian_x))*(-(np.sin(rotate_radian_z)))*(np.cos(rotate_radian_y)))+(np.sin(rotate_radian_x)*(np.sin(rotate_radian_y)))*(np.sin(undo_rotate_radian_z)))+(((np.cos(rotate_radian_x))*(np.cos(rotate_radian_z)))*(np.cos(undo_rotate_radian_z))))*(np.cos(undo_rotate_radian_x)))+(((((np.cos(rotate_radian_x))*(-(np.sin(rotate_radian_z)))*(-(np.sin(rotate_radian_y))))+((np.sin(rotate_radian_x))*(np.cos(rotate_radian_y)))))*(-(np.sin(undo_rotate_radian_x)))),
        #               (((((np.cos(rotate_radian_x))*(-(np.sin(rotate_radian_z)))*(np.cos(rotate_radian_y)))+(np.sin(rotate_radian_x)*(np.sin(rotate_radian_y)))*(np.sin(undo_rotate_radian_z)))+(((np.cos(rotate_radian_x))*(np.cos(rotate_radian_z)))*(np.cos(undo_rotate_radian_z))))*(np.sin(undo_rotate_radian_x)))+(((((np.cos(rotate_radian_x))*(-(np.sin(rotate_radian_z)))*(-(np.sin(rotate_radian_y))))+((np.sin(rotate_radian_x))*(np.cos(rotate_radian_y)))))*((np.cos(undo_rotate_radian_x)))),
        #               (0)],
        #              [(((((-(np.sin(rotate_radian_x)))*(-(np.sin(rotate_radian_z))))*(np.cos(rotate_radian_y)))+(np.cos(rotate_radian_x)*(np.sin(rotate_radian_y)))*(np.cos(undo_rotate_radian_z)))+((((-(np.sin(rotate_radian_x)))*(np.cos(rotate_radian_z))))*(-(np.sin(undo_rotate_radian_z))))),
        #               ((((((-(np.sin(rotate_radian_x)))*(-(np.sin(rotate_radian_z))))*(np.cos(rotate_radian_y)))+(np.cos(rotate_radian_x)*(np.sin(rotate_radian_y)))*(np.sin(undo_rotate_radian_z)))+((((-(np.sin(rotate_radian_x)))*(np.cos(rotate_radian_z))))*(np.cos(undo_rotate_radian_z))))*(np.cos(undo_rotate_radian_x)))+(((((-(np.sin(rotate_radian_x)))*(-(np.sin(rotate_radian_z))))*(-(np.sin(rotate_radian_y))))+((np.cos(rotate_radian_x))*((np.cos(rotate_radian_y)))))*(-(np.sin(undo_rotate_radian_x)))),
        #               ((((((-(np.sin(rotate_radian_x)))*(-(np.sin(rotate_radian_z))))*(np.cos(rotate_radian_y)))+(np.cos(rotate_radian_x)*(np.sin(rotate_radian_y)))*(np.sin(undo_rotate_radian_z)))+((((-(np.sin(rotate_radian_x)))*(np.cos(rotate_radian_z))))*(np.cos(undo_rotate_radian_z))))*(np.sin(undo_rotate_radian_x)))+(((((-(np.sin(rotate_radian_x)))*(-(np.sin(rotate_radian_z))))*(-(np.sin(rotate_radian_y))))+((np.cos(rotate_radian_x))*((np.cos(rotate_radian_y)))))*((np.cos(undo_rotate_radian_x)))),
        #               (0)],
        #              [(((((-axis_center[0])*(np.cos(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))*(-(np.sin(rotate_radian_z))))*(np.cos(rotate_radian_y)))+(((-axis_center[1])*(np.sin(rotate_radian_x)))+((-axis_center[0])*(np.cos(rotate_radian_x)))*(np.sin(rotate_radian_y)))*(np.cos(undo_rotate_radian_z)))+(((-axis_center[0])*(np.sin(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))* (np.cos(rotate_radian_z)))*(-(np.sin(undo_rotate_radian_z))))),
        #               ((((((-axis_center[0])*(np.cos(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))*(-(np.sin(rotate_radian_z))))*(np.cos(rotate_radian_y)))+(((-axis_center[1])*(np.sin(rotate_radian_x)))+((-axis_center[0])*(np.cos(rotate_radian_x)))*(np.sin(rotate_radian_y)))*((np.sin(undo_rotate_radian_z))))+(((-axis_center[0])*(np.sin(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))* (np.cos(rotate_radian_z)))*(np.cos(undo_rotate_radian_z))))*(np.cos(undo_rotate_radian_x)))+(((((-axis_center[0])*(np.cos(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))*(-(np.sin(rotate_radian_z))))*(-(np.sin(rotate_radian_y))))+(((-axis_center[1])*(np.sin(rotate_radian_x)))+((-axis_center[0])*(np.cos(rotate_radian_x)))*(np.cos(rotate_radian_y))))*(-(np.sin(undo_rotate_radian_x)))),
        #               ((((((-axis_center[0])*(np.cos(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))*(-(np.sin(rotate_radian_z))))*(np.cos(rotate_radian_y)))+(((-axis_center[1])*(np.sin(rotate_radian_x)))+((-axis_center[0])*(np.cos(rotate_radian_x)))*(np.sin(rotate_radian_y)))*((np.sin(undo_rotate_radian_z))))+(((-axis_center[0])*(np.sin(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))* (np.cos(rotate_radian_z)))*(np.cos(undo_rotate_radian_z))))*(np.sin(undo_rotate_radian_x)))+(((((-axis_center[0])*(np.cos(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))*(-(np.sin(rotate_radian_z))))*(-(np.sin(rotate_radian_y))))+(((-axis_center[1])*(np.sin(rotate_radian_x)))+((-axis_center[0])*(np.cos(rotate_radian_x)))*(np.cos(rotate_radian_y))))*((np.cos(undo_rotate_radian_x)))),
        #               (1)]]

        undo_translation_matrix = [[1, 0, 0, 0],
                                   [0, 1, 0, 0],
                                   [0, 0, 1, 0],
                                   [axis_center[0], axis_center[1], axis_center[0], 1]]

        final_matrix = [[(((np.cos(rotate_radian_z))*(np.cos(rotate_radian_y))*(np.cos(undo_rotate_radian_z)))+(((np.sin(rotate_radian_z)))*(-(np.sin(undo_rotate_radian_z))))),
                         ((((np.cos(rotate_radian_z))*(np.cos(rotate_radian_y))*(np.sin(undo_rotate_radian_z)))+(((np.sin(rotate_radian_z)))* (np.cos(undo_rotate_radian_z))))*(np.cos(undo_rotate_radian_x)))+((((np.cos(rotate_radian_z))*(-(np.sin(rotate_radian_y)))))*(-(np.sin(undo_rotate_radian_x)))),
                         ((((np.cos(rotate_radian_z))*(np.cos(rotate_radian_y))*(np.sin(undo_rotate_radian_z)))+(((np.sin(rotate_radian_z)))* (np.cos(undo_rotate_radian_z))))*(np.sin(undo_rotate_radian_x)))+((((np.cos(rotate_radian_z))*(-(np.sin(rotate_radian_y)))))*((np.cos(undo_rotate_radian_x)))),
                         (0)],
                        [(((np.cos(rotate_radian_x))*(-(np.sin(rotate_radian_z)))*(np.cos(rotate_radian_y)))+(np.sin(rotate_radian_x)*(np.sin(rotate_radian_y)))*(np.cos(undo_rotate_radian_z)))+(((np.cos(rotate_radian_x))*(np.cos(rotate_radian_z)))*(-(np.sin(undo_rotate_radian_z)))),
                         (((((np.cos(rotate_radian_x))*(-(np.sin(rotate_radian_z)))*(np.cos(rotate_radian_y)))+(np.sin(rotate_radian_x)*(np.sin(rotate_radian_y)))*(np.sin(undo_rotate_radian_z)))+(((np.cos(rotate_radian_x))*(np.cos(rotate_radian_z)))*(np.cos(undo_rotate_radian_z))))*(np.cos(undo_rotate_radian_x)))+(((((np.cos(rotate_radian_x))*(-(np.sin(rotate_radian_z)))*(-(np.sin(rotate_radian_y))))+((np.sin(rotate_radian_x))*(np.cos(rotate_radian_y)))))*(-(np.sin(undo_rotate_radian_x)))),
                         (((((np.cos(rotate_radian_x))*(-(np.sin(rotate_radian_z)))*(np.cos(rotate_radian_y)))+(np.sin(rotate_radian_x)*(np.sin(rotate_radian_y)))*(np.sin(undo_rotate_radian_z)))+(((np.cos(rotate_radian_x))*(np.cos(rotate_radian_z)))*(np.cos(undo_rotate_radian_z))))*(np.sin(undo_rotate_radian_x)))+(((((np.cos(rotate_radian_x))*(-(np.sin(rotate_radian_z)))*(-(np.sin(rotate_radian_y))))+((np.sin(rotate_radian_x))*(np.cos(rotate_radian_y)))))*((np.cos(undo_rotate_radian_x)))),
                         (0)],
                        [(((((-(np.sin(rotate_radian_x)))*(-(np.sin(rotate_radian_z))))*(np.cos(rotate_radian_y)))+(np.cos(rotate_radian_x)*(np.sin(rotate_radian_y)))*(np.cos(undo_rotate_radian_z)))+((((-(np.sin(rotate_radian_x)))*(np.cos(rotate_radian_z))))*(-(np.sin(undo_rotate_radian_z))))),
                         ((((((-(np.sin(rotate_radian_x)))*(-(np.sin(rotate_radian_z))))*(np.cos(rotate_radian_y)))+(np.cos(rotate_radian_x)*(np.sin(rotate_radian_y)))*(np.sin(undo_rotate_radian_z)))+((((-(np.sin(rotate_radian_x)))*(np.cos(rotate_radian_z))))*(np.cos(undo_rotate_radian_z))))*(np.cos(undo_rotate_radian_x)))+(((((-(np.sin(rotate_radian_x)))*(-(np.sin(rotate_radian_z))))*(-(np.sin(rotate_radian_y))))+((np.cos(rotate_radian_x))*((np.cos(rotate_radian_y)))))*(-(np.sin(undo_rotate_radian_x)))),
                         ((((((-(np.sin(rotate_radian_x)))*(-(np.sin(rotate_radian_z))))*(np.cos(rotate_radian_y)))+(np.cos(rotate_radian_x)*(np.sin(rotate_radian_y)))*(np.sin(undo_rotate_radian_z)))+((((-(np.sin(rotate_radian_x)))*(np.cos(rotate_radian_z))))*(np.cos(undo_rotate_radian_z))))*(np.sin(undo_rotate_radian_x)))+(((((-(np.sin(rotate_radian_x)))*(-(np.sin(rotate_radian_z))))*(-(np.sin(rotate_radian_y))))+((np.cos(rotate_radian_x))*((np.cos(rotate_radian_y)))))*((np.cos(undo_rotate_radian_x)))),
                         (0)],
                        [((((((-axis_center[0])*(np.cos(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))*(-(np.sin(rotate_radian_z))))*(np.cos(rotate_radian_y)))+(((-axis_center[1])*(np.sin(rotate_radian_x)))+((-axis_center[0])*(np.cos(rotate_radian_x)))*(np.sin(rotate_radian_y)))*(np.cos(undo_rotate_radian_z)))+(((-axis_center[0])*(np.sin(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))* (np.cos(rotate_radian_z)))*(-(np.sin(undo_rotate_radian_z))))))+(axis_center[0]),
                         (((((((-axis_center[0])*(np.cos(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))*(-(np.sin(rotate_radian_z))))*(np.cos(rotate_radian_y)))+(((-axis_center[1])*(np.sin(rotate_radian_x)))+((-axis_center[0])*(np.cos(rotate_radian_x)))*(np.sin(rotate_radian_y)))*((np.sin(undo_rotate_radian_z))))+(((-axis_center[0])*(np.sin(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))* (np.cos(rotate_radian_z)))*(np.cos(undo_rotate_radian_z))))*(np.cos(undo_rotate_radian_x)))+(((((-axis_center[0])*(np.cos(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))*(-(np.sin(rotate_radian_z))))*(-(np.sin(rotate_radian_y))))+(((-axis_center[1])*(np.sin(rotate_radian_x)))+((-axis_center[0])*(np.cos(rotate_radian_x)))*(np.cos(rotate_radian_y))))*(-(np.sin(undo_rotate_radian_x)))))+(axis_center[1]),
                         (((((((-axis_center[0])*(np.cos(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))*(-(np.sin(rotate_radian_z))))*(np.cos(rotate_radian_y)))+(((-axis_center[1])*(np.sin(rotate_radian_x)))+((-axis_center[0])*(np.cos(rotate_radian_x)))*(np.sin(rotate_radian_y)))*((np.sin(undo_rotate_radian_z))))+(((-axis_center[0])*(np.sin(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))* (np.cos(rotate_radian_z)))*(np.cos(undo_rotate_radian_z))))*(np.cos(undo_rotate_radian_x)))+(((((-axis_center[0])*(np.cos(rotate_radian_z)))+(((-axis_center[1])*(np.cos(rotate_radian_x)))+((-axis_center[0])*(-(np.sin(rotate_radian_x))))*(-(np.sin(rotate_radian_z))))*(-(np.sin(rotate_radian_y))))+(((-axis_center[1])*(np.sin(rotate_radian_x)))+((-axis_center[0])*(np.cos(rotate_radian_x)))*(np.cos(rotate_radian_y))))*(-(np.sin(undo_rotate_radian_x)))))+(axis_center[2]),
                         1]]

        for point in self.points:
            points_matrix = [point[0], point[1], point[2], 1]

            #result_points = np.matmul(points_matrix, translation_matrix)
            #result_points = np.matmul(result_points, rotation_matrix_x)
            #result_points = np.matmul(result_points, rotation_matrix_z)
            #result_points = np.matmul(result_points, rotation_matrix_y)
            #result_points = np.matmul(result_points, undo_rotation_matrix_z)
            #result_points = np.matmul(result_points, undo_rotation_matrix_x)
            #result_points = np.matmul(result_points, undo_translation_matrix)

            result_points = np.matmul(points_matrix, final_matrix)

            point[0] = result_points[0]
            point[1] = result_points[1]
            point[2] = result_points[2]

        self.drawn(viewport, normalized_window)
        normalized_window.update_table(self)

    def find_axis(self):
        axis = [self.points[0], self.points[(len(self.points)+1)//2]]
        axis_center_x = (axis[0][0] + axis[1][0]) / 2
        axis_center_y = (axis[0][1] + axis[1][1]) / 2
        axis_center_z = (axis[0][2] + axis[1][2]) / 2
        return axis, [axis_center_x, axis_center_y, axis_center_z]
 
    def obj_string(self, list_of_points, list_of_colors):
        pass
