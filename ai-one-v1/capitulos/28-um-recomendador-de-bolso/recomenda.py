from similaridade import cosseno


def colunas(compras, n_discos):
    # o vetor de cada disco: 1 para cada cliente que o comprou
    vetores = [[0] * len(compras) for _ in range(n_discos)]
    for c, discos in enumerate(compras):
        for d in discos:
            vetores[d][c] = 1
    return vetores


def similaridades(compras, n_discos):
    # a matriz de cosseno entre todos os pares de discos
    vetores = colunas(compras, n_discos)
    return [[cosseno(u, v) for v in vetores] for u in vetores]


def recomendar(comprados, sim, quantos=10):
    # nota de cada disco não comprado: soma das semelhanças
    # com os discos que o cliente já tem
    notas = []
    for d in range(len(sim)):
        if d not in comprados:
            nota = sum(sim[d][c] for c in comprados)
            notas.append((nota, d))
    notas = sorted(notas, reverse=True)
    return [d for _, d in notas[:quantos]]
