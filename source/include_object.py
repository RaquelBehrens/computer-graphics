from tkinter import *
from constants import INCLUDE_WINDOW_WIDTH, INCLUDE_WINDOW_HEIGHT, VIEWPORT_HEIGHT 
from copy import copy
from objects import *

class IncludeWindow:
    def __init__(self, viewport, erros, objects_list, table):
        self.main_window = Tk()
        self.main_window.title("Incluir objeto")
        self.main_window.geometry(f"{INCLUDE_WINDOW_HEIGHT}x{INCLUDE_WINDOW_WIDTH}")
        self.viewport = viewport
        self.erros = erros
        self.objects_list = objects_list
        self.table = table

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

            nome = self.nome.get()
            if nome != '':
                id = self.drawn_line(x1, y1, x2, y2)
                objeto = Line(id, nome, (x1, y1), (x2, y2))
                self.objects_list.append(objeto)
                self.include_object_in_table(objeto)
                
                #object = self.verifyPolygon(x1, y1, x2, y2, self.lines_list)

                self.erros['text'] = 'objeto criado com sucesso'
                return objeto
            else:
                self.erros['text'] = 'falta nome'
                return None
        except ValueError:
            self.erros['text'] = 'mensagem de erro'
            return None

    def include_object_in_table(self, object):
        self.table.insert('', 0, values=(object.getName(), object.getPoints(), object.getId()))

    def close_window(self):
        self.main_window.destroy()

    def drawn_line(self, x1, y1, x2, y2):
        y1 = VIEWPORT_HEIGHT - y1
        y2 = VIEWPORT_HEIGHT - y2
        id = self.viewport.create_line((x1, y1), (x2, y2), width=3, fill='white')
        self.close_window()
        return id


    #def verifyPolygon(self, x1, y1, x2, y2, lines_list):
    #    copy_lines_list = copy(lines_list)
    #    for line in copy_lines_list:
    #        for point in line.getPoints():
    #            if (point.get(0) == x1 and point.get(1) == y1) or (point.get(0) == x2 and point.get(1) == y2):           
    #    pass
