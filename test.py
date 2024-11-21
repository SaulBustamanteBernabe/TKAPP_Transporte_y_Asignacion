import numpy as np

m1 = np.array([[1,2,3],[4,5,6], [7,8,9]])
m2 = np.array([[1,2,3],[4,5,6], [7,8,9]])

lista = []
lista.append(m1)
lista.append(m2)

lista[0][0,0] = 10

print(lista)
print(m1)
print(m2)