import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from .frameCelda import frameCelda


class lblFrameTabla(ttk.LabelFrame):
    def __init__(self, parent, rows = 3, columns = 3, readonly=False, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)
        # Variables de los widgets
        self.canvasTable: ttk.Canvas = None
        self.scroll_x: ttk.Scrollbar = None
        self.scroll_y: ttk.Scrollbar = None
        self.frameTable: ttk.Frame = None
        self.entryTable: list[list[frameCelda]] = []
        self.listaLabelOrigen: list[ttk.Label] = []
        self.listaLabelDestino: list[ttk.Label] = []
        self.listaEntryOrigen: list[ttk.Entry] = []
        self.listaEntryDestino: list[ttk.Entry] = []
        self.labelOrigenDestino: ttk.Label = None
        self.labelOferta: ttk.Label = None
        self.labelDemanda: ttk.Label = None

        self.frameControles: ttk.Frame = None
        self.button_add_row: ttk.Button = None
        self.button_remove_row: ttk.Button = None
        self.button_add_column: ttk.Button = None
        self.button_remove_column: ttk.Button = None
        # Variables logicas
        self.readonly: bool = readonly
        self.row_count: int = rows
        self.column_count: int = columns
        self.ofertas: list[ttk.StringVar] = []
        self.demandas: list[ttk.StringVar] = []
        # Metodos de inicialización
        self.create_widgets()


    def create_widgets(self):
        # Estructura de la aplicación
        if not self.readonly:
            self.frameControles = ttk.Frame(self)
            self.frameControles.pack(side=TOP, fill=X, ipadx=5, ipady=5)
            self.create_buttons()
        self.canvasTable = ttk.Canvas(self)
        self.scroll_x = ttk.Scrollbar(self, orient=HORIZONTAL, command=self.canvasTable.xview)
        self.scroll_y = ttk.Scrollbar(self, orient=VERTICAL, command=self.canvasTable.yview)
        self.scroll_x.pack(side=BOTTOM, fill=X)
        self.scroll_y.pack(side=RIGHT, fill=Y)
        self.canvasTable.pack(side=TOP, fill=BOTH, expand=TRUE)
        self.canvasTable.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        self.canvasTable.bind('<Configure>', self.on_canvas_resize)
        self.frameTable = ttk.Frame(self.canvasTable)
        self.canvasTable.create_window((0, 0), window=self.frameTable, anchor="nw")
        self.create_table()

    def set_readonly(self):
        self.frameControles.pack_forget()

    def set_costos(self, costos):
        for r in range(self.row_count):
            for c in range(self.column_count):
                self.entryTable[r][c].set_costo(costos[r][c])

    def set_solucion(self, catidades):
        for r in range(self.row_count):
            for c in range(self.column_count):
                self.entryTable[r][c].set_cantidad(catidades[r][c])
    
    def set_ofertas(self, ofertas):
        for r in range(self.row_count):
            self.ofertas[r].set(ofertas[r])
    
    def set_demandas(self, demandas):
        for r in range(self.column_count):
            self.demandas[r].set(demandas[r])
            
    def get_data(self):
        matriz_costos: list[list[float]] = []
        ofertas: list[float] = None
        demandas: list[float] = None
        try:
            for r in range(self.row_count):
                matriz_costos.append([])
                for c in range(self.column_count):
                    matriz_costos[r].append(self.entryTable[r][c].get_costo())
            ofertas = self.get_ofertas()
            demandas = self.get_demandas()
        except ValueError as e:
            return e
        return matriz_costos, ofertas, demandas

    def get_ofertas(self):
        ofertas: list[float] = []
        try:
            for o in self.ofertas:
                ofertas.append(float(o.get()))
        except ValueError:
            raise ValueError("El valor introducido no es un número")
        return ofertas

    def get_demandas(self):
        demandas: list[float] = []
        try:
            for d in self.demandas:
                demandas.append(float(d.get()))
        except ValueError:
            raise ValueError("El valor introducido no es un número")
        return demandas

    def create_buttons(self):
        self.add_row_btn = ttk.Button(self.frameControles, text="Añadir Fila", command=self.add_row, bootstyle=SUCCESS)
        self.add_row_btn.pack(side=LEFT, padx=8, ipadx=5, ipady=5)
        self.add_col_btn = ttk.Button(self.frameControles, text="Añadir Columna", command=self.add_column, bootstyle=SUCCESS)
        self.add_col_btn.pack(side=LEFT, padx=8, ipadx=5, ipady=5)
        self.remove_row_btn = ttk.Button(self.frameControles, text="Eliminar Fila", command=self.remove_row, bootstyle=DANGER)
        self.remove_row_btn.pack(side=LEFT, padx=8, ipadx=5, ipady=5)
        self.remove_col_btn = ttk.Button(self.frameControles, text="Eliminar Columna", command=self.remove_column, bootstyle=DANGER)
        self.remove_col_btn.pack(side=LEFT, padx=8, ipadx=5, ipady=5)

    def create_table(self):
        self.labelOrigenDestino = ttk.Label(self.frameTable, text="Origen/Destino", font=("Consolas", 10))
        self.labelOrigenDestino.grid(row=0, column=0, padx=5, pady=5)
        for r in range(self.row_count): # Crea las filas
            row = []
            for c in range(self.column_count): # Crea las columnas
                celda = frameCelda(self.frameTable)
                celda.grid(row=r+1, column=c+1, padx=5, pady=5)
                row.append(celda)
            self.entryTable.append(row)

        for r in range(self.row_count): # Crea Origen
            self.listaLabelOrigen.append(ttk.Label(self.frameTable, text=f"{r+1}", font=("Consolas", 14)))
            self.listaLabelOrigen[r].grid(row=r+1, column=0, padx=5, pady=5)
            self.ofertas.append(ttk.StringVar(value="0"))
            self.listaEntryOrigen.append(ttk.Entry(self.frameTable, textvariable=self.ofertas[r], font=("Consolas", 12), width=12, justify=RIGHT))
            self.listaEntryOrigen[r].grid(row=r+1, column=self.column_count+1, padx=5, pady=5)

        for c in range(self.column_count): # Crea Destino
            self.listaLabelDestino.append(ttk.Label(self.frameTable, text=f"{c+1}", font=("Consolas", 14)))
            self.listaLabelDestino[c].grid(row=0, column=c+1, padx=5, pady=5)
            self.demandas.append(ttk.StringVar(value="0"))
            self.listaEntryDestino.append(ttk.Entry(self.frameTable, textvariable=self.demandas[c], font=("Consolas", 12), width=12, justify=RIGHT))
            self.listaEntryDestino[c].grid(row=self.row_count+1, column=c+1, padx=5, pady=5)
        
        self.labelOferta = ttk.Label(self.frameTable, text="Oferta", font=("Consolas", 12))
        self.labelOferta.grid(row=0, column=self.column_count+1, padx=5, pady=5)
        self.labelDemanda = ttk.Label(self.frameTable, text="Demanda", font=("Consolas", 12))
        self.labelDemanda.grid(row=self.row_count+1, column=0, padx=5, pady=5)
        self.update_scrollregion()

    def add_row(self):
        # Olvida la poción de la fila Demanda
        self.forget_demanda()
        # Crea una fila nueva
        row = []
        for c in range(self.column_count):
            celda = frameCelda(self.frameTable)
            celda.grid(row=self.row_count+1, column=c+1, padx=5, pady=5)
            row.append(celda)
        self.entryTable.append(row)
        self.row_count += 1
        # Añade una nueva entrada de Oferta
        self.listaLabelOrigen.append(ttk.Label(self.frameTable, text=f"{self.row_count}", font=("Consolas", 14)))
        self.listaLabelOrigen[-1].grid(row=self.row_count, column=0, padx=5, pady=5)
        self.ofertas.append(ttk.StringVar(value="0"))
        self.listaEntryOrigen.append(ttk.Entry(self.frameTable, textvariable=self.ofertas[-1], font=("Consolas", 12), width=12, justify=RIGHT))
        self.listaEntryOrigen[-1].grid(row=self.row_count, column=self.column_count+1, padx=5, pady=5)
        # Añade la poción de la fila Demanda
        self.assign_demanda()
        self.update_scrollregion()

    def remove_row(self):
        # Elimina la última fila si hay mas de una
        if self.row_count > 1:
            # Olvida la poción de la fila Demanda
            self.forget_demanda()
            for entry in self.entryTable[-1]:
                entry.destroy()
            self.entryTable.pop()
            self.row_count -= 1
            # Elimina la ultima fila de Origen
            self.listaLabelOrigen[-1].destroy()
            self.listaEntryOrigen[-1].destroy()
            self.listaLabelOrigen.pop()
            self.listaEntryOrigen.pop()
            self.ofertas.pop()
            # Añade la poción de la fila Demanda
            self.assign_demanda()
            self.update_scrollregion()

    def add_column(self):
        # Olvida la poción de la columna Oferta
        self.forget_oferta()
        # Crea una columna nueva
        for r in range(self.row_count):
            self.entryTable[r].append(frameCelda(self.frameTable))
            self.entryTable[r][-1].grid(row=r+1, column=self.column_count+1, padx=5, pady=5)
        self.column_count += 1
        # Añade una nueva entrada de Demanda
        self.listaLabelDestino.append(ttk.Label(self.frameTable, text=f"{self.column_count}", font=("Consolas", 14)))
        self.listaLabelDestino[-1].grid(row=0, column=self.column_count, padx=5, pady=5)
        self.demandas.append(ttk.StringVar(value="0"))
        self.listaEntryDestino.append(ttk.Entry(self.frameTable, textvariable=self.demandas[-1], font=("Consolas", 12), width=12, justify=RIGHT))
        self.listaEntryDestino[-1].grid(row=self.row_count+1, column=self.column_count, padx=5, pady=5)
        # Añade la poción de la columna Oferta
        self.assign_oferta()
        self.update_scrollregion()

    def remove_column(self):
        # Elimina la última columna si hay mas de una
        if self.column_count > 1:
            # Olvida la poción de la columna Oferta
            self.forget_oferta()
            for r in range(self.row_count): # Crea las filas
                self.entryTable[r][-1].destroy()
                self.entryTable[r].pop()
            self.column_count -= 1
            # Elimina la ultima columna de Destino
            self.listaLabelDestino[-1].destroy()
            self.listaEntryDestino[-1].destroy()
            self.listaLabelDestino.pop()
            self.listaEntryDestino.pop()
            self.demandas.pop()
            # Añade la poción de la columna Oferta
            self.assign_oferta()
            self.update_scrollregion()

    def forget_demanda(self):
        # Olvida la ultima fila de Destino
        self.labelDemanda.grid_forget()
        for entry in self.listaEntryDestino:
            entry.grid_forget()
    
    def assign_demanda(self):
        # Asigna la ultima fila a Destino
        self.labelDemanda.grid(row=self.row_count+1, column=0, padx=5, pady=5)
        for c in range(self.column_count):
            self.listaEntryDestino[c].grid(row=self.row_count+1, column=c+1, padx=5, pady=5)

    def forget_oferta(self):
        # Olvida la ultima columna de Oferta
        self.labelOferta.grid_forget()
        for entry in self.listaEntryOrigen:
            entry.grid_forget()
    
    def assign_oferta(self):
        # Asigna la ultima columna a Oferta
        self.labelOferta.grid(row=0, column=self.column_count+1, padx=5, pady=5)
        for r in range(self.row_count):
            self.listaEntryOrigen[r].grid(row=r+1, column=self.column_count+1, padx=5, pady=5)

    def on_canvas_resize(self, event):
        """Actualiza la región desplazable cuando el canvas cambia de tamaño."""
        self.canvasTable.configure(scrollregion=self.canvasTable.bbox("all"))

    def update_scrollregion(self):
        """Actualiza la región desplazable para incluir todos los widgets."""
        self.canvasTable.update_idletasks()
        self.canvasTable.configure(scrollregion=self.canvasTable.bbox("all"))