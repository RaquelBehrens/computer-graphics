import numpy as np

from constants import VIEWPORT_HEIGHT
from .object import Object


class Line(Object):
    def __init__(self, name, points, color): #points=[[x1, y1],[x2, y2]]
        super().__init__()
        self.name = name
        self.points = points
        self.color = color
       
    def drawn(self, viewport, normalized_window):
        if normalized_window.clipping_mode.get() == 1:
            new_point = normalized_window.line_clipping_CS(self, self.points)
        else:
            new_point = normalized_window.line_clipping_LB(self, self.points)
        if not self.clipped:
            viewport_y1 = VIEWPORT_HEIGHT - new_point[0][1]
            viewport_y2 = VIEWPORT_HEIGHT - new_point[1][1]
            self.id = viewport.create_line((new_point[0][0], viewport_y1), (new_point[1][0], viewport_y2), width=3, fill=self.color)

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
            if normalized_window.clipping_mode.get() == 1:
                new_point = normalized_window.line_clipping_CS(self, self.points)
            else:
                new_point = normalized_window.line_clipping_LB(self, self.points)
            if not self.clipped:
                viewport_y1 = VIEWPORT_HEIGHT - new_point[0][1]
                viewport_y2 = VIEWPORT_HEIGHT - new_point[1][1]
                viewport.coords(self.id, new_point[0][0], viewport_y1, new_point[1][0], viewport_y2)
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
            if normalized_window.clipping_mode.get() == 1:
                new_point = normalized_window.line_clipping_CS(self, self.points)
            else:
                new_point = normalized_window.line_clipping_LB(self, self.points)
            if not self.clipped:
                viewport_y1 = VIEWPORT_HEIGHT - new_point[0][1]
                viewport_y2 = VIEWPORT_HEIGHT - new_point[1][1]
                viewport.coords(self.id, new_point[0][0], viewport_y1, new_point[1][0], viewport_y2)
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
            if normalized_window.clipping_mode.get() == 1:
                new_point = normalized_window.line_clipping_CS(self, self.points)
            else:
                new_point = normalized_window.line_clipping_LB(self, self.points)
            if not self.clipped:
                viewport_y1 = VIEWPORT_HEIGHT - new_point[0][1]
                viewport_y2 = VIEWPORT_HEIGHT - new_point[1][1]
                viewport.coords(self.id, new_point[0][0], viewport_y1, new_point[1][0], viewport_y2)
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
            if normalized_window.clipping_mode.get() == 1:
                new_point = normalized_window.line_clipping_CS(self, self.points)
            else:
                new_point = normalized_window.line_clipping_LB(self, self.points)
            if not self.clipped:
                viewport_y1 = VIEWPORT_HEIGHT - new_point[0][1]
                viewport_y2 = VIEWPORT_HEIGHT - new_point[1][1]
                viewport.coords(self.id, new_point[0][0], viewport_y1, new_point[1][0], viewport_y2)
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
            if normalized_window.clipping_mode.get() == 1:
                new_point = normalized_window.line_clipping_CS(self, self.points)
            else:
                new_point = normalized_window.line_clipping_LB(self, self.points)
            if not self.clipped:
                viewport_y1 = VIEWPORT_HEIGHT - new_point[0][1]
                viewport_y2 = VIEWPORT_HEIGHT - new_point[1][1]
                viewport.coords(self.id, new_point[0][0], viewport_y1, new_point[1][0], viewport_y2)
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
        points = f"l {points}\n"

        return name, color, points
