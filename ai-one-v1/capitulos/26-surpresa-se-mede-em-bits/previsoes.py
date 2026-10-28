GENEROS = ["MPB", "frevo", "jazz", "rock"]

# compras anteriores de cada cliente, na ordem de GENEROS,
# e o gênero do disco que ele comprou em seguida
CLIENTES = [
    ([5, 1, 0, 0], 0), ([0, 4, 1, 0], 1), ([1, 3, 0, 0], 1),
    ([0, 0, 3, 1], 2), ([4, 0, 1, 1], 0), ([0, 1, 0, 3], 3),
    ([1, 0, 4, 0], 2), ([3, 2, 0, 0], 0), ([3, 2, 0, 0], 1),
    ([1, 0, 2, 0], 0), ([0, 1, 3, 0], 2), ([4, 0, 0, 1], 3),
]


def groove(historico):
    # o sistema da Synapsys: 94% no gênero mais comprado
    chute = historico.index(max(historico))
    return [0.94 if g == chute else 0.02 for g in range(4)]


def contagem(historico):
    # o sistema do Caíque: proporções, mais uma compra em cada
    total = sum(historico) + 4
    return [(c + 1) / total for c in historico]
