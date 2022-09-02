from tkinter import *
from constants import INCLUDE_WINDOW_WIDTH, INCLUDE_WINDOW_HEIGHT 

class IncludeWindow:
    def __init__(self):
        self.main_window = Tk()
        self.main_window.title("Incluir objeto")
        self.main_window.geometry(f"{INCLUDE_WINDOW_HEIGHT}x{INCLUDE_WINDOW_WIDTH}")

        self.frame1 = Frame(self.main_window)
        self.frame1.pack()
        self.frame2 = Frame(self.main_window)
        self.frame2.pack()
        self.frame3 = Frame(self.main_window)
        self.frame3.pack()
        self.frame4 = Frame(self.main_window)
        self.frame4.pack()

        Label(self.frame1, text='Nome: ', font=("Times", "11"), height=2).pack(side=LEFT)
        self.nome = Entry(self.frame1, width=30, font=("Times", "11"))
        self.nome.focus_force()
        self.nome.pack(side=LEFT)

        Label(self.frame2, text='Coordenadas Iniciais', font=("Times", "11"), height=2).pack()
        Label(self.frame2, text='x1: ', font=("Times", "11")).pack(side=LEFT)
        self.x1 = Entry(self.frame2, width=3, font=("Times", "11")).pack(side=LEFT)
        Label(self.frame2, text=' y1: ', font=("Times", "11")).pack(side=LEFT)
        self.y1 = Entry(self.frame2, width=3, font=("Times", "11")).pack(side=LEFT)

        Label(self.frame3, text='Coordenadas Finais', font=("Times", "11"), height=2).pack()
        Label(self.frame3, text='x2: ', font=("Times", "11")).pack(side=LEFT)
        self.x2 = Entry(self.frame3, width=3, font=("Times", "11")).pack(side=LEFT)
        Label(self.frame3, text=' y2: ', font=("Times", "11")).pack(side=LEFT)
        self.y2 = Entry(self.frame3, width=3, font=("Times", "11")).pack(side=LEFT)

        Label(self.frame4, text='').pack()
        self.cancelar = Button(self.frame4, font=("Times", "11"), text='Cancelar', command=self.frame4.quit)
        self.cancelar.pack(side=LEFT)
        Label(self.frame4, text='     ').pack(side=LEFT)
        self.confirmar = Button(self.frame4, font=("Times", "11"), text='Confirmar')
        self.confirmar.pack(side=LEFT)


window = IncludeWindow()
window.main_window.mainloop()