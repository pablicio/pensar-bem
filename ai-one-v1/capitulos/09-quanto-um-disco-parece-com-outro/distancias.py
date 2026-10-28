import math


def distancia(u, v):
    total = 0
    for a, b in zip(u, v):
        total += (a - b) ** 2
    return math.sqrt(total)


def manhattan(u, v):
    total = 0
    for a, b in zip(u, v):
        total += abs(a - b)
    return total


def norma(v):
    total = 0
    for a in v:
        total += a ** 2
    return math.sqrt(total)
