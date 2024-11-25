import numpy as np
from classes.PD.Transporte import Transporte

res = ([[12.0, 13.0, 4.0, 6.0], [6.0, 4.0, 10.0, 11.0], [10.0, 9.0, 12.0, 4.0]], [500.0, 700.0, 800.0], [400.0, 900.0, 200.0, 500.0])#ELIMINAR LINEA

matriz_costos, ofertas, demandas = res
print(res)

transporte = Transporte(matriz_costos, ofertas, demandas)
transporte.banquillo()
for i in transporte.proceso_cantidad_solucion:
    print(i)
print(transporte.cantidad_solucion)