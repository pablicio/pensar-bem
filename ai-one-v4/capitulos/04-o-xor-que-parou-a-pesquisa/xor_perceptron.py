import numpy as np

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([0, 1, 1, 0])                     # o ou exclusivo

w, b = np.zeros(2), 0.0
vistos = {}
for passada in range(1, 101):
    erros = 0
    for xi, yi in zip(X, y):
        previsto = 1 if xi @ w + b > 0 else 0
        if previsto != yi:
            w += (yi - previsto) * xi
            b += yi - previsto
            erros += 1
    print(f"passada {passada}: {erros} erros, w={w}, b={b:g}")
    estado = (*w, b)
    if estado in vistos:
        print(f"o mesmo estado da passada {vistos[estado]}:"
              " daqui em diante, tudo se repete")
        break
    vistos[estado] = passada
