import numpy as np

M1 = np.array([[1, 2, 3], [4, np.inf, 6]])

print(np.where(np.isinf(M1), "X", M1))