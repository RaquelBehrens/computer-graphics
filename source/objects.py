from abc import ABC, abstractmethod
from constants import VIEWPORT_HEIGHT, POINT_SIZE
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
    def translate(self, viewport, translation_points, coord_scn):
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


class Point(Object):
    def __init__(self, name, points, color): #points = [[x1, y1]]
        super().__init__()
        self.points = points
        self.name = name
        self.color = color
        
    def drawn(self, viewport, normalized_window):
        normalized_window.point_clipping(self)
        if not self.clipped:
            viewport_y1 = VIEWPORT_HEIGHT - self.points[0][1]
            self.id = viewport.create_oval(self.points[0][0], viewport_y1, self.points[0][0], viewport_y1, width=POINT_SIZE, outline=self.color)

    def translate(self, viewport, translation_points, coord_scn):
        translation_points = translation_points.split()
        
        rotate_radian = -(np.radians(float(coord_scn.angle)))
        rotation_matrix = [[np.cos(rotate_radian), -(np.sin(rotate_radian)), 0],
                           [np.sin(rotate_radian), np.cos(rotate_radian), 0],
                           [0, 0, 1]]
    
        points_matrix = []
        translation_matrix = [[1, 0, 0],
                              [0, 1, 0],
                              [float(translation_points[0]), float(translation_points[1]), 1]]
        
        rotate_radian = (np.radians(float(coord_scn.angle)))
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
            coord_scn.point_clipping(self)
            if not self.clipped:
                viewport_y1 = VIEWPORT_HEIGHT - self.points[0][1]
                viewport.coords(self.id, self.points[0][0], viewport_y1, self.points[0][0], viewport_y1)
        else:
            self.drawn(viewport, coord_scn)
            coord_scn.update_table(self)

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

    def translate(self, viewport, translation_points, coord_scn):
        translation_points = translation_points.split()
        
        rotate_radian = -(np.radians(float(coord_scn.angle)))
        rotation_matrix = [[np.cos(rotate_radian), -(np.sin(rotate_radian)), 0],
                           [np.sin(rotate_radian), np.cos(rotate_radian), 0],
                           [0, 0, 1]]
        
        points_matrix = []
        translation_matrix = [[1, 0, 0],
                              [0, 1, 0],
                              [float(translation_points[0]), float(translation_points[1]), 1]]
       
        rotate_radian = (np.radians(float(coord_scn.angle)))
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
            if coord_scn.clipping_mode.get() == 1:
                new_point = coord_scn.line_clipping_CS(self, self.points)
            else:
                new_point = coord_scn.line_clipping_LB(self, self.points)
            if not self.clipped:
                viewport_y1 = VIEWPORT_HEIGHT - new_point[0][1]
                viewport_y2 = VIEWPORT_HEIGHT - new_point[1][1]
                viewport.coords(self.id, new_point[0][0], viewport_y1, new_point[1][0], viewport_y2)
        else:
            self.drawn(viewport, coord_scn)
            coord_scn.update_table(self)

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


