import time

import matplotlib.pyplot as plt
import numpy as np
import torch

from lupa.corpus import prepara
from lupa.gpt import GPT, lote, taxa

torch.set_num_threads(4)
tok, treino, teste = prepara()
V, T, B, PASSOS = len(tok.vocab), 128, 32, 300
fixo = torch.Generator().manual_seed(1)
validacao = [lote(teste, B, T, fixo) for _ in range(10)]

tamanhos, perdas = [], []
for d in [32, 64, 96, 128]:
    torch.manual_seed(0)
    modelo = GPT(V, T, d=d)
    N = 12 * d * d * 4                  # sem os embeddings
    opt = torch.optim.AdamW(modelo.parameters(), lr=3e-3,
                            betas=(0.9, 0.95),
                            weight_decay=0.1)
    inicio = time.time()
    for passo in range(PASSOS):
        for g in opt.param_groups:
            g["lr"] = taxa(passo, 3e-3, 30, PASSOS)
        x, y = lote(treino, B, T)
        perda = modelo(x, y)
        opt.zero_grad()
        perda.backward()
        torch.nn.utils.clip_grad_norm_(modelo.parameters(),
                                       1.0)
        opt.step()
    modelo.eval()
    with torch.no_grad():
        val = sum(modelo(x, y).item()
                  for x, y in validacao) / 10
    tamanhos.append(N)
    perdas.append(val)
    print(f"d = {d:3}  N = {N:7}  validação {val:.3f}"
          f"  ({time.time() - inicio:.0f} s)")

# uma reta em log-log: log L = log a - alfa log N
inclinacao, intercepto = np.polyfit(np.log(tamanhos),
                                    np.log(perdas), 1)
print(f"L(N) = {np.exp(intercepto):.1f} N^({inclinacao:.3f})")

fig, eixo = plt.subplots(figsize=(6, 3))
eixo.loglog(tamanhos, perdas, "o")
ns = np.geomspace(tamanhos[0] / 2, tamanhos[-1] * 2)
eixo.loglog(ns, np.exp(intercepto) * ns ** inclinacao, "--")
eixo.set_xlabel("parâmetros sem os embeddings, N")
eixo.set_ylabel("perda de validação")
fig.tight_layout()
fig.savefig("escala.png", dpi=300)
