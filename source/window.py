from tkinter import *
from constants import WINDOW_HEIGHT, WINDOW_WIDTH, APPLICATION_NAME, VIEWPORT_WIDTH, VIEWPORT_HEIGHT
from include_object import IncludeWindow

class Window:
  def __init__(self):
    self.root = Tk()
    self.root.title('Sistema Básico CG - 2D')
    #root.iconbitmap()
    self.root.geometry(f"{WINDOW_HEIGHT}x{WINDOW_WIDTH}")
    
        self.frame1 = Frame(self.root)
        self.frame1.grid(row=0, column=0, sticky=NW)
        self.frame2 = Frame(self.root)
        self.frame2.grid(row=0, column=1, sticky=NW)

        Label(self.frame1, text='Menu de funções', font=('Time', '13')).grid(row=0, column=0, sticky=NW)
        
        Label(self.frame2, text='Viewport', font=('Time', '11')).grid(row=0, column=0, sticky=N)
        self.viewport = Canvas(self.frame2, width=VIEWPORT_WIDTH, height=VIEWPORT_HEIGHT, bg='grey')
        self.viewport.grid(row=1, column=0)
        self.erros = Label(self.frame2, width=60, height=2, bg='grey', font=('Time', '13'))
        self.erros.grid(row=2, column=0, sticky=N, padx=5)

        Label(self.frame1, text='Objetos',  font=('Times', '13')).grid(row=1, column=0, sticky=NW)
        self.objetos = Canvas(self.frame1, width=150, height=200, bg='white')
        self.objetos.grid(row=2, column=0, sticky=NW, padx=5)
        # caixa de texto, vai preenchendo conforme cria objetos

        Label(self.frame1, text='Window', font=('Times', '13')).grid(row=3, column=0, sticky=NW)
        self.up = Button(self.frame1, text='Up', font=('Times', '12'), command=self.move_up)
        self.up.grid(row=4, column=0, sticky=NW, padx=45)
        self.left = Button(self.frame1, text='Left', font=('Times', '12'), command=self.move_left)
        self.left.grid(row=5, column=0, sticky=NW, padx=20)
        self.right = Button(self.frame1, text='Right', font=('Times', '12'), command=self.move_right)
        self.right.grid(row=5, column=0, columnspan=2)
        self.down = Button(self.frame1, text='Down', font=('Times', '12'), command=self.move_down)
        self.down.grid(row=6, column=0, sticky=NW, padx=35)

        Label(self.frame1, text='Zoom: ', font=('Times', '13')).grid(row=7, column=0, sticky=NW)
        self.more_zoom = Button(self.frame1, text='+', font=('Times', '12'), command=self.zoom_in)
        self.more_zoom.grid(row=8, column=0, sticky=NW, padx=40)
        self.less_zoom = Button(self.frame1, text='-', font=('Times', '12'), command=self.zoom_out)
        self.less_zoom.grid(row=8, column=0, columnspan=2)
        self.set_window = Button(self.frame1, text='Include object', font=('Times', '12'), command=self.include_object)
        self.set_window.grid(row=9, column=0, sticky=NW, pady=15, padx=20)

    def include_object(self):
        IncludeWindow(self.viewport, self.erros)

    def zoom_in(self):
        self.viewport.scale("all", WINDOW_HEIGHT/2, WINDOW_WIDTH/2, 1.1, 1.1)
    
    def zoom_out(self):
        self.viewport.scale("all", WINDOW_HEIGHT/2, WINDOW_WIDTH/2, 0.9, 0.9)

    def move_up(self):
        self.viewport.move("all", 0, 10)

    def move_left(self):
        self.viewport.move("all", 10, 0)
    
    def move_right(self):
        self.viewport.move("all", -10, 0)

    def move_down(self):
        self.viewport.move("all", 0, -10)

window = Window()
window.root.mainloop()
