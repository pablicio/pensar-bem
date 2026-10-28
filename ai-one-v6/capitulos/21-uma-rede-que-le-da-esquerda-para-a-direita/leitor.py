import time

import numpy as np
import torch

from rio.leitor import (Leitor, preenche, probabilidades,
                        treina_leitor)
from rio.texto import (CLASSES, Vocabulario, mensagens,
                       palavras, parte)

tab = mensagens()
treino, valid, teste = (parte(tab, p) for p in
                        ("treino", "validacao", "teste"))
voc = Vocabulario(treino["texto"], palavras)


def dados(t, coluna="classe"):
    x, n = preenche(voc, t["texto"])
    y = t[coluna].map(CLASSES.index).to_numpy()
    return x, n, torch.tensor(y.copy())


torch.manual_seed(0)
modelo = Leitor(len(voc))
total = sum(p.numel() for p in modelo.parameters())
print("parâmetros:", total)
inicio = time.time()
epocas, perda = treina_leitor(modelo, dados(treino),
                              dados(valid))
print(f"{epocas} épocas, {time.time() - inicio:.0f} s,"
      f" perda de validação {perda:.3f}")
torch.save(modelo.state_dict(), "leitor.pt")
x, n, y = dados(teste, "verdade")
previsto = probabilidades(modelo, x, n).argmax(1)
y = y.numpy()
julia = teste["classe"].map(CLASSES.index).to_numpy()
print(f"acerto no teste: {np.mean(previsto == y):.2%}"
      " pela verdade,")
print(f"  {np.mean(previsto == julia):.2%} pelos rótulos"
      " da Júlia")
conf = np.zeros((4, 4), dtype=int)
np.add.at(conf, (y, previsto), 1)
print("verdade  ", " ".join(f"{c:>6}" for c in CLASSES),
      " revocação")
for k, (c, linha) in enumerate(zip(CLASSES, conf)):
    print(f"{c:9}", " ".join(f"{v:6d}" for v in linha),
          f"{linha[k] / linha.sum():10.3f}")
