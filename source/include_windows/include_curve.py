from tkinter import *
from tkinter.messagebox import askyesno

from constants import INCLUDE_WINDOW_WIDTH, INCLUDE_WINDOW_HEIGHT
from .include_window import IncludeWindow
from objects import (Curve)

class IncludeCurve(IncludeWindow):
    def __init__(self, viewport, erros, display_file, table, coord_scn):
        super().__init__(viewport, erros, display_file, table, coord_scn)
        self.main_window.title("Incluir Curva")
        self.main_window.geometry(f"{INCLUDE_WINDOW_WIDTH+100}x{INCLUDE_WINDOW_HEIGHT-10}")

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
        
        Label(self.frame0, text='Instruções:', font=("Times", "11"), height=0).grid(row=0, column=0, sticky=NW)
        Label(self.frame0, text='Cada ponto digitado adjacentemente, será adjacente no Canvas.', font=("Times", "11"), height=0).grid(row=1, column=0, sticky=NW)

        Label(self.frame1, text='Nome: ', font=("Times", "11"), height=2).grid(row=0, column=0, sticky=NW)
        self.nome = Entry(self.frame1, width=30, font=("Times", "11"))
        self.nome.grid(row=0, column=1)

        Label(self.frame2, text='Coordenadas: ', font=("Times", "11")).grid(row=0, column=0, sticky=NW)
        self.entry_polygon = Entry(self.frame2, width=30, font=("Times", "11"))
        self.entry_polygon.grid(row=0, column=1, sticky=NW)
        Label(self.frame2, text='(x1,y1), (x2,y2), ..., (xn,yn)', font=("Times", "11")).grid(row=1, column=1)

        Label(self.frame3, text='Defina a cor', font=("Times", "11")).grid(row=0, column=0, columnspan=2)
        
        self.color_button = Button(self.frame4, text='Escolher cor', font=('Times', '11'), command=self.choose_color, bg=self.color)
        self.color_button.grid(row=0, column=3, padx=10)

        self.cancelar = Button(self.frame5, font=("Times", "11"), text='Cancelar', command=self.close_window)
        self.cancelar.grid(row=0, column=0, pady=15, padx=18)
        self.confirmar = Button(self.frame5, font=("Times", "11"), text='Confirmar', command=self.create_object)
        self.confirmar.grid(row=0, column=1, pady=15, padx=18)

    def create_object(self):
        try:
            coordinates = self.convert_to_list(self.entry_polygon.get())
            name = self.nome.get()
            already_used = False
            for objects in self.display_file:
                if objects.name == name:
                    already_used = True

            closed = False
            if name != '' and not already_used:
                if coordinates[0] == coordinates[-1]:
                    closed = True
                    answer = askyesno(title='Opção de preenchimento', message='Você deseja criar um objeto com cor preenchida?')
                    if answer:
                        color_mode = 2
                    else:
                        color_mode = 1
                else:
                    color_mode = 1
                objeto = Curve(name, coordinates, self.color, color_mode)
                objeto.drawn(self.viewport, self.coord_scn)
                self.closed = closed

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
                coords.append([aux_coords[i], aux_coords[i+1]])
            return coords
        else:
            self.erros['text'] = 'Entradas inválidas'
