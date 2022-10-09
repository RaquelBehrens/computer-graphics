from tkinter import *
from tkinter import colorchooser
from abc import ABC, abstractmethod
from constants import INCLUDE_WINDOW_WIDTH, INCLUDE_WINDOW_HEIGHT

class IncludeWindow(ABC):
    @abstractmethod
    def __init__(self, viewport, erros, display_file, table, coord_scn):
        self.main_window = Toplevel()
        self.main_window.title("Incluir objeto")
        self.main_window.geometry(f"{INCLUDE_WINDOW_WIDTH}x{INCLUDE_WINDOW_HEIGHT}")
        self.viewport = viewport
        self.erros = erros
        self.display_file = display_file
        self.table = table
        self.coord_scn = coord_scn
        self.color = "#FFFFFF"

    @abstractmethod
    def create_object(self):
        pass

    def include_object_in_table(self, object):
        self.table.insert('', 0, values=(object.get_name(), object.get_points(), object.get_id()))

    def close_window(self):
        self.main_window.destroy()

    def choose_color(self):
        color_code = colorchooser.askcolor(title ="Escolha a cor")
        self.color = color_code[1]
        self.color_button.configure(bg=self.color)
