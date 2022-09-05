from tkinter import *
from constants import INCLUDE_WINDOW_WIDTH, INCLUDE_WINDOW_HEIGHT, VIEWPORT_HEIGHT, POINT_SIZE
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
                    objeto = self.draw_point(name, x1, y1)
                    self.display_file.append(objeto)
                    self.include_object_in_table(objeto)
                else:
                    objeto = self.draw_line(name, x1, y1, x2, y2)
                    self.display_file.append(objeto)
                    self.include_object_in_table(objeto)
                    formed_polygon, polygons_points_list, polygons_lines_list, copy_lines_list = self.verify_polygon(objeto, self.lines_list)
                    if formed_polygon:
                        self.draw_polygon(polygons_points_list, polygons_lines_list)
                        self.lines_list = copy_lines_list

                self.erros['text'] = 'objeto criado com sucesso'
            else:
                self.erros['text'] = 'falta nome'

        except ValueError:
            self.erros['text'] = 'mensagem de erro'

    def include_object_in_table(self, object):
        self.table.insert('', 0, values=(object.getName(), object.getPoints(), object.getId()))

    def close_window(self):
        self.main_window.destroy()

    def draw_line(self, name, x1, y1, x2, y2):
        viewport_y1 = VIEWPORT_HEIGHT - y1
        viewport_y2 = VIEWPORT_HEIGHT - y2
        id = self.viewport.create_line((x1, viewport_y1), (x2, viewport_y2), width=3, fill='white')
        self.viewport.scale(id, VIEWPORT_HEIGHT/2, VIEWPORT_WIDTH/2, self.aplied_zoom, self.aplied_zoom)
        self.viewport.move(id, self.aplied_move[0], self.aplied_move[1])
        self.close_window()        
        #create line object
        objeto = Line(id, name, (x1, y1), (x2, y2))
        self.lines_list.append(objeto)
        return objeto

    def draw_point(self, name, x1, y1):
        viewport_y1 = VIEWPORT_HEIGHT - y1
        id = self.viewport.create_oval(x1, viewport_y1, x1, viewport_y1, width=POINT_SIZE, fill="white")
        self.viewport.scale(id, VIEWPORT_HEIGHT/2, VIEWPORT_WIDTH/2, self.aplied_zoom, self.aplied_zoom)
        self.viewport.move(id, self.aplied_move[0], self.aplied_move[1])
        self.close_window()
        #create point object
        objeto = Point(id, name, (x1, y1))
        return objeto

    def draw_polygon(self, polygons_points_list, polygons_lines_list):
        list_ids = []
        for line in polygons_lines_list:
            list_ids.append(line.getId())

        for item in self.table.get_children():
            item_id = self.table.item(item).get('values')[2]
            if item_id in list_ids:
                self.table.delete(item)

        name = simpledialog.askstring(title="Polygon Name",
                                  prompt="Please, type the Polygon name:")
        objeto = Wireframe(polygons_lines_list[0].getId(), name, polygons_points_list)
        self.include_object_in_table(objeto)
    
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



