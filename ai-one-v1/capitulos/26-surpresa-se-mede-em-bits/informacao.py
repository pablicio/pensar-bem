import math


def surpresa(p):
    # em bits: quantas vezes a chance p cabe pela metade
    return -math.log2(p)


def entropia(distribuicao):
    # a surpresa média de uma distribuição
    return sum(p * surpresa(p) for p in distribuicao if p > 0)


def entropia_cruzada(previsoes, ocorridos):
    # a surpresa média de quem previu, diante do que ocorreu
    total = 0
    for q, real in zip(previsoes, ocorridos):
        total += surpresa(q[real])
    return total / len(ocorridos)
