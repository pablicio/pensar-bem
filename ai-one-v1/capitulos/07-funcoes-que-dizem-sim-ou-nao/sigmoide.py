import math


def degrau(z):
    if z >= 0:
        return 1
    return 0


def sigmoide(z):
    # duas formas, para nunca calcular exp de número grande
    if z >= 0:
        return 1 / (1 + math.exp(-z))
    e = math.exp(z)
    return e / (1 + e)
