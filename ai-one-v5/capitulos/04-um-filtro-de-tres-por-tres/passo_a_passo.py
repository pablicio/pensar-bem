import numpy as np

from folha.convolucao import convolui, correlaciona

X = np.array([[1, 2, 0, 1, 3],
              [0, 1, 2, 3, 1],
              [1, 0, 1, 2, 2],
              [2, 1, 0, 1, 0],
              [0, 2, 1, 0, 1]])
K = np.array([[-1, 0, 1],
              [-2, 0, 2],
              [-1, 0, 1]])
print("a primeira janela:")
print(X[0:3, 0:3])
print("janela × núcleo, elemento a elemento:")
print(X[0:3, 0:3] * K)
print("soma:", (X[0:3, 0:3] * K).sum())
print("correlação cruzada:")
print(correlaciona(X, K).astype(int))
print("convolução (núcleo virado):")
print(convolui(X, K).astype(int))
