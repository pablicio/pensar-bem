import random

PRECOS = [40, 55, 60, 65, 70, 75, 85, 89.9, 95, 110, 120, 130,
          150]


def vendas_do_mes(semente, quantas):
    # cada venda leva de 1 a 3 discos de preços típicos
    random.seed(semente)
    vendas = []
    for _ in range(quantas):
        total = 0
        for _ in range(random.randint(1, 3)):
            total += random.choice(PRECOS)
        vendas.append(round(total, 2))
    return vendas
