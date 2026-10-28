import time

import torch

from rio.extrator import (Extrator, alvos, registro,
                          treina_extrator, vocabularios)
from rio.leitor import preenche
from rio.texto import mensagens, parte

tab = mensagens()
pedidos = tab[tab["verdade"].isin(["risco", "ajuda"])]
treino = parte(pedidos, "treino")
registros = [registro(l) for _, l in treino.iterrows()]
print(len(treino), "pedidos de treino; por exemplo:")
for t, r in list(zip(treino["texto"], registros))[:2]:
    print("  ", t[:56])
    print("  ->", r)
entrada, saida = vocabularios(treino["texto"], registros)
print(f"caracteres: {len(entrada)} na entrada,"
      f" {len(saida)} na saída")
x, n = preenche(entrada, treino["texto"], maximo=240)
y = alvos(saida, registros)
torch.manual_seed(0)
modelo = Extrator(len(entrada), len(saida))
total = sum(p.numel() for p in modelo.parameters())
print("parâmetros:", total)
inicio = time.time()
treina_extrator(modelo, x, n, y)
print(f"{(time.time() - inicio) / 60:.0f} min de treino")
torch.save(modelo.state_dict(), "extrator.pt")
