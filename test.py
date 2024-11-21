import numpy as np

matriz_costos = np.array([[3.0, 2.0, 7.0, 6.0], [7.0, 5.0, 2.0, 3.0], [2.0, 5.0, 4.0, 5.0]])

print(np.argmin(matriz_costos, axis=1))
print(matriz_costos.shape)
print(np.unravel_index(np.argmin(matriz_costos, axis=1), matriz_costos.shape))