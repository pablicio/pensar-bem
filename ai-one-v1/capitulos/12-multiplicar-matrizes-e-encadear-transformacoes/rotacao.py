import math

from matriz import matriz_vezes_vetor, multiplicar


def rotacao(graus):
    t = math.radians(graus)
    return [[math.cos(t), -math.sin(t)],
            [math.sin(t), math.cos(t)]]


print(matriz_vezes_vetor(rotacao(45), [1, 0]))
print(multiplicar(rotacao(45), rotacao(45)))
