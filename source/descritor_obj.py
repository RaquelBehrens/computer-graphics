from utils import hex_to_rgb

class DescritorOBJ():
    def __init__(self, viewport, display_file):
        self.display_file = display_file
        self.viewport = viewport
        self.wavefront_file = open("wavefront.obj", "w")
        self.sample_file = open("sample.mtl", "w")

        self.list_of_colors = {}
        self.list_of_objects = []
        self.list_of_points = {}
        self.list_of_vertexes = []

        self.objects_in_file_type()
        self.create_OBJ_file()

    def create_OBJ_file(self):
        for vertex in self.list_of_vertexes:
            self.wavefront_file.write(vertex)

        self.wavefront_file.write("mtllib sample.mtl\n")
        self.wavefront_file.write("o window\n")

        x0 = self.viewport.winfo_screenwidth()/2
        y0 = self.viewport.winfo_screenheight()/2
        self.wavefront_file.write(f"w {x0} {y0}\n")

        for object in self.list_of_objects:
            self.wavefront_file.write(object)

    def objects_in_file_type(self):
        counter = 1
        
        for object in self.display_file:
            points = object.get_points()
            for point in points:
                if point not in self.list_of_points.values():
                    self.list_of_points[str(counter)] = point
                    self.list_of_vertexes.append(f"{counter} v {point[0]} {point[1]} 0.0\n")
                    counter += 1
            self.add_color_to_sample(object)
         
        for object in self.display_file:
            name, color, points = object.obj_string(self.list_of_points, self.list_of_colors)

            self.list_of_objects.append(name)
            self.list_of_objects.append(color)
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
