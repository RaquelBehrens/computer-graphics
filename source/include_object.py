from tkinter import *
from tkinter import ttk
from constants import INCLUDE_WINDOW_WIDTH, INCLUDE_WINDOW_HEIGHT, VIEWPORT_HEIGHT, VIEWPORT_WIDTH, POINT_SIZE
from copy import copy
from objects import *
from tkinter import simpledialog


class IncludeWindow:
    def __init__(self, viewport, erros, display_file, table, modification):
        self.main_window = Tk()
        self.main_window.title("Incluir objeto")
        self.main_window.geometry(f"{INCLUDE_WINDOW_WIDTH}x{INCLUDE_WINDOW_HEIGHT}")
        self.viewport = viewport
        self.erros = erros
        self.display_file = display_file
        self.table = table
        self.modification = modification

    def create_object(self):
        pass

    def include_object_in_table(self, object):
        self.table.insert('', 0, values=(object.getName(), object.getPoints(), object.getId()))

    def close_window(self):
        self.main_window.destroy()


class IncludePoint(IncludeWindow):
    def __init__(self, viewport, erros, display_file, table,modification):
        super().__init__(viewport, erros, display_file, table,modification)
        self.main_window.title("Incluir ponto")
        self.main_window.geometry(f"{INCLUDE_WINDOW_WIDTH}x{INCLUDE_WINDOW_HEIGHT-70}")

        self.frame1 = Frame(self.main_window)
        self.frame1.grid()
        self.frame2 = Frame(self.main_window)
        self.frame2.grid()
        self.frame3 = Frame(self.main_window)
        self.frame3.grid()
        self.frame4 = Frame(self.main_window)
        self.frame4.grid()

        Label(self.frame1, text='Nome: ', font=("Times", "11"), height=2).grid(row=0, column=0, sticky=NW)
        self.nome = Entry(self.frame1, width=30, font=("Times", "11"))
        self.nome.grid(row=0, column=1)

        Label(self.frame2, text='Coordenadas', font=("Times", "11"), height=2).grid(row=0, column=0, columnspan=2)

        Label(self.frame3, text='x1: ', font=("Times", "11")).grid(row=0, column=0, sticky=NW)
        self.x1 = Entry(self.frame3, width=3, font=("Times", "11"))
        self.x1.grid(row=0, column=1, sticky=NW)
        Label(self.frame3, text=' y1: ', font=("Times", "11")).grid(row=0, column=2, sticky=NW)
        self.y1 = Entry(self.frame3, width=3, font=("Times", "11"))
        self.y1.grid(row=0, column=3, sticky=NW)

        self.cancelar = Button(self.frame4, font=("Times", "11"), text='Cancelar', command=self.close_window)
        self.cancelar.grid(row=0, column=0, pady=15, padx=18)
        self.confirmar = Button(self.frame4, font=("Times", "11"), text='Confirmar', command=self.create_object)
        self.confirmar.grid(row=0, column=1, pady=15, padx=18)

    def create_object(self):
        try:
            x1 = float(self.x1.get())
            y1 = float(self.y1.get())
            name = self.nome.get()

            if name != '':
                objeto = Point(name, (x1, y1))
                objeto.drawn(self.viewport)

                for element in self.modification:
                    if element[0] == 'zoom':
                        self.viewport.scale(objeto.id, VIEWPORT_HEIGHT/2, VIEWPORT_WIDTH/2, element[1], element[1])
                    elif element[0] == 'move_hor':
                        self.viewport.move(objeto.id, 0, element[1])
                    else:
                        self.viewport.move(objeto.id, element[1], 0)
                
                self.close_window()                
                self.display_file.append(objeto)
                self.include_object_in_table(objeto)
                self.erros['text'] = 'objeto criado com sucesso'
            else:
                self.erros['text'] = 'falta nome'

        except ValueError:
            self.erros['text'] = 'mensagem de erro'


