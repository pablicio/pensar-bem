from distancias import norma
from matriz import matriz_vezes_vetor


def iteracao_potencia(M, passos=50):
    v = [1.0] + [0.0] * (len(M) - 1)
    for _ in range(passos):
        w = matriz_vezes_vetor(M, v)
        tamanho = norma(w)
        v = [x / tamanho for x in w]
    return v, tamanho
