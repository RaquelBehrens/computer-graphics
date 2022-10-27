from tkinter import messagebox
from objects import (Point, Line, Wireframe, Curve, Point3D, Object3D)
from utils import hex_to_rgb

class DescritorOBJ():
    def __init__(self, viewport, coord_scn, display_file):
        self.display_file = display_file
        self.coord_scn = coord_scn
        self.viewport = viewport
        self.list_of_colors = {}
        self.list_of_objects = []
        self.list_of_points = {}
        self.list_of_vertexes = []

    def create_OBJ_file(self):
        self.wavefront_file = open("wavefront.obj", "w")
        self.sample_file = open("sample.mtl", "w")

        self.objects_in_file_type()
        self.append_in_file()

        self.wavefront_file.close()
        self.sample_file.close()

    def append_in_file(self):
        for vertex in self.list_of_vertexes:
            self.wavefront_file.write(vertex)

        self.wavefront_file.write("mtllib sample.mtl\n")
        self.wavefront_file.write("o window\n")

        x0 = self.coord_scn.wc[0]
        y0 = self.coord_scn.wc[1]
        z0 = self.coord_scn.wc[2]
        self.wavefront_file.write(f"w {x0} {y0} {z0}\n")

        for object in self.list_of_objects:
            self.wavefront_file.write(object)

    def objects_in_file_type(self):
        counter = 1
        
        for object in self.display_file:
            if isinstance(object, Point3D) or isinstance(object, Object3D):
                points = object.get_points()
                for point in points:
                    if point not in self.list_of_points.values():
                        self.list_of_points[str(counter)] = point
                        self.list_of_vertexes.append(f"v {point[0]} {point[1]} {point[1]}\n")
                        counter += 1
                self.add_color_to_sample(object)
            else:
                points = object.get_points()
                for point in points:
                    if point not in self.list_of_points.values():
                        self.list_of_points[str(counter)] = point
                        self.list_of_vertexes.append(f"v {point[0]} {point[1]} 0.0\n")
                        counter += 1
                self.add_color_to_sample(object)
            
        for object in self.display_file:
            name, color, points = object.obj_string(self.list_of_points, self.list_of_colors)

            self.list_of_objects.append(name)
            self.list_of_objects.append(color)
            
            if isinstance(object, Object3D):
                for point in points:
                    self.list_of_objects.append(point)
            else:
                self.list_of_objects.append(points)

    def add_color_to_sample(self, object):
        color = object.get_color()
        if color not in self.list_of_colors:
            color_name = f"color{color}"
            color_name_line = f"newmtl {color_name}\n"

            self.list_of_colors[color] = color_name

            color_rgb = hex_to_rgb(color[1:])
            color_code = f"Kd {color_rgb[0]} {color_rgb[1]} {color_rgb[2]}\n"

            self.sample_file.write(color_name_line)
            self.sample_file.write(color_code)
            self.sample_file.write('\n')

    def read_OBJ_file(self):
        objetos = []
        v_dict = {}
        color_dict = {}
        objeto_atual = ''
        vertices_atuais = []
        cor_atual = ''

        try:
            with open('wavefront.obj') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    line_words_list = line.strip("\n").split(" ")

                    if line_words_list[0] == 'v':
                        v_dict[i+1] = [line_words_list[1], line_words_list[2], line_words_list[3]]

                    elif line_words_list[0] == 'mtllib':
                        color_dict = self.get_color_dict(line_words_list[1])

                    elif line_words_list[0] == 'o':
                        objeto_atual = line_words_list[1]

                    elif line_words_list[0] == 'w':
                        vertices_atuais = [float(line_words_list[1]), float(line_words_list[2])]

                    elif line_words_list[0] == 'usemtl':
                        cor_atual = color_dict.get(line_words_list[1])

                    elif line_words_list[0] == 'p':
                        vertices_atuais = [v_dict.get(int(line_words_list[1]))]
                        objetos.append(['ponto', objeto_atual, cor_atual, vertices_atuais])

                    elif line_words_list[0] == 'l':
                        vertices_atuais = []
                        for i in range(1, len(line_words_list), 1):
                            vertices_atuais.append(v_dict.get(int(line_words_list[i])))
                        objetos.append(['linha', objeto_atual, cor_atual, vertices_atuais])

                    elif line_words_list[0] == 'f':
                        vertices_atuais = [v_dict.get(int(line_words_list[1].split('/')[0])), v_dict.get(int(line_words_list[2].split('/')[0])), v_dict.get(int(line_words_list[3].split('/')[0]))]
                        objetos.append(['poligono', objeto_atual, cor_atual, vertices_atuais])

                    elif line_words_list[0] == 'g':
                        objeto_atual = line_words_list[1]
            
            return objetos
        except Exception as e:
            messagebox.showerror('Erro', e)

    def get_color_dict(self, file_name):
        sample_list = []
        with open(file_name) as f:
            lines = f.readlines()
            for line in lines:
                sample_words_list = line.strip("\n").split(" ")
                if sample_words_list:
                    if sample_words_list[0] == 'newmtl':
                        sample_list.append(sample_words_list[1])
                    elif sample_words_list[0] == 'Kd':
                        sample_list.append([sample_words_list[1],sample_words_list[2],sample_words_list[3]])

        color_dict = {}
        for i in range(0, len(sample_list), 2):
            color_dict[sample_list[i]] = sample_list[i+1]
        
        return color_dict
        