class IncludeLine(IncludeWindow):
    def __init__(self, viewport, erros, display_file, lines_list, table,modification):
        super().__init__(viewport, erros, display_file, table,modification)
        self.main_window.title("Incluir linha")
        self.lines_list = lines_list

        self.frame1 = Frame(self.main_window)
        self.frame1.grid()
        self.frame2 = Frame(self.main_window)
        self.frame2.grid()
        self.frame3 = Frame(self.main_window)
        self.frame3.grid()
        self.frame4 = Frame(self.main_window)
        self.frame4.grid()
        self.frame5 = Frame(self.main_window)
        self.frame5.grid()
        self.frame6 = Frame(self.main_window)
        self.frame6.grid()

        Label(self.frame1, text='Nome: ', font=("Times", "11"), height=2).grid(row=0, column=0, sticky=NW)
        self.nome = Entry(self.frame1, width=30, font=("Times", "11"))
        self.nome.grid(row=0, column=1)

        Label(self.frame2, text='Coordenadas Iniciais', font=("Times", "11"), height=2).grid(row=0, column=0, columnspan=2)

        Label(self.frame3, text='x1: ', font=("Times", "11")).grid(row=0, column=0, sticky=NW)
        self.x1 = Entry(self.frame3, width=3, font=("Times", "11"))
        self.x1.grid(row=0, column=1, sticky=NW)
        Label(self.frame3, text=' y1: ', font=("Times", "11")).grid(row=0, column=2, sticky=NW)
        self.y1 = Entry(self.frame3, width=3, font=("Times", "11"))
        self.y1.grid(row=0, column=3, sticky=NW)

        Label(self.frame4, text='Coordenadas Finais', font=("Times", "11"), height=2).grid(row=0, column=0, columnspan=2)

        Label(self.frame5, text='x2: ', font=("Times", "11")).grid(row=0, column=0, sticky=NW)
        self.x2 = Entry(self.frame5, width=3, font=("Times", "11"))
        self.x2.grid(row=0, column=1, sticky=NW)
        Label(self.frame5, text=' y2: ', font=("Times", "11")).grid(row=0, column=2, sticky=NW)
        self.y2 = Entry(self.frame5, width=3, font=("Times", "11"))
        self.y2.grid(row=0, column=3, sticky=NW)

        self.cancelar = Button(self.frame6, font=("Times", "11"), text='Cancelar', command=self.close_window)
        self.cancelar.grid(row=0, column=0, pady=15, padx=18)
        self.confirmar = Button(self.frame6, font=("Times", "11"), text='Confirmar', command=self.create_object)
        self.confirmar.grid(row=0, column=1, pady=15, padx=18)

    def create_object(self):
        try:
            x1 = float(self.x1.get())
            y1 = float(self.y1.get())
            x2 = float(self.x2.get())
            y2 = float(self.y2.get())

            name = self.nome.get()
            if name != '':
                if x1 == x2 and y1 == y2:
                    objeto = Point(name, (x1, y1))
                else:
                    objeto = Line(name, [(x1, y1), (x2, y2)])
                    self.lines_list.append(objeto)

                objeto.drawn(self.viewport)

                for element in self.modification:
                    if element[0] == 'zoom':
                        self.viewport.scale(objeto.id, VIEWPORT_HEIGHT/2, VIEWPORT_WIDTH/2, element[1], element[1])
                    elif element[0] == 'move_hor':
                        self.viewport.move(objeto.id, 0, element[1])
                    else:
                        self.viewport.move(objeto.id, element[1], 0)
                
                self.close_window()                
                self.display_file.append(objeto)
                self.include_object_in_table(objeto)
                self.erros['text'] = 'objeto criado com sucesso'

                formed_polygon, polygons_points_list, polygons_lines_list, copy_lines_list = self.verify_polygon(objeto, self.lines_list) 
                if formed_polygon:
                    self.substitute_lines_for_polygon(polygons_points_list, polygons_lines_list)
                    self.lines_list = copy_lines_list
            else:
                self.erros['text'] = 'falta nome'

        except ValueError:
            self.erros['text'] = 'mensagem de erro'

    def substitute_lines_for_polygon(self, polygons_points_list, polygons_lines_list):
        list_ids = []
        for line in polygons_lines_list:
            list_ids.append(line.getId())
            self.display_file.remove(line)
            self.lines_list.remove(line)

        for item in self.table.get_children():
            item_id = self.table.item(item).get('values')[2]
            if item_id in list_ids:
                self.table.delete(item)

        name = simpledialog.askstring(title="Polygon Name",
                                  prompt="Please, type the Polygon name:")
        objeto = Wireframe(name, polygons_points_list, polygons_lines_list[0].getId(), list_ids)
        self.include_object_in_table(objeto)
        self.display_file.append(objeto)
    
    def verify_polygon(self, last_line, lines_list):
        last_line_points = last_line.getPoints()
        x1 = last_line_points[0][0]
        y1 = last_line_points[0][1]
        x2 = last_line_points[1][0]
        y2 = last_line_points[1][1]

        copy_lines_list = copy(lines_list)
        copy_lines_list.remove(last_line)

        can_continue = True

        x_target = x1
        y_target = y1
        polygons_points_list = [(x1,y1)]
        polygons_lines_list = [last_line]

        amount_points = 1

        while can_continue:
            can_continue = False

            for line in copy_lines_list:
                points = line.getPoints()

                #checking first point
                if points[0][0] == x_target and points[0][1] == y_target:
                    x_target = points[1][0]
                    y_target = points[1][1]

                    polygons_points_list.append((x_target, y_target))
                    polygons_lines_list.append(line)
                    copy_lines_list.remove(line)

                    can_continue = True
                    amount_points += 1

                    if amount_points >= 3 and x_target == x2 and y_target == y2:
                        return True, polygons_points_list, polygons_lines_list, copy_lines_list

                    break

                #checking second point 
                elif points[1][0] == x_target and points[1][1] == y_target:
                    x_target = points[0][0]
                    y_target = points[0][1]

                    polygons_points_list.append((x_target, y_target))
                    polygons_lines_list.append(line)
                    copy_lines_list.remove(line)

                    can_continue = True
                    amount_points += 1

                    if amount_points >= 3 and x_target == x2 and y_target == y2:
                        return True, polygons_points_list, polygons_lines_list, copy_lines_list

                    break

        return False, None, None, None


