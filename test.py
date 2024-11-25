import numpy as np
from classes.PD.Transporte import Transporte

res = ([[3.0, 2.0, 7.0, 6.0], [7.0, 5.0, 2.0, 3.0], [2.0, 5.0, 4.0, 5.0]], [5000.0, 6000.0, 2500.0], [6000.0, 4000.0, 2000.0, 1500.0])
matriz_costos, ofertas, demandas = res
print(res)

transporte = Transporte(matriz_costos, ofertas, demandas)
transporte.banquillo()
for i in transporte.proceso_cantidad_solucion:
    print(i)
print(transporte.cantidad_solucion)