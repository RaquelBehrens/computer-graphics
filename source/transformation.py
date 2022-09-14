from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from math import degrees

class Transformation():
    def __init__(self):
        self.main_window = Toplevel()
        self.main_window.title("Transformações")

        self.create_widgets()

    def create_widgets(self):
        self.frame1 = Frame(self.main_window)
        self.frame1.grid()

        Label(self.frame1, text='Transformações', font=("Times", "12"), height=2).grid(row=0, column=0, sticky=NW)

        self.tab_control = ttk.Notebook(self.main_window)
        self.tab1 = Frame(self.tab_control)
        self.tab2 = Frame(self.tab_control)
        self.tab3 = Frame(self.tab_control)

        self.tab_control.add(self.tab1, text='Translação')
        self.tab_control.add(self.tab2, text='Escalonamento')
        self.tab_control.add(self.tab3, text='Rotação')
        self.tab_control.grid()

        self.tab_translation()
        self.tab_escalation()
        self.tab_rotation()

        self.create_table()

        self.frame3 = Frame(self.main_window)
        self.frame3.grid()

        self.cancelar = Button(self.frame3, font=("Times", "11"), text='Cancelar', command=self.close_window)
        self.cancelar.grid(row=0, column=0, pady=10, padx=18)
        self.remover = Button(self.frame3, font=("Times", "11"), text='Remover', command=self.remove_transformation)
        self.remover.grid(row=0, column=1, pady=10, padx=18)
        self.adicionar = Button(self.frame3, font=("Times", "11"), text='Adicionar', command=self.add_transformation)
        self.adicionar.grid(row=0, column=2, pady=10, padx=18)
        self.confirmar = Button(self.frame3, font=("Times", "11"), text='Aplicar', command=self.apply_changes)
        self.confirmar.grid(row=0, column=3, pady=10, padx=18)

        self.transformations = [] #(tranformacao, valor)
                                  #valor quando em torno de algum ponto = [x, y, angulo], senao = angulo

    def tab_translation(self):
        self.frame_trans = Frame(self.tab1)
        self.frame_trans.grid()
        self.frame_trans2 = Frame(self.tab1)
        self.frame_trans2.grid()

        Label(self.frame_trans, text='Vetor de translação', font=("Times", "11")).grid(row=0, column=0, padx=58)

        Label(self.frame_trans2, text='x: ', font=("Times", "11"), height=2).grid(row=1, column=0, sticky=NW)
        self.vetor_x_translation = Entry(self.frame_trans2, width=3, font=("Times", "11"))
        self.vetor_x_translation.grid(row=1, column=1)
        Label(self.frame_trans2, text=' y: ', font=("Times", "11"), height=2).grid(row=1, column=2, sticky=NW)
        self.vetor_y_translation = Entry(self.frame_trans2, width=3, font=("Times", "11"))
        self.vetor_y_translation.grid(row=1, column=3)

    def tab_escalation(self):
        self.frame_esc = Frame(self.tab2)
        self.frame_esc.grid()
        self.frame_esc2 = Frame(self.tab2)
        self.frame_esc2.grid()

        Label(self.frame_esc, text='Vetor de escalonamento', font=("Times", "11")).grid(row=0, column=0, padx=40)

        Label(self.frame_esc2, text='x: ', font=("Times", "11"), height=2).grid(row=1, column=0, sticky=NW)
        self.vetor_x_escalation = Entry(self.frame_esc2, width=3, font=("Times", "11"))
        self.vetor_x_escalation.grid(row=1, column=1)
        Label(self.frame_esc2, text=' y: ', font=("Times", "11"), height=2).grid(row=1, column=2, sticky=NW)
        self.vetor_y_escalation = Entry(self.frame_esc2, width=3, font=("Times", "11"))
        self.vetor_y_escalation.grid(row=1, column=3)

    def tab_rotation(self):
        self.frame_rot = Frame(self.tab3)
        self.frame_rot.grid()
        self.frame_rot2 = Frame(self.tab3)
        self.frame_rot2.grid()

        self.radio_variable = IntVar()
        self.radio_variable.set(0)

        self.seila1 = Radiobutton(self.frame_rot, text='Centro do mundo', variable=self.radio_variable, value=1).grid(row=0, column=0, stick=W)
        self.seila2 = Radiobutton(self.frame_rot, text='Centro do objeto', variable=self.radio_variable, value=2).grid(row=1, column=0, stick=W)
        self.seila3 = Radiobutton(self.frame_rot, text='Ponto qualquer', variable=self.radio_variable, value=3).grid(row=2, column=0, stick=W)

        Label(self.frame_rot, text='x: ', font=("Times", "10")).grid(row=2, column=1, stick=SE)
        self.rotation_x = Entry(self.frame_rot, width=3, font=("Times", "10"))
        self.rotation_x.grid(row=2, column=2, stick=SE)
        Label(self.frame_rot, text='y: ', font=("Times", "10")).grid(row=2, column=3, stick=SE)
        self.rotation_y = Entry(self.frame_rot, width=3, font=("Times", "10"))
        self.rotation_y.grid(row=2, column=4, stick=SE)
 
        Label(self.frame_rot2, text='Ângulo: ', font=("Times", "11")).grid(row=0, column=0)
        self.angle = Entry(self.frame_rot2, width=3, font=("Times", "11"))
        self.angle.grid(row=0, column=1)
        Label(self.frame_rot2, text='°', font=("Times", "11")).grid(row=0, column=2)

    def create_table(self):
        self.frame2 = Frame(self.main_window)
        self.frame2.grid(padx=5, pady=5)

        self.terminal_scrollbar = Scrollbar(self.frame2, orient=VERTICAL)
        self.terminal_scrollbar.grid(row=0, column=3, sticky=NS)

        self.table = ttk.Treeview(self.frame2)
        self.table.grid(row=0, column=0, sticky=EW)
        self.table.configure(yscrollcommand=self.terminal_scrollbar.set)
        self.table["columns"] = ("1", "2")
        self.table['show'] = 'headings'
        self.table.column("# 1", anchor=CENTER)
        self.table.heading("# 1", text="Transformação")
        self.table.column("# 2", anchor=CENTER)
        self.table.heading("# 2", text="Valores")  

    def close_window(self):
        self.main_window.destroy()

    def apply_changes(self):
        self.main_window.destroy()

    def add_transformation(self):
        try:
            if self.tab_control.tab(self.tab_control.select(), "text") == 'Translação':
                vetor_x = float(self.vetor_x_translation.get())
                vetor_y = float(self.vetor_y_translation.get())
                self.table.insert('', 0, values=('Translação', (vetor_x, vetor_y)))
            elif self.tab_control.tab(self.tab_control.select(), "text") == 'Escalonamento':
                vetor_x = float(self.vetor_x_escalation.get())
                vetor_y = float(self.vetor_y_escalation.get())
                self.table.insert('', 0, values=('Escalonamento', (vetor_x, vetor_y)))
            elif self.tab_control.tab(self.tab_control.select(), "text") == 'Rotação':
                angle = float(self.angle.get())
                if self.radio_variable.get() == 1:
                    self.table.insert('', 0, values=('Rotação em torno do mundo', angle))
                elif self.radio_variable.get() == 2:
                    self.table.insert('', 0, values=('Rotação em torno do objeto', angle))
                elif self.radio_variable.get() == 3:
                    rotation_x = float(self.rotation_x.get())
                    rotation_y = float(self.rotation_y.get())
                    self.table.insert('', 0, values=('Rotação em torno do ponto', ('x:', rotation_x, ',', 'y:', rotation_y, ',', angle, '°')))
        except ValueError:
            messagebox.showerror('Erro', 'Entradas inválidas')
            
    def remove_transformation(self):
        try:
            selected_item = self.table.selection()[0]
            self.table.delete(selected_item)
        except IndexError:
            messagebox.showerror('Erro', 'Selecione um item para remover')