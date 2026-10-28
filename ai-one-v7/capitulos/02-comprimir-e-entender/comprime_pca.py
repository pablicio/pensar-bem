import time

import matplotlib.pyplot as plt
import torch

from lauber.acervo import carrega, grade, partes
from lauber.pca import PCA

imgs, _ = carrega()
treino, _, teste = partes(len(imgs))
inicio = time.time()
pca = PCA(imgs[treino])
print(f"PCA de {len(treino)} estampas de {imgs[0].numel()}"
      f" números: {time.time() - inicio:.1f} s")
fracao = pca.variancia.cumsum(0) / pca.variancia.sum()
print("componentes  variância  erro no teste")
erros = {}
for k in (1, 4, 16, 64, 256, 1024):
    volta = pca.descomprime(pca.comprime(imgs[teste], k))
    erros[k] = float(((volta - imgs[teste]) ** 2).mean())
    print(f"{k:11d} {fracao[k - 1]:10.1%} {erros[k]:14.4f}")
amostra = imgs[teste[:6]]
linhas = [amostra] + [pca.descomprime(pca.comprime(amostra, k))
                      for k in (4, 16, 64)]
grade(torch.cat(linhas), "reconstrucoes.png", colunas=6)
fig, ax = plt.subplots(figsize=(5, 3))
ax.plot(list(erros), list(erros.values()), "o-")
ax.set_xscale("log")
ax.set_xlabel("componentes")
ax.set_ylabel("erro quadrático médio")
fig.tight_layout()
fig.savefig("erro_pca.png", dpi=300)
# as oito primeiras direções, desenhadas como imagens
direcoes = pca.direcoes[:8].view(8, *pca.forma)
escala = direcoes.abs().amax(dim=(1, 2, 3), keepdim=True)
grade(0.5 + 0.5 * direcoes / escala, "direcoes.png", colunas=8)
