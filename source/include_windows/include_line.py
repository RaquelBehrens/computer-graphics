from tkinter import *
from tkinter import simpledialog
from copy import copy

from .include_window import IncludeWindow
from objects import (Point, Line, Wireframe)


class IncludeLine(IncludeWindow):
    def __init__(self, viewport, erros, display_file, lines_list, table, coord_scn):
        super().__init__(viewport, erros, display_file, table, coord_scn)
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
        self.frame7 = Frame(self.main_window)
        self.frame7.grid()
        self.frame8 = Frame(self.main_window)
        self.frame8.grid()

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

        Label(self.frame6, text='Defina uma cor', font=("Times", "11"), height=2).grid(row=0, column=0, columnspan=2)
        self.color_button = Button(self.frame7, text='Escolher cor', font=('Times', '11'), command=self.choose_color, bg=self.color)
        self.color_button.grid(row=0, column=3, padx=10)

        self.cancelar = Button(self.frame8, font=("Times", "11"), text='Cancelar', command=self.close_window)
        self.cancelar.grid(row=0, column=0, pady=15, padx=18)
        self.confirmar = Button(self.frame8, font=("Times", "11"), text='Confirmar', command=self.create_object)
        self.confirmar.grid(row=0, column=1, pady=15, padx=18)

    def create_object(self):
        try:
            x1 = float(self.x1.get())
            y1 = float(self.y1.get())
            x2 = float(self.x2.get())
            y2 = float(self.y2.get())

            name = self.nome.get()
            already_used = False
            for objects in self.display_file:
                if objects.name == name:
                    already_used = True
            if name != '' and not already_used:
                if x1 == x2 and y1 == y2:
                    objeto = Point(name, [[x1, y1]], self.color)
                else:
                    objeto = Line(name, [[x1, y1], [x2, y2]], self.color)
                    self.lines_list.append(objeto)

                self.coord_scn.generate_scn(objeto)
                
                self.close_window()                
                self.display_file.append(objeto)
                self.include_object_in_table(objeto)
                self.erros['text'] = 'Objeto criado com sucesso'

                if isinstance(objeto, Line):
                    formed_polygon, polygons_points_list, polygons_lines_list, copy_lines_list = self.verify_polygon(objeto, self.lines_list) 
                    if formed_polygon:
                        self.substitute_lines_for_polygon(polygons_points_list, polygons_lines_list)
                        self.lines_list = copy_lines_list
            else:
                if name == '':
                    self.erros['text'] = 'Digite um nome'
                else:
                    self.erros['text'] = 'Nome já utilizado'

        except ValueError:
            self.erros['text'] = 'Entradas inválidas'

    def substitute_lines_for_polygon(self, polygons_points_list, polygons_lines_list):
        name = simpledialog.askstring(title="Polygon Name", prompt="Por favor, digite o nome do novo polígono:")
        self.choose_color()

        list_ids = []
        for line in polygons_lines_list:
            list_ids.append(line.get_id())
            self.display_file.remove(line)
            self.lines_list.remove(line)
            self.viewport.itemconfig(line.get_id(), fill=self.color)

        for item in self.table.get_children():
            item_id = self.table.item(item).get('values')[2]
            if item_id in list_ids:
                self.table.delete(item)

        objeto = Wireframe(name, polygons_points_list, self.color, 1, polygons_lines_list[0].get_id())
        objeto.list_ids = list_ids
        self.include_object_in_table(objeto)
        self.display_file.append(objeto)
    
    def verify_polygon(self, last_line, lines_list):
        last_line_points = last_line.get_points()
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
                points = line.get_points()

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
