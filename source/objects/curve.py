import numpy as np

from constants import VIEWPORT_HEIGHT, BEZIER_EPSILON
from .object import Object


class Curve(Object):  #This is a Polygon
    def __init__(self, name, list_points, color, color_mode=1,id=None):
        super().__init__()
        self.name = name
        self.points = list_points #[[x1,y1], [x2,y2], [x3,y3]]
        self.id = id
        self.list_ids = []
        self.color = color

        self.closed = None
        self.color_mode = color_mode
        self.fill_form = None

        self.epsilon = BEZIER_EPSILON
        self.bezier_points = []
            
    def drawn(self, viewport, normalized_window, new_points=None):
        if not new_points:
            self.bezier_points = self.bezier_algorythm(self.points)
        else:
            self.bezier_points = self.bezier_algorythm(new_points)

            for i in range(len(self.list_ids)):
                viewport.delete(self.list_ids[i])
            
            self.list_ids = []

        if self.fill_form != None:
            viewport.delete(self.fill_form)
            self.fill_form = None
            
        new_points = normalized_window.wireframe_clipping(self.bezier_points, self.closed)
        
        if new_points == []:
            self.clipped = True
        else:
            self.clipped = False

        if not self.clipped:
            for i in range(len(new_points)):
                if i < len(new_points) - 1:
                    x1 = new_points[i][0]
                    viewport_y1 = VIEWPORT_HEIGHT - new_points[i][1]

                    x2 = new_points[i+1][0]
                    viewport_y2 = VIEWPORT_HEIGHT - new_points[i+1][1]

                    self.id = viewport.create_line((x1, viewport_y1), (x2, viewport_y2), width=3, fill=self.color)
                    self.list_ids.append(self.id)

            if self.color_mode == 2:
                fill_points = []
                for point in new_points:    
                    fill_points.append([point[0], VIEWPORT_HEIGHT - point[1]])
                self.fill_form = viewport.create_polygon(fill_points, fill=self.color)

    def bezier_algorythm(self, points):
        bezier_matrix = np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]])
        points_set = self.points_set(points)
        new_points = []

        for bezier_points in points_set:
            while len(bezier_points) != 4:
                bezier_points.append([bezier_points[-1][0], bezier_points[-1][1]])
            for i in range(self.epsilon+1):
                t = i / self.epsilon
                t_list = np.array([t * t * t, t * t, t, 1])        
                px = []
                py = []

                for i in range(len(bezier_points)):
                    px.append(bezier_points[i][0])
                    py.append(bezier_points[i][1])

                x = t_list @ bezier_matrix @ px
                y = t_list @ bezier_matrix @ py
                new_points.append([x,y])
    
        return new_points

    def points_set(self, points):
        for i in range(0, len(points) - 1, 3):
            yield points[i : (i + 4)]

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

        self.drawn(viewport, normalized_window)
        normalized_window.update_table(self)

    def rotate_around_object(self, viewport, rotate_angle, normalized_window):
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
        points = f"curv {points}\n"

        return name, color, points
