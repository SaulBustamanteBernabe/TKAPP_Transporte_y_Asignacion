import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class lblFrameControles(ttk.LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(side=ttk.TOP, fill=ttk.BOTH, padx=10, pady=(0, 10))

        # Variables de los widgets
        self.optionMethod: ttk.Combobox = None
        self.btnResolver:ttk.Button = None

        # Variables logicas
        self.options = ["Esquina Noroeste", "Voguel", "Costo Mínimo"]

        self.create_widgets()

    def create_widgets(self):
        self.optionMethod = ttk.Combobox(self, bootstyle=READONLY, state='readonly', values=self.options, width=24, font=("Cascadia", 11))
        self.optionMethod.current(0)
        self.optionMethod.pack(side=ttk.LEFT, padx=10, pady=(10, 15))
        self.btnResolver = ttk.Button(self, text="Resolver", bootstyle=PRIMARY)
        self.btnResolver.pack(side=ttk.RIGHT, padx=10, pady=(10, 15))
