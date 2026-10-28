from distancias import norma
from matriz import matriz_vezes_vetor

A = [[2, 1], [1, 2]]
v = [1, 0]
for passo in range(1, 9):
    w = matriz_vezes_vetor(A, v)
    tamanho = norma(w)
    v = [x / tamanho for x in w]
    print(passo, [round(x, 4) for x in v], round(tamanho, 4))