class IncludeTriangle(IncludeWindow):
    def __init__(self, viewport, erros, display_file, table,modification):
        super().__init__(viewport, erros, display_file, table,modification)
        self.main_window.title("Incluir Triângulo")

        self.frame1 = Frame(self.main_window)
        self.frame1.grid()
        self.frame2 = Frame(self.main_window)
        self.frame2.grid()
        self.frame3 = Frame(self.main_window)
        self.frame3.grid()
        self.frame4 = Frame(self.main_window)
        self.frame4.grid()
        self.frame5 = Frame(self.main_window)
        self.frame5.grid()
        self.frame6 = Frame(self.main_window)
        self.frame6.grid()

        Label(self.frame1, text='Nome: ', font=("Times", "11"), height=2).grid(row=0, column=0, sticky=NW)
        self.nome = Entry(self.frame1, width=30, font=("Times", "11"))
        self.nome.grid(row=0, column=1)

        Label(self.frame2, text='Coordenadas', font=("Times", "11"), height=2).grid(row=0, column=0, columnspan=2)

        Label(self.frame3, text='x1: ', font=("Times", "11")).grid(row=0, column=0, sticky=NW)
        self.x1 = Entry(self.frame3, width=3, font=("Times", "11"))
        self.x1.grid(row=0, column=1, sticky=NW)
        Label(self.frame3, text=' y1: ', font=("Times", "11")).grid(row=0, column=2, sticky=NW)
        self.y1 = Entry(self.frame3, width=3, font=("Times", "11"))
        self.y1.grid(row=0, column=3, sticky=NW)

        Label(self.frame4, text='x2: ', font=("Times", "11")).grid(row=0, column=0, sticky=NW)
        self.x2 = Entry(self.frame4, width=3, font=("Times", "11"))
        self.x2.grid(row=0, column=1, sticky=NW)
        Label(self.frame4, text=' y2: ', font=("Times", "11")).grid(row=0, column=2, sticky=NW)
        self.y2 = Entry(self.frame4, width=3, font=("Times", "11"))
        self.y2.grid(row=0, column=3, sticky=NW)

        Label(self.frame5, text='x3: ', font=("Times", "11")).grid(row=0, column=0, sticky=NW)
        self.x3 = Entry(self.frame5, width=3, font=("Times", "11"))
        self.x3.grid(row=0, column=1, sticky=NW)
        Label(self.frame5, text=' y3: ', font=("Times", "11")).grid(row=0, column=2, sticky=NW)
        self.y3 = Entry(self.frame5, width=3, font=("Times", "11"))
        self.y3.grid(row=0, column=3, sticky=NW)

        self.cancelar = Button(self.frame6, font=("Times", "11"), text='Cancelar', command=self.close_window)
        self.cancelar.grid(row=0, column=0, pady=15, padx=18)
        self.confirmar = Button(self.frame6, font=("Times", "11"), text='Confirmar', command=self.create_object)
        self.confirmar.grid(row=0, column=1, pady=15, padx=18)

    def create_object(self):
        try:
            x1 = float(self.x1.get())
            y1 = float(self.y1.get())
            x2 = float(self.x2.get())
            y2 = float(self.y2.get())
            x3 = float(self.x3.get())
            y3 = float(self.y3.get())

            name = self.nome.get()
            if name != '':
                if (x1 == x2 and y1 == y2) or (x1 == x3 and y1 == y3):
                    self.erros['text'] = 'Os pontos coincidem'
                else:
                    
                    objeto = Wireframe(name, [(x1,y1), (x2,y2), (x3,y3)])
                    objeto.drawn(self.viewport)

                    for element in self.modification:
                        if element[0] == 'zoom':
                            self.viewport.scale(objeto.id, VIEWPORT_HEIGHT/2, VIEWPORT_WIDTH/2, element[1], element[1])
                        elif element[0] == 'move_hor':
                            self.viewport.move(objeto.id, 0, element[1])
                        else:
                            self.viewport.move(objeto.id, element[1], 0)
                    
                    self.close_window()                
                    self.display_file.append(objeto)
                    self.include_object_in_table(objeto)
                    self.erros['text'] = 'objeto criado com sucesso'
            else:
                self.erros['text'] = 'falta nome'

        except ValueError:
            self.erros['text'] = 'mensagem de erro'


