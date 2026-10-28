import random
import time

import torch

from lupa.extrator import (INI, Vocabulario, acertos, extrai,
                           lote, pares, treina)
from lupa.qkv_rnn import ExtratorQKV

random.seed(0)
torch.manual_seed(0)
dados = pares()
random.shuffle(dados)
teste, treino = dados[:400], dados[400:]
voc = Vocabulario([e + s for e, s in treino])

modelo = ExtratorQKV(len(voc))
n = sum(p.numel() for p in modelo.parameters())
print(n, "parâmetros")
inicio = time.time()
treina(modelo, treino, voc, epocas=10)
print(f"treino: {time.time() - inicio:.0f} s")
torch.save(modelo.state_dict(), "extrator_qkv.pt")

linhas = acertos(modelo, teste, voc)
FAIXAS = [(0, 120), (120, 160), (160, 200), (200, 400)]
print("\ntokens   extratos  prazo  valor  tamanho  dígitos")
for lo, hi in FAIXAS:
    sel = [x[1:] for x in linhas if lo <= x[0] < hi]
    p, v, n, d = [sum(c) / len(sel) for c in zip(*sel)]
    print(f"{lo:3}–{hi:<3} {len(sel):9} {p:6.0%} {v:6.0%}"
          f" {n:8.0%} {d:8.0%}")

# o prazo do maior extrato: para onde olha agora?
e, s = max(teste, key=lambda par: len(par[0]))
saida = extrai(modelo, e, voc)
print("\nsaída:", " ".join(saida))
x, _, _ = lote([(e, [])], voc)
y = torch.tensor([[INI] + voc.codifica(saida)])
with torch.no_grad():
    modelo(x, y)
pesos = modelo.pesos[0, :len(saida), -len(e):]
for k, token in enumerate(saida[:5]):
    w, i = pesos[k].max(dim=0)
    viz = " ".join(e[max(0, i - 2):i + 3])
    print(f"{token:9} {e[i]:12} ({w:.2f})  …{viz}…")
