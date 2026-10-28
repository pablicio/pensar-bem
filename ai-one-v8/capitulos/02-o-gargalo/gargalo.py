import random
import time

import matplotlib.pyplot as plt
import torch

from lupa.extrator import (Extrator, Vocabulario, acertos,
                           extrai, pares, treina)

random.seed(0)
torch.manual_seed(0)
dados = pares()
random.shuffle(dados)
teste, treino = dados[:400], dados[400:]
voc = Vocabulario([e + s for e, s in treino])
print(len(treino), "extratos de treino,", len(teste),
      "de teste\nvocabulário:", len(voc), "tokens")

modelo = Extrator(len(voc))
inicio = time.time()
treina(modelo, treino, voc, epocas=15)
print(f"treino: {time.time() - inicio:.0f} s")
torch.save(modelo.state_dict(), "extrator_rnn.pt")

linhas = acertos(modelo, teste, voc)
FAIXAS = [(0, 120), (120, 160), (160, 200), (200, 400)]
print("\ntokens   extratos  prazo  valor  tamanho  dígitos")
colunas = []
for lo, hi in FAIXAS:
    sel = [x[1:] for x in linhas if lo <= x[0] < hi]
    medias = [sum(c) / len(sel) for c in zip(*sel)]
    colunas.append(medias)
    p, v, n, d = medias
    print(f"{lo:3}–{hi:<3} {len(sel):9} {p:6.0%} {v:6.0%}"
          f" {n:8.0%} {d:8.0%}")

e, s = max(teste, key=lambda par: len(par[0]))
print("\no maior extrato do teste:", len(e), "tokens")
print("certo:", " ".join(s))
print("saída:", " ".join(extrai(modelo, e, voc)))

nomes = [f"{lo}–{hi}" for lo, hi in FAIXAS]
fig, eixo = plt.subplots(figsize=(6, 3))
for k, rotulo in [(0, "prazo"), (1, "valor"), (3, "dígitos")]:
    desloca = {0: -0.27, 1: 0, 3: 0.27}[k]
    eixo.bar([i + desloca for i in range(4)],
             [c[k] for c in colunas], 0.27, label=rotulo)
eixo.set_xticks(range(4), nomes)
eixo.set_xlabel("tamanho do extrato (tokens)")
eixo.set_ylabel("acerto")
eixo.legend()
fig.tight_layout()
fig.savefig("gargalo.png", dpi=300)
