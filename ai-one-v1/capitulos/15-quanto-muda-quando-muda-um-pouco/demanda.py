import math


def demanda(preco):
    # reedições vendidas por mês, pelas vendas de 2024 a 2026
    return 500 * math.exp(-0.02 * preco)
