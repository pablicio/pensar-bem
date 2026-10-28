import random


def notas_e_precos(semente, quantos):
    # discos usados vendidos: nota de estado e preço de venda
    random.seed(semente)
    pares = []
    for _ in range(quantos):
        nota = random.randint(3, 10)
        preco = 13 * nota - 12 + random.gauss(0, 9)
        pares.append((nota, round(preco)))
    return pares
