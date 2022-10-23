from tkinter import *

from constants import INCLUDE_WINDOW_WIDTH, INCLUDE_WINDOW_HEIGHT
from .include_window import IncludeWindow
from objects import (Point3D)


class IncludePoint3D(IncludeWindow):
    def __init__(self, viewport, erros, display_file, table, coord_scn):
        super().__init__(viewport, erros, display_file, table, coord_scn)
        self.main_window.title("Incluir Ponto 3D:")
        self.main_window.geometry(f"{INCLUDE_WINDOW_WIDTH}x{INCLUDE_WINDOW_HEIGHT-70}")

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
        Label(self.frame3, text=' z1: ', font=("Times", "11")).grid(row=0, column=4, sticky=NW)
        self.z1 = Entry(self.frame3, width=3, font=("Times", "11"))
        self.z1.grid(row=0, column=5, sticky=NW)

        Label(self.frame4, text='Defina uma cor', font=("Times", "11"), height=2).grid(row=0, column=0, columnspan=2)
        self.color_button = Button(self.frame5, text='Escolher cor', font=('Times', '11'), command=self.choose_color, bg=self.color)
        self.color_button.grid(row=0, column=3, padx=10)

        self.cancelar = Button(self.frame6, font=("Times", "11"), text='Cancelar', command=self.close_window)
        self.cancelar.grid(row=0, column=0, pady=15, padx=18)
        self.confirmar = Button(self.frame6, font=("Times", "11"), text='Confirmar', command=self.create_object)
        self.confirmar.grid(row=0, column=1, pady=15, padx=18)

    def create_object(self):
        try:
            x1 = float(self.x1.get())
            y1 = float(self.y1.get())
            z1 = float(self.z1.get())
            name = self.nome.get()
            already_used = False
            for objects in self.display_file:
                if objects.name == name:
                    already_used = True

            if name != '' and not already_used:
                objeto = Point3D(name, [[x1, y1, z1]], self.color)
                objeto.drawn(self.viewport, self.coord_scn)

                self.coord_scn.generate_scn(objeto)
                
                self.close_window()                
                self.display_file.append(objeto)
                self.include_object_in_table(objeto)
                self.erros['text'] = 'Objeto criado com sucesso'
            else:
                if name == '':
                    self.erros['text'] = 'Digite um nome'
                else:
                    self.erros['text'] = 'Nome já utilizado'

        except ValueError:
            self.erros['text'] = 'Entradas inválidas'
