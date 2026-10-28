import numpy as np

from folha.conjunto import abre, parte, tabela

fotos = tabela()
X = np.stack([abre(f["foto"], 32).ravel() for f in fotos])
X = X / 255
rotulo = np.array([f["rotulo"] for f in fotos])
folha = np.array([f["folha"] for f in fotos])


def vizinho(teste):
    """Para cada foto de teste, a de treino mais parecida."""
    A, B = X[~teste], X[teste]
    d = (B ** 2).sum(1)[:, None] - 2 * B @ A.T \
        + (A ** 2).sum(1)[None, :]
    return np.flatnonzero(~teste)[d.argmin(axis=1)]


sorteio = np.random.default_rng(0)
por_foto = sorteio.random(len(fotos)) < 0.2
por_fazenda = np.array([parte(f["fazenda"]) == "teste"
                        for f in fotos])
for nome, teste in [("por foto", por_foto),
                    ("por fazenda", por_fazenda)]:
    v, t = vizinho(teste), np.flatnonzero(teste)
    # a gêmea: outra foto da mesma folha, no treino
    gemea = np.array([(folha[~teste] == folha[i]).any()
                      for i in t])
    acerto = (rotulo[v] == rotulo[t]).mean()
    achou = (folha[v] == folha[t]) & gemea
    print(f"{nome:12} acerto {acerto:.1%};"
          f" com gêmea {gemea.mean():.0%};"
          f" vizinho é a gêmea {achou.sum()}")
