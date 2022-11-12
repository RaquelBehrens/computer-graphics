import numpy as np
from constants import VIEWPORT_HEIGHT
from .object import Object
from utils import angle_between


class FdSurface3D(Object):
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
        self.fill_form = None

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
        self.bspline_algorythm(self.points)

    def bspline_algorythm(self, points):
        n_s = 15
        n_t = 15

        delta_s = 1.0 / (n_s - 1)
        delta_t = 1.0 / (n_t - 1)

        E_s = self.delta_matrix(delta_s)
        E_t = self.delta_matrix(delta_t)

        b_splines_matrix = np.array([[-1/6, 1/2, -1/2, 1/6], [1/2, -1, 1/2, 0], [-1/2, 0, 1/2, 0], [1/6, 2/3, 1/6, 0]])

        points_set = self.bezier_points_set(points)
        first_set = []
        second_set = []

        for set in points_set:    
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

            #primeira iteração
            DDx = E_s @ b_splines_matrix @ px @ np.transpose(b_splines_matrix) @ np.transpose(E_t)
            DDy = E_s @ b_splines_matrix @ py @ np.transpose(b_splines_matrix) @ np.transpose(E_t)
            DDz = E_s @ b_splines_matrix @ pz @ np.transpose(b_splines_matrix) @ np.transpose(E_t)
            
            for i in range(n_s):
                x, dx, d2x, d3x = DDx[0]
                y, dy, d2y, d3y = DDy[0]
                z, dz, d2z, d3z = DDz[0]
                
                #retorna uma lista de pontos que devem ficar interligadas entre si
                #coloca essa lista no first_set
                first_set.append(self.fwd_diff(n_t, x, dx, d2x, d3x, y, dy, d2y, d3y, z, dz, d2z, d3z))

                DDx[0] = DDx[1]
                DDx[1] = DDx[2]
                DDx[2] = DDx[3]

                DDy[0] = DDy[1]
                DDy[1] = DDy[2]
                DDy[2] = DDy[3]

                DDz[0] = DDz[1]
                DDz[1] = DDz[2]
                DDz[2] = DDz[3]

            #segunda iteração
            DDx = E_s @ b_splines_matrix @ px @ np.transpose(b_splines_matrix) @ np.transpose(E_t)
            DDy = E_s @ b_splines_matrix @ py @ np.transpose(b_splines_matrix) @ np.transpose(E_t)
            DDz = E_s @ b_splines_matrix @ pz @ np.transpose(b_splines_matrix) @ np.transpose(E_t)

            DDx = np.transpose(DDx)
            DDy = np.transpose(DDy)
            DDz = np.transpose(DDz)
            
            for i in range(n_t):
                x, dx, d2x, d3x = DDx[0]
                y, dy, d2y, d3y = DDy[0]
                z, dz, d2z, d3z = DDz[0]

                #retorna uma lista de pontos que devem ficar interligadas entre si
                #coloca essa lista no first_set
                second_set.append(self.fwd_diff(n_s, x, dx, d2x, d3x, y, dy, d2y, d3y, z, dz, d2z, d3z))

                DDx[0] = DDx[1]
                DDx[1] = DDx[2]
                DDx[2] = DDx[3]

                DDy[0] = DDy[1]
                DDy[1] = DDy[2]
                DDy[2] = DDy[3]

                DDz[0] = DDz[1]
                DDz[1] = DDz[2]
                DDz[2] = DDz[3]

            for set in first_set:
                for i in range(len(set) - 1):
                    self.vectors.append([set[i], set[i+1]])

            for set in second_set:
                for i in range(len(set) - 1):
                    self.vectors.append([set[i], set[i+1]])

    def bezier_points_set(self, points):
        for i in range(0, len(points) - 1, 3):
            yield points[i : (i + 4)]

    def delta_matrix(self, d):
        d2 = d * d
        d3 = d * d * d
        matrix = np.array([[0, 0, 0, 1], [d3, d2, d, 0], [6 * d3, 2 * d2, 0, 0], [6 * d3, 0, 0, 0]])
        return matrix

    def fwd_diff(self, n, x, dx, d2x, d3x, y, dy, d2y, d3y, z, dz, d2z, d3z):
        i = 1
        return_points = [[x, y, z]]
        
        while(i < n):
            i += 1
        
            x += dx
            dx += d2x
            d2x += d3x
            
            y += dy
            dy += d2y
            d2y += d3y

            z += dz
            dz += d2z
            d2z += d3z

            return_points.append([x, y, z])

        return return_points

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
