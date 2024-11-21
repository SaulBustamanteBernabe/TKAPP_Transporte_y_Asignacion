import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class EntryTableApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self.parent = parent
        self.row_count = 5  # Número inicial de filas
        self.col_count = 5  # Número inicial de columnas
        self.table = []
        self.build_ui()

    def build_ui(self):
        # Crear el Canvas y Scrollbars
        container = ttk.Frame(self)
        container.pack(fill=BOTH, expand=TRUE)

        self.canvas = tk.Canvas(container)
        self.scroll_y = ttk.Scrollbar(container, orient=VERTICAL, command=self.canvas.yview)
        self.scroll_x = ttk.Scrollbar(container, orient=HORIZONTAL, command=self.canvas.xview)

        self.scroll_y.pack(side=RIGHT, fill=Y)
        self.scroll_x.pack(side=BOTTOM, fill=X)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        self.canvas.bind('<Configure>', self.on_canvas_resize)

        # Frame interno para los widgets
        self.table_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        # Botones para control
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=X, pady=10)

        add_row_btn = ttk.Button(control_frame, text="Añadir Fila", command=self.add_row, bootstyle=SUCCESS)
        add_row_btn.pack(side=LEFT, padx=5)

        add_col_btn = ttk.Button(control_frame, text="Añadir Columna", command=self.add_column, bootstyle=SUCCESS)
        add_col_btn.pack(side=LEFT, padx=5)

        # Crear la tabla inicial
        self.create_table()

    def create_table(self):
        """Crea la tabla inicial."""
        for r in range(self.row_count):
            row = []
            for c in range(self.col_count):
                entry = ttk.Entry(self.table_frame, width=10)
                entry.grid(row=r, column=c, padx=5, pady=5)
                row.append(entry)
            self.table.append(row)
        self.update_scrollregion()

    def add_row(self):
        """Añade una fila nueva."""
        row = []
        for c in range(self.col_count):
            entry = ttk.Entry(self.table_frame, width=10)
            entry.grid(row=self.row_count, column=c, padx=5, pady=5)
            row.append(entry)
        self.table.append(row)
        self.row_count += 1
        self.update_scrollregion()

    def add_column(self):
        """Añade una columna nueva."""
        for r in range(self.row_count):
            entry = ttk.Entry(self.table_frame, width=10)
            entry.grid(row=r, column=self.col_count, padx=5, pady=5)
            self.table[r].append(entry)
        self.col_count += 1
        self.update_scrollregion()

    def on_canvas_resize(self, event):
        """Actualiza la región desplazable cuando el canvas cambia de tamaño."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_scrollregion(self):
        """Actualiza la región desplazable para incluir todos los widgets."""
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    import tkinter as tk
    app = ttk.Window(themename="darkly")
    app.title("Tabla con Scrollbars")
    app.geometry("600x400")
    table_app = EntryTableApp(app)
    table_app.pack(fill=BOTH, expand=TRUE)
    app.mainloop()
