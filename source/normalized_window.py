import numpy as np
from tkinter import *

from constants import POINT_SIZE, VIEWPORT_HEIGHT, VIEWPORT_WIDTH
from objects import (Line, Wireframe, Curve, Point3D, Object3D)
from utils import adjacents

class NormalizedWindow:
    def __init__(self, viewport, main_table):
        self.viewport = viewport
        self.main_table = main_table
        self.wc = [0, 0, 0]
        self.angle = 0
        self.s = [1, 1, 1]
        self.x_min = 10
        self.x_max = VIEWPORT_WIDTH-10
        self.y_min = 10
        self.y_max = VIEWPORT_HEIGHT-10
        self.vrp = [0, 0, 0, 1]
        self.vpn = None
        self.clipping_mode = None

    def generate_scn(self, object):
        new_points = [None] * len(object.points)
        for i in range(len(new_points)):
            new_points[i] = [None] * 2

        if not isinstance(object, Object3D) and not isinstance(object, Point3D):
            for index, point in enumerate(object.points):
                points_matrix = [point[0], point[1], 1]
                result_points = np.matmul(points_matrix, self.transformation_matrix())
                new_points[index][0] = result_points[0]
                new_points[index][1] = result_points[1]

            object.drawn(self.viewport, self, new_points)
            self.update_table(object)
        else:
            
            #Nessa função precisa colocar a parte de Projeção Paralela Ortogonal

            for i, point in enumerate(object.points):
                points_matrix = [point[0], point[1], 1]
                result_points = np.matmul(points_matrix, self.transformation_matrix())
                new_points[i][0] = result_points[0]
                new_points[i][1] = result_points[1]

            object.drawn(self.viewport, self, new_points)
            self.update_table(object)

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

    def update_table(self, object):
        all_items = self.main_table.get_children()

        for item in all_items:
            if self.main_table.item(item).get('values')[0] == object.name:
                self.main_table.item(item,
                                    values=(object.get_name(), object.get_points(), 
                                    object.get_id()))

    def point_clipping(self, object, new_points):
        for point in new_points:
            if self.x_min <= point[0] <= self.x_max and self.y_min <= point[1] <= self.y_max:
                object.clipped = False
            else:
                object.clipped = True

    def line_clipping_CS(self, object, points):
        RC = [None] * len(points)
        for i in range(len(RC)):
            RC[i] = [None] * 4

        P3 = False
        return_values = [[points[0][0], points[0][1]], [points[1][0], points[1][1]]]
        old_clipping = object.clipped
        
        for i, point in enumerate(points):
            if point[0] < self.x_min:
                RC[i][3] = 1
            else:
                RC[i][3] = 0
            
            if point[0] > self.x_max:
                RC[i][2] = 1
            else:
                RC[i][2] = 0

            if point[1] < self.y_min:
                RC[i][1] = 1
            else:
                RC[i][1] = 0

            if point[1] > self.y_max:
                RC[i][0] = 1
            else:
                RC[i][0] = 0

        if RC[0] == [0,0,0,0] and RC[1] == [0,0,0,0]:
            object.clipped = False
        elif [RC0 and RC1 for RC0, RC1 in zip(RC[0], RC[1])] != [0,0,0,0]:
            object.clipped = True
        elif [RC0 and RC1 for RC0, RC1 in zip(RC[0], RC[1])] == [0,0,0,0]:
            object.clipped = False
            P3 = True

        if P3:
            m = (points[1][1] - points[0][1]) / ((points[1][0] - points[0][0]))

            for i, position in enumerate(RC):
                x = None
                y = None
                if position[0] == 1:
                    x = points[i][0] + (1 / m) * (self.y_max - points[i][1])
                    return_values[i][1] = self.y_max
                if position[1] == 1:
                    x = points[i][0] + (1 / m )* (self.y_min - points[i][1])
                    return_values[i][1] = self.y_min
                if position[2] == 1:
                    y = m * (self.x_max - points[0][0]) + points[0][1]
                    return_values[i][0] = self.x_max
                if position[3] == 1:
                    y = m * (self.x_min - points[0][0]) + points[0][1]
                    return_values[i][0] = self.x_min

                if x != None:
                    if not (self.x_min < x < self.x_max):
                        if y == None:
                            object.clipped = True
                            return_values[i][1] = points[i][1]
                            break
                    else:
                        return_values[i][0] = x
                
                if y != None:
                    if not (self.y_min < y < self.y_max):
                        if x == None:
                            object.clipped = True
                            return_values[i][0] = points[i][0]
                            break
                    else:
                        return_values[i][1] = y

        if not object.clipped:
            self.viewport.itemconfigure(object.id, state='normal')
            return return_values
        else:
            if old_clipping == False:
                # Quando o objeto já está desenhado, caso esteja fora da window, "esconde" ele
                self.viewport.itemconfigure(object.id, state='hidden')

    def line_clipping_LB(self, object, points):
        p = [None] * 4
        q = [None] * 4
        zeta = [None] * 2
        
        r = [[], []]
        return_values = [[points[0][0], points[0][1]], [points[1][0], points[1][1]]]
        old_clipping = object.clipped
        object.clipped = False
        in_limit = True
        
        p[0] = -(points[1][0] - points[0][0])
        p[1] = points[1][0] - points[0][0]
        p[2] = -(points[1][1] - points[0][1])
        p[3] = points[1][1] - points[0][1]

        q[0] = points[0][0] - self.x_min
        q[1] = self.x_max - points[0][0]
        q[2] = points[0][1] - self.y_min
        q[3] = self.y_max - points[0][1]

        for i, element in enumerate(p):
            if element == 0:
                if q[i] < 0:
                    object.clipped = True
                    in_limit = False
                else:
                    return return_values
            elif element < 0:
                r[0].append(q[i] / element)
            else:
                r[1].append(q[i] / element)

        if in_limit:
            zeta[0] = 0
            zeta[1] = 1

            for value in r[0]:
                if value > zeta[0]:
                    zeta[0] = value
            for value in r[1]:
                if value < zeta[1]:
                    zeta[1] = value

            if zeta[0] > zeta[1]:
                object.clipped = True
            else:
                if zeta[0] != 0:
                    return_values[0][0] = points[0][0] + (zeta[0] * p[1])
                    return_values[0][1] = points[0][1] + (zeta[0] * p[3])

                if zeta[1] != 1:
                    return_values[1][0] = points[0][0] + (zeta[1] * p[1])
                    return_values[1][1] = points[0][1] + (zeta[1] * p[3])

        if not object.clipped:
            self.viewport.itemconfigure(object.id, state='normal')
            return return_values
        else:
            if old_clipping == False:
                # Quando o objeto já está desenhado, caso esteja fora da window, "esconde" ele
                self.viewport.itemconfigure(object.id, state='hidden')

    def wireframe_clipping(self, points, circular=True):
        clipped_points = points
        clipped_points = self.clip_right_x(clipped_points, circular)
        clipped_points = self.clip_left_x(clipped_points, circular)
        clipped_points = self.clip_upper_y(clipped_points, circular)
        clipped_points = self.clip_bottom_y(clipped_points, circular)
        return clipped_points
    
    def clip_left_x(self, points, circular):
        new_points = []
        delta = [0, 0]

        if adjacents(points, circular) != None:
            for p0, p1 in adjacents(points, circular):
                if not circular:
                    new_points.append(p0)
                if p0[0] < self.x_min < p1[0]:
                    delta[0] = p1[0] - p0[0]
                    delta[1] = p1[1] - p0[1]
                    if delta[0] == 0:
                        continue
                    r =  delta[1] / delta[0]
                    x = self.x_min 
                    y = r * (x - p0[0]) + p0[1]
                    new_points.append([x, y])

                elif p1[0] < self.x_min < p0[0]:
                    delta[0] = p0[0] - p1[0]
                    delta[1] = p0[1] - p1[1]
                    if delta[0] == 0:
                        continue
                    r =  delta[1] / delta[0]
                    x = self.x_min 
                    y = r * (x - p1[0]) + p1[1]
                    new_points.append([x, y])

                new_points.append(p1)

        clipped = []

        for point in new_points:
            if point[0] >= self.x_min:
                clipped.append(point)

        return clipped

    def clip_right_x(self, points, circular):
        new_points = []
        delta = [0, 0]

        if adjacents(points, circular) != None:
            for p0, p1 in adjacents(points, circular):
                if not circular:
                    new_points.append(p0)
                if p0[0] > self.x_max > p1[0]:
                    delta[0] = p1[0] - p0[0]
                    delta[1] = p1[1] - p0[1]
                    if delta[0] == 0:
                        continue
                    r =  delta[1] / delta[0]
                    x = self.x_max 
                    y = r * (x - p0[0]) + p0[1]
                    new_points.append([x,y])

                elif p1[0] > self.x_max > p0[0]:
                    delta[0] = p0[0] - p1[0]
                    delta[1] = p0[1] - p1[1]
                    if delta[0] == 0:
                        continue
                    r =  delta[1] / delta[0]
                    x = self.x_max 
                    y = r * (x - p1[0]) + p1[1]
                    new_points.append([x,y])

                new_points.append(p1)

        clipped = []

        for point in new_points:
            if point[0] <= self.x_max:
                clipped.append(point)

        return clipped

    def clip_bottom_y(self, points, circular):
        new_points = []
        delta = [0, 0]

        if adjacents(points, circular) != None:
            for p0, p1 in adjacents(points, circular):
                if not circular:
                    new_points.append(p0)
                if p0[1] < self.y_min < p1[1]:
                    delta[0] = p1[0] - p0[0]
                    delta[1] = p1[1] - p0[1]
                    if delta[0] == 0:
                        y = self.y_min
                        x = p0[0] 
                    else:
                        r =  delta[1] / delta[0]
                        y = self.y_min
                        x = p0[0] + (y - p0[1]) / r
                    new_points.append([x,y])

                elif p1[1] < self.y_min < p0[1]:
                    delta[0] = p0[0] - p1[0]
                    delta[1] = p0[1] - p1[1]
                    if delta[0] == 0:
                        y = self.y_min
                        x = p1[0]
                    else: 
                        r =  delta[1] / delta[0]
                        y = self.y_min
                        x = p1[0] + (y - p1[1]) / r
                    new_points.append([x,y])

                new_points.append(p1)
            
        clipped = []

        for point in new_points:
            if point[1] >= self.y_min:
                clipped.append(point)

        return clipped

    def clip_upper_y(self, points, circular):
        new_points = []
        delta = [0, 0]

        if adjacents(points, circular) != None:
            for p0, p1 in adjacents(points, circular):
                if not circular:
                    new_points.append(p0)
                if p0[1] > self.y_max > p1[1]:
                    delta[0] = p1[0] - p0[0]
                    delta[1] = p1[1] - p0[1]
                    if delta[0] == 0:
                        y = self.y_max
                        x = p0[0]
                    else:
                        r =  delta[1]/ delta[0]
                        y = self.y_max
                        x = p0[0] + (y - p0[1]) / r
                    new_points.append([x,y])

                elif p1[1]> self.y_max > p0[1]:
                    delta[0] = p0[0] - p1[0]
                    delta[1] = p0[1] - p1[1]
                    if delta[0]== 0:
                        y = self.y_max
                        x = p1[0]
                    else: 
                        r =  delta[1]/ delta[0]
                        y = self.y_max
                        x = p1[0] + (y - p1[1]) / r
                    new_points.append([x,y])

                new_points.append(p1)

        clipped = []

        for point in new_points:
            if point[1]<= self.y_max:
                clipped.append(point)

        return clipped
    
    def define_vpn(self, translate_matrix):
        w1 = np.array([0, VIEWPORT_HEIGHT, 0, 1])
        w1 = np.matmul(w1, translate_matrix)
        w2 = np.array([VIEWPORT_WIDTH, VIEWPORT_HEIGHT, 0, 1])
        w2 = np.matmul(w2, translate_matrix)
        
        vrp = np.matmul(self.vrp, translate_matrix)

        vector_a = vrp - w1
        vector_b = w2 - vrp

        result_x = vector_a[1]*vector_b[2] - vector_a[2]*vector_b[1]
        result_y = vector_a[2]*vector_b[0] - vector_a[0]*vector_b[2]
        result_z = vector_a[0]*vector_b[1] - vector_a[1]*vector_b[0]

        return [result_x, result_y, result_z]
