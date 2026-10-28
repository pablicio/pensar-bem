"""Treinar as células de NumPy, e o problema da soma."""
import numpy as np


def norma(g):
    """A norma do gradiente, com todos os pesos juntos."""
    quadrados = [np.sum(v ** 2) for v in g.values()]
    return float(np.sqrt(sum(quadrados)))


def recorta(g, limite):
    """Encolhe o gradiente se a norma passar do limite."""
    n = norma(g)
    fator = 1.0 if n <= limite else limite / n
    return {nome: v * fator for nome, v in g.items()}


def adam_inicia(p):
    """A memória do Adam: as duas médias e o contador."""
    return {"m": {n: np.zeros_like(v) for n, v in p.items()},
            "v": {n: np.zeros_like(v) for n, v in p.items()},
            "t": 0}


def epoca(p, gradiente, x, y, sorteio, taxa, limite,
          adam=None):
    """Uma passada pelos exemplos, um de cada vez, com recorte.
    Com `adam`, o passo é o do Adam; sem, o da descida."""
    for i in sorteio.permutation(len(x)):
        _, g = gradiente(p, x[i], y[i])
        g = recorta(g, limite)
        if adam is None:
            for nome in p:
                p[nome] = p[nome] - taxa * g[nome]
            continue
        adam["t"] += 1
        t = adam["t"]
        for nome in p:
            m = 0.9 * adam["m"][nome] + 0.1 * g[nome]
            v = 0.999 * adam["v"][nome] + 0.001 * g[nome] ** 2
            adam["m"][nome], adam["v"][nome] = m, v
            m, v = m / (1 - 0.9 ** t), v / (1 - 0.999 ** t)
            p[nome] = p[nome] - taxa * m / (np.sqrt(v) + 1e-8)


def tarefa_soma(sorteio, n, passos):
    """O problema da soma: dois valores marcados, um no começo
    e outro no fim da sequência; o alvo é a soma dos dois."""
    xs = np.zeros((n, passos, 2))
    xs[:, :, 0] = sorteio.random((n, passos))
    q = max(passos // 5, 1)
    a = sorteio.integers(0, q, n)
    b = sorteio.integers(passos - q, passos, n)
    linhas = np.arange(n)
    xs[linhas, a, 1] = 1
    xs[linhas, b, 1] = 1
    return xs, xs[linhas, a, 0] + xs[linhas, b, 0]
