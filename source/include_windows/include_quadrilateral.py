from tkinter import *

from constants import INCLUDE_WINDOW_WIDTH, INCLUDE_WINDOW_HEIGHT
from .include_window import IncludeWindow
from objects import (Wireframe)


class IncludeQuadrilateral(IncludeWindow):
    def __init__(self, viewport, erros, display_file, table, coord_scn):
        super().__init__(viewport, erros, display_file, table, coord_scn)
        self.main_window.title("Incluir Quadrilátero")
        self.main_window.geometry(f"{INCLUDE_WINDOW_WIDTH}x{INCLUDE_WINDOW_HEIGHT+170}")

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
        self.frame8 = Frame(self.main_window)
        self.frame8.grid()
        self.frame9 = Frame(self.main_window)
        self.frame9.grid()
        
        Label(self.frame0, text='Instruções:', font=("Times", "11"), height=0).grid(row=0, column=0, sticky=NW)
        Label(self.frame0, text='(x1, y1) = canto superior esquerdo;', font=("Times", "11"), height=0).grid(row=1, column=0, sticky=NW)
        Label(self.frame0, text='(x2, y2) = canto superior direito;', font=("Times", "11"), height=0).grid(row=2, column=0, sticky=NW)
        Label(self.frame0, text='(x3, y3) = canto inferior direito;', font=("Times", "11"), height=0).grid(row=3, column=0, sticky=NW)
        Label(self.frame0, text='(x4, y4) = canto inferior esquerdo.', font=("Times", "11"), height=0).grid(row=4, column=0, sticky=NW)

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

        Label(self.frame7, text='Defina a cor', font=("Times", "11")).grid(row=0, column=0, columnspan=2)
        
        self.radio_variable = IntVar()
        self.radio_variable.set(0)

        Radiobutton(self.frame7, text='Apenas a borda', variable=self.radio_variable, value=1).grid(row=1, column=0, stick=W)
        Radiobutton(self.frame7, text='Objeto preenchido', variable=self.radio_variable, value=2).grid(row=2, column=0, stick=W)
        
        self.color_button = Button(self.frame8, text='Escolher cor', font=('Times', '11'), command=self.choose_color, bg=self.color)
        self.color_button.grid(row=0, column=3, padx=10)

        self.cancelar = Button(self.frame9, font=("Times", "11"), text='Cancelar', command=self.close_window)
        self.cancelar.grid(row=0, column=0, pady=15, padx=18)
        self.confirmar = Button(self.frame9, font=("Times", "11"), text='Confirmar', command=self.create_object)
        self.confirmar.grid(row=0, column=1, pady=15, padx=18)
        
    def verify_quadrilateral(self, coordenate_1, coordenate_2, coordenate_3, coordenate_4):
        det_right_1 = coordenate_1[0] * coordenate_2[1] + coordenate_3[0] * coordenate_1[1] + coordenate_2[0] * coordenate_3[1]
        det_left_1 = coordenate_3[0] * coordenate_2[1] + coordenate_2[0] * coordenate_1[1] + coordenate_1[0] * coordenate_3[1]
        det_total_1 = det_right_1 - det_left_1

        det_right_2 = coordenate_1[0] * coordenate_3[1] + coordenate_4[0] * coordenate_1[1] + coordenate_3[0] * coordenate_4[1]
        det_left_2 = coordenate_4[0] * coordenate_3[1] + coordenate_3[0] * coordenate_1[1] + coordenate_1[0] * coordenate_4[1]
        det_total_2 = det_right_2 - det_left_2

        if det_total_1 != 0 and det_total_2 != 0:
            return True
        return False

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
            already_used = False
            for objects in self.display_file:
                if objects.name == name:
                    already_used = True
            if name != '' and not already_used:
                if (x1 == x2 and y1 == y2) or (x1 == x3 and y1 == y3) or (x1 == x4 and y1 == y4) or (x2 == x4 and y2 == y4) or (x3 == x4 and y3 == y4) or (x2 == x3 and y2 == y3):
                    self.erros['text'] = 'Os pontos coincidem'
                elif not self.verify_quadrilateral((x1,y1),(x2,y2),(x3,y3),(x4,y4)):
                    self.erros['text'] = 'Não formam um quadrilátero'
                else:
                    if self.radio_variable.get() != 0:
                        objeto = Wireframe(name, [[x1,y1], [x2,y2], [x3,y3], [x4,y4]], self.color, self.radio_variable.get())

                        self.coord_scn.generate_scn(objeto)

                        self.close_window()                
                        self.display_file.append(objeto)
                        self.include_object_in_table(objeto)
                        self.erros['text'] = 'Objeto criado com sucesso'
                    else:
                        self.erros['text'] = 'Selecione uma opção de preenchimento'
            else:
                if name == '':
                    self.erros['text'] = 'Digite um nome'
                else:
                    self.erros['text'] = 'Nome já utilizado'

        except ValueError:
            self.erros['text'] = 'Entradas inválidas'
