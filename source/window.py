from tkinter import *
from tkinter import ttk
from constants import WINDOW_HEIGHT, WINDOW_WIDTH, APPLICATION_NAME, VIEWPORT_WIDTH, VIEWPORT_HEIGHT
from include_object import IncludeWindow
from objects import Line, Wireframe


class Window(Frame):
    def __init__(self):
        self.root = Tk()
        self.root.title(APPLICATION_NAME)
        #self.root.iconbitmap()
        self.root.geometry(f"{WINDOW_HEIGHT}x{WINDOW_WIDTH}")
        Frame.__init__(self, self.root) # , bg="red")

        self.pack(fill='both', expand=True)

        self.display_file = []
        self.lines_list = []
        
        self.aplied_zoom = 1
        self.aplied_move = [0,0]

        self.create_widgets()
        self.create_table()

    def create_widgets(self):
        #labels
        self.frame1 = Frame(self)
        self.frame1.grid(row=0, column=0, sticky=NW)
        self.frame2 = Frame(self)
        self.frame2.grid(row=0, column=1, sticky=NW)

        Label(self.frame1, text='Menu de funções', font=('Time', '13')).grid(row=0, column=0, sticky=NW)

        Label(self.frame2, text='Viewport', font=('Time', '11')).grid(row=0, column=0, sticky=N)
        self.viewport = Canvas(self.frame2, width=VIEWPORT_WIDTH, height=VIEWPORT_HEIGHT, bg='grey')
        self.viewport.grid(row=1, column=0, pady=15)
        self.erros = Label(self.frame2, width=60, height=2, bg='grey', font=('Time', '13'))
        self.erros.grid(row=2, column=0, sticky=N, padx=5)  

        Label(self.frame1, text='Window:', font=('Time', '13')).grid(row=3, column=0, sticky=NW, pady=10)
        self.up = Button(self.frame1, text='Cima', font=('Time', '11'), command=self.move_up)
        self.up.grid(row=4, column=0, sticky=NW, padx=70, pady=3)
        self.left = Button(self.frame1, text='Esquerda', font=('Time', '11'), command=self.move_left)
        self.left.grid(row=5, column=0, sticky=NW, padx=20)
        self.right = Button(self.frame1, text='Direita', font=('Time', '11'), command=self.move_right)
        self.right.grid(row=5, column=0, columnspan=5, padx=100)
        self.down = Button(self.frame1, text='Baixo', font=('Time', '11'), command=self.move_down)
        self.down.grid(row=6, column=0, sticky=NW, padx=70, pady=3)

        Label(self.frame1, text='Zoom: ', font=('Time', '13')).grid(row=7, column=0, sticky=NW, pady=10)
        self.more_zoom = Button(self.frame1, text='  +  ', font=('Time', '11'), command=self.zoom_in)
        self.more_zoom.grid(row=8, column=0, sticky=NW, padx=40, pady=3)
        self.less_zoom = Button(self.frame1, text='  -  ', font=('Time', '11'), command=self.zoom_out)
        self.less_zoom.grid(row=8, column=0, columnspan=2, pady=3)
        
        Label(self, text='Objetos: ',  font=('Time', '13')).grid(row=1, column=0, sticky=NW)
        self.include = Button(self, text='Criar Objeto', font=('Time', '11'), command=self.include_object)
        self.include.grid(row=3, column=0, sticky=NW, padx=0, pady=5)
        self.delete = Button(self, text='Deletar Objeto', font=('Time', '11'), command=self.delete_object)
        self.delete.grid(row=3, column=1, sticky=NW, padx=0, pady=5)

        # scroll bar for the terminal outputs
        self.terminal_scrollbar = Scrollbar(self, orient=VERTICAL)
        self.terminal_scrollbar.grid(row=4, column=3, sticky=NS)

    def create_table(self):
        # terminal outputs
        self.table = ttk.Treeview(self)
        self.table.grid(row=4, column=0, columnspan=2, sticky=EW)
        self.table.configure(yscrollcommand=self.terminal_scrollbar.set)
        self.table["columns"] = ("1", "2", "3")
        self.table['show'] = 'headings'
        self.table.column("# 1", anchor=CENTER)
        self.table.heading("# 1", text="Nome")
        self.table.column("# 2", anchor=CENTER)
        self.table.heading("# 2", text="Pontos")
        self.table.column("# 3", anchor=CENTER)
        self.table.heading("# 3", text="Id")

        self.columnconfigure(2, weight=1) # column with treeview
        self.rowconfigure(2, weight=1) # row with treeview    
        
        #self.display_file = self.viewport.find_all()

    def include_object(self):
        IncludeWindow(self.viewport, self.erros, self.display_file, self.lines_list, self.table, self.aplied_move, self.aplied_zoom)

    def delete_object(self):
        selected_item = self.table.selection()[0]
        selected_item_id = self.table.item(selected_item).get('values')[2]

        for object in self.display_file:
            if object.getId() == selected_item_id:
                self.delete_object_from_table(selected_item)
                self.display_file.remove(object)
                if isinstance(object, Line):
                    self.lines_list.remove(object)
                    self.viewport.delete(selected_item_id)
                elif isinstance(object, Wireframe):
                    for id in object.list_ids:
                        self.viewport.delete(id)
                else:
                    self.viewport.delete(selected_item_id)

    def delete_object_from_table(self, id):
        self.table.delete(id)     

    def zoom_in(self):
        self.aplied_zoom *= 1.1
        self.viewport.scale("all", VIEWPORT_HEIGHT/2, VIEWPORT_WIDTH/2, 1.1, 1.1)
    
    def zoom_out(self):
        self.aplied_zoom *= 0.9
        self.viewport.scale("all", VIEWPORT_HEIGHT/2, VIEWPORT_WIDTH/2, 0.9, 0.9)

    def move_up(self):
        self.aplied_move[1] += 10
        self.viewport.move("all", 0, 10)

    def move_left(self):
        self.aplied_move[0] += 10
        self.viewport.move("all", 10, 0)
    
    def move_right(self):
        self.aplied_move[0] -= 10
        self.viewport.move("all", -10, 0)

    def move_down(self):
        self.aplied_move[1] -= 10
        self.viewport.move("all", 0, -10)

window = Window()
window.root.mainloop()
