import numpy as np

from mnist import carregar

imagens, rotulos = carregar("treino")
so = (rotulos == 3) | (rotulos == 8)
X = imagens[so].reshape(-1, 784) / 255
y = (rotulos[so] == 8).astype(int)

w, b = np.zeros(784), 0.0
for passada in range(1, 51):
    erros = 0
    for xi, yi in zip(X, y):
        previsto = 1 if xi @ w + b > 0 else 0
        if previsto != yi:
            w += (yi - previsto) * xi
            b += yi - previsto
            erros += 1
    if passada in (1, 2, 5, 10, 20, 30, 40, 50):
        print(f"passada {passada:2}: {erros:4} erros")
