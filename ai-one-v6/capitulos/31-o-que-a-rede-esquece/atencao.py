import time

import torch

from rio.atencao import ExtratorComAtencao
from rio.extrator import (alvos, registro, treina_extrator,
                          vocabularios)
from rio.leitor import preenche
from rio.texto import mensagens, parte

tab = mensagens()
treino = parte(tab[tab["verdade"].isin(["risco", "ajuda"])],
               "treino")
registros = [registro(l) for _, l in treino.iterrows()]
entrada, saida = vocabularios(treino["texto"], registros)
x, n = preenche(entrada, treino["texto"], maximo=240)
y = alvos(saida, registros)
torch.manual_seed(0)
modelo = ExtratorComAtencao(len(entrada), len(saida))
total = sum(p.numel() for p in modelo.parameters())
print("parâmetros:", total)
inicio = time.time()
treina_extrator(modelo, x, n, y)
print(f"{(time.time() - inicio) / 60:.0f} min de treino")
torch.save(modelo.state_dict(), "atencao.pt")
