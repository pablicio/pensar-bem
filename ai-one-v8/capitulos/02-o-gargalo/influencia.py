import random

import matplotlib.pyplot as plt
import torch

from lupa.extrator import (Extrator, Vocabulario, influencia,
                           pares)

REGIOES = ["cabeçalho", "objeto", "dígitos do valor",
           "cláusulas", "10 últimos"]


def regioes(e, s):
    """As posições de cada região de um extrato tokenizado."""
    obj = e.index("objeto")
    val = e.index("valor", obj)
    alvo = s[s.index(";") + 1:]
    ini = next(i for i in range(val, len(e))
               if e[i:i + len(alvo)] == alvo)
    ass = e.index("assinatura", ini)
    fim = len(e) - 10
    return {"cabeçalho": range(0, obj),
            "objeto": range(obj + 2, val),
            "dígitos do valor": range(ini, ini + len(alvo)),
            "cláusulas": range(ass + 2, fim),
            "10 últimos": range(fim, len(e))}


def mede(modelo, teste, voc):
    soma = {r: 0.0 for r in REGIOES}
    for e, s in teste:
        g = influencia(modelo, (e, s), voc).flip(0)  # em ordem
        for r, pos in regioes(e, s).items():
            soma[r] += g[list(pos)].mean().item() / len(teste)
    return soma


if __name__ == "__main__":
    random.seed(0)
    torch.manual_seed(0)
    dados = pares()
    random.shuffle(dados)
    teste, treino = dados[:400], dados[400:]
    voc = Vocabulario([e + s for e, s in treino])
    longos = [p for p in teste if len(p[0]) >= 150]
    modelo = Extrator(len(voc))
    modelo.load_state_dict(torch.load("extrator_rnn.pt"))
    media = mede(modelo, longos, voc)
    print(len(longos), "extratos com 150 tokens ou mais")
    for r, v in media.items():
        print(f"{r:17} {v:.1e}")
    fig, eixo = plt.subplots(figsize=(6, 3))
    eixo.bar(REGIOES, list(media.values()))
    eixo.set_yscale("log")
    eixo.set_ylabel("norma do gradiente")
    fig.tight_layout()
    fig.savefig("influencia.png", dpi=300)
