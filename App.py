import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from classes.templates.lblFrameTabla import lblFrameTabla


class App(ttk.Window):
    def __init__(self):
        super().__init__()
        # Establece las propiedades de la aplicación
        self.window_width: int = None
        self.window_height: int = None
        # Estilo de la app
        self.styleApp = ttk.Style()
        self.iconbitmap("./assets/icons/Transporte_Logo_Icono_64x64.ico")
        self.styleApp.theme_use("litera")
        self.set_styles()
        # Variables de los widgets
        self.tabla: lblFrameTabla = None
        # Metodos de inicialización y configuración de la aplicación
        self.title("Transporte y Asignación")
        self.set_window(resizable=(True, True))
        self.create_widgets()


    def create_widgets(self):
        # Estructura de la aplicación
        self.tabla = lblFrameTabla(self, text="Tabla de Transporte")
    

    def set_window(self, width=None, height=None, resizable=(False, False)):
        # Obtiene el tamaño de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Si no se especifica el tamaño, se usa el 70% del tamaño de la pantalla
        if width is None:
            width = int(screen_width * 0.7)
        if height is None:
            height = int(screen_height * 0.7)

        self.window_width = width
        self.window_height = height

        # Calcula la posición centrada
        center_x = int(screen_width / 2 - self.window_width / 2)
        center_y = int(screen_height / 2 - self.window_height / 2)

        # Establece la geometría de la ventana
        self.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        self.resizable(*resizable)

    def set_styles(self):
        pass


if __name__ == '__main__':
    app = App()
    app.mainloop()
