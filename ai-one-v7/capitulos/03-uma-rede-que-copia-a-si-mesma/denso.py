import time

import torch

from lauber.acervo import carrega, grade, partes
from lauber.autoencoder import Denso, erro, treina
from lauber.pca import PCA

torch.manual_seed(0)
imgs, _ = carrega()
treino, _, teste = partes(len(imgs))
rede = Denso(codigo=16)
print("parâmetros:", sum(p.numel() for p in rede.parameters()))
inicio = time.time()
historico = treina(rede, imgs[treino], epocas=10)
print(f"{time.time() - inicio:.0f} s; perda por época:")
for i in (0, 5):
    trecho = historico[i:i + 5]
    print("  ", " ".join(f"{h:.4f}" for h in trecho))
pca = PCA(imgs[treino])
de_volta = pca.descomprime(pca.comprime(imgs[teste], 16))
erro_pca = ((de_volta - imgs[teste]) ** 2).mean()
print(f"erro no teste com 16 números: PCA {erro_pca:.4f},"
      f" autoencoder {erro(rede, imgs[teste]).mean():.4f}")
amostra = imgs[teste[:6]]
with torch.no_grad():
    do_pca = pca.descomprime(pca.comprime(amostra, 16))
    linhas = [amostra, do_pca, rede(amostra)]
grade(torch.cat(linhas), "pca_e_rede.png", colunas=6)
torch.save(rede.state_dict(), "denso.pt")
