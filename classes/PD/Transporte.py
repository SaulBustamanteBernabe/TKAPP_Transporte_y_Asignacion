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

    def voguel(self):
        pass
    
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
        