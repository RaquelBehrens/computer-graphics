from tkinter import *
from tkinter import ttk

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
        self.remover = Button(self.frame3, font=("Times", "11"), text='Remover')
        self.remover.grid(row=0, column=1, pady=10, padx=18)
        self.adicionar = Button(self.frame3, font=("Times", "11"), text='Adicionar')
        self.adicionar.grid(row=0, column=2, pady=10, padx=18)
        self.confirmar = Button(self.frame3, font=("Times", "11"), text='Aplicar')
        self.confirmar.grid(row=0, column=3, pady=10, padx=18)

    def tab_translation(self):
        self.frame_trans = Frame(self.tab1)
        self.frame_trans.grid()
        self.frame_trans2 = Frame(self.tab1)
        self.frame_trans2.grid()

        Label(self.frame_trans, text='Vetor de translação', font=("Times", "11")).grid(row=0, column=0, padx=58)

        Label(self.frame_trans2, text='x: ', font=("Times", "11"), height=2).grid(row=1, column=0, sticky=NW)
        self.vetor_x = Entry(self.frame_trans2, width=3, font=("Times", "11"))
        self.vetor_x.grid(row=1, column=1)
        Label(self.frame_trans2, text=' y: ', font=("Times", "11"), height=2).grid(row=1, column=2, sticky=NW)
        self.vetor_y = Entry(self.frame_trans2, width=3, font=("Times", "11"))
        self.vetor_y.grid(row=1, column=3)

    def tab_escalation(self):
        self.frame_esc = Frame(self.tab2)
        self.frame_esc.grid()
        self.frame_esc2 = Frame(self.tab2)
        self.frame_esc2.grid()

        Label(self.frame_esc, text='Vetor de escalonamento', font=("Times", "11")).grid(row=0, column=0, padx=40)

        Label(self.frame_esc2, text='x: ', font=("Times", "11"), height=2).grid(row=1, column=0, sticky=NW)
        self.vetor_x = Entry(self.frame_esc2, width=3, font=("Times", "11"))
        self.vetor_x.grid(row=1, column=1)
        Label(self.frame_esc2, text=' y: ', font=("Times", "11"), height=2).grid(row=1, column=2, sticky=NW)
        self.vetor_y = Entry(self.frame_esc2, width=3, font=("Times", "11"))
        self.vetor_y.grid(row=1, column=3)

    def tab_rotation(self):
        self.frame_rot = Frame(self.tab3)
        self.frame_rot.grid()
        self.frame_rot2 = Frame(self.tab3)
        self.frame_rot2.grid()

        self.radio_variable = IntVar()
        self.radio_variable.set(0)

        self.seila1 = Radiobutton(self.frame_rot, text='Centro do mundo', variable=self.radio_variable, value=1).grid(stick=W)
        self.seila2 = Radiobutton(self.frame_rot, text='Centro do objeto', variable=self.radio_variable, value=2).grid(stick=W)
        self.seila3 = Radiobutton(self.frame_rot, text='Ponto qualquer', variable=self.radio_variable, value=3).grid(stick=W)

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
