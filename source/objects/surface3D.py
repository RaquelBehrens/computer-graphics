import numpy as np
from constants import VIEWPORT_HEIGHT, BEZIER_EPSILON
from .object import Object
from utils import angle_between


class Surface3D(Object):
    def __init__(self, name, list_points, color, id=None, projection=None):
        self.name = name
        self.points = list_points
        self.vectors = None
        self.id = id
        self.list_ids = []
        self.color = color
        self.closed = None
        self.projection = projection
        self.vectors = []

        self.epsilon = BEZIER_EPSILON
        self.bezier_points = []
        self.define_vectors()

    def drawn(self, viewport, normalized_window, new_vectors=[]):
        if not new_vectors:
            normalized_points = normalized_window.wireframe_clipping(self.vectors, vector=True)
            if normalized_points != []:
                new_vectors = normalized_points
        else:
            normalized_points = normalized_window.wireframe_clipping(new_vectors, vector=True)
            new_vectors = normalized_points
            for i in range(len(self.list_ids)):
                viewport.delete(self.list_ids[i])
            self.list_ids = []

        if new_vectors == []:
            self.clipped = True
        else:
            self.clipped = False
        
        if not self.clipped:
            for new_points in new_vectors:
                x1 = new_points[0][0]
                viewport_y1 = VIEWPORT_HEIGHT - new_points[0][1]

                x2 = new_points[1][0]
                viewport_y2 = VIEWPORT_HEIGHT - new_points[1][1]

                id = viewport.create_line((x1, viewport_y1), (x2, viewport_y2), width=3, fill=self.color)
                self.list_ids.append(id)

            self.id = self.list_ids[-1]

    def define_vectors(self):
        self.bezier_points = self.bezier_algorythm(self.points)
        for i in range(len(self.bezier_points)):
            for j in range(len(self.bezier_points[i])):
                if j != len(self.bezier_points[i])-1:
                    self.vectors.append([self.bezier_points[i][j], self.bezier_points[i][j+1]])
                else:
                    self.vectors.append([self.bezier_points[i][j], self.bezier_points[i][0]])

    def bezier_algorythm(self, points):
        bezier_matrix = np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]])
        new_points = []
        new_lines = []

        points_set = self.bezier_points_set(points)

<<<<<<< HEAD
=======
        for set in points_set:
>>>>>>> mudando_bezier_3d
            for k in range(self.epsilon+1):
                t = k / self.epsilon
                s = 1
                t_list = np.array([t * t * t, t * t, t, 1])
                s_list = np.array([s * s * s, s * s, s, 1])     
                px = [[None, None, None, None],
                        [None, None, None, None],
                        [None, None, None, None],
                        [None, None, None, None]]
                py = [[None, None, None, None],
                        [None, None, None, None],
                        [None, None, None, None],
                        [None, None, None, None]]
                pz = [[None, None, None, None],
                        [None, None, None, None],
                        [None, None, None, None],
                        [None, None, None, None]]

                for i in range(len(set)):
                    for j in range(len(set[i])):
                        px[i][j] = set[i][j][0]
                        py[i][j] = set[i][j][1]
                        pz[i][j] = set[i][j][2]

                x = s_list @ bezier_matrix @ px @ bezier_matrix @ np.transpose(t_list)
                y = s_list @ bezier_matrix @ py @ bezier_matrix @ np.transpose(t_list)
                z = s_list @ bezier_matrix @ pz @ bezier_matrix @ np.transpose(t_list)
                new_points.append([x,y,z])
    
            new_lines.append(new_points)
            new_points = []

<<<<<<< HEAD
        return new_points
=======
        return new_lines
