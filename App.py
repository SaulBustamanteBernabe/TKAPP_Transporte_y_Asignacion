import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialogs import Messagebox
from classes.templates.lblFrameTabla import lblFrameTabla
from classes.templates.lblFrameControles import lblFrameControles
from classes.PD.Transporte import Transporte

class App(ttk.Window):
    def __init__(self):
        super().__init__()
        # Establece las propiedades de la aplicación
        self.window_width: int = None
        self.window_height: int = None
        # Estilo de la app
        self.styleApp = ttk.Style()
        self.iconbitmap("./assets/icons/Transporte_Logo_Icono_64x64.ico")
        self.styleApp.theme_use("cerculean")
        self.set_styles()
        # Variables de los widgets
        self.tabla: lblFrameTabla = None
        self.controles: lblFrameControles = None
        # Metodos de inicialización y configuración de la aplicación
        self.title("Transporte y Asignación")
        self.set_window(resizable=(True, True))
        self.create_widgets()


    def create_widgets(self):
        # Estructura de la aplicación
        self.tabla = lblFrameTabla(self, text="Tabla de Transporte")
        self.controles = lblFrameControles(self, text="Controles")
        self.controles.btnResolver.config(command=self.resolver)
    
    def resolver(self):
        # Obtiene los datos de la tabla
        res = self.tabla.get_data()
        if isinstance(res, ValueError):
            Messagebox.show_error(parent=self, title="Error", message="Ingresa unicamente valores numéricos")
            return
        # res = ([[3.0, 2.0, 7.0, 6.0], [7.0, 5.0, 2.0, 3.0], [2.0, 5.0, 4.0, 5.0]], [5000.0, 6000.0, 2500.0], [6000.0, 4000.0, 2000.0, 1500.0])#ELIMINAR LINEA
        # res = ([[25.0, 35.0, 36.0, 60.0], [55.0, 30.0, 45.0, 38.0], [40.0, 50.0, 26.0, 65.0], [60.0, 40.0, 66.0, 27.0]], [15.0, 6.0, 14.0, 11.0], [10.0, 12.0, 15.0, 9.0])
        # res = ([[12.0, 13.0, 4.0, 6.0], [6.0, 4.0, 10.0, 11.0], [10.0, 9.0, 12.0, 4.0]], [500.0, 700.0, 800.0], [400.0, 900.0, 200.0, 500.0])#ELIMINAR LINEA
        matriz_costos, ofertas, demandas = res
        print(res)
        # Metodo de resolución
        metodo = self.controles.optionMethod.get()
        if metodo == "Esquina Noroeste":
            transporte = Transporte(matriz_costos, ofertas, demandas)
            transporte.esquina_noroeste()
            self.tabla.set_solucion(transporte.cantidad_solucion)
        elif metodo == "Voguel":
            transporte = Transporte(matriz_costos, ofertas, demandas)
            transporte.voguel()
            self.tabla.set_solucion(transporte.cantidad_solucion)
        elif metodo == "Costo Mínimo":
            transporte = Transporte(matriz_costos, ofertas, demandas)
            transporte.costo_minimo()
            self.tabla.set_solucion(transporte.cantidad_solucion)
        for i in range(len(transporte.proceso_cantidad_solucion)):
            pcs, pos, pds = transporte.proceso_cantidad_solucion[i], transporte.proceso_oferta_solucion[i], transporte.proceso_demanda_solucion[i]
            print("Cantidades: ")
            print(pcs)
            print("Ofertas: ", pos)
            print("Demandas: ", pds)
            if transporte.proceso_penalidades:
                print("Penalidades: ", transporte.proceso_penalidades[i])
            if transporte.proceso_costo_solucion:
                print("Costos: ")
                print(transporte.proceso_costo_solucion[i])
            print("\n")
        print("Costo total: ", transporte.costo_total)

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
