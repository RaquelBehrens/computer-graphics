class DescritorOBJ():
    def __init__(self, viewport, display_file):
        self.display_file = display_file
        self.viewport = viewport
        self.file = open("wavefront.obj", "w")
        listOfObjects, listOfVertexes = self.objectsInFileType()
        self.createOBJFile(listOfObjects, listOfVertexes)

    def createOBJFile(self, listOfObjects, listOfVertexes):
        for vertex in listOfVertexes:
            self.file.write(vertex)

        self.file.write("mtllib sample.mtl")
        self.file.write("o window")

        x0 = self.viewport.winfo_screenwidth()/2
        y0 = self.viewport.winfo_screenheight()/2
        self.file.write(f"w {x0} {y0}")

    def objectsInFileType(self):
        listOfVertexes = []
        writeList = []
        counter = 0
        
        for object in self.display_file:
            vertexes, name, color, points = object.objString(counter)
            listOfVertexes.append(vertexes)
            writeList.append(name)
            writeList.append(color)
            writeList.append(points)

        return writeList, listOfVertexes