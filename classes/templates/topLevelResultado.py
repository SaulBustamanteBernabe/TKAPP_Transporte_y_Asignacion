import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import numpy as np
from .lblFrameTabla import lblFrameTabla
from ..PD.Transporte import Transporte

class topLevelResultado(ttk.Toplevel):
    def __init__(self, parent: ttk.Window, resultados: Transporte, title: str="", option=None, **kwargs):
        super().__init__(parent, **kwargs)
        # Inicializa la ventana
        self.window_width = None
        self.window_height = None
        self.title(title)
        # Icono de la ventana
        self.iconbitmap("./assets/icons/Transporte_Logo_Icono_64x64.ico")
        # Variables de los widgets
        self.notebook: ttk.Notebook = None
        self.tablas: list[lblFrameTabla] = []
        self.frame_costo_total: ttk.Frame = None
        self.label_costo_total: ttk.Label = None
        # Variables logicas
        self.resultados: Transporte = resultados
        self.option = option
        # Metodos de inicialización
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.set_window( width=int(screen_width * 0.7), height=int(screen_height * 0.7), resizable=(True, True))
        self.create_widgets()

    def create_widgets(self):
        # Creo notebook para mostrar las tablas en pestañas
        self.notebook = ttk.Notebook(self, bootstyle=SUCCESS)
        # Bucle para crear las tablas
        for i in range(len(self.resultados.proceso_cantidad_solucion)):
            # Obtengo los datos del proceso de cada tabla
            if self.resultados.proceso_costo_solucion:
                costos = self.resultados.proceso_costo_solucion[i]
            else:
                costos = self.resultados.matriz_costos
            pcs = self.resultados.proceso_cantidad_solucion[i]
            pos = self.resultados.proceso_oferta_solucion[i]
            pds = self.resultados.proceso_demanda_solucion[i]
            # Crear tabla de solo lectura
            tabla = lblFrameTabla(self.notebook, rows=len(pos), columns=len(pds), text=f"Paso {i}", readonly=True)
            # Insertar datos en tabla
            tabla.set_costos(np.where(np.isinf(costos), "X", costos))
            tabla.set_solucion(pcs)
            tabla.set_ofertas(pos)
            tabla.set_demandas(pds)
            # Guardar tabla
            self.tablas.append(tabla)
            self.notebook.add(tabla, text=f"Proceso {i}")
        # Pestaña de Costo Total
        self.frame_costo_total = ttk.Frame(self.notebook)
        self.label_costo_total = ttk.Label(self.frame_costo_total, text=f"Costo Total = {self.resultados.costo_total}", style=DARK, font=("Rockwell", 48))
        self.label_costo_total.pack(side=ttk.TOP, expand=True)
        self.notebook.add(self.frame_costo_total, text="Costo Total", sticky=NSEW)
        # Mostrar resultados una vez que se carguen todas las tablas
        self.notebook.pack(side=ttk.TOP, fill=ttk.BOTH, expand=True)

    def set_window(self, width=None, height=None, resizable=(False, False)):
        # Obtiene el tamaño de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Si no se especifica el tamaño, se usa el 50% del tamaño de la pantalla
        if width is None:
            width = int(screen_width * 0.5)
        if height is None:
            height = int(screen_height * 0.5)

        self.window_width = width
        self.window_height = height

        # Calcula la posición centrada
        center_x = int(screen_width / 2 - self.window_width / 2)
        center_y = int(screen_height / 2 - self.window_height / 2)

        # Establece la geometría de la ventana
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        self.resizable(*resizable)
