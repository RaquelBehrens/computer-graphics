from tkinter import *
from tkinter import ttk
from constants import INCLUDE_WINDOW_WIDTH, INCLUDE_WINDOW_HEIGHT, VIEWPORT_HEIGHT, VIEWPORT_WIDTH, POINT_SIZE
from copy import copy
from objects import *
from tkinter import simpledialog

class IncludeWindow:
    def __init__(self, viewport, erros, display_file, lines_list, table, move, zoom):
        self.main_window = Tk()
        self.main_window.title("Incluir objeto")
        self.main_window.geometry(f"{INCLUDE_WINDOW_HEIGHT}x{INCLUDE_WINDOW_WIDTH}")
        self.viewport = viewport
        self.erros = erros
        self.display_file = display_file
        self.lines_list = lines_list
        self.table = table
        self.aplied_move = move
        self.aplied_zoom = zoom
        
        self.entry_point = []
        self.entry_line = []
        self.entry_polygon = []

        self.frame1 = Frame(self.main_window)
        self.frame1.grid()

        Label(self.frame1, text='Nome: ', font=("Times", "11"), height=2).grid(row=0, column=0, sticky=NW)
        self.nome = Entry(self.frame1, width=30, font=("Times", "11"))
        self.nome.grid(row=0, column=1)

        self.tab_control = ttk.Notebook(self.main_window)
        self.tab1 = Frame(self.tab_control)
        self.tab2 = Frame(self.tab_control)
        self.tab3 = Frame(self.tab_control)

        self.tab_control.add(self.tab1, text='Ponto')
        self.tab_control.add(self.tab2, text='Linha')
        self.tab_control.add(self.tab3, text='Polígono')
        self.tab_control.grid()

        self.tab_point()
        self.tab_line()
        self.tab_polygon()

        self.frame2 = Frame(self.main_window)
        self.frame2.grid()

        self.cancelar = Button(self.frame2, font=("Times", "11"), text='Cancelar', command=self.close_window)
        self.cancelar.grid(row=0, column=0, pady=15, padx=18)
        self.confirmar = Button(self.frame2, font=("Times", "11"), text='Confirmar', command=self.create_object)
        self.confirmar.grid(row=0, column=1, pady=15, padx=18)

    def create_object(self):
        try:
            name = self.nome.get()
            if name != '':
                tab_index = self.tab_control.index(self.tab_control.select())
                if tab_index == 0:
                    for i in range(len(self.entry_point)):
                        self.entry_point[i] = float(self.entry_point[i].get())
                    objeto = Point(name, self.entry_point)
                else:
                    if tab_index == 1:
                        for i in range(len(self.entry_line)):
                            self.entry_line[i] = float(self.entry_line[i].get())
                        objeto = Line(name, self.entry_line)
                        self.lines_list.append(objeto)
                    else:
                        self.entry_polygon = self.ConvertToList()
                        objeto = Wireframe(name, self.entry_line)
                    # Aqui estava dando um erro depois que eu mudei. Vou ver isso e arrumar.
                    # formed_polygon, polygons_points_list, polygons_lines_list, copy_lines_list = self.verify_polygon(objeto, self.lines_list)
                    # if formed_polygon:
                    #     self.draw_polygon(polygons_points_list, polygons_lines_list)
                    #     self.lines_list = copy_lines_list
                    
                objeto.drawn(self.viewport)
                self.close_window()
                self.display_file.append(objeto)
                self.include_object_in_table(objeto)

                self.erros['text'] = 'objeto criado com sucesso'
            else:
                self.erros['text'] = 'falta nome'

        except ValueError:
            self.erros['text'] = 'mensagem de erro'

    def include_object_in_table(self, object):
        self.table.insert('', 0, values=(object.getName(), object.getPoints(), object.getId()))

    def close_window(self):
        self.main_window.destroy()

    def tab_point(self):
        self.frame_ponto = Frame(self.tab1)
        self.frame_ponto.grid()
        self.frame_ponto2 = Frame(self.tab1)
        self.frame_ponto2.grid()

        Label(self.frame_ponto, text='Coordenadas', font=("Times", "11"), height=2).grid(row=0, column=0, columnspan=2)

        Label(self.frame_ponto2, text='x1: ', font=("Times", "11")).grid(row=0, column=0, sticky=NW)
        self.entry_point.append(Entry(self.frame_ponto2, width=3, font=("Times", "11")))
        self.entry_point[0].grid(row=0, column=1, sticky=NW)
        Label(self.frame_ponto2, text=' y1: ', font=("Times", "11")).grid(row=0, column=2, sticky=NW)
        self.entry_point.append(Entry(self.frame_ponto2, width=3, font=("Times", "11")))
        self.entry_point[1].grid(row=0, column=3, sticky=NW)

    def tab_line(self):
        self.linha = Frame(self.tab2)
        self.linha.grid()
        self.linha2 = Frame(self.tab2)
        self.linha2.grid()
        self.linha3 = Frame(self.tab2)
        self.linha3.grid()
        self.linha4 = Frame(self.tab2)
        self.linha4.grid()

        Label(self.linha, text='Coordenadas Iniciais', font=("Times", "11"), height=2).grid(row=0, column=0, columnspan=2)

        Label(self.linha2, text='x1: ', font=("Times", "11")).grid(row=0, column=0, sticky=NW)
        self.entry_line.append(Entry(self.linha2, width=3, font=("Times", "11")))
        self.entry_line[0].grid(row=0, column=1, sticky=NW)
        Label(self.linha2, text=' y1: ', font=("Times", "11")).grid(row=0, column=2, sticky=NW)
        self.entry_line.append(Entry(self.linha2, width=3, font=("Times", "11")))
        self.entry_line[1].grid(row=0, column=3, sticky=NW)

        Label(self.linha3, text='Coordenadas Finais', font=("Times", "11"), height=2).grid(row=0, column=0, columnspan=2)

        Label(self.linha4, text='x2: ', font=("Times", "11")).grid(row=0, column=0, sticky=NW)
        self.entry_line.append(Entry(self.linha4, width=3, font=("Times", "11")))
        self.entry_line[2].grid(row=0, column=1, sticky=NW)
        Label(self.linha4, text=' y2: ', font=("Times", "11")).grid(row=0, column=2, sticky=NW)
        self.entry_line.append(Entry(self.linha4, width=3, font=("Times", "11")))
        self.entry_line[3].grid(row=0, column=3, sticky=NW)

    def tab_polygon(self):
        self.frame_poly = Frame(self.tab3)
        self.frame_poly.grid()
        self.frame_poly2 = Frame(self.tab3)
        self.frame_poly2.grid()

        Label(self.frame_poly, text='Coordenadas', font=("Times", "11"), height=2).grid(row=0, column=0, columnspan=2)
        Label(self.frame_poly, text='(x1,y1), (x2,y2), ..., (xn,yn): ', font=("Times", "11"), height=2).grid(row=1, column=0)

        self.entry_polygon = Entry(self.frame_poly2, width=20, font=("Times", "11"))
        self.entry_polygon.grid(row=0, column=0, sticky=NW)

    def draw_polygon(self, polygons_points_list, polygons_lines_list):
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
        objeto = Wireframe(polygons_lines_list[0].getId(), name, list_ids, polygons_points_list)
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

    def ConvertToList(self):
        lista = list(self.entry_polygon.get())
        coords = []
        for i in range(len(lista)):
            try:
                coords.append(float(lista[i]))
            except ValueError:
                pass 
        if len(coords) % 2 == 0 and len(coords) > 6:     
            return coords
        else:
            self.erros['text'] = 'mensagem de erro'

