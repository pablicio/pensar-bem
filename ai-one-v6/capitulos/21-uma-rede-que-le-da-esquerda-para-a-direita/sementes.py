import numpy as np
import torch

from rio.leitor import (Leitor, preenche, probabilidades,
                        treina_leitor)
from rio.provinha import PROVINHA
from rio.texto import (CLASSES, Vocabulario, mensagens,
                       palavras, parte)

tab = mensagens()
treino, valid, teste = (parte(tab, p) for p in
                        ("treino", "validacao", "teste"))
voc = Vocabulario(treino["texto"], palavras)


def dados(textos, classes):
    x, n = preenche(voc, textos)
    y = np.array([CLASSES.index(c) for c in classes])
    return x, n, torch.tensor(y)


tr = dados(treino["texto"], treino["classe"])
va = dados(valid["texto"], valid["classe"])
te = dados(teste["texto"], teste["verdade"])
pv = dados(*zip(*PROVINHA))
ivone = teste["texto"].str.endswith("ivone").to_numpy()
print("semente   teste provinha riscos P(risco) Ivone")
for semente in range(5):
    torch.manual_seed(semente)
    modelo = Leitor(len(voc))
    treina_leitor(modelo, tr, va)
    p = probabilidades(modelo, te[0], te[1])
    certo = np.mean(p.argmax(1) == te[2].numpy())
    q = probabilidades(modelo, pv[0], pv[1]).argmax(1)
    y = pv[2].numpy()
    print(f"{semente:7d} {certo:7.2%} {np.sum(q == y):5d}/24"
          f" {np.sum((q == 0) & (y == 0)):4d}/6"
          f" {p[ivone, 0][0]:14.2f}")
