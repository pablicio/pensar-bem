import numpy as np

from folha.convolucao import correlaciona, im2col, toeplitz

X = np.array([[1, 2, 0],
              [0, 1, 2],
              [1, 0, 1]])
K = np.array([[1, 2],
              [3, 4]])
print("convolução direta:")
print(correlaciona(X, K).astype(int))

colunas, formato = im2col(X[None], 2)
print("im2col: uma janela por coluna")
print(colunas.astype(int))
produto = K.ravel() @ colunas
print("núcleo em fila · colunas:", produto.astype(int))

T = toeplitz(K, 3)
print("matriz de Toeplitz T (4 × 9):")
print(T.astype(int))
print("T · X em fila:", (T @ X.ravel()).astype(int))
