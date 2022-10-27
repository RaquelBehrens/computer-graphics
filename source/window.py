import numpy as np
from tkinter import *
from tkinter import ttk, messagebox

from objects import (Point, Line, Wireframe, Curve, Point3D, Object3D)
from include_windows import (IncludePoint, 
                             IncludeLine, 
                             IncludeTriangle, 
                             IncludeQuadrilateral, 
                             IncludePolygon, 
                             IncludeCurve,
                             IncludePoint3D,
                             IncludeObject3D)
from transformation import Transformation
from normalized_window import NormalizedWindow
from descritor_obj import DescritorOBJ

from constants import WINDOW_HEIGHT, WINDOW_WIDTH, APPLICATION_NAME, VIEWPORT_WIDTH, VIEWPORT_HEIGHT
from utils import rgb_to_hex


class Window(Frame):
    def __init__(self):
        self.root = Tk()
        self.root.title(APPLICATION_NAME)
        #self.root.iconbitmap()
        self.root.geometry(f"{WINDOW_HEIGHT}x{WINDOW_WIDTH}")
        Frame.__init__(self, self.root) # , bg="red")

        self.pack(fill='both', expand=True)

        self.display_file = []
        self.lines_list = []

        self.create_widgets()
        self.create_table()
        self.clipping_select()
        
        self.coord_scn = NormalizedWindow(self.viewport, self.table)
        self.coord_scn.clipping_mode = self.radio_variable
        self.coord_scn.define_viewport()

    def create_widgets(self):
        #labels
        self.frame1 = Frame(self)
        self.frame1.grid(row=0, column=0, sticky=NW)
        self.frame2 = Frame(self)
        self.frame2.grid(row=0, column=1, sticky=NW)

        Label(self.frame1, text='Menu de funções', font=('Time', '13')).grid(row=0, column=0, sticky=NW)

        Label(self.frame2, text='Viewport', font=('Time', '11')).grid(row=0, column=0, sticky=N)
        self.viewport = Canvas(self.frame2, width=VIEWPORT_WIDTH, height=VIEWPORT_HEIGHT, bg='grey')
        self.viewport.grid(row=1, column=0, pady=15)
        self.erros = Label(self.frame2, width=60, height=2, bg='grey', font=('Time', '13'))
        self.erros.grid(row=2, column=0, sticky=N, padx=5)  

        Label(self.frame1, text='Window:', font=('Time', '13')).grid(row=3, column=0, sticky=NW, pady=10)
        self.up = Button(self.frame1, text='Cima', font=('Time', '11'), command=self.move_up)
        self.up.grid(row=4, column=0, sticky=NW, padx=70)
        self.left = Button(self.frame1, text='Esquerda', font=('Time', '11'), command=self.move_left)
        self.left.grid(row=5, column=0, sticky=NW, padx=5, pady=3)
        self.right = Button(self.frame1, text='Direita', font=('Time', '11'), command=self.move_right)
        self.right.grid(row=5, column=0, columnspan=5, padx=100, pady=3)
        self.down = Button(self.frame1, text='Baixo', font=('Time', '11'), command=self.move_down)
        self.down.grid(row=6, column=0, sticky=NW, padx=70)

        Label(self.frame1, text='Zoom: ', font=('Time', '13')).grid(row=7, column=0, sticky=NW, pady=10)
        self.more_zoom = Button(self.frame1, text='  +  ', font=('Time', '11'), command=self.zoom_in)
        self.more_zoom.grid(row=8, column=0, sticky=NW, padx=30, pady=0)
        self.less_zoom = Button(self.frame1, text='  -  ', font=('Time', '11'), command=self.zoom_out)
        self.less_zoom.grid(row=8, column=0, columnspan=2, pady=0)
        
        Label(self.frame1, text='Rotação eixo z: ', font=('Time', '13')).grid(row=9, column=0, sticky=NW, pady=10)
        self.right_rotation = Button(self.frame1, text='  ↻  ', font=('Time', '11'), command=self.rotate_left)
        self.right_rotation.grid(row=10, column=0, sticky=NW, padx=30, pady=0)
        self.left_rotation = Button(self.frame1, text='  ↺  ', font=('Time', '11'), command=self.rotate_right)
        self.left_rotation.grid(row=10, column=0, columnspan=2, pady=0)
        
        Label(self.frame2, text='Rotação eixo x: ', font=('Time', '13')).grid(row=1, column=1, sticky=NE)
        self.right_rotation_x = Button(self.frame2, text='  ↻  ', font=('Time', '11'), command=self.rotate_x_left)
        self.right_rotation_x.grid(row=1, column=1, stick=N, padx=40, pady=40)
        self.left_rotation_x = Button(self.frame2, text='  ↺  ', font=('Time', '11'), command=self.rotate_x_right)
        self.left_rotation_x.grid(row=1, column=1, stick=NE, pady=40)

        Label(self.frame2, text='Rotação eixo y: ', font=('Time', '13')).grid(row=1, column=1, sticky=NE, pady=80)
        self.right_rotation = Button(self.frame2, text='  ↻  ', font=('Time', '11'), command=self.rotate_y_left)
        self.right_rotation.grid(row=1, column=1, stick=N, padx=40, pady=120)
        self.left_rotation = Button(self.frame2, text='  ↺  ', font=('Time', '11'), command=self.rotate_y_right)
        self.left_rotation.grid(row=1, column=1, stick=NE, pady=120)

        Label(self.frame1, text='Objetos: ', font=('Time', '13')).grid(row=11, column=0, sticky=NW, pady=10)
        self.point = Button(self.frame1, text='Criar Ponto', font=('Time', '11'), command=self.include_point)
        self.point.grid(row=12, column=0, sticky=NW, padx=10)
        self.line = Button(self.frame1, text='Criar Linha', font=('Time', '11'), command=self.include_line)
        self.line.grid(row=12, column=0, sticky=NW, padx=(102,0))
        self.triangle = Button(self.frame1, text='Criar Triângulo', font=('Time', '11'), command=self.include_triangle)
        self.triangle.grid(row=13, column=0, sticky=NW, padx=10, pady=3)
        self.quadrilateral = Button(self.frame1, text='Criar Quadrilátero', font=('Time', '11'), command=self.include_quadrilateral)
        self.quadrilateral.grid(row=13, column=0, sticky=NW, padx=(125,0), pady=3)
        self.polygon = Button(self.frame1, text='Criar Outro Polígono', font=('Time', '11'), command=self.include_polygon)
        self.polygon.grid(row=14, column=0, sticky=NW, padx=10, pady=3)
        self.curve = Button(self.frame1, text='Criar Curva', font=('Time', '11'), command=self.include_curve)
        self.curve.grid(row=14, column=0, sticky=NW, padx=(162,0), pady=3)
        self.point3D = Button(self.frame1, text='Criar Ponto 3D', font=('Time', '11'), command=self.include_point3D)
        self.point3D.grid(row=15, column=0, sticky=NW, padx=10, pady=3)
        self.object3D = Button(self.frame1, text='Criar Objeto 3D', font=('Time', '11'), command=self.include_object3D)
        self.object3D.grid(row=15, column=0, sticky=NW, padx=(127,0), pady=3)
        
        Label(self, text='Operações: ',  font=('Time', '13')).grid(row=1, column=0, pady=(10,0), sticky=NW)
        self.delete = Button(self, text='Deletar Objeto', font=('Time', '11'), command=self.delete_object)
        self.delete.grid(row=3, column=0, sticky=NW, padx=0, pady=5)
        self.delete = Button(self, text='Deletar Tudo', font=('Time', '11'), command=self.delete_all_objects)
        self.delete.grid(row=3, column=1, sticky=NW, padx=0, pady=5)
        
        self.transformation = Button(self, text='Transformações', font=('Time', '11'), command=self.transform_object)
        self.transformation.grid(row=4, column=0, sticky=NW, padx=0, pady=5)

        self.generate_obj = Button(self, text='Gerar OBJ file', font=('Time', '11'), command=self.generate_obj_file)
        self.generate_obj.grid(row=4, column=1, sticky=NW, padx=0, pady=5)

        self.read_obj = Button(self, text='Ler OBJ file', font=('Time', '11'), command=self.read_obj_file)
        self.read_obj.grid(row=4, column=1, sticky=NW, padx=200, pady=5)

        self.retore_window_config = Button(self, text='Restaurar configurações da window', font=('Time', '11'), command=self.retore_window)
        self.retore_window_config.grid(row=3, column=1, sticky=NW, padx=200, pady=5)

        # scroll bar for the terminal outputs
        self.terminal_scrollbar = Scrollbar(self, orient=VERTICAL)
        self.terminal_scrollbar.grid(row=5, column=3, sticky=NS)

    def create_table(self):
        # terminal outputs
        self.table = ttk.Treeview(self)
        self.table.grid(row=5, column=0, columnspan=2, sticky=EW, padx=5)
        self.table.configure(yscrollcommand=self.terminal_scrollbar.set)
        self.table["columns"] = ("1", "2", "3")
        self.table['show'] = 'headings'
        self.table.column("# 1", anchor=CENTER)
        self.table.heading("# 1", text="Nome")
        self.table.column("# 2", anchor=CENTER)
        self.table.heading("# 2", text="Pontos")
        self.table.column("# 3", anchor=CENTER)
        self.table.heading("# 3", text="Id")

        self.columnconfigure(2, weight=1) # column with treeview
        self.rowconfigure(2, weight=1) # row with treeview    

    def include_point(self):
        IncludePoint(self.viewport, self.erros, self.display_file, self.table, self.coord_scn)

    def include_line(self):
        IncludeLine(self.viewport, self.erros, self.display_file, self.lines_list, self.table, self.coord_scn)

    def include_triangle(self):
        IncludeTriangle(self.viewport, self.erros, self.display_file, self.table, self.coord_scn)

    def include_quadrilateral(self):
        IncludeQuadrilateral(self.viewport, self.erros, self.display_file, self.table, self.coord_scn)

    def include_polygon(self):
        IncludePolygon(self.viewport, self.erros, self.display_file, self.table, self.coord_scn)

    def include_curve(self):
        IncludeCurve(self.viewport, self.erros, self.display_file, self.table, self.coord_scn)

    def include_point3D(self):
        IncludePoint3D(self.viewport, self.erros, self.display_file, self.table, self.coord_scn)

    def include_object3D(self):
        IncludeObject3D(self.viewport, self.erros, self.display_file, self.table, self.coord_scn)

    def delete_object(self):
        try:
            selected_item = self.table.selection()[0]
            self.delete_object_from_system(selected_item)
        except IndexError:
            self.erros['text'] = 'Selecione um item para remover'

    def delete_all_objects(self):
        all_items = self.table.get_children()

        for item in all_items:
            self.delete_object_from_system(item)

    def delete_object_from_system(self, selected_item):
        try:
            selected_item_id = self.table.item(selected_item).get('values')[2]
            selected_item_name = self.table.item(selected_item).get('values')[0]

            for object in self.display_file:
                if object.get_id() == selected_item_id:
                    self.delete_object_from_table(selected_item)
                    self.display_file.remove(object)
                    if isinstance(object, Line):
                        self.lines_list.remove(object)
                        self.viewport.delete(selected_item_id)
                    elif isinstance(object, Wireframe) or isinstance(object, Curve) or isinstance(object, Object3D):
                        for id in object.list_ids:
                            self.viewport.delete(id)
                        if object.fill_form != None:    
                            self.viewport.delete(object.fill_form)
                            object.fill_form = None
                    else:
                        self.viewport.delete(selected_item_id)
                elif object.get_name() == selected_item_name and object.get_id() == None:
                    self.delete_object_from_table(selected_item)
                    self.display_file.remove(object)
            self.erros['text'] = 'Objeto removido com sucesso'
        except IndexError:
            self.erros['text'] = 'Selecione um item para remover'

    def delete_object_from_table(self, id):
        self.table.delete(id)

    def update_object_from_table(self, id, item):
        self.table.item(id, 0, values=(item.get_name(), item.get_points(), item.get_id()))
        
    def transform_object(self):
        try:
            selected_item = self.table.selection()[0]
            selected_item_name = self.table.item(selected_item).get('values')[0]
            item = None
            for object in self.display_file:
                if object.get_name() == selected_item_name:
                    item = object
                    break
            Transformation(self.viewport, self.table, selected_item, item, self.coord_scn)
        except IndexError:
            self.erros['text'] = 'Selecione um item para transformar'

    def zoom_in(self):
        self.coord_scn.s[0] *= 1.1
        self.coord_scn.s[1] *= 1.1

        for object in self.display_file:
            self.coord_scn.generate_scn(object)
    
    def zoom_out(self):
        self.coord_scn.s[0] *= 0.9
        self.coord_scn.s[1] *= 0.9

        for object in self.display_file:
            self.coord_scn.generate_scn(object)

    def move_up(self):
        rotate_radian = (np.radians(float(self.coord_scn.angle_z)))
        rotate_radian_x = (np.radians(float(self.coord_scn.angle_x)))
        rotate_radian_y = (np.radians(float(self.coord_scn.angle_y)))
        sin = np.sin(rotate_radian)
        cos = np.cos(rotate_radian)
        sin_x = np.sin(rotate_radian_x)
        cos_x = np.cos(rotate_radian_x)
        sin_y = np.sin(rotate_radian_y)
        cos_y = np.cos(rotate_radian_y)

        self.coord_scn.wc[0] += 10*(sin)
        self.coord_scn.wc[1] += 10*(cos)

        self.coord_scn.vrp[0] -= 10*(sin)*(cos_y)
        self.coord_scn.vrp[1] += (10*(sin)*(sin_x)*(sin_y) + 10*(cos)*(cos_x))
        self.coord_scn.vrp[2] -= (10*(sin)*(cos_x)*(sin_y) - 10*(cos)*(sin_x)) 

        #[self.coord_scn.vrp[0], self.coord_scn.vrp[1], self.coord_scn.vrp[2]] = self.translation_of_window([self.coord_scn.vrp[0], self.coord_scn.vrp[1], self.coord_scn.vrp[2]], [0, 10, 0])

        for object in self.display_file:
            self.coord_scn.generate_scn(object)

    def move_left(self):
        rotate_radian = (np.radians(float(self.coord_scn.angle_z)))
        rotate_radian_x = (np.radians(float(self.coord_scn.angle_x)))
        rotate_radian_y = (np.radians(float(self.coord_scn.angle_y)))
        sin = np.sin(rotate_radian)
        cos = np.cos(rotate_radian)
        sin_x = np.sin(rotate_radian_x)
        cos_x = np.cos(rotate_radian_x)
        sin_y = np.sin(rotate_radian_y)
        cos_y = np.cos(rotate_radian_y)

        self.coord_scn.wc[0] -= 10*(cos)
        self.coord_scn.wc[1] += 10*(sin)

        self.coord_scn.vrp[0] -= 10*(cos)*(cos_y)
        self.coord_scn.vrp[1] += (10*(cos)*(sin_x)*(sin_y) - 10*(sin)*(cos_x))
        self.coord_scn.vrp[2] += (10*(cos)*(cos_x)*(sin_y) + 10*(sin)*(sin_x)) 

        for object in self.display_file:
            self.coord_scn.generate_scn(object)
    
    def move_right(self):
        rotate_radian = (np.radians(float(self.coord_scn.angle_z)))
        rotate_radian_x = (np.radians(float(self.coord_scn.angle_x)))
        rotate_radian_y = (np.radians(float(self.coord_scn.angle_y)))
        sin = np.sin(rotate_radian)
        cos = np.cos(rotate_radian)
        sin_x = np.sin(rotate_radian_x)
        cos_x = np.cos(rotate_radian_x)
        sin_y = np.sin(rotate_radian_y)
        cos_y = np.cos(rotate_radian_y)

        self.coord_scn.wc[0] += 10*(cos)
        self.coord_scn.wc[1] -= 10*(sin)

        self.coord_scn.vrp[0] += 10*(cos)*(cos_y)
        self.coord_scn.vrp[1] -= (10*(cos)*(sin_x)*(sin_y) - 10*(sin)*(cos_x))
        self.coord_scn.vrp[2] -= (10*(cos)*(cos_x)*(sin_y) + 10*(sin)*(sin_x))

        for object in self.display_file:
            self.coord_scn.generate_scn(object)

    def move_down(self):
        rotate_radian = (np.radians(float(self.coord_scn.angle_z)))
        rotate_radian_x = (np.radians(float(self.coord_scn.angle_x)))
        rotate_radian_y = (np.radians(float(self.coord_scn.angle_y)))
        sin = np.sin(rotate_radian)
        cos = np.cos(rotate_radian)
        sin_x = np.sin(rotate_radian_x)
        cos_x = np.cos(rotate_radian_x)
        sin_y = np.sin(rotate_radian_y)
        cos_y = np.cos(rotate_radian_y)

        self.coord_scn.wc[0] -= 10*(sin)
        self.coord_scn.wc[1] -= 10*(cos)

        self.coord_scn.vrp[0] += 10*(sin)*(cos_y)
        self.coord_scn.vrp[1] -= (10*(sin)*(sin_x)*(sin_y) + 10*(cos)*(cos_x))
        self.coord_scn.vrp[2] += (10*(sin)*(cos_x)*(sin_y) - 10*(cos)*(sin_x))

        for object in self.display_file:
            self.coord_scn.generate_scn(object)

    def rotate_right(self):
        self.coord_scn.angle_z -= 10

        for object in self.display_file:
            self.coord_scn.generate_scn(object)

    def rotate_left(self):
        self.coord_scn.angle_z += 10

        for object in self.display_file:
            self.coord_scn.generate_scn(object)
            

    def rotate_x_right(self):
        self.coord_scn.angle_x -= 10

        for object in self.display_file:
            self.coord_scn.generate_scn(object)

    def rotate_x_left(self):
        self.coord_scn.angle_x += 10

        for object in self.display_file:
            self.coord_scn.generate_scn(object)

    def rotate_y_right(self):
        self.coord_scn.angle_y -= 10

        for object in self.display_file:
            self.coord_scn.generate_scn(object)

    def rotate_y_left(self):
        self.coord_scn.angle_y += 10

        for object in self.display_file:
            self.coord_scn.generate_scn(object)

    def retore_window(self):
        self.coord_scn.wc[0] = 0
        self.coord_scn.wc[1] = 0
        self.coord_scn.wc[2] = 0
        self.coord_scn.vrp[0] = 0
        self.coord_scn.vrp[1] = 0
        self.coord_scn.vrp[2] = 0
        self.coord_scn.angle_x = 0
        self.coord_scn.angle_y = 0
        self.coord_scn.angle_z = 0

        for object in self.display_file:
            self.coord_scn.generate_scn(object)

    def translation_of_window(self, point, translation_points):
        x_rotated_angle = -self.coord_scn.angle_x
        rotation_matrix_x = [[1, 0, 0, 0],
                             [0, (np.cos(x_rotated_angle)), (np.sin(x_rotated_angle)), 0],
                             [0, -(np.sin(x_rotated_angle)), (np.cos(x_rotated_angle)), 0],
                             [0, 0, 0, 1]]
        
        y_rotated_angle = -self.coord_scn.angle_y
        rotation_matrix_y = [[(np.cos(y_rotated_angle)), 0, -(np.sin(y_rotated_angle)), 0],
                             [0, 1, 0, 0],
                             [(np.sin(y_rotated_angle)), 0, (np.cos(y_rotated_angle)), 0],
                             [0, 0, 0, 1]]

        z_rotated_angle = -self.coord_scn.angle_z
        rotation_matrix_z = [[(np.cos(z_rotated_angle)), (np.sin(z_rotated_angle)), 0, 0],
                             [-(np.sin(z_rotated_angle)), (np.cos(z_rotated_angle)), 0, 0],
                             [0, 0, 1, 0],
                             [0, 0, 0, 1]]
                
        points_matrix = []
        translation_matrix = [[1, 0, 0, 0],
                              [0, 1, 0, 0],
                              [0, 0, 1, 0],
                              [float(translation_points[0]), float(translation_points[1]), float(translation_points[2]), 1]]
        
        x_rotated_angle_inverse = -x_rotated_angle
        rotation_matrix_x_inverse = [[1, 0, 0, 0],
                                     [0, (np.cos(x_rotated_angle_inverse)), (np.sin(x_rotated_angle_inverse)), 0],
                                     [0, -(np.sin(x_rotated_angle_inverse)), (np.cos(x_rotated_angle_inverse)), 0],
                                     [0, 0, 0, 1]]

        y_rotated_angle_inverse = -y_rotated_angle
        rotation_matrix_y_inverse = [[(np.cos(y_rotated_angle_inverse)), 0, -(np.sin(y_rotated_angle_inverse)), 0],
                                     [0, 1, 0, 0],
                                     [(np.sin(y_rotated_angle_inverse)), 0, (np.cos(y_rotated_angle_inverse)), 0],
                                     [0, 0, 0, 1]]

        z_rotated_angle_inverse = -z_rotated_angle
        rotation_matrix_z_inverse = [[(np.cos(z_rotated_angle_inverse)), (np.sin(z_rotated_angle_inverse)), 0, 0],
                                     [-(np.sin(z_rotated_angle_inverse)), (np.cos(z_rotated_angle_inverse)), 0, 0],
                                     [0, 0, 1, 0],
                                     [0, 0, 0, 1]]

        points_matrix = [point[0], point[1], point[2], 1]
        result_points = np.matmul(points_matrix, rotation_matrix_x)
        #result_points = np.matmul(result_points, rotation_matrix_y)
        #result_points = np.matmul(result_points, rotation_matrix_z)
        
        result_points = np.matmul(result_points, translation_matrix)

        result_points = np.matmul(result_points, rotation_matrix_x_inverse)
        #result_points = np.matmul(result_points, rotation_matrix_y_inverse)
        #result_points = np.matmul(result_points, rotation_matrix_z_inverse)

        return [result_points[0], result_points[1], result_points[2]]

    def generate_obj_file(self):
        descritor_obj = DescritorOBJ(self.viewport, self.coord_scn, self.display_file)
        descritor_obj.create_OBJ_file()

    def read_obj_file(self):
        try:
            descritor_obj = DescritorOBJ(self.viewport, self.display_file)
            objetos = descritor_obj.read_OBJ_file()

            poligonos_adicionados = {}

            for objeto in objetos:
                tipo, nome, cor, vertices = objeto
                cor = f'#{rgb_to_hex(cor)}'
                lista_objetos = []

                for vertice in vertices:
                    for i in range(len(vertice)):
                        vertice[i] = float(vertice[i])

                    vertice.pop()

                if tipo == 'ponto':
                    objeto = Point(nome, vertices, cor)
                    lista_objetos.append(objeto)
                if tipo == 'linha':
                    if len(vertices) == 2:
                        objeto = Line(nome, vertices, cor)   
                        lista_objetos.append(objeto)             
                    else:
                        for i in range(len(vertices)):
                            if i == len(vertices)-1:
                                objeto = Line(nome, [vertices[i], vertices[0]], cor)
                            else:
                                objeto = Line(nome, [vertices[i], vertices[i+1]], cor)
                            lista_objetos.append(objeto) 
                if tipo == 'poligono':
                    if nome not in poligonos_adicionados.keys():
                        arestas = []
                        for i in range(len(vertices)-1):
                            arestas.append([vertices[i], vertices[i+1]])
                        objeto = Object3D(nome, vertices, arestas, cor)
                        lista_objetos.append(objeto)
                    else:
                        arestas = []
                        for i in range(len(vertices)-1):
                            arestas.append([vertices[i], vertices[i+1]])
                        poligonos_adicionados[nome].points = poligonos_adicionados[nome].points + vertices
                        poligonos_adicionados[nome].vectors = poligonos_adicionados[nome].vectors + arestas

                for objeto in lista_objetos:
                    objeto.drawn(self.viewport)
                    self.coord_scn.generate_scn(objeto)
                    self.display_file.append(objeto)
                    self.include_object_in_table(objeto)

            for object in self.display_file:
                self.coord_scn.generate_scn(object)

            messagebox.showerror('Sucesso', 'Arquivo OBJ lido e objetos criados!')
        except:
            messagebox.showerror('Erro', 'Algo falhou!')

    def include_object_in_table(self, object):
        self.table.insert('', 0, values=(object.get_name(), object.get_points(), object.get_id()))

    def rgb_to_hex(self, rgb):
        for i in range(len(rgb)):
            rgb[i] = int(rgb[i])
        return '%02x%02x%02x' % tuple(rgb)

    def clipping_select(self):
        self.radio_variable = IntVar()
        self.radio_variable.set(1)

        Radiobutton(self.frame2, text='Recorte de linha de CS', variable=self.radio_variable, value=1).grid(row=2, column=1, stick=N)
        Radiobutton(self.frame2, text='Recorte de linha de LB', variable=self.radio_variable, value=2).grid(row=2, column=1, stick=S)