>>>>>>> mudando_bezier_3d

    def bezier_points_set(self, points):
        for i in range(0, len(points) - 1, 3):
            yield points[i : (i + 4)]

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

        for i in range(len(self.vectors)):
            for j in range(len(self.vectors[i])):
                points_matrix = [self.vectors[i][j][0], self.vectors[i][j][1], self.vectors[i][j][2], 1]
                result_points = np.matmul(points_matrix, rotation_matrix)
                result_points = np.matmul(result_points, translation_matrix)
                result_points = np.matmul(result_points, rotation_matrix_inverse)
                
                self.vectors[i][j] = [result_points[0], result_points[1], result_points[2]]            

        normalized_window.generate_scn(self)
    
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

        for i in range(len(self.vectors)):
            for j in range(len(self.vectors[i])):
                points_matrix = [self.vectors[i][j][0], self.vectors[i][j][1], self.vectors[i][j][2], 1]
                result_points = np.matmul(points_matrix, first_translation_matrix)
                result_points = np.matmul(result_points, scale_matrix)
                result_points = np.matmul(result_points, second_translation_matrix)
                
                self.vectors[i][j] = [result_points[0], result_points[1], result_points[2]]     

        normalized_window.generate_scn(self)

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

        for i in range(len(self.vectors)):
            for j in range(len(self.vectors[i])):
                points_matrix = [self.vectors[i][j][0], self.vectors[i][j][1], self.vectors[i][j][2], 1]
                result_points = np.matmul(points_matrix, rotation_matrix)
                
                self.vectors[i][j] = [result_points[0], result_points[1], result_points[2]] 

        normalized_window.generate_scn(self)

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

        for i in range(len(self.vectors)):
            for j in range(len(self.vectors[i])):
                points_matrix = [self.vectors[i][j][0], self.vectors[i][j][1], self.vectors[i][j][2], 1]
                result_points = np.matmul(points_matrix, first_translation_matriz)
                result_points = np.matmul(result_points, rotation_matrix)
                result_points = np.matmul(result_points, second_translation_matriz)
                
                self.vectors[i][j] = [result_points[0], result_points[1], result_points[2]] 

        normalized_window.generate_scn(self)

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

        for i in range(len(self.vectors)):
            for j in range(len(self.vectors[i])):
                points_matrix = [self.vectors[i][j][0], self.vectors[i][j][1], self.vectors[i][j][2], 1]
                result_points = np.matmul(points_matrix, first_translation_matriz)
                result_points = np.matmul(result_points, rotation_matrix)
                result_points = np.matmul(result_points, second_translation_matriz)
                
                self.vectors[i][j] = [result_points[0], result_points[1], result_points[2]] 

        normalized_window.generate_scn(self)

    def rotate_around_axis(self, viewport, rotate_points, normalized_window):
        rotate_points = rotate_points.split()
        rotate_radian = -(np.radians(float(rotate_points[13])))
        
        axis = [[float(rotate_points[1]),float(rotate_points[3]),float(rotate_points[5])],
                [float(rotate_points[7]),float(rotate_points[9]),float(rotate_points[11])]]
        axis_center = self.find_axis_center(axis)

        translation_matrix = [[1, 0, 0, 0],
                              [0, 1, 0, 0],
                              [0, 0, 1, 0],
                              [-axis_center[0], -axis_center[1], -axis_center[0], 1]]

        rotate_radian_x = angle_between(axis, [[0,0,0],[1, 0, 0]])
        rotation_matrix_x = [[1, 0, 0, 0],
                             [0, (np.cos(rotate_radian_x)), (np.sin(rotate_radian_x)), 0],
                             [0, -(np.sin(rotate_radian_x)), (np.cos(rotate_radian_x)), 0],
                             [0, 0, 0, 1]]

        rotate_radian_z = (np.radians(float(angle_between(axis, [[0,0,0],[0, 0, 1]]))))
        rotation_matrix_z = [[(np.cos(rotate_radian_z)), (np.sin(rotate_radian_z)), 0, 0],
                             [-(np.sin(rotate_radian_z)), (np.cos(rotate_radian_z)), 0, 0],
                             [0, 0, 1, 0],
                             [0, 0, 0, 1]]

        rotate_radian_y = rotate_radian
        rotation_matrix_y = [[(np.cos(rotate_radian_y)), 0, -(np.sin(rotate_radian_y)), 0],
                             [0, 1, 0, 0],
                             [(np.sin(rotate_radian_y)), 0, (np.cos(rotate_radian_y)), 0],
                             [0, 0, 0, 1]]

        undo_rotate_radian_z = -rotate_radian_z
        undo_rotation_matrix_z = [[(np.cos(undo_rotate_radian_z)), (np.sin(undo_rotate_radian_z)), 0, 0],
                                  [-(np.sin(undo_rotate_radian_z)), (np.cos(undo_rotate_radian_z)), 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1]]

        undo_rotate_radian_x = -rotate_radian_x
        undo_rotation_matrix_x = [[1, 0, 0, 0],
                             [0, (np.cos(undo_rotate_radian_x)), (np.sin(undo_rotate_radian_x)), 0],
                             [0, -(np.sin(undo_rotate_radian_x)), (np.cos(undo_rotate_radian_x)), 0],
                             [0, 0, 0, 1]]

        undo_translation_matrix = [[1, 0, 0, 0],
                                   [0, 1, 0, 0],
                                   [0, 0, 1, 0],
                                   [axis_center[0], axis_center[1], axis_center[0], 1]]

        for point in self.points:
            points_matrix = [point[0], point[1], point[2], 1]

            result_points = np.matmul(points_matrix, translation_matrix)
            result_points = np.matmul(result_points, rotation_matrix_x)
            result_points = np.matmul(result_points, rotation_matrix_z)
            result_points = np.matmul(result_points, rotation_matrix_y)
            result_points = np.matmul(result_points, undo_rotation_matrix_z)
            result_points = np.matmul(result_points, undo_rotation_matrix_x)
            result_points = np.matmul(result_points, undo_translation_matrix)

            for i in range(len(self.vectors)):
                for j in range(len(self.vectors[i])):
                    if (self.vectors[i][j] == point):
                        self.vectors[i][j] = [result_points[0], result_points[1], result_points[2]]

            point[0] = result_points[0]
            point[1] = result_points[1]
            point[2] = result_points[2]

        normalized_window.generate_scn(self)

    def find_axis_center(self, axis):
        axis_center_x = (axis[0][0] + axis[1][0]) / 2
        axis_center_y = (axis[0][1] + axis[1][1]) / 2
        axis_center_z = (axis[0][2] + axis[1][2]) / 2
        return [axis_center_x, axis_center_y, axis_center_z]

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
        name = f"o {self.name}\n"
        color = f"usemtl {list_of_colors.get(self.color)}\n"

        lines = []
        for vector in self.vectors:
            points = []
            for point in vector:
                point_index = list(list_of_points.keys())[list(list_of_points.values()).index(point)]
                points.append(point_index)
            
            points = " ".join(map(str,points))
            points = f"l {points}\n"
            lines.append(points)

        return name, color, lines
