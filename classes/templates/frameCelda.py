import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class frameCelda(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        # Variables de los widgets
        self.entryCosto: ttk.Entry = None
        self.entryCantidad: ttk.Entry = None
        # Variables logicas
        self.costo = ttk.StringVar(value="0")
        self.cantidad = ttk.StringVar(value="0")
        # Metodos de inicialización
        self.create_widgets()


    def create_widgets(self):
        # Estructura de la aplicación
        self.entryCosto = ttk.Entry(self, textvariable=self.costo)
        self.entryCosto.pack(side=TOP, fill=BOTH, expand=True)
        self.entryCantidad = ttk.Entry(self, textvariable=self.cantidad, state=DISABLED)
        self.entryCantidad.pack(side=TOP, fill=BOTH, expand=True)
    
    def get_costo(self):
        try:
            return float(self.costo.get())
        except ValueError:
            raise ValueError("El valor introducido no es un número")
    
    def get_cantidad(self):
        try:
            return float(self.cantidad.get())
        except ValueError:
            raise ValueError("El valor introducido no es un número")
        
    def set_costo(self, value):
        self.costo.set(value)
    
    def set_cantidad(self, value):
        self.cantidad.set(value)