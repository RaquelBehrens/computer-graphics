from tkinter import *
import numpy as np
from constants import VIEWPORT_HEIGHT, VIEWPORT_WIDTH
from objects import Line, Wireframe

class NormalizedWindow:
    def __init__(self, viewport):
        self.viewport = viewport
        self.wc = [0, 0]
        self.angle = 0
        self.s = [1, 1]

    def generate_scn(self, object):
        new_points = [None] * len(object.points)
        for i in range(len(new_points)):
            new_points[i] = [None] * 2

        if not isinstance(object, Wireframe):
            for index, point in enumerate(object.points):
                points_matrix = [point[0], point[1], 1]
                result_points = np.matmul(points_matrix, self.transformation_matrix())
                new_points[index][0] = result_points[0]
                new_points[index][1] = result_points[1]

            if isinstance(object, Line):
                viewport_y1 = VIEWPORT_HEIGHT - new_points[0][1]
                viewport_y2 = VIEWPORT_HEIGHT - new_points[1][1]
                self.viewport.coords(object.id, new_points[0][0], viewport_y1, new_points[1][0], viewport_y2)
            else:
                viewport_y1 = VIEWPORT_HEIGHT - new_points[0][1]
                self.viewport.coords(object.id, new_points[0][0], viewport_y1, new_points[0][0], viewport_y1)
        else:
            x_aux = None
            y_aux = None
            first_x = None
            first_y = None

            for i, point in enumerate(object.points):
                points_matrix = [point[0], point[1], 1]
                result_points = np.matmul(points_matrix, self.transformation_matrix())
                new_points[i][0] = result_points[0]
                new_points[i][1] = result_points[1]

                if not (i == 0):
                    viewport_y1 = VIEWPORT_HEIGHT - y_aux
                    viewport_y2 = VIEWPORT_HEIGHT - new_points[i][1]
                    self.viewport.coords(object.list_ids[i], x_aux, viewport_y1, new_points[i][0], viewport_y2)
                else:
                    first_x = new_points[i][0]
                    first_y = new_points[i][1]

                x_aux = new_points[i][0]
                y_aux = new_points[i][1]

            viewport_y1 = VIEWPORT_HEIGHT - y_aux
            viewport_y2 = VIEWPORT_HEIGHT - first_y
            self.viewport.coords(object.list_ids[0], x_aux, viewport_y1, first_x, viewport_y2)

    def transformation_matrix(self):
        rotate_radian = -(np.radians(float(self.angle)))

        translation_matrix = [[1, 0, 0],
                              [0, 1, 0],
                              [-(self.wc[0]), -(self.wc[1]), 1]]
        rotate_matrix = [[np.cos(rotate_radian), -(np.sin(rotate_radian)), 0],
                         [np.sin(rotate_radian), np.cos(rotate_radian), 0],
                         [0, 0, 1]]
        scale_matrix = [[self.s[0], 0, 0],
                        [0, self.s[1], 0],
                        [0, 0, 1]]

        result_matrix = np.matmul(translation_matrix, rotate_matrix)
        result_matrix = np.matmul(result_matrix, scale_matrix)

        return result_matrix

    def define_viewport(self):
        self.viewport.create_rectangle(10, 10, VIEWPORT_WIDTH-10, VIEWPORT_HEIGHT-10, outline='red')
