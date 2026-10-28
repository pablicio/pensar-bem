import textwrap

import numpy as np
import torch

from rio.leitor import Leitor, preenche, probabilidades
from rio.provinha import PROVINHA
from rio.texto import (CLASSES, Vocabulario, mensagens,
                       palavras, parte)

voc = Vocabulario(parte(mensagens(), "treino")["texto"],
                  palavras)
modelo = Leitor(len(voc))
modelo.load_state_dict(torch.load("leitor.pt"))
textos = [t for t, _ in PROVINHA]
y = np.array([CLASSES.index(c) for _, c in PROVINHA])
x, n = preenche(voc, textos)
p = probabilidades(modelo, x, n)
previsto = p.argmax(1)
print(f"provinha: {np.sum(previsto == y)} de {len(y)} certas")
for c in CLASSES:
    k = CLASSES.index(c)
    print(f"  {c:6} {np.sum((y == k) & (previsto == k))}"
          f" de {np.sum(y == k)}")
print("as erradas, com P(risco):")
for i in np.flatnonzero(previsto != y):
    certa, lida_como = CLASSES[y[i]], CLASSES[previsto[i]]
    print(f"  {certa} lida como {lida_como},"
          f" P(risco) = {p[i, 0]:.2f}")
    lida = voc.decodifica(x[i, :n[i]].tolist())
    print(textwrap.fill(lida, 60, initial_indent="    ",
                        subsequent_indent="    "))