class Wireframe(Object):  #This is a Polygon
    def __init__(self, name, list_points, color, id=None):
        super().__init__()
        self.name = name
        self.points = list_points #[[x1,y1], [x2,y2], [x3,y3]]
        self.id = id
        self.list_ids = []
        self.color = color
            
    def drawn(self, viewport, normalized_window):
        x_aux = None
        viewport_aux_y = None

        first_x = None
        first_viewport_y = None

        new_points = normalized_window.wireframe_clipping(self, self.points)

        if not self.clipped:
            for i, point in enumerate(new_points):
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

    def translate(self, viewport, translation_points, coord_scn):
        translation_points = translation_points.split()
        
        rotate_radian = -(np.radians(float(coord_scn.angle)))
        rotation_matrix = [[np.cos(rotate_radian), -(np.sin(rotate_radian)), 0],
                           [np.sin(rotate_radian), np.cos(rotate_radian), 0],
                           [0, 0, 1]]
        
        points_matrix = []
        translation_matrix = [[1, 0, 0],
                              [0, 1, 0],
                              [float(translation_points[0]), float(translation_points[1]), 1]]
        
        rotate_radian = (np.radians(float(coord_scn.angle)))
        rotation_matrix_inverse = [[np.cos(rotate_radian), -(np.sin(rotate_radian)), 0],
                                   [np.sin(rotate_radian), np.cos(rotate_radian), 0],
                                   [0, 0, 1]]

        for i, point in enumerate(self.points):
            points_matrix = [point[0], point[1], 1]
            result_points = np.matmul(points_matrix, rotation_matrix)
            result_points = np.matmul(result_points, translation_matrix)
            result_points = np.matmul(result_points, rotation_matrix_inverse)
            point[0] = result_points[0]
            point[1] = result_points[1]

        if self.id != None:
            new_points = coord_scn.wireframe_clipping(self, self.points)
            x_aux = None
            y_aux = None
            first_x = None
            first_y = None
            for i, point in enumerate(new_points):
                if not (i == 0):
                    viewport_y1 = VIEWPORT_HEIGHT - y_aux
                    viewport_y2 = VIEWPORT_HEIGHT - point[1]
                    viewport.coords(self.list_ids[i-1], x_aux, viewport_y1, point[0], viewport_y2)
                else:
                    first_x = point[0]
                    first_y = point[1]

                x_aux = point[0]
                y_aux = point[1]

            viewport_y1 = VIEWPORT_HEIGHT - y_aux
            viewport_y2 = VIEWPORT_HEIGHT - first_y
            viewport.coords(self.id, x_aux, viewport_y1, first_x, viewport_y2)
        else:
            self.drawn(viewport, coord_scn)
            coord_scn.update_table(self)

    
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

        for i, point in enumerate(self.points):
                points_matrix = [point[0], point[1], 1]
                result_points = np.matmul(points_matrix, first_translation_matrix)
                result_points = np.matmul(result_points, scale_matrix)
                result_points = np.matmul(result_points, second_translation_matrix)
                point[0] = result_points[0]
                point[1] = result_points[1]

        if self.id != None:
            new_points = normalized_window.wireframe_clipping(self, self.points)
            x_aux = None
            y_aux = None
            first_x = None
            first_y = None
            for i, point in enumerate(new_points):
                if not (i == 0):
                    viewport_y1 = VIEWPORT_HEIGHT - y_aux
                    viewport_y2 = VIEWPORT_HEIGHT - point[1]
                    viewport.coords(self.list_ids[i-1], x_aux, viewport_y1, point[0], viewport_y2)
                else:
                    first_x = point[0]
                    first_y = point[1]

                x_aux = point[0]
                y_aux = point[1]

            viewport_y1 = VIEWPORT_HEIGHT - y_aux
            viewport_y2 = VIEWPORT_HEIGHT - first_y
            viewport.coords(self.id, x_aux, viewport_y1, first_x, viewport_y2)

        else:
            self.drawn(viewport, normalized_window)
            normalized_window.update_table(self)

    def rotate_around_world(self, viewport, rotate_angle, normalized_window):
        rotate_radian = -(np.radians(float(rotate_angle)))
        points_matrix = []
        rotation_matrix = [[np.cos(rotate_radian), -(np.sin(rotate_radian)), 0],
                           [np.sin(rotate_radian), np.cos(rotate_radian), 0],
                           [0, 0, 1]]

        for i, point in enumerate(self.points):
            points_matrix = [point[0], point[1], 1]
            result_points = np.matmul(points_matrix, rotation_matrix)
            point[0] = result_points[0]
            point[1] = result_points[1]

        if self.id != None:
            new_points = normalized_window.wireframe_clipping(self, self.points)
            x_aux = None
            y_aux = None
            first_x = None
            first_y = None
            for i, point in enumerate(new_points):
                if not (i == 0):
                    viewport_y1 = VIEWPORT_HEIGHT - y_aux
                    viewport_y2 = VIEWPORT_HEIGHT - point[1]
                    viewport.coords(self.list_ids[i-1], x_aux, viewport_y1, point[0], viewport_y2)
                else:
                    first_x = point[0]
                    first_y = point[1]

                x_aux = point[0]
                y_aux = point[1]

            viewport_y1 = VIEWPORT_HEIGHT - y_aux
            viewport_y2 = VIEWPORT_HEIGHT - first_y
            viewport.coords(self.id, x_aux, viewport_y1, first_x, viewport_y2)

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

        for i, point in enumerate(self.points):
            points_matrix = [point[0], point[1], 1]
            result_points = np.matmul(points_matrix, first_translation_matriz)
            result_points = np.matmul(result_points, rotation_matrix)
            result_points = np.matmul(result_points, second_translation_matriz)
            point[0] = result_points[0]
            point[1] = result_points[1]

        if self.id != None:
            new_points = normalized_window.wireframe_clipping(self, self.points)
            x_aux = None
            y_aux = None
            first_x = None
            first_y = None
            for i, point in enumerate(new_points):
                if not (i == 0):
                    viewport_y1 = VIEWPORT_HEIGHT - y_aux
                    viewport_y2 = VIEWPORT_HEIGHT - point[1]
                    viewport.coords(self.list_ids[i-1], x_aux, viewport_y1, point[0], viewport_y2)
                else:
                    first_x = point[0]
                    first_y = point[1]

                x_aux = point[0]
                y_aux = point[1]

            viewport_y1 = VIEWPORT_HEIGHT - y_aux
            viewport_y2 = VIEWPORT_HEIGHT - first_y
            viewport.coords(self.id, x_aux, viewport_y1, first_x, viewport_y2)

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

        for i, point in enumerate(self.points):
            points_matrix = [point[0], point[1], 1]
            result_points = np.matmul(points_matrix, first_translation_matriz)
            result_points = np.matmul(result_points, rotation_matrix)
            result_points = np.matmul(result_points, second_translation_matriz)
            point[0] = result_points[0]
            point[1] = result_points[1]

        if self.id != None:
            new_points = normalized_window.wireframe_clipping(self, self.points)
            x_aux = None
            y_aux = None
            first_x = None
            first_y = None
            for i, point in enumerate(new_points):
                if not (i == 0):
                    viewport_y1 = VIEWPORT_HEIGHT - y_aux
                    viewport_y2 = VIEWPORT_HEIGHT - point[1]
                    viewport.coords(self.list_ids[i-1], x_aux, viewport_y1, point[0], viewport_y2)
                else:
                    first_x = point[0]
                    first_y = point[1]

                x_aux = point[0]
                y_aux = point[1]

            viewport_y1 = VIEWPORT_HEIGHT - y_aux
            viewport_y2 = VIEWPORT_HEIGHT - first_y
            viewport.coords(self.id, x_aux, viewport_y1, first_x, viewport_y2)

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
