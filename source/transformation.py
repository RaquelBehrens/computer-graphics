from msilib.schema import Error
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from objects import (Object3D, Point3D, ParametricSurface3D, FdSurface3D)


class Transformation():
    def __init__(self, viewport, main_table, object_id, object, coord_scn):
        self.main_window = Toplevel()
        self.main_window.title("Transformações")
        self.transformations = [] #(tranformacao, valor)
                                  #valor quando em torno de algum ponto = [x, y, angulo], senao = angulo
        self.coord_scn = coord_scn
        self.viewport = viewport
        self.main_table = main_table
        self.object_id = object_id
        self.object = object
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

        if isinstance(self.object, Object3D) or isinstance(self.object, Point3D) or isinstance(self.object, ParametricSurface3D) or isinstance(object, FdSurface3D):
            self.around_axis_radio = IntVar()
            self.around_axis_radio.set(0)

            Radiobutton(self.frame1, text='Referência eixo x', variable=self.around_axis_radio, value=1).grid(row=3, column=0, stick=W)
            Radiobutton(self.frame1, text='Referência eixo y', variable=self.around_axis_radio, value=2).grid(row=4, column=0, stick=W)
            Radiobutton(self.frame1, text='Referência eixo z', variable=self.around_axis_radio, value=3).grid(row=5, column=0, stick=W)


        self.create_table()

        self.frame3 = Frame(self.main_window)
        self.frame3.grid()

        self.cancelar = Button(self.frame3, font=("Times", "11"), text='Fechar', command=self.close_window)
        self.cancelar.grid(row=0, column=0, pady=10, padx=18)
        self.remover = Button(self.frame3, font=("Times", "11"), text='Remover', command=self.remove_transformation)
        self.remover.grid(row=0, column=1, pady=10, padx=18)
        self.adicionar = Button(self.frame3, font=("Times", "11"), text='Adicionar', command=self.add_transformation)
        self.adicionar.grid(row=0, column=2, pady=10, padx=18)
        self.confirmar = Button(self.frame3, font=("Times", "11"), text='Aplicar', command=self.apply_changes)
        self.confirmar.grid(row=0, column=3, pady=10, padx=18)

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

        if isinstance(self.object, Point3D) or isinstance(self.object, Object3D) or isinstance(self.object, ParametricSurface3D) or isinstance(object, FdSurface3D):
            Label(self.frame_trans2, text=' z: ', font=("Times", "11"), height=2).grid(row=1, column=4, sticky=NW)
            self.vetor_z_translation = Entry(self.frame_trans2, width=3, font=("Times", "11"))
            self.vetor_z_translation.grid(row=1, column=5)

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

        if isinstance(self.object, Object3D) or isinstance(self.object, Point3D) or isinstance(self.object, ParametricSurface3D) or isinstance(object, FdSurface3D):
            Label(self.frame_esc2, text=' z: ', font=("Times", "11"), height=2).grid(row=1, column=4, sticky=NW)
            self.vetor_z_escalation = Entry(self.frame_esc2, width=3, font=("Times", "11"))
            self.vetor_z_escalation.grid(row=1, column=5)

    def tab_rotation(self):
        self.frame_rot = Frame(self.tab3)
        self.frame_rot.grid()
        self.frame_rot2 = Frame(self.tab3)
        self.frame_rot2.grid()
        self.frame_rot3 = Frame(self.tab3)
        self.frame_rot3.grid()

        self.radio_variable = IntVar()
        self.radio_variable.set(0)

        Radiobutton(self.frame_rot, text='Centro do mundo', variable=self.radio_variable, value=1).grid(row=0, column=0, stick=W)
        Radiobutton(self.frame_rot, text='Centro do objeto', variable=self.radio_variable, value=2).grid(row=1, column=0, stick=W)
        Radiobutton(self.frame_rot, text='Ponto qualquer', variable=self.radio_variable, value=3).grid(row=2, column=0, stick=W)

        Label(self.frame_rot, text='x: ', font=("Times", "10")).grid(row=2, column=1, stick=SE)
        self.rotation_x = Entry(self.frame_rot, width=3, font=("Times", "10"))
        self.rotation_x.grid(row=2, column=2, stick=SE)
        Label(self.frame_rot, text='y: ', font=("Times", "10")).grid(row=2, column=3, stick=SE)
        self.rotation_y = Entry(self.frame_rot, width=3, font=("Times", "10"))
        self.rotation_y.grid(row=2, column=4, stick=SE)

        if isinstance(self.object, Object3D) or isinstance(self.object, Point3D):
            Label(self.frame_rot, text='z: ', font=("Times", "10")).grid(row=2, column=5, stick=SE)
            self.rotation_z = Entry(self.frame_rot, width=3, font=("Times", "10"))
            self.rotation_z.grid(row=2, column=6, stick=SE)

        if isinstance(self.object, Object3D) or isinstance(self.object, ParametricSurface3D):
            Radiobutton(self.frame_rot, text='Eixo', variable=self.radio_variable, value=4).grid(row=3, column=0, stick=W)
            self.axis = Entry(self.frame_rot, width=10, font=("Times", "11"))
            self.axis.grid(row=3, column=0, sticky=NW, pady=0, padx=(50,0))
            Label(self.frame_rot, text='(x1,y1,z1), (x2,y2,z2)', font=("Times", "9")).grid(row=4, column=0, pady=0, padx=(50,0))
    
        Label(self.frame_rot2, text='Ângulo: ', font=("Times", "11")).grid(row=0, column=0, pady=(20,0))
        self.angle = Entry(self.frame_rot2, width=3, font=("Times", "11"))
        self.angle.grid(row=0, column=1, pady=(20,0))
        Label(self.frame_rot2, text='°', font=("Times", "11")).grid(row=0, column=2, pady=(20,0))

    def create_table(self):
        self.frame2 = Frame(self.main_window)
        self.frame2.grid(padx=5, pady=5)

        self.terminal_scrollbar = Scrollbar(self.frame2, orient=VERTICAL)
        self.terminal_scrollbar.grid(row=0, column=3, sticky=NS)

        self.table = ttk.Treeview(self.frame2)
        self.table.grid(row=0, column=0, sticky=EW)
        self.table.configure(yscrollcommand=self.terminal_scrollbar.set)
        self.table["columns"] = ("1", "2", "3")
        self.table['show'] = 'headings'
        self.table.column("# 1", anchor=CENTER)
        self.table.heading("# 1", text="Id da Transformação")
        self.table.column("# 2", anchor=CENTER)
        self.table.heading("# 2", text="Transformação")
        self.table.column("# 3", anchor=CENTER)
        self.table.heading("# 3", text="Valores")  

    def close_window(self):
        self.main_window.destroy()

    def apply_changes(self):
        all_items = self.table.get_children()
        for item in all_items:
            id, _, values = self.table.item(item).get('values')
            
            if id == 1:
                self.object.translate(self.viewport, values, self.coord_scn)
            elif id == 2:
                self.object.scale(self.viewport, values, self.coord_scn)
            elif id == 3:
                self.object.rotate_around_world(self.viewport, values, self.coord_scn)
            elif id == 4:
                self.object.rotate_around_object(self.viewport, values, self.coord_scn)
            elif id == 5:
                self.object.rotate_around_point(self.viewport, values, self.coord_scn)
            elif id == 6:
                self.object.rotate_around_axis(self.viewport, values, self.coord_scn)
            
            self.coord_scn.generate_scn(self.object)

            #alterar objeto na tabela principal
            self.main_table.item(self.object_id,
                                 values=(self.object.get_name(), self.object.get_points(), 
                                         self.object.get_id()))
            self.delete_object_from_table(item)

    def add_transformation(self):
        try:
                if isinstance(self.object, Object3D) or isinstance(self.object, Point3D) or isinstance(self.object, ParametricSurface3D) or isinstance(object, FdSurface3D):
                    around_axis_radio = self.around_axis_radio.get()

                    if around_axis_radio == 0:
                        messagebox.showerror('Erro', 'Selecione um eixo de referência')
                        raise Error
                    elif around_axis_radio == 1:
                        around_axis = 'x'
                    elif around_axis_radio == 2:
                        around_axis = 'y'
                    elif around_axis_radio == 3:
                        around_axis = 'z'
                    else:
                        around_axis = ''
                    
                    if self.tab_control.tab(self.tab_control.select(), "text") == 'Translação':
                        vetor_x = float(self.vetor_x_translation.get())
                        vetor_y = float(self.vetor_y_translation.get())
                        vetor_z = float(self.vetor_z_translation.get())
                        self.table.insert('', 0, values=(1, 'Translação', (vetor_x, vetor_y, vetor_z, ',', 'eixo:', around_axis)))
                    elif self.tab_control.tab(self.tab_control.select(), "text") == 'Escalonamento':
                        vetor_x = float(self.vetor_x_escalation.get())
                        vetor_y = float(self.vetor_y_escalation.get())
                        vetor_z = float(self.vetor_z_escalation.get())
                        self.table.insert('', 0, values=(2, 'Escalonamento', (vetor_x, vetor_y, vetor_z, ',', 'eixo:', around_axis)))
                    elif self.tab_control.tab(self.tab_control.select(), "text") == 'Rotação':
                        angle = float(self.angle.get())                        
                        if self.radio_variable.get() == 1:
                            self.table.insert('', 0, values=(3, 'Rotação em torno do mundo', (angle, '°,eixo:', around_axis)))
                        elif self.radio_variable.get() == 2:
                            self.table.insert('', 0, values=(4, 'Rotação em torno do objeto', (angle, '°,eixo:', around_axis)))
                        elif self.radio_variable.get() == 3:
                            rotation_x = float(self.rotation_x.get())
                            rotation_y = float(self.rotation_y.get())
                            rotation_z = float(self.rotation_z.get())
                            self.table.insert('', 0, values=(5, 'Rotação em torno do ponto', ('x:', rotation_x, ',', 'y:', rotation_y, ',', 'z:', rotation_z, ',', angle, '°,eixo:', around_axis)))
                        elif self.radio_variable.get() == 4:
                            if isinstance(self.object, Object3D) == False or isinstance(self.object, ParametricSurface3D) == False or isinstance(object, FdSurface3D) == False:
                                raise Error
                            else:
                                axis = self.convert_to_list(self.axis.get())
                                self.table.insert('', 0, values=(6, 'Rotação em torno do eixo', ('x1:', axis[0][0], ',y1:', axis[0][1], ',z1', axis[0][2], ',x2:', axis[1][0], ',y2:', axis[1][1], ',z2:', axis[1][2], ',angle:', angle, '°')))
                else:
                    if self.tab_control.tab(self.tab_control.select(), "text") == 'Translação':
                        vetor_x = float(self.vetor_x_translation.get())
                        vetor_y = float(self.vetor_y_translation.get())
                        self.table.insert('', 0, values=(1, 'Translação', (vetor_x, vetor_y)))
                    elif self.tab_control.tab(self.tab_control.select(), "text") == 'Escalonamento':
                        vetor_x = float(self.vetor_x_escalation.get())
                        vetor_y = float(self.vetor_y_escalation.get())
                        self.table.insert('', 0, values=(2, 'Escalonamento', (vetor_x, vetor_y)))
                    elif self.tab_control.tab(self.tab_control.select(), "text") == 'Rotação':
                        angle = float(self.angle.get())
                        if self.radio_variable.get() == 1:
                            self.table.insert('', 0, values=(3, 'Rotação em torno do mundo', (angle)))
                        elif self.radio_variable.get() == 2:
                            self.table.insert('', 0, values=(4, 'Rotação em torno do objeto', (angle)))
                        elif self.radio_variable.get() == 3:
                            rotation_x = float(self.rotation_x.get())
                            rotation_y = float(self.rotation_y.get())
                            self.table.insert('', 0, values=(5, 'Rotação em torno do ponto', ('x:', rotation_x, ',', 'y:', rotation_y, ',', angle, '°')))
                        elif self.radio_variable.get() == 4:
                            raise Error

        except ValueError:
            messagebox.showerror('Erro', 'Entradas inválidas')
            
    def remove_transformation(self):
        try:
            selected_item = self.table.selection()[0]
            self.table.delete(selected_item)
        except IndexError:
            messagebox.showerror('Erro', 'Selecione um item para remover')

    def delete_object_from_table(self, id):
        self.table.delete(id)

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
  
        for i in range(0, len(aux_coords), 3):
            coords.append([aux_coords[i], aux_coords[i+1], aux_coords[i+2]])
        return coords