class IncludeQuadrilateral(IncludeWindow):
    def __init__(self, viewport, erros, display_file, table,modification):
        super().__init__(viewport, erros, display_file, table,modification)
        self.main_window.title("Incluir Quadrilátero")
        self.main_window.geometry(f"{INCLUDE_WINDOW_WIDTH}x{INCLUDE_WINDOW_HEIGHT+130}")

        self.frame0 = Frame(self.main_window)
        self.frame0.grid()
        self.frame1 = Frame(self.main_window)
        self.frame1.grid()
        self.frame2 = Frame(self.main_window)
        self.frame2.grid()
        self.frame3 = Frame(self.main_window)
        self.frame3.grid()
        self.frame4 = Frame(self.main_window)
        self.frame4.grid()
        self.frame5 = Frame(self.main_window)
        self.frame5.grid()
        self.frame6 = Frame(self.main_window)
        self.frame6.grid()
        self.frame7 = Frame(self.main_window)
        self.frame7.grid()
        
        Label(self.frame0, text='Instruções:', font=("Times", "11"), height=0).grid(row=0, column=0, sticky=NW)
        Label(self.frame0, text='(x1, y1) = canto superior esquerdo;', font=("Times", "11"), height=0).grid(row=1, column=0, sticky=NW)
        Label(self.frame0, text='(x2, y2) = canto superior direito;', font=("Times", "11"), height=0).grid(row=2, column=0, sticky=NW)
        Label(self.frame0, text='(x3, y3) = canto inferior esquerdo;', font=("Times", "11"), height=0).grid(row=3, column=0, sticky=NW)
        Label(self.frame0, text='(x4, y4) = canto inferior direito.', font=("Times", "11"), height=0).grid(row=4, column=0, sticky=NW)

        Label(self.frame1, text='Nome: ', font=("Times", "11"), height=2).grid(row=0, column=0, sticky=NW)
        self.nome = Entry(self.frame1, width=30, font=("Times", "11"))
        self.nome.grid(row=4, column=1)

        Label(self.frame2, text='Coordenadas', font=("Times", "11"), height=2).grid(row=0, column=0, columnspan=2)

        Label(self.frame3, text='x1: ', font=("Times", "11")).grid(row=0, column=0, sticky=NW)
        self.x1 = Entry(self.frame3, width=3, font=("Times", "11"))
        self.x1.grid(row=0, column=1, sticky=NW)
        Label(self.frame3, text=' y1: ', font=("Times", "11")).grid(row=0, column=2, sticky=NW)
        self.y1 = Entry(self.frame3, width=3, font=("Times", "11"))
        self.y1.grid(row=0, column=3, sticky=NW)

        Label(self.frame4, text='x2: ', font=("Times", "11")).grid(row=0, column=0, sticky=NW)
        self.x2 = Entry(self.frame4, width=3, font=("Times", "11"))
        self.x2.grid(row=0, column=1, sticky=NW)
        Label(self.frame4, text=' y2: ', font=("Times", "11")).grid(row=0, column=2, sticky=NW)
        self.y2 = Entry(self.frame4, width=3, font=("Times", "11"))
        self.y2.grid(row=0, column=3, sticky=NW)

        Label(self.frame5, text='x3: ', font=("Times", "11")).grid(row=0, column=0, sticky=NW)
        self.x3 = Entry(self.frame5, width=3, font=("Times", "11"))
        self.x3.grid(row=0, column=1, sticky=NW)
        Label(self.frame5, text=' y3: ', font=("Times", "11")).grid(row=0, column=2, sticky=NW)
        self.y3 = Entry(self.frame5, width=3, font=("Times", "11"))
        self.y3.grid(row=0, column=3, sticky=NW)

        Label(self.frame6, text='x4: ', font=("Times", "11")).grid(row=0, column=0, sticky=NW)
        self.x4 = Entry(self.frame6, width=3, font=("Times", "11"))
        self.x4.grid(row=0, column=1, sticky=NW)
        Label(self.frame6, text=' y4: ', font=("Times", "11")).grid(row=0, column=2, sticky=NW)
        self.y4 = Entry(self.frame6, width=3, font=("Times", "11"))
        self.y4.grid(row=0, column=3, sticky=NW)

        self.cancelar = Button(self.frame7, font=("Times", "11"), text='Cancelar', command=self.close_window)
        self.cancelar.grid(row=0, column=0, pady=15, padx=18)
        self.confirmar = Button(self.frame7, font=("Times", "11"), text='Confirmar', command=self.create_object)
        self.confirmar.grid(row=0, column=1, pady=15, padx=18)

    def create_object(self):
        try:
            x1 = float(self.x1.get())
            y1 = float(self.y1.get())
            x2 = float(self.x2.get())
            y2 = float(self.y2.get())
            x3 = float(self.x3.get())
            y3 = float(self.y3.get())
            x4 = float(self.x4.get())
            y4 = float(self.y4.get())

            name = self.nome.get()
            if name != '':
                if (x1 == x2 and y1 == y2) or (x1 == x3 and y1 == y3) or (x1 == x4 and y1 == y4) or (x2 == x4 and y2 == y4) or (x3 == x4 and y3 == y4) or (x2 == x3 and y2 == y3):
                    self.erros['text'] = 'Os pontos coincidem'
                else:
                    objeto = Wireframe(name, [(x1,y1), (x2,y2), (x3,y3), (x4,y4)])
                    objeto.drawn(self.viewport)

                    for element in self.modification:
                        if element[0] == 'zoom':
                            self.viewport.scale(objeto.id, VIEWPORT_HEIGHT/2, VIEWPORT_WIDTH/2, element[1], element[1])
                        elif element[0] == 'move_hor':
                            self.viewport.move(objeto.id, 0, element[1])
                        else:
                            self.viewport.move(objeto.id, element[1], 0)
                    
                    self.close_window()                
                    self.display_file.append(objeto)
                    self.include_object_in_table(objeto)
                    self.erros['text'] = 'objeto criado com sucesso'
            else:
                self.erros['text'] = 'falta nome'

        except ValueError:
            self.erros['text'] = 'mensagem de erro'


