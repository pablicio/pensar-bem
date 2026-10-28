import math


def media(valores):
    return sum(valores) / len(valores)


def mediana(valores):
    ordenados = sorted(valores)
    n = len(ordenados)
    meio = n // 2
    if n % 2 == 1:
        return ordenados[meio]
    return (ordenados[meio - 1] + ordenados[meio]) / 2


def variancia(valores):
    m = media(valores)
    return sum((x - m) ** 2 for x in valores) / len(valores)


def desvio_padrao(valores):
    return math.sqrt(variancia(valores))


def percentil(valores, p):
    # o menor valor com pelo menos p% dos dados até ele
    ordenados = sorted(valores)
    posicao = math.ceil(p / 100 * len(ordenados))
    return ordenados[max(posicao, 1) - 1]
