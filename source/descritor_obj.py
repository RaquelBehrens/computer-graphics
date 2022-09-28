class DescritorOBJ():
    def __init__(self, viewport, display_file):
        self.display_file = display_file
        self.viewport = viewport
        self.wavefront_file = open("wavefront.obj", "w")
        self.sample_file = open("sample.mtl", "w")
        list_of_objects, list_of_vertexes = self.objects_in_file_type()
        self.create_OBJ_file(list_of_objects, list_of_vertexes)

    def create_OBJ_file(self, list_of_objects, list_of_vertexes):
        for vertex in list_of_vertexes:
            self.wavefront_file.write(vertex)

        self.wavefront_file.write("mtllib sample.mtl\n")
        self.wavefront_file.write("o window\n")

        x0 = self.viewport.winfo_screenwidth()/2
        y0 = self.viewport.winfo_screenheight()/2
        self.wavefront_file.write(f"w {x0} {y0}\n")

        for object in list_of_objects:
            self.wavefront_file.write(object)

    def objects_in_file_type(self):
        list_of_vertexes = []
        writeList = []
        counter = 1

        list_of_points = {}
        for object in self.display_file:
            points = object.get_points()
            for point in points:
                if point not in list_of_points.values():
                    list_of_points[str(counter)] = point
                    list_of_vertexes.append(f"{counter} v {point[0]} {point[1]} 0.0\n")
                    counter += 1
        
        for object in self.display_file:
            name, color, points, color_name, color_code = object.obj_string(list_of_points)

            writeList.append(name)
            writeList.append(color)
            writeList.append(points)

            self.sample_file.write(color_name)
            self.sample_file.write(color_code)
            self.sample_file.write('\n')

        return writeList, list_of_vertexes