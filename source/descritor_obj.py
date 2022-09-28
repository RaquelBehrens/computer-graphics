class DescritorOBJ():
    def __init__(self, viewport, display_file):
        self.display_file = display_file
        self.viewport = viewport
        self.wavefront_file = open("wavefront.obj", "w")
        self.sample_file = open("sample.mtl", "w")
        listOfObjects, listOfVertexes = self.objectsInFileType()
        self.createOBJFile(listOfObjects, listOfVertexes)

    def createOBJFile(self, listOfObjects, listOfVertexes):
        for vertex in listOfVertexes:
            self.wavefront_file.write(vertex)

        self.wavefront_file.write("mtllib sample.mtl\n")
        self.wavefront_file.write("o window\n")

        x0 = self.viewport.winfo_screenwidth()/2
        y0 = self.viewport.winfo_screenheight()/2
        self.wavefront_file.write(f"w {x0} {y0}\n")

        for object in listOfObjects:
            self.wavefront_file.write(object)

    def objectsInFileType(self):
        listOfVertexes = []
        writeList = []
        counter = 1

        list_of_points = {}
        for object in self.display_file:
            points = object.get_points()
            for point in points:
                if point not in list_of_points.values():
                    list_of_points[str(counter)] = point
                    listOfVertexes.append(f"{counter} v {point[0]} {point[1]} 0.0\n")
                    counter += 1
        
        for object in self.display_file:
            name, color, points, color_name, color_code = object.obj_string(list_of_points)

            writeList.append(name)
            writeList.append(color)
            writeList.append(points)

            self.sample_file.write(color_name)
            self.sample_file.write(color_code)
            self.sample_file.write('\n')

        return writeList, listOfVertexes