class IncludePolygon(IncludeWindow):
    def __init__(self, viewport, erros, display_file, table,modification):
        super().__init__(viewport, erros, display_file, table,modification)
        self.main_window.title("Incluir Outro Polígono")
        self.main_window.geometry(f"{INCLUDE_WINDOW_WIDTH+100}x{INCLUDE_WINDOW_HEIGHT-50}")

        self.frame0 = Frame(self.main_window)
        self.frame0.grid()
        self.frame1 = Frame(self.main_window)
        self.frame1.grid()
        self.frame2 = Frame(self.main_window)
        self.frame2.grid()
        self.frame3 = Frame(self.main_window)
        self.frame3.grid()
        self.frame4 = Frame(self.main_window)
        self.frame4.grid()
        
        Label(self.frame0, text='Instruções:', font=("Times", "11"), height=0).grid(row=0, column=0, sticky=NW)
        Label(self.frame0, text='Cada ponto digitado adjacentemente, será adjacente no Canvas.', font=("Times", "11"), height=0).grid(row=1, column=0, sticky=NW)

        Label(self.frame1, text='Nome: ', font=("Times", "11"), height=2).grid(row=0, column=0, sticky=NW)
        self.nome = Entry(self.frame1, width=30, font=("Times", "11"))
        self.nome.grid(row=0, column=1)

        Label(self.frame2, text='Coordenadas: ', font=("Times", "11")).grid(row=0, column=0, sticky=NW)
        self.entry_polygon = Entry(self.frame2, width=30, font=("Times", "11"))
        self.entry_polygon.grid(row=0, column=1, sticky=NW)
        Label(self.frame2, text='(x1,y1), (x2,y2), ..., (xn,yn)', font=("Times", "11")).grid(row=1, column=1)

        self.cancelar = Button(self.frame4, font=("Times", "11"), text='Cancelar', command=self.close_window)
        self.cancelar.grid(row=0, column=0, pady=15, padx=18)
        self.confirmar = Button(self.frame4, font=("Times", "11"), text='Confirmar', command=self.create_object)
        self.confirmar.grid(row=0, column=1, pady=15, padx=18)

    def create_object(self):
        try:
            coordinates = self.convert_to_list(self.entry_polygon.get())
            name = self.nome.get()

            if name != '':
                objeto = Wireframe(name, coordinates)
                objeto.drawn(self.viewport)

                for element in self.modification:
                    if element[0] == 'zoom':
                        self.viewport.scale(objeto.id, VIEWPORT_HEIGHT/2, VIEWPORT_WIDTH/2, element[1], element[1])
                    elif element[0] == 'move_hor':
                        self.viewport.move(objeto.id, 0, element[1])
                    else:
                        self.viewport.move(objeto.id, element[1], 0)
                
                self.close_window()                
                self.display_file.append(objeto)
                self.include_object_in_table(objeto)
                self.erros['text'] = 'objeto criado com sucesso'
            else:
                self.erros['text'] = 'falta nome'

        except ValueError:
            self.erros['text'] = 'mensagem de erro'

    def convert_to_list(self, coordinates):
        lista = coordinates
        coords = []

        aux = []
        aux_coords = []
        for i in range(len(lista)):
            try:
                if lista[i] == ',' or i == len(lista)-1:
                    number = "".join(aux)
                    aux_coords.append(float(number))
                    aux.clear()
                float(lista[i])
                aux.append(lista[i])
            except ValueError:
                pass

        if len(aux_coords) % 2 == 0 and len(aux_coords) >= 6:    
            for i in range(0, len(aux_coords), 2):
                coords.append((aux_coords[i], aux_coords[i+1]))
            return coords
        else:
            self.erros['text'] = 'mensagem de erro'
