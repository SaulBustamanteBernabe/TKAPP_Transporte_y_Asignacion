import numpy as np
from numpy import ndarray

class Transporte:
    def __init__(self, matriz_costos = None, ofertas = None, demandas = None):
        # Entrada basica
        self.matriz_costos: ndarray = np.array(matriz_costos)
        self.ofertas: ndarray = np.array(ofertas)
        self.demandas: ndarray = np.array(demandas)
        # Variables de la solución
        self.proceso_costo_solucion: list = list()
        self.proceso_cantidad_solucion: list = list()
        self.proceso_oferta_solucion: list = list()
        self.proceso_demanda_solucion: list = list()
        self.costo_solucion: ndarray = np.empty(0)
        self.cantidad_solucion: ndarray = np.empty(0)
        self.oferta_solucion: ndarray = np.empty(0)
        self.demanda_solucion: ndarray = np.empty(0)
        self.costo_total: float = 0.0
        self.proceso_penalidades: list = list()

    def esquina_noroeste(self):
        # Comprobar datos de entrada
        if self.ofertas is None:
            raise ValueError("No se han definido las ofertas")
        if self.demandas is None:
            raise ValueError("No se han definido las demandas")
        # Crear copia de datos de entrada
        ofertas = self.ofertas.copy()
        demandas = self.demandas.copy()
        # Crear matriz de asignaciones
        cantidad = np.zeros((len(ofertas), len(demandas)))
        # Crear bucle de resolución
        filas, columnas = len(ofertas), len(demandas)
        i, j = 0, 0
        while i < filas and j < columnas:
            # Proceso de asignación
            asignacion = min(ofertas[i], demandas[j])
            cantidad[i][j] = asignacion
            ofertas[i] -= asignacion
            demandas[j] -= asignacion
            if ofertas[i] == 0:
                i += 1
            elif demandas[j] == 0:
                j += 1
            # Guardar iteracion en array de procesos
            self.proceso_cantidad_solucion.append(cantidad.copy())
            self.proceso_oferta_solucion.append(ofertas.copy())
            self.proceso_demanda_solucion.append(demandas.copy())
        # Almacenar ultimo resultado de interación
        self.cantidad_solucion = cantidad.copy()
        self.oferta_solucion = ofertas.copy()
        self.demanda_solucion = demandas.copy()
        # Calcular costo total
        self.calcular_costo_total()

    def voguel(self):
        # Comprobar datos de entrada
        if self.matriz_costos is None:
            raise ValueError("No se han definido los costos")
        if self.ofertas is None:
            raise ValueError("No se han definido las ofertas")
        if self.demandas is None:
            raise ValueError("No se han definido las demandas")
        # Crear copia de datos de entrada
        ofertas = self.ofertas.copy()
        demandas = self.demandas.copy()
        costos = self.matriz_costos.copy()
        # Crear matriz de asignaciones
        cantidad = np.zeros_like(self.matriz_costos)
        # Crear bucle de resolución
        filas, columnas = len(ofertas), len(demandas)
        while np.any(ofertas > 0) and np.any(demandas > 0):
            penalidades = []
            #Calcular penalidades de filas
            for i in range(filas):
                if ofertas[i] > 0:
                    costos_fila = costos[i, demandas > 0]
                    if len(costos_fila) >= 2:
                        costos_fila_ordenado = np.sort(costos_fila)
                        penalidades.append(((costos_fila_ordenado[1] - costos_fila_ordenado[0]), i, 'fila'))
                    else:
                        penalidades.append((-np.inf, i, 'fila'))
            #Calcular penalidades de columnas
            for j in range(columnas):
                if demandas[j] > 0:
                    costos_columna = costos[ofertas > 0, j]
                    if len(costos_columna) >= 2:
                        costos_columna_ordenado = np.sort(costos_columna)
                        penalidades.append(((costos_columna_ordenado[1] - costos_columna_ordenado[0]), j, 'columna'))
                    else:
                        penalidades.append((-np.inf, j, 'columna'))
            # Seleccionar penalidad maxima
            penalidad_max = max(penalidades, key=lambda x: x[0])
            if penalidad_max[2] == 'fila':
                i = penalidad_max[1]
                j = np.argmin(costos[i, :])
            elif penalidad_max[2] == 'columna':
                j = penalidad_max[1]
                i = np.argmin(costos[:, j])
            # Proceso de asignación
            asignacion = min(ofertas[i], demandas[j])
            cantidad[i, j] = asignacion
            ofertas[i] -= asignacion
            demandas[j] -= asignacion
            if ofertas[i] == 0:
                costos[i, :] = np.inf
            if demandas[j] == 0:
                costos[:, j] = np.inf
            # Guardar iteracion en array de procesos
            self.proceso_cantidad_solucion.append(cantidad.copy())
            self.proceso_oferta_solucion.append(ofertas.copy())
            self.proceso_demanda_solucion.append(demandas.copy())
            self.proceso_costo_solucion.append(costos.copy())
            self.proceso_penalidades.append(penalidades)
        # Almacenar ultimo resultado de interación
        self.cantidad_solucion = cantidad.copy()
        self.oferta_solucion = ofertas.copy()
        self.demanda_solucion = demandas.copy()
        self.costo_solucion = costos.copy()
        # Calcular costo total
        self.calcular_costo_total()
                

    def costo_minimo(self):
        # Comprobar datos de entrada
        if self.matriz_costos is None:
            raise ValueError("No se han definido los costos")
        if self.ofertas is None:
            raise ValueError("No se han definido las ofertas")
        if self.demandas is None:
            raise ValueError("No se han definido las demandas")
        # Crear copia de datos de entrada
        ofertas = self.ofertas.copy()
        demandas = self.demandas.copy()
        costos = self.matriz_costos.copy()
        # Crear matriz de asignaciones
        cantidad = np.zeros_like(self.matriz_costos)
        # Crear bucle de resolución
        filas, columnas = len(ofertas), len(demandas)
        while np.any(ofertas) and np.any(demandas):
            # Encontrar la celda de menor costo
            min_cost = np.inf
            min_pos = None
            for i in range(filas):
                for j in range(columnas):
                    if costos[i, j] < min_cost and ofertas[i] > 0 and demandas[j] > 0:
                        min_cost = costos[i, j]
                        min_pos = (i, j)
            # Proceso de asignación
            i, j = min_pos
            asignacion = min(ofertas[i], demandas[j])
            cantidad[i, j] = asignacion
            ofertas[i] -= asignacion
            demandas[j] -= asignacion
            if ofertas[i] == 0:
                costos[i, :] = np.inf
            if demandas[j] == 0:
                costos[:, j] = np.inf
            # Guardar iteracion en array de procesos
            self.proceso_cantidad_solucion.append(cantidad.copy())
            self.proceso_oferta_solucion.append(ofertas.copy())
            self.proceso_demanda_solucion.append(demandas.copy())
            self.proceso_costo_solucion.append(costos.copy())
        # Almacenar ultimo resultado de interación
        self.cantidad_solucion = cantidad.copy()
        self.oferta_solucion = ofertas.copy()
        self.demanda_solucion = demandas.copy()
        self.costo_solucion = costos.copy()
        # Calcular costo total
        self.calcular_costo_total()

    def calcular_costo_total(self):
        self.costo_total = np.sum(self.matriz_costos * self.cantidad_solucion)