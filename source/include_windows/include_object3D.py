from tkinter import *

from constants import INCLUDE_WINDOW_WIDTH, INCLUDE_WINDOW_HEIGHT
from .include_window import IncludeWindow
from objects import (Object3D)

class IncludeObject3D(IncludeWindow):
    def __init__(self, viewport, erros, display_file, table, coord_scn):
        super().__init__(viewport, erros, display_file, table, coord_scn)
        self.main_window.title("Incluir Objeto 3D")
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
        
        Label(self.frame0, text='Nome: ', font=("Times", "11"), height=2).grid(row=0, column=0, padx=(42,0), sticky=NW)
        self.nome = Entry(self.frame0, width=30, font=("Times", "11"))
        self.nome.grid(row=0, column=1, pady=(10,20))

        Label(self.frame1, text='Coordenadas: ', font=("Times", "11")).grid(row=0, column=0, sticky=NW)
        self.points = Entry(self.frame1, width=30, font=("Times", "11"))
        self.points.grid(row=0, column=1, sticky=NW)
        Label(self.frame1, text='(x1,y1), (x2,y2), ..., (xn,yn)', font=("Times", "11")).grid(row=1, column=1, pady=(0,20))

        Label(self.frame2, text='Vetores: ', font=("Times", "11")).grid(row=0, column=0, padx=(10,0), sticky=NW)
        self.vectors = Entry(self.frame2, width=40, font=("Times", "11"))
        self.vectors.grid(row=0, column=1, sticky=NW)
        Label(self.frame2, text='[(x1,y1), (x2,y2)], ..., [(xn-1, yn-1), (xn,yn)]', font=("Times", "11")).grid(row=1, column=1, pady=(0,20))

        self.color_button = Button(self.frame3, text='Escolher cor', font=('Times', '11'), command=self.choose_color, bg=self.color)
        self.color_button.grid(row=0, column=3, padx=10)

        self.cancelar = Button(self.frame4, font=("Times", "11"), text='Cancelar', command=self.close_window)
        self.cancelar.grid(row=0, column=0, pady=15, padx=18)
        self.confirmar = Button(self.frame4, font=("Times", "11"), text='Confirmar', command=self.create_object)
        self.confirmar.grid(row=0, column=1, pady=15, padx=18)

    def create_object(self):
        try:
            points = self.convert_to_list(self.points.get())
            vectors = self.convert_to_matrix(self.vectors.get())
            name = self.nome.get()
            already_used = False
            for objects in self.display_file:
                if objects.name == name:
                    already_used = True

            if name != '' and not already_used:
                objeto = Object3D(name, points, vectors, self.color)
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

    def convert_to_matrix(self, vectors):
        matrix = []
        aux = []

        for i in range(len(vectors)):
            try:
                if vectors[i] not in ['[', ']']:
                    aux.append(vectors[i])
                
                if vectors[i] == ']':
                    matrix.append(self.convert_to_list("".join(aux)))
                    aux = []
            except ValueError:
                pass
        
        is_valid = True
        for i in range(len(matrix)):
            if len(matrix[i]) != 2:
                is_valid = False
                break

        if is_valid:    
            return matrix
        else:
            self.erros['text'] = 'Entradas inválidas'
