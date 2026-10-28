import random
import time

import torch

from lupa.alinhamento import ExtratorComAtencao
from lupa.extrator import Vocabulario, acertos, pares, treina

random.seed(0)
torch.manual_seed(0)
dados = pares()
random.shuffle(dados)
teste, treino = dados[:400], dados[400:]
voc = Vocabulario([e + s for e, s in treino])

modelo = ExtratorComAtencao(len(voc))
n = sum(p.numel() for p in modelo.parameters())
print(n, "parâmetros")
inicio = time.time()
treina(modelo, treino, voc, epocas=10)
print(f"treino: {time.time() - inicio:.0f} s")
torch.save(modelo.state_dict(), "extrator_atencao.pt")

linhas = acertos(modelo, teste, voc)
FAIXAS = [(0, 120), (120, 160), (160, 200), (200, 400)]
print("\ntokens   extratos  prazo  valor  tamanho  dígitos")
for lo, hi in FAIXAS:
    sel = [x[1:] for x in linhas if lo <= x[0] < hi]
    p, v, n, d = [sum(c) / len(sel) for c in zip(*sel)]
    print(f"{lo:3}–{hi:<3} {len(sel):9} {p:6.0%} {v:6.0%}"
          f" {n:8.0%} {d:8.0%}")
