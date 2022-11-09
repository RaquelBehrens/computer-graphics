from tkinter import *
from msilib.schema import Error

from constants import INCLUDE_WINDOW_WIDTH, INCLUDE_WINDOW_HEIGHT
from .include_window import IncludeWindow
from objects import (Surface3D)

class IncludeSurface3D(IncludeWindow):
    def __init__(self, viewport, erros, display_file, table, coord_scn):
        super().__init__(viewport, erros, display_file, table, coord_scn)
        self.main_window.title("Incluir Superfície 3D")
        self.main_window.geometry(f"{INCLUDE_WINDOW_WIDTH+100}x{INCLUDE_WINDOW_HEIGHT+200}")

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
        Label(self.frame1, text='Colocar sempre 16 vértices em 16,', font=("Times", "11")).grid(row=1, column=1, pady=(0,20))
        Label(self.frame1, text='e separar por ponto e vírgula de 4 em 4:', font=("Times", "11")).grid(row=2, column=1, pady=(0,20))
        Label(self.frame1, text='(x1,y1,z1), (x2,y2,z2), ..., (xn,yn,zn);', font=("Times", "11")).grid(row=3, column=1, pady=(0,20))
        Label(self.frame1, text='(x1,y1,z1), (x2,y2,z2), ..., (xn,yn,zn);', font=("Times", "11")).grid(row=4, column=1, pady=(0,20))
        Label(self.frame1, text='(x1,y1,z1), (x2,y2,z2), ..., (xn,yn,zn);', font=("Times", "11")).grid(row=5, column=1, pady=(0,20))
        Label(self.frame1, text='(x1,y1,z1), (x2,y2,z2), ..., (xn,yn,zn)', font=("Times", "11")).grid(row=6, column=1, pady=(0,20))

        self.color_button = Button(self.frame2, text='Escolher cor', font=('Times', '11'), command=self.choose_color, bg=self.color)
        self.color_button.grid(row=0, column=3, padx=10)
        
        self.radio_variable = IntVar()
        self.radio_variable.set(0)

        Radiobutton(self.frame3, text='Projeção Paralela', variable=self.radio_variable, value=1).grid(row=0, column=0, sticky=NW)
        Radiobutton(self.frame3, text='Projeção em Perspectiva', variable=self.radio_variable, value=2).grid(row=1, column=0, sticky=NW)

        self.cancelar = Button(self.frame4, font=("Times", "11"), text='Cancelar', command=self.close_window)
        self.cancelar.grid(row=0, column=0, pady=15, padx=18)
        self.confirmar = Button(self.frame4, font=("Times", "11"), text='Confirmar', command=self.create_object)
        self.confirmar.grid(row=0, column=1, pady=15, padx=18)

    def create_object(self):
        try:
            if self.radio_variable.get() != 0:
                points = self.convert_to_list(self.points.get())
                name = self.nome.get()
                already_used = False
                for objects in self.display_file:
                    if objects.name == name:
                        already_used = True

                if name != '' and not already_used:
                    objeto = Surface3D(name, points, self.color, projection=self.radio_variable.get())

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
            else:
                self.erros['text'] = 'Escolha uma projeção'

        except ValueError:
            self.erros['text'] = 'Entradas inválidas'

    def convert_to_list(self, coordinates):
        lista = coordinates
        coords = []

        aux = []
        aux_coords = []
        final_list = []
        for i in range(len(lista)):
            try:
                if lista[i] == ';' or i == len(lista)-1:
                    number = "".join(aux)
                    aux_coords.append(float(number))
                    aux.clear()

                    if len(aux_coords) % 3 == 0:
                        for j in range(0, len(aux_coords), 3):
                            final_list.append([aux_coords[j], aux_coords[j+1], aux_coords[j+2]]) 
                    else:
                        raise Error 

                    coords.append(final_list)  
                    
                    if len(final_list) % 4 != 0:
                        raise Error

                    aux_coords = []
                    final_list = []
                
                if lista[i] == ',' or i == len(lista)-1:
                    number = "".join(aux)
                    aux_coords.append(float(number))
                    aux.clear()
                float(lista[i])
                aux.append(lista[i])
            except ValueError:
                if lista[i] == '-':
                    aux.append(lista[i])

        if len(coords) % 4 == 0:
            return coords
        else:
            self.erros['text'] = 'Entradas inválidas